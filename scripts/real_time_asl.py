import cv2
import numpy as np
from tensorflow import keras
import json
from sklearn.preprocessing import LabelEncoder
import os

# Load the saved model
model = keras.models.load_model('../models/asl_model.keras')

# Load the labels and initialize the LabelEncoder
with open('../data/MSASL_train.json', 'r') as f:
    data = json.load(f)

# Collect only labels that have corresponding video files
video_folder = '../videos'
available_labels = {f.split(".mp4")[0] for f in os.listdir(video_folder) if f.endswith(".mp4")}
all_labels = [video['clean_text'] for video in data if video['clean_text'].replace(" ", "_").replace("/", "-") in available_labels]

label_encoder = LabelEncoder()
label_encoder.fit(all_labels)

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

IMG_SIZE = 224  # Size to resize frames

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    frame_resized = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    frame_normalized = frame_resized / 255.0  # Normalize pixel values
    input_data = np.expand_dims(frame_normalized, axis=0)  # Add batch dimension

    # Make a prediction
    prediction = model.predict(input_data)
    predicted_class = np.argmax(prediction)
    
    # Map the predicted class to the label name
    label_name = label_encoder.inverse_transform([predicted_class])[0]
    
    # Display the prediction on the frame
    cv2.putText(frame, label_name, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('ASL Recognition', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
