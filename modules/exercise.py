from mediapipe.python.solutions import pose as mp_pose
from modules.bicep_curls import BicepCurls

class Exercise:
    def __init__(self):
        self.bicep_curls = None
        self.timer_expired = False

    def setup_bicep_curls(self):
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            self.bicep_curls = BicepCurls(pose)
            self.bicep_curls.timer_instance.start()

    def perform_bicep_curls(self, frame):
        frame, angle, counter = self.bicep_curls.perform_exercise(frame)
        return frame, angle, counter