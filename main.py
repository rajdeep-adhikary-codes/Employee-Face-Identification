import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import os
import cv2
import numpy as np
from tqdm import tqdm  # Import tqdm for loading animation

# Function to load and preprocess images
def load_images(directory):
    images = []
    labels = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (1920, 1080))  # Adjust the size as needed
            images.append(img)
            labels.append(filename.split("_")[0])  # Extract MongoDB ID from the filename
    return np.array(images), np.array(labels)

# Load and preprocess the training dataset
trainset_directory = "./dataset/train/"
X_train, y_train = load_images(trainset_directory)

# Load and preprocess the test dataset
testset_directory = "./dataset/test/"
X_test, y_test = load_images(testset_directory)


# Normalize pixel values to be between 0 and 1
X_train, X_test = X_train / 255.0, X_test / 255.0

# Define the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)  # Assuming a binary classification task (one output node)
])

# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.MeanSquaredError(),
              metrics=['accuracy'])

# Train the model with tqdm for loading animation
epochs = 10
for epoch in range(epochs):
    print(f"Epoch {epoch + 1}/{epochs}")
    for X_batch, y_batch in tqdm(zip(X_train, y_train), total=len(X_train)):
        model.train_on_batch(np.expand_dims(X_batch, axis=0), np.array([y_batch]))

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# Save the trained model
model.save("face_recognition_model.h5")
