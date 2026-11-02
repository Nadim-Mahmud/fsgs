import cv2
import os
import glob
from pathlib import Path

# Set your paths here
PROJECT_DIR = Path(__file__).resolve().parent.parent
COLMAP_MASK_DIR = PROJECT_DIR / "data/cameleon_masked/projected_masks"  # Where COLMAP output the masks
CLEAN_MASK_DIR = PROJECT_DIR / "data/cameleon_masked/thresholded_mask"  # Where your clean masks will go

os.makedirs(CLEAN_MASK_DIR, exist_ok=True)


# Search nested mask folders for PNG images.
mask_paths = glob.glob(os.path.join(COLMAP_MASK_DIR, "**", "*.png"), recursive=True)

print(f"Found {len(mask_paths)} masks to process.")

for path in mask_paths:
    relative_path = os.path.relpath(path, COLMAP_MASK_DIR)
    
    # 1. Read the mask in grayscale mode
    gray_mask = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if gray_mask is None:
        raise RuntimeError(f"Could not read mask: {path}")
    
    # 2. Force any interpolated gray edges to pure black (0) or pure white (255)
    # Otsu selects a threshold from the image intensity distribution.
    _, binary_mask = cv2.threshold(gray_mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 3. Save the crisp binary mask
    output_path = os.path.join(CLEAN_MASK_DIR, relative_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if not cv2.imwrite(output_path, binary_mask):
        raise RuntimeError(f"Could not save mask: {output_path}")

print(f"Done! Clean, strict binary masks saved to: {CLEAN_MASK_DIR}")
