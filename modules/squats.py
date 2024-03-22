import numpy as np
import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose

class Squats:
    def __init__(self, pose):
        self.counter = 0
        self.stage = None
        self.pose = pose
        
        # Setup mediapipe instance
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def calculate_angle(self, a, b, c):
        # Calculate the angle between three points using numpy
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
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
        # Update squat counter based on the angle
        if 70 < angle < 160:
            if self.stage == "down":
                self.counter += 1
            self.stage = "up"
        elif 190 < angle < 280:
            self.stage = "down"
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
        # Perform squat exercise
        image, landmarks = self.detect(frame)

        if landmarks is not None:
            shoulder = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            hip = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                    landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # Calculate knee angle
            angle_knee = self.calculate_angle(hip, knee, ankle)
            knee_angle = 180 - angle_knee

            # Calculate hip angle
            angle_hip = self.calculate_angle(shoulder, hip, knee)
            hip_angle = 180 - angle_hip

            self.counter = self.update(angle_knee)
            
            image = self.render_counter(frame)

            # Render the counter and landmarks on the frame
            mp_drawing.draw_landmarks(
                image, landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )

            # Visualize knee angle
            knee_coords = tuple(np.multiply(knee, [frame.shape[1], frame.shape[0]]).astype(int))
            cv2.putText(image, str(angle_knee), knee_coords, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # # Visualize hip angle
            hip_coords = tuple(np.multiply(hip, [frame.shape[1], frame.shape[0]]).astype(int))
            cv2.putText(image, str(angle_hip), hip_coords, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        else:
            knee_angle = 0
            hip_angle = 0

        return image, knee_angle, hip_angle