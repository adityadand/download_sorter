import os
import shutil
from pathlib import Path


# 📂 Source (Downloads) and Destination (your external HDD)
downloads = Path.home() / "F:/backup pc/Downloads"
destination = Path("F:/Download")


# Create destination if it doesn't exist
destination.mkdir(exist_ok=True)


def safe_move_file(src, dst):
    """Safely move a file with error handling"""
    try:
        # Check if destination file already exists
        if dst.exists():
            # Create a unique name by adding a counter
            counter = 1
            stem = dst.stem
            suffix = dst.suffix
            parent = dst.parent
            
            while dst.exists():
                new_name = f"{stem}_{counter}{suffix}"
                dst = parent / new_name
                counter += 1
            
            print(f"  → Renamed to avoid conflict: {dst.name}")
        
        shutil.move(str(src), str(dst))
        return True, dst
        
    except PermissionError as e:
        print(f"  ❌ PERMISSION DENIED: {src.name} - Skipping system file")
        return False, None
    except Exception as e:
        print(f"  ❌ ERROR moving {src.name}: {str(e)}")
        return False, None


# --- Move files first (sorted smallest → largest) ---
files = [(f, f.stat().st_size) for f in downloads.iterdir() if f.is_file()]
files.sort(key=lambda x: x[1])

moved_files = 0
skipped_files = 0

for f, size in files:
    # Skip hidden/system files like desktop.ini
    if f.name.startswith('.') or f.name.lower() in ['desktop.ini', 'thumbs.db']:
        print(f"⏭️  SKIPPED system file: {f.name}")
        skipped_files += 1
        continue
    
    ext = f.suffix.lower()[1:] if f.suffix else "Others"
    ext_folder = destination / ext
    ext_folder.mkdir(exist_ok=True)
    
    new_path = ext_folder / f.name
    success, final_path = safe_move_file(f, new_path)
    
    if success:
        print(f"✅ Moved FILE: {f.name} → {ext_folder} ({size/1024:.2f} KB)")
        moved_files += 1
    else:
        skipped_files += 1


# --- Now move folders ---
folders = [d for d in downloads.iterdir() if d.is_dir()]
folders_dest = destination / "folders"
folders_dest.mkdir(exist_ok=True)

moved_folders = 0
skipped_folders = 0

for folder in folders:
    new_path = folders_dest / folder.name
    success, final_path = safe_move_file(folder, new_path)
    
    if success:
        print(f"✅ Moved FOLDER: {folder.name} → {folders_dest}")
        moved_folders += 1
    else:
        skipped_folders += 1


print(f"\n📊 SUMMARY:")
print(f"Files moved: {moved_files}")
print(f"Files skipped: {skipped_files}")
print(f"Folders moved: {moved_folders}")
print(f"Folders skipped: {skipped_folders
