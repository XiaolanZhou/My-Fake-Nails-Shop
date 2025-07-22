#!/usr/bin/env python3
"""Batch-crop/resize all images in client/public/uploads/ to 432×320.

Run:
    python scripts/resize_images.py

Requires Pillow (added to requirements.txt)
"""
from pathlib import Path
from PIL import Image

TARGET_SIZE = (432, 320)  # width, height

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "client" / "public" / "uploads"


def resize_image(img_path: Path) -> None:
    with Image.open(img_path) as im:
        # Convert to RGBA to preserve transparency, then back to RGB when saving JPEG
        im = im.convert("RGBA")
        # Center-crop to aspect ratio 432:320 (1.35)
        target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]
        w, h = im.size
        current_ratio = w / h

        if current_ratio > target_ratio:  # too wide → crop left/right
            new_width = int(h * target_ratio)
            left = (w - new_width) // 2
            im = im.crop((left, 0, left + new_width, h))
        else:  # too tall → crop top/bottom
            new_height = int(w / target_ratio)
            top = (h - new_height) // 2
            im = im.crop((0, top, w, top + new_height))

        # Resize to target
        im = im.resize(TARGET_SIZE, Image.LANCZOS)

        # Preserve original format
        save_kwargs = {}
        if img_path.suffix.lower() in {".jpg", ".jpeg"}:
            im = im.convert("RGB")
            save_kwargs["quality"] = 90
        im.save(img_path, **save_kwargs)
        print(f"✔ Resized {img_path.name}")


if __name__ == "__main__":
    if not UPLOAD_DIR.exists():
        print(f"Upload directory not found: {UPLOAD_DIR}")
        exit(1)

    for img_file in UPLOAD_DIR.iterdir():
        if img_file.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            try:
                resize_image(img_file)
            except Exception as e:
                print(f"✖ Failed {img_file.name}: {e}") 