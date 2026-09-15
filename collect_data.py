import cv2
import csv
import os
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Model
model_path = "hand_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=model_path
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)


# CSV file
csv_file = "landmarks.csv"

if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)

        header = []

        for i in range(21):
            header.extend([f"x{i}", f"y{i}", f"z{i}"])

        header.append("label")

        writer.writerow(header)


# Camera
cap = cv2.VideoCapture(0)

timestamp = 0
current_label = None

print("Press keys:")
print("1 = Next")
print("2 = Previous")
print("3 = Exit")
print("4 = Neutral")
print("q = Quit")


while True:

    success, frame = cap.read()

    if not success:
        print("Camera not found")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp += 1

    result = detector.detect_for_video(
        mp_image,
        timestamp
    )

    # Draw landmarks
    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        h, w, _ = frame.shape

        for landmark in hand:

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

        # Save data
        if current_label is not None:

            row = []

            for landmark in hand:
                row.extend([
                    landmark.x,
                    landmark.y,
                    landmark.z
                ])

            row.append(current_label)

            with open(csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row)

            cv2.putText(
                frame,
                f"Recording: {current_label}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    cv2.imshow("Dataset Collection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("1"):
        current_label = "next"
        print("Recording NEXT")

    elif key == ord("2"):
        current_label = "previous"
        print("Recording PREVIOUS")

    elif key == ord("3"):
        current_label = "exit"
        print("Recording EXIT")

    elif key == ord("4"):
        current_label = "neutral"
        print("Recording NEUTRAL")

    elif key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()