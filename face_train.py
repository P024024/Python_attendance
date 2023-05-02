import cv2
import numpy as np
import os

# Define the size of the images for training
width, height = 100, 100

# Load the classifier for detecting faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize the recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Create an empty list to store the training images and labels
training_data = []
labels = []

# Create a dictionary to map person names to integer labels
label_dict = {}

# Loop through the directory of images for each person
for subdir, dirs, files in os.walk('dataset'):
    # Skip empty directories
    if len(files) == 0:
        continue

    # Assign a unique integer label to each person
    label = len(label_dict)
    label_dict[subdir] = label

    for file in files:
        # Skip hidden files
        if file.startswith('.'):
            continue

        # Load the image
        img_path = os.path.join(subdir, file)
        img = cv2.imread(img_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the face in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Crop the face from the image and resize it
        for (x, y, w, h) in faces:
            face = cv2.resize(gray[y:y+h, x:x+w], (width, height))

            # Add the face and its label to the training data
            training_data.append(face)
            labels.append(label)

# Convert labels to numpy.ndarray with a data type of np.int32
labels = np.array(labels).astype(np.int32)

# Train the recognizer using the training data and labels
recognizer.train(training_data, labels)

# Save the trained recognizer to a file
if not os.path.exists('trainer.yml'):
    open('trainer.yml', 'w').close()
recognizer.write('trainer.yml')
