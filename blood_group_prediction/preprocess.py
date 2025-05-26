import cv2
import os
import numpy as np

# Define dataset path
dataset_path = "dataset/"
categories = ["A", "B", "AB", "O"]  # Blood groups
image_size = (128, 128)  # Standard size for all images

X = []  # Images data
Y = []  # Labels

for category in categories:
    folder_path = os.path.join(dataset_path, category)
    
    if not os.path.exists(folder_path):
        print(f"Warning: Folder {folder_path} not found, skipping...")
        continue

    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)

        # Load and preprocess the image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is not None:
            resized_image = cv2.resize(image, image_size)  # Resize
            normalized_image = resized_image / 255.0  # Normalize
            X.append(normalized_image)  # Add to dataset
            Y.append(categories.index(category))  # Label (0=A, 1=B, 2=AB, 3=O)

# Convert lists to NumPy arrays
X = np.array(X)
Y = np.array(Y)

# Save as NumPy files for training
np.save("X.npy", X)
np.save("Y.npy", Y)

print("✅ Dataset preprocessing complete!")
print(f"Total Images Processed: {len(X)}")

