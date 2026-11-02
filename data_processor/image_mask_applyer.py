from pathlib import Path

import cv2


repo_root = Path(__file__).resolve().parents[1]
image_dir = repo_root / "data/cameleon/images"
mask_root = repo_root / "data/cameleon_masked/thresholded_mask"
output_root = repo_root / "data/cameleon_masked"

for mask_folder in sorted(mask_root.iterdir()):
    if not mask_folder.is_dir():
        continue

    count = 0
    for mask_path in sorted((mask_folder / "images").rglob("*.png")):
        relative_path = mask_path.relative_to(mask_folder / "images")
        image_path = image_dir / relative_path
        image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if image is None or mask is None:
            raise RuntimeError(f"Could not read image/mask pair: {image_path}, {mask_path}")
        if image.shape[:2] != mask.shape:
            raise ValueError(f"Image/mask dimensions differ: {image_path}, {mask_path}")

        # White mask pixels keep the image; black mask pixels remove it.
        masked_image = image.copy()
        masked_image[mask == 0] = 0

        output_path = output_root / mask_folder.name / "images" / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(output_path), masked_image):
            raise RuntimeError(f"Could not save image: {output_path}")
        count += 1

    print(f"{mask_folder.name}: saved {count} masked images")
