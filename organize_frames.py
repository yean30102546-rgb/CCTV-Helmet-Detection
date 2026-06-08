import os
import shutil
import glob

def organize_dataset_folders():
    base_dir = r"c:\Workplace\CCTV project\dataset_frames"
    
    if not os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} does not exist.")
        return

    old_dir = os.path.join(base_dir, "old_batch")
    new_dir = os.path.join(base_dir, "new_batch")

    os.makedirs(old_dir, exist_ok=True)
    os.makedirs(new_dir, exist_ok=True)

    print("Organizing files in dataset_frames...")

    # Find old frames: frame_*.jpg
    old_files = glob.glob(os.path.join(base_dir, "frame_*.jpg"))
    # Find new frames: hour*.jpg
    new_files = glob.glob(os.path.join(base_dir, "hour*.jpg"))
    # Find any other stray images in the root directory like test_seek_frame.jpg
    stray_images = glob.glob(os.path.join(base_dir, "*.jpg"))
    
    # Filter out files that were already moved or are in subdirectories
    stray_images = [f for f in stray_images if os.path.dirname(f) == base_dir and not os.path.basename(f).startswith("hour") and not os.path.basename(f).startswith("frame_")]

    # Move old files
    print(f"Moving {len(old_files)} old frames to {old_dir}...")
    for f in old_files:
        filename = os.path.basename(f)
        shutil.move(f, os.path.join(old_dir, filename))

    # Move new files
    print(f"Moving {len(new_files)} new frames to {new_dir}...")
    for f in new_files:
        filename = os.path.basename(f)
        shutil.move(f, os.path.join(new_dir, filename))

    # Move stray files to old or keep them
    if stray_images:
        print(f"Moving {len(stray_images)} stray images to {old_dir}...")
        for f in stray_images:
            filename = os.path.basename(f)
            shutil.move(f, os.path.join(old_dir, filename))

    print("\nSuccessfully organized frames!")
    print(f"Old batch folder: {old_dir} (Contains {len(glob.glob(os.path.join(old_dir, '*')))} files)")
    print(f"New batch folder: {new_dir} (Contains {len(glob.glob(os.path.join(new_dir, '*')))} files)")

if __name__ == "__main__":
    organize_dataset_folders()
