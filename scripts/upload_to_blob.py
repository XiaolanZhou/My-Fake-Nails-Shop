#!/usr/bin/env python3
"""Upload all images from client/public/uploads/ to Vercel Blob."""

import os
import requests
from pathlib import Path

BLOB_TOKEN = "vercel_blob_rw_HTHAOtTxeEQJYFfd_zh0Qs92hbDApyVG0y68k8JoO59KsBs"
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "client" / "public" / "uploads"

def get_content_type(filename: str) -> str:
    ext = filename.rsplit('.', 1)[-1].lower()
    return {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'webp': 'image/webp',
        'gif': 'image/gif',
    }.get(ext, 'application/octet-stream')

def upload_to_blob(file_path: Path) -> str:
    """Upload file to Vercel Blob and return URL."""
    filename = file_path.name
    content_type = get_content_type(filename)
    
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
    
    response = requests.put(
        f"https://blob.vercel-storage.com/uploads/{filename}",
        headers={
            "Authorization": f"Bearer {BLOB_TOKEN}",
            "Content-Type": content_type,
            "x-api-version": "7",
        },
        data=file_bytes,
    )
    
    if response.status_code != 200:
        raise Exception(f"Upload failed for {filename}: {response.text}")
    
    return response.json()["url"]

if __name__ == "__main__":
    print("Uploading images to Vercel Blob...\n")
    
    results = {}
    for img_file in UPLOAD_DIR.iterdir():
        if img_file.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
            try:
                url = upload_to_blob(img_file)
                results[img_file.name] = url
                print(f"✓ {img_file.name}")
                print(f"  → {url}\n")
            except Exception as e:
                print(f"✗ {img_file.name}: {e}\n")
    
    print("\n" + "="*60)
    print("SQL to update product image URLs:")
    print("="*60 + "\n")
    
    # Generate SQL update statements
    for filename, url in results.items():
        # Map filename to product name pattern
        name_pattern = filename.replace('.png', '').replace('.jpg', '').replace('-', '%')
        print(f"UPDATE products SET image_url = '{url}' WHERE image_url LIKE '%{filename}';")
