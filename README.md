# Driver-Drowsiness-Detection
Real-time driver drowsiness detection using MediaPipe Face Mesh, OpenCV, and Eye Aspect Ratio (EAR) with an audio alert system.


# 🚗 Driver Drowsiness Detection

A real-time AI-powered Driver Drowsiness Detection System built with **Python**, **OpenCV**, and **MediaPipe Face Mesh**.

The system continuously tracks both eyes, calculates the **Eye Aspect Ratio (EAR)**, and detects prolonged eye closure to identify signs of driver drowsiness. If both eyes remain closed for a predefined duration, an audible alarm is triggered to alert the driver.



---

## ✨ Features

- Real-time face landmark detection
- Eye Aspect Ratio (EAR) calculation
- Independent left and right eye tracking
- Detects drowsiness only when **both eyes** are closed
- Continuous timer for eye closure duration
- Audible warning alarm
- Live visualization of facial landmarks
- Lightweight and runs using a standard webcam

---

## 🛠 Technologies Used

- Python
- OpenCV
- MediaPipe Face Mesh
- NumPy
- Winsound
- Multithreading

---

## 📖 How It Works

1. Capture frames from the webcam.
2. Detect facial landmarks using MediaPipe Face Mesh.
3. Extract eye landmarks.
4. Calculate the Eye Aspect Ratio (EAR) for both eyes.
5. Compute the average EAR.
6. Monitor eye closure duration.
7. Trigger an alarm if both eyes remain closed longer than the threshold.

---

## 📐 Eye Aspect Ratio (EAR)

The Eye Aspect Ratio is calculated as:

EAR = (Vertical Distance 1 + Vertical Distance 2) / (2 × Horizontal Distance)

A lower EAR indicates that the eye is closing.

---

## 📁 Project Structure

```
Driver-Drowsiness-Detection/
│
├── main.py
├── README.md
└── requirements.txt
```

---

## ⚡ Configuration

You can easily modify the detection parameters:

```python
ALARM_THRESHOLD = 0.20
CLOSED_TIME_LIMIT = 1.5
```

---

## 🚨 Alert Logic

The alarm activates only when:

- Left eye is closed.
- Right eye is closed.
- Both remain closed longer than the configured threshold.

This reduces false alarms caused by blinking or closing only one eye.

