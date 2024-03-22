import cv2
import signal
from mediapipe.python.solutions import pose as mp_pose
from modules.bicep_curls import BicepCurls
from modules.squats import Squats
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

cap = None
bicep_curls = None
squats = None

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    global cap, bicep_curls, squats

    if cap is None:
        cap = cv2.VideoCapture(1)

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Create an instance of BicepCurls
        bicep_curls = BicepCurls(pose)

        # Create an instance of Squats
        squats = Squats(pose)

@socketio.on('start_bicep_curls')
def start_bicep_curls():
    global cap, bicep_curls

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Create an instance of BicepCurls
        bicep_curls = BicepCurls(pose)

    while cap.isOpened():
        ret, frame = cap.read()

        # Check if frame was successfully captured
        if not ret:
            break

        # Perform bicep curls exercise using the BicepCurls instance
        frame, angle = bicep_curls.perform_exercise(frame)

        # Check if image size is valid before displaying
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
            cv2.imshow('Mediapipe Feed Bicep Curls', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Close the OpenCV window before releasing the camera
    cv2.destroyAllWindows()

@socketio.on('start_squats')
def start_squats():
    global cap, squats

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Create an instance of Squats
        squats = Squats(pose)

    while cap.isOpened():
        ret, frame = cap.read()

        # Check if frame was successfully captured
        if not ret:
            break

        # Perform squats exercise using the Squats instance
        frame, angle = squats.perform_exercise(frame)

        # Check if image size is valid before displaying
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
            cv2.imshow('Mediapipe Feed Squats', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Close the OpenCV window before releasing the camera
    cv2.destroyAllWindows()

def signal_handler(signal, frame):
    global cap

    if cap is not None:
        cap.release()

    # Emit a custom event to stop the exercise
    socketio.emit('stop_exercise')

    # Let the event be processed before stopping the server
    socketio.sleep(1)

    # Get the Flask application instance from the SocketIO instance
    app = socketio.server.app

    # Stop the Flask application
    socketio.stop()

    # Stop the Flask development server
    app.shutdown()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    socketio.run(app, debug=True)