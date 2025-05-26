import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Load preprocessed data
X = np.load("X.npy")
Y = np.load("Y.npy")

# Reshape X for CNN input
X = X.reshape(-1, 128, 128, 1)  # Add channel dimension for grayscale

# Convert labels to categorical (One-Hot Encoding)
Y = tf.keras.utils.to_categorical(Y, num_classes=4)

# Define CNN model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 1)),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax')  # 4 output classes (A, B, AB, O)
])

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X, Y, epochs=10, batch_size=32, validation_split=0.2)

# Save trained model
model.save("blood_group_model.h5")

print("✅ Model training complete! Model saved as 'blood_group_model.h5'")
