import os
import shutil
from pathlib import Path

# 📂 Source (Downloads) and Destination (your external HDD)
downloads = Path.home() / "Downloads"
destination = Path("F:/Download")

# Create destination if it doesn't exist
destination.mkdir(exist_ok=True)

# Get all files with size
files = [(f, f.stat().st_size) for f in downloads.iterdir() if f.is_file()]

# Sort by size (smallest → largest)
files.sort(key=lambda x: x[1])

for f, size in files:
    # Get extension (default to 'Others' if no extension)
    ext = f.suffix.lower()[1:] if f.suffix else "Others"

    # Create folder for that extension inside F:\Download
    ext_folder = destination / ext
    ext_folder.mkdir(exist_ok=True)

    # Destination path
    new_path = ext_folder / f.name

    # Move file
    shutil.move(str(f), str(new_path))

    print(f"Moved {f.name} → {ext_folder} ({size/1024:.2f} KB)")
