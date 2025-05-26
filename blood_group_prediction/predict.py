import cv2
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model("blood_group_model.h5")

# Define blood group labels
blood_groups = ["A", "B", "AB", "O"]

def predict_blood_group(image_path):
    """Predicts the blood group based on a fingerprint image."""
    
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        return "Error: Could not load image!"

    # Preprocess the image (resize & normalize)
    image = cv2.resize(image, (128, 128))  # Resize to match training size
    image = image / 255.0  # Normalize
    image = np.expand_dims(image, axis=[0, -1])  # Reshape for model input

    # Make prediction
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)  # Get class with highest probability

    return blood_groups[predicted_class]

# Example usage (You can replace 'test.bmp' with an actual file path)
if __name__ == "__main__":
    test_image = "dataset/A/cluster_0_5652.BMP"  # Use an existing file
 # Replace with an actual test image
    result = predict_blood_group(test_image)
    print(f"Predicted Blood Group: {result}")
