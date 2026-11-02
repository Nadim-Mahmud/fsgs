from pathlib import Path

import numpy as np
from PIL import Image


repo_root = Path(__file__).resolve().parents[1]
image_dir = repo_root / "data/cameleon_masked/cameleon/images"
mask_root = repo_root / "data/cameleon_masked/original_masks"
output_root = repo_root / "data/cameleon_masked/masked_256_256"

mask_folders = sorted(folder for folder in mask_root.iterdir() if folder.is_dir())
if not mask_folders:
    raise SystemExit(f"No mask sets found under {mask_root} (expected <set>/images/*.png)")

for mask_folder in mask_folders:
    mask_dir = mask_folder / "images"
    if not mask_dir.is_dir():
        mask_dir = mask_folder

    count = 0
    for mask_path in sorted(mask_dir.rglob("*.png")):
        relative_path = mask_path.relative_to(mask_dir)
        image_path = image_dir / relative_path
        if not image_path.exists():
            raise FileNotFoundError(f"No matching image for mask: {image_path}")

        image = np.array(Image.open(image_path))
        mask = np.array(Image.open(mask_path).convert("L"))
        if image.shape[:2] != mask.shape:
            raise ValueError(
                f"Image/mask dimensions differ: {image_path} {image.shape[:2]}, "
                f"{mask_path} {mask.shape}"
            )

        # White mask pixels keep the image; black mask pixels remove it.
        masked_image = image.copy()
        masked_image[mask == 0] = 0

        output_path = output_root / mask_folder.name / "images" / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(masked_image).save(output_path)
        count += 1

    print(f"{mask_folder.name}: saved {count} masked images")
