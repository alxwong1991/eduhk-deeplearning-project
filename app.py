import cv2
# from peewee import *
# from models.leaderboard import Leaderboard
from mediapipe.python.solutions import pose as mp_pose
from modules.bicep_curls import BicepCurls
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

cap = None
bicep_curls = None

# Connect to the database
# db = SqliteDatabase('user_data.db')

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('start_bicep_curls')
def start_bicep_curls():
    global cap, bicep_curls

    if cap is None:
        cap = cv2.VideoCapture(1)

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Create an instance of BicepCurls
        bicep_curls = BicepCurls(pose)

    counter = 0  # Reset the counter before starting the exercise

    # Connect to the database
    # db.connect()
    # db.create_tables([Leaderboard])

    # Create a new leaderboard record in the database
    # leaderboard = Leaderboard.create(name='Bicep Curls', reps=0, counter=counter)

    while cap.isOpened():
        ret, frame = cap.read()

        # Check if frame was successfully captured
        if not ret:
            break

        # Perform bicep curls exercise using the BicepCurls instance
        frame, angle, counter = bicep_curls.perform_exercise(frame)

        # Check if image size is valid before displaying
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
            cv2.imshow('Mediapipe Feed Bicep Curls', frame)

        # Emit the counter value to the client
        socketio.emit('update_counter', counter)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Close the OpenCV window before releasing the camera
    cv2.destroyAllWindows()

    # Release the camera capture
    if cap is not None:
        cap.release()

    # Emit the final counter value after the exercise ends
    socketio.emit('exercise_finished', counter)

if __name__ == '__main__':
    socketio.run(app, debug=True)