import cv2
from mediapipe.python.solutions import pose as mp_pose
from modules.bicep_curls import BicepCurls
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/bicep_curls")
def bicep_curls():
    cap = cv2.VideoCapture(1)

    # Curl counter variables
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
            if image is not None and image.shape[0] > 0 and image.shape[1] > 0:
                cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    return render_template('bicep_curls.html')

if __name__ == '__main__':
    app.run(debug=True)