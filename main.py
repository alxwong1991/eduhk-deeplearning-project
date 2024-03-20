import cv2
# from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose
from modules.bicep_curls import BicepCurls

cap = cv2.VideoCapture(1)

#Curl counter variables
counter = 0
stage = None

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # Create an instance of BicepCurls
    bicep_curls = BicepCurls()

    while cap.isOpened():
        ret, frame = cap.read()

        # Check if frame was successfully captured
        if not ret:
            break

        # Perform bicep curls exercise using the BicepCurls instance
        image, angle = bicep_curls.perform_exercise(frame)

        # Check if image size is valid before displaying
        if image.shape[0] > 0 and image.shape[1] > 0:
            cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()