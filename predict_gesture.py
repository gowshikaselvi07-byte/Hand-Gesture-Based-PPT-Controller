import cv2
import mediapipe as mp
import joblib
import numpy as np
import pyautogui
import win32gui
import win32con
import time

from collections import deque, Counter


# =========================
# LOAD MODEL
# =========================

model = joblib.load("gesture_model.pkl")
scaler = joblib.load("scaler.pkl")


# =========================
# MEDIAPIPE SETUP
# =========================

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

landmarker = HandLandmarker.create_from_options(options)


# =========================
# FIND POWERPOINT WINDOW
# =========================

def activate_powerpoint():

    windows = []

    def find_window(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)

        if "PowerPoint" in title:
            windows.append(hwnd)

    win32gui.EnumWindows(find_window, None)

    if windows:
        hwnd = windows[0]

        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

        time.sleep(0.1)

        return True

    return False


# =========================
# WEBCAM
# =========================

cap = cv2.VideoCapture(0)

timestamp = 0


# =========================
# GESTURE SMOOTHING
# =========================

gesture_history = deque(maxlen=7)

last_action = "neutral"

cooldown = 0
COOLDOWN_FRAMES = 30


print("Gesture Presentation Controller Started")
print("----------------------------------------")
print("Index finger  = NEXT")
print("Index + Middle = PREVIOUS")
print("Fist           = EXIT")
print("Open Palm      = NEUTRAL")
print("Press Q to quit")
print("----------------------------------------")


# =========================
# MAIN LOOP
# =========================

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    # Mirror webcam
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp += 1

    result = landmarker.detect_for_video(
        mp_image,
        timestamp
    )


    # =========================
    # HAND DETECTED
    # =========================

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        landmarks = []

        for landmark in hand:

            landmarks.extend([
                landmark.x,
                landmark.y,
                landmark.z
            ])


        # =========================
        # WRIST NORMALIZATION
        # =========================

        landmarks = np.array(landmarks)

        landmarks = landmarks.reshape(21, 3)

        wrist = landmarks[0].copy()

        landmarks = landmarks - wrist

        landmarks = landmarks.flatten()


        # =========================
        # SCALE FEATURES
        # =========================

        features = landmarks.reshape(1, -1)

        features_scaled = scaler.transform(features)


        # =========================
        # PREDICT GESTURE
        # =========================

        prediction = model.predict(features_scaled)[0]

        gesture_history.append(prediction)


        # =========================
        # MAJORITY VOTE
        # =========================

        stable_gesture = Counter(
            gesture_history
        ).most_common(1)[0][0]


        # =========================
        # COOLDOWN
        # =========================

        if cooldown > 0:
            cooldown -= 1


        # =========================
        # POWERPOINT CONTROL
        # =========================

        if (
            stable_gesture != last_action
            and cooldown == 0
        ):

            # NEXT SLIDE
            if stable_gesture == "next":

                print("NEXT SLIDE")

                if activate_powerpoint():

                    pyautogui.press("right")

                last_action = "next"

                cooldown = COOLDOWN_FRAMES


            # PREVIOUS SLIDE
            elif stable_gesture == "previous":

                print("PREVIOUS SLIDE")

                if activate_powerpoint():

                    pyautogui.press("left")

                last_action = "previous"

                cooldown = COOLDOWN_FRAMES


            # EXIT PRESENTATION
            elif stable_gesture == "exit":

                print("EXIT PRESENTATION")

                if activate_powerpoint():

                    pyautogui.press("esc")

                last_action = "exit"

                cooldown = COOLDOWN_FRAMES


            # NEUTRAL
            elif stable_gesture == "neutral":

                last_action = "neutral"


        # =========================
        # DISPLAY GESTURE
        # =========================

        cv2.putText(
            frame,
            "Gesture: " + stable_gesture,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )


        # =========================
        # DRAW LANDMARKS
        # =========================

        for landmark in hand:

            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])

            cv2.circle(
                frame,
                (x, y),
                4,
                (255, 0, 0),
                -1
            )


    else:

        # No hand detected
        gesture_history.clear()

        cv2.putText(
            frame,
            "No Hand",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )


    # =========================
    # SHOW CAMERA
    # =========================

    cv2.imshow(
        "Gesture Presentation Controller",
        frame
    )


    # =========================
    # QUIT
    # =========================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# =========================
# CLEANUP
# =========================

cap.release()

cv2.destroyAllWindows()

landmarker.close()

print("Program stopped.")