
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from alarm import AlarmSystem

import cv2
import mediapipe as mp
import numpy as np
import time

EAR_THRESHOLD = 0.22

CLOSED_TIME_THRESHOLD = 1.5 

ASSET_PATH = os.path.join(current_dir, '..', 'assets', 'alarm.wav')

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def calculate_ear(landmarks, indices, img_w, img_h):
    """
    Calculate Eye Aspect Ratio (EAR).
    EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
    """
    coords = []
    for idx in indices:
        lm = landmarks[idx]
        coords.append(np.array([lm.x * img_w, lm.y * img_h]))

    v1 = np.linalg.norm(coords[1] - coords[5])
    v2 = np.linalg.norm(coords[2] - coords[4])

    h = np.linalg.norm(coords[0] - coords[3])

    if h == 0: return 0.0 # Prevent division by zero
    
    ear = (v1 + v2) / (2.0 * h)
    return ear

def main():
    # 1. Initialize Alarm
    alarm = AlarmSystem(ASSET_PATH)

    # 2. Setup Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    # 3. Setup Face Mesh
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        print("✅ System Started. Press 'q' to quit.")
        
        # State variables
        start_time_closed = None
        eyes_closed = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Mirror frame for natural interaction
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process Face Mesh
            results = face_mesh.process(rgb_frame)

            # Default status
            status_text = "Status: EYES OPEN"
            color = (0, 255, 0) # Green

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    lm = face_landmarks.landmark

                    # Calculate EAR for both eyes
                    left_ear = calculate_ear(lm, LEFT_EYE, w, h)
                    right_ear = calculate_ear(lm, RIGHT_EYE, w, h)

                    # Average EAR
                    avg_ear = (left_ear + right_ear) / 2.0

                    # ---------------------------
                    # DROWSINESS LOGIC
                    # ---------------------------
                    if avg_ear < EAR_THRESHOLD:
                        if not eyes_closed:
                            eyes_closed = True
                            start_time_closed = time.time()
                        
                        # Calculate duration
                        duration = time.time() - start_time_closed
                        
                        # Visual Feedback
                        status_text = f"Status: EYES CLOSED ({duration:.1f}s)"
                        color = (0, 165, 255) # Orange

                        # Check Trigger
                        if duration > CLOSED_TIME_THRESHOLD:
                            status_text = f"🚨 WAKE UP! ({duration:.1f}s) 🚨"
                            color = (0, 0, 255) # Red
                            alarm.start_alarm()
                            
                            # Draw visual border for alarm
                            cv2.rectangle(frame, (0,0), (w,h), (0,0,255), 10)
                    
                    else:
                        # Eyes are open
                        eyes_closed = False
                        start_time_closed = None
                        alarm.stop_alarm()

                    # Display EAR on screen
                    cv2.putText(frame, f"EAR: {avg_ear:.2f}", (20, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Display Status
            cv2.putText(frame, status_text, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            # Show Frame
            cv2.imshow("Driver Drowsiness Detection", frame)

            # Exit logic
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    alarm.stop_alarm()

if __name__ == "__main__":
    main()