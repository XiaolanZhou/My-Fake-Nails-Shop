import os
import io
import requests
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from typing import Tuple, cast
import uuid

uploads_bp = Blueprint("uploads", __name__)

TARGET_SIZE: Tuple[int, int] = (432, 320)  # width, height

# Vercel Blob token from environment
BLOB_TOKEN = os.getenv("BLOB_READ_WRITE_TOKEN")


def resize_image_bytes(file_bytes: bytes, filename: str) -> tuple[bytes, str]:
    """Center-crop and resize image, return bytes and content type."""
    with Image.open(io.BytesIO(file_bytes)) as im:
        im = im.convert("RGBA")
        target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]
        w, h = im.size
        ratio = w / h
        if ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            im = im.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            im = im.crop((0, top, w, top + new_h))
        im = im.resize(TARGET_SIZE, Image.LANCZOS)  # type: ignore[attr-defined]

        # Determine output format
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'png'
        output = io.BytesIO()
        
        if ext in ('jpg', 'jpeg'):
            im = im.convert("RGB")
            im.save(output, format='JPEG', quality=90)
            content_type = 'image/jpeg'
        elif ext == 'webp':
            im.save(output, format='WEBP', quality=90)
            content_type = 'image/webp'
        else:  # png, gif, etc
            im.save(output, format='PNG')
            content_type = 'image/png'
        
        return output.getvalue(), content_type


def upload_to_vercel_blob(file_bytes: bytes, filename: str, content_type: str) -> str:
    """Upload file to Vercel Blob and return the URL."""
    # Generate unique filename to avoid collisions
    unique_name = f"uploads/{uuid.uuid4().hex[:8]}_{filename}"
    
    response = requests.put(
        f"https://blob.vercel-storage.com/{unique_name}",
        headers={
            "Authorization": f"Bearer {BLOB_TOKEN}",
            "Content-Type": content_type,
            "x-api-version": "7",
        },
        data=file_bytes,
    )
    
    if response.status_code != 200:
        raise Exception(f"Blob upload failed: {response.text}")
    
    return response.json()["url"]


@uploads_bp.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files["file"]  # type: ignore[index]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(cast(str, file.filename))
    file_bytes = file.read()

    # Check if Vercel Blob is configured
    if BLOB_TOKEN:
        try:
            # Resize and upload to Vercel Blob
            resized_bytes, content_type = resize_image_bytes(file_bytes, filename)
            blob_url = upload_to_vercel_blob(resized_bytes, filename, content_type)
            return jsonify({"image_url": blob_url}), 201
        except Exception as e:
            return jsonify({"message": "Upload failed", "detail": str(e)}), 500
    else:
        # Fallback to local storage (development)
        from pathlib import Path
        UPLOAD_DIR = Path(__file__).resolve().parents[3] / "client" / "public" / "uploads"
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        
        dst_path = UPLOAD_DIR / filename
        counter = 1
        while dst_path.exists():
            stem = dst_path.stem
            suffix = dst_path.suffix
            filename = f"{stem}_{counter}{suffix}"
            dst_path = UPLOAD_DIR / filename
            counter += 1

        # Write and resize locally
        dst_path.write_bytes(file_bytes)
        try:
            resized_bytes, _ = resize_image_bytes(file_bytes, filename)
            dst_path.write_bytes(resized_bytes)
        except Exception as e:
            dst_path.unlink(missing_ok=True)
            return jsonify({"message": "Image processing failed", "detail": str(e)}), 500

        return jsonify({"image_url": f"/uploads/{filename}"}), 201
