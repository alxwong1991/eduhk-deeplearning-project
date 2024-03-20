import numpy as np
import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose

class Squats:
    def __init__(self, pose):
        # Squat counter variables
        self.counter = 0
        self.stage = None
        self.pose = pose
        
        # Setup mediapipe instance
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def detect(self, frame):
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = self.pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        return image, results.pose_landmarks

    def update(self, angle):
        # Squat counter logic
        if angle > 160:
            self.stage = "down"
        if angle < 30 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            print(self.counter)

        return self.counter

    def render_counter(self, frame):
        # Setup status box
        cv2.rectangle(frame, (0, 0), (290, 73), (245, 117, 16), -1)

        # Rep data
        cv2.putText(frame, "REPS", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(self.counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Stage data
        cv2.putText(frame, "STAGE", (105, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, self.stage, (110, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        return frame

    def perform_exercise(self, frame):
        # Perform squats exercise
        image, landmarks = self.detect(frame)
        
        if landmarks is not None:
            left_hip = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y]
            left_knee = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y]
            left_ankle = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y]

            # Calculate angle
            angle = self.calculate_angle(left_hip, left_knee, left_ankle)

            # Update exercise counter
            self.counter = self.update(angle)

            # Render counter on the frame
            image = self.render_counter(frame)

            # Draw landmarks and connections on the frame
            mp_drawing.draw_landmarks(
                image, landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )
            
            # Visualize angle
            knee_coords = tuple(np.multiply(left_knee, [frame.shape[1], frame.shape[0]]).astype(int))
            cv2.putText(image, str(angle), knee_coords, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            angle = 0

        # Return the modified image and angle
        return image, angle