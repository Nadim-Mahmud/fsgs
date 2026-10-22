import cv2
import numpy as np
import os
import glob
from tqdm import tqdm



input_dir = "../data/cameleon/images"
output_dir = "../data/cameleon_rand_drop/"


os.makedirs(output_dir, exist_ok=True)

image_dirs = glob.glob(os.path.join(input_dir, "*.png"))
rng = np.random.default_rng(seed=42)  # For reproducibility


for image_dir in tqdm(image_dirs, desc="Dropping random pixels"):
    image = cv2.imread(image_dir)
    
    for i in range(5, 101, 5):
        drop_rate = i / 100.0

        mask = np.zeros(image.shape[:2], dtype=bool)
        indices = rng.choice(mask.size, size=int(drop_rate * mask.size), replace=False)
        mask.flat[indices] = True

        # Replace selected pixels with black
        output_image = image.copy()
        output_image[mask] = 0

        output_subdir = os.path.join(output_dir, f"drop_{i}/")
        os.makedirs(output_subdir, exist_ok=True)

        cv2.imwrite(os.path.join(output_subdir, os.path.basename(image_dir)), output_image)