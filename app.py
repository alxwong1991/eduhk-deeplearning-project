import cv2
from mediapipe.python.solutions import pose as mp_pose
from modules.bicep_curls import BicepCurls
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

cap = None
bicep_curls = None

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    global cap, bicep_curls

    if cap is None:
        cap = cv2.VideoCapture(1)

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Create an instance of BicepCurls
        bicep_curls = BicepCurls(pose)

@socketio.on('start_bicep_curls')
def start_bicep_curls():
    global cap, bicep_curls

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

    # Close the OpenCV window before releasing the camera
    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    socketio.run(app, debug=True)