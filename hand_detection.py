import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Model path
model_path = "hand_landmarker.task"

# Create Base Options
base_options = python.BaseOptions(
    model_asset_path=model_path
)

# Create Hand Landmarker options
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2
)

# Create Hand Landmarker
detector = vision.HandLandmarker.create_from_options(options)

# Open webcam
cap = cv2.VideoCapture(0)

timestamp = 0

while True:

    success, frame = cap.read()

    if not success:
        print("Camera not found")
        break

    # Flip camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to MediaPipe Image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Detect hands
    timestamp += 1

    result = detector.detect_for_video(
        mp_image,
        timestamp
    )

    # Draw landmarks
    if result.hand_landmarks:

        for hand_landmarks in result.hand_landmarks:

            for landmark in hand_landmarks:

                h, w, _ = frame.shape

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

    # Display
    cv2.imshow("Hand Detection", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()