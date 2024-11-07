import os
import cv2
import numpy as np
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Directory where snippets are stored
video_folder = '../videos'
IMG_SIZE = 224  # Size to resize frames

images = []
labels = []

# Load the training data
with open('../data/MSASL_train.json', 'r') as f:
    data = json.load(f)

# Collect only labels that have corresponding video files
available_labels = {f.split(".mp4")[0] for f in os.listdir(video_folder) if f.endswith(".mp4")}

# Iterate over each snippet file that was successfully downloaded
for video in data:
    label_name = video['clean_text'].replace(" ", "_").replace("/", "-")
    snippet_path = os.path.join(video_folder, f"{label_name}.mp4")

    # Check if the snippet file exists and the label is in available labels
    if label_name not in available_labels:
        continue

    # Read the snippet using OpenCV
    cap = cv2.VideoCapture(snippet_path)
    success, frame = cap.read()
    if success:
        # Preprocess the frame: resize and normalize
        frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        frame = frame / 255.0  # Normalize pixel values
        images.append(frame)
        labels.append(label_name)
    cap.release()

# Convert lists to numpy arrays
images = np.array(images)

# Encode labels
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Save the preprocessed data as .npy files
np.save('../data/X_train.npy', X_train)
np.save('../data/X_test.npy', X_test)
np.save('../data/y_train.npy', y_train)
np.save('../data/y_test.npy', y_test)
