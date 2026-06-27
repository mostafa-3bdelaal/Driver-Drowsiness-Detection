import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import cv2
import numpy as np
import mediapipe as mp
import winsound
import threading
import time

# ================= Face Mesh =================
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

# ================= Distance Function =================
def distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

# ================= Alarm System =================
ALARM_ON = False

def alarm_sound():
    while ALARM_ON:
        winsound.Beep(1200, 300)

# ================= Drowsiness Settings =================
ALARM_THRESHOLD = 0.20
CLOSED_TIME_LIMIT = 1.5

closed_start_time = None
closed_duration = 0

cv2.namedWindow("Eye Drowsiness System", cv2.WINDOW_NORMAL)

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            h, w, _ = frame.shape

            # ================= Eye Landmarks =================
            left_eye = [33, 160, 158, 133, 153, 144]
            right_eye = [362, 385, 387, 263, 373, 380]

            left_points = []
            right_points = []

            # ================= LEFT EYE =================
            for idx in left_eye:

                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)

                left_points.append((x, y))

                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            # ================= RIGHT EYE =================
            for idx in right_eye:

                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)

                right_points.append((x, y))

                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            # ================= EAR LEFT =================
            left_horizontal = distance(left_points[0], left_points[3])

            if left_horizontal == 0:
                continue

            EAR_left = (
                distance(left_points[1], left_points[5]) +
                distance(left_points[2], left_points[4])
            ) / (2.0 * left_horizontal)

            # ================= EAR RIGHT =================
            right_horizontal = distance(right_points[0], right_points[3])

            if right_horizontal == 0:
                continue

            EAR_right = (
                distance(right_points[1], right_points[5]) +
                distance(right_points[2], right_points[4])
            ) / (2.0 * right_horizontal)

            # ================= Average EAR =================
            EAR = (EAR_left + EAR_right) / 2.0

            # ================= Drowsiness Logic =================
            #  Must 2 eyes be closed
            if EAR_left < ALARM_THRESHOLD and EAR_right < ALARM_THRESHOLD:

                if closed_start_time is None:
                    closed_start_time = time.time()

                closed_duration = time.time() - closed_start_time

            else:

                closed_start_time = None
                closed_duration = 0

                if ALARM_ON:
                    ALARM_ON = False

            # ================= ALERT =================
            if closed_duration >= CLOSED_TIME_LIMIT:

                cv2.putText(
                    frame,
                    "DROWSINESS ALERT !!!",
                    (40, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                if not ALARM_ON:

                    ALARM_ON = True

                    threading.Thread(
                        target=alarm_sound,
                        daemon=True
                    ).start()

            # ================= Display =================

            cv2.putText(
                frame,
                f"Average EAR: {EAR:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Closed Time: {closed_duration:.1f}s",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

    cv2.imshow("Eye Drowsiness System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ================= Cleanup =================
ALARM_ON = False

cap.release()
cv2.destroyAllWindows()