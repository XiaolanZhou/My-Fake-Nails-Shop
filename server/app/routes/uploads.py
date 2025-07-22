from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from PIL import Image
from typing import Tuple, cast

uploads_bp = Blueprint("uploads", __name__)

TARGET_SIZE: Tuple[int, int] = (432, 320)  # width, height

# Directory where frontend serves images
UPLOAD_DIR = Path(__file__).resolve().parents[3] / "client" / "public" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def resize_image(img_path: Path) -> None:
    """Center-crop and resize image to TARGET_SIZE in-place."""
    with Image.open(img_path) as im:
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
        save_kwargs = {}
        if img_path.suffix.lower() in {".jpg", ".jpeg"}:
            im = im.convert("RGB")
            save_kwargs["quality"] = 90
        im.save(img_path, **save_kwargs)


@uploads_bp.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files["file"]  # type: ignore[index]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(cast(str, file.filename))
    # Prevent name collision
    dst_path = UPLOAD_DIR / filename
    counter = 1
    while dst_path.exists():
        stem = dst_path.stem
        suffix = dst_path.suffix
        filename = f"{stem}_{counter}{suffix}"
        dst_path = UPLOAD_DIR / filename
        counter += 1

    file.save(dst_path)
    try:
        resize_image(dst_path)
    except Exception as e:
        dst_path.unlink(missing_ok=True)
        return jsonify({"message": "Image processing failed", "detail": str(e)}), 500

    # Return relative URL that the React app can use directly
    return jsonify({"image_url": f"/uploads/{filename}"}), 201 