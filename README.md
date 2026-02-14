# Driver Drowsiness Detection System (Anti-Sleep Alarm)

An anti sleep alarm for drivers.
An end-to-end Computer Vision project designed to prevent accidents caused by driver fatigue. This system uses a webcam to track a driver's eyes in real-time, calculates the Eye Aspect Ratio (EAR), and triggers a loud, non-blocking audio alarm if the driver falls asleep.

## Features
* **Real-Time Eye Tracking:** High-performance facial landmark detection using Google's MediaPipe Face Mesh (>30 FPS).
* **Robust Drowsiness Logic:** Calculates the Eye Aspect Ratio (EAR) based on the 6-point eye contour to accurately determine eye openness, even in low-light conditions.
* **Asynchronous Alarm:** Uses Pygame to play a continuous warning alarm that does not freeze the video feed. Stops immediately when the driver opens their eyes.
* **Visual Status HUD:** On-screen display showing current status (EYES OPEN / EYES CLOSED), timer, and EAR value.

## 📁 Project Structure
Ensure your files are organized exactly like this before running:

```text
ANTI_SLEEP_ALARM/
├── README.md
├── backend/
│   ├── eye_detector.py      # Main computer vision & logic script
│   ├── alarm.py             # Audio handling class
│   └── requirements.txt     # Python dependencies
└── assets/
    └── alarm.wav            # The loud alarm sound file (Must be here!)
Prerequisites (macOS)
Python 3.8+

Built-in webcam or external USB camera.

Allow Terminal/VS Code to access your camera in macOS settings: System Settings > Privacy & Security > Camera.

Installation & Setup
It is highly recommended to use a Virtual Environment (.venv) to prevent library conflicts on macOS.

1. Navigate to the project folder:

Bash
cd path/to/ANTI_SLEEP_ALARM
2. Create and activate a virtual environment:

Bash
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies:

Bash
cd backend
pip install -r requirements.txt
(Note: If you experience missing packages, run: pip install opencv-python mediapipe numpy pygame)

How to Run
Make sure your virtual environment is activated (you should see (.venv) in your terminal prompt).

Ensure you are in the backend folder.

Run the detector:

Bash
python eye_detector.py
Press q to quit the video window.

Configuration
You can adjust the system's sensitivity by modifying the variables at the top of backend/eye_detector.py:

EAR_THRESHOLD = 0.22: The threshold for eye closure. Lower this number (e.g., 0.19) if the system thinks your eyes are closed when they are actually open.

CLOSED_TIME_THRESHOLD = 1.5: How long (in seconds) the driver's eyes must remain closed before the alarm triggers.

Troubleshooting Common Errors
No such file or directory: requirements.txt: You are in the wrong folder. Run cd backend first.

ModuleNotFoundError: No module named 'cv2': Your virtual environment is not activated, or the libraries installed to the wrong Python version. Run source ../.venv/bin/activate and install again.

A wall of objc[...] Class SDL... warnings: This is a known conflict between OpenCV and Pygame on macOS. It is generally harmless. If it causes a crash, ensure from alarm import AlarmSystem is the very first import at the top of eye_detector.py.
