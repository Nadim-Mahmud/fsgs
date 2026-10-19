import cv2
import numpy as np
import os
import glob
from tqdm import tqdm



# input_dir = "../data/cameleon/input"
# output_dir = "../data/cameleon_random/input"

input_dir = "../data/cameleon_random/images_original_colmap"
output_dir = "../data/cameleon_random/images"

os.makedirs(output_dir, exist_ok=True)

image_dirs = glob.glob(os.path.join(input_dir, "*.png"))


for image_dir in tqdm(image_dirs, desc="Dropping random pixels"):
    image = cv2.imread(image_dir)
    drop_rate = 0.50

    
    mask = np.random.random(image.shape[:2]) < drop_rate

    # Replace selected pixels with black
    image[mask] = 0

    cv2.imwrite(os.path.join(output_dir, os.path.basename(image_dir)), image)