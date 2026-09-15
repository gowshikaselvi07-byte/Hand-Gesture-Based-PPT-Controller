# Hand Gesture Based PowerPoint Controller

A real-time computer vision project that allows users to control PowerPoint presentations using hand gestures through a webcam.

## Project Overview

This project uses MediaPipe to detect hand landmarks and Machine Learning to recognize different hand gestures.

The recognized gestures are converted into keyboard commands to control a PowerPoint presentation without using a mouse or keyboard manually.

## Features

- Real-time hand gesture detection using a webcam
- Hand landmark detection using MediaPipe
- Machine Learning based gesture classification
- Next slide control
- Previous slide control
- Exit presentation control
- PowerPoint control using Python

## Gesture Controls

| Gesture | Action |
|---|---|
| Next Gesture | Move to next slide |
| Previous Gesture | Move to previous slide |
| Exit Gesture | Exit the presentation |
| Neutral | No action |

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Scikit-learn
- NumPy
- PyWin32

## How It Works

1. The webcam captures the user's hand.
2. MediaPipe detects the hand landmarks.
3. The landmark coordinates are converted into features.
4. The trained Machine Learning model predicts the gesture.
5. The predicted gesture is mapped to a PowerPoint command.
6. PowerPoint performs the corresponding action.

## Project Files

- `collect_data.py` – Collects hand gesture data
- `train_model.py` – Trains the Machine Learning model
- `predict_gesture.py` – Performs real-time gesture prediction
- `test_ppt.py` – Tests PowerPoint control
- `hand_detection.py` – Hand detection related functionality
- `gesture_model.pkl` – Trained Machine Learning model
- `scaler.pkl` – Feature scaler
- `hand_landmarker.task` – MediaPipe hand landmark model
- `landmarks.csv` – Collected gesture dataset

## Requirements

Install the required Python libraries:

```bash
pip install opencv-python mediapipe scikit-learn numpy pywin32
How to Run
1. Collect gesture data
python collect_data.py
2. Train the model
python train_model.py
3. Start the gesture controller
python predict_gesture.py
4. Open PowerPoint

Start the PowerPoint presentation in Slide Show mode and use the recognized hand gestures to control the slides.

Applications

Touchless presentation control
Smart classrooms
Online teaching
Interactive presentations
Accessibility-focused computer interaction

Future Improvements

Add more gesture commands
Improve gesture recognition accuracy
Support other presentation software
Add voice control
Add customizable gestures
