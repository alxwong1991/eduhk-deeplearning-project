import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO
from modules.camera import Camera
from modules.exercise import Exercise

app = Flask(__name__)
socketio = SocketIO(app)
camera = Camera()
exercise = Exercise()

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('start_bicep_curls')
def start_bicep_curls():
    camera.start_capture()
    exercise.setup_bicep_curls()

    counter = 0  # Reset the counter before starting the exercise

    while camera.cap.isOpened():
        ret, frame = camera.read_frame()

        # Check if frame was successfully captured
        if not ret:
            break

        # Perform bicep curls exercise using the Exercise instance
        frame, angle, counter = exercise.perform_bicep_curls(frame)

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
    camera.release_capture()

    # Emit the final counter value after the exercise ends
    socketio.emit('exercise_finished', counter)

if __name__ == '__main__':
    socketio.run(app, debug=True)