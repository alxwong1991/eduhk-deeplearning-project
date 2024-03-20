// Get the video element
var videoElement = document.getElementById('video');

// Setup mediapipe instance
var pose = new Pose({
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});

// Create an instance of BicepCurls
var bicepCurls = new BicepCurls();

// Function to start the bicep curls exercise
function startExercise() {
  // Request access to the webcam
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
        // Attach the video stream to the video element
        videoElement.srcObject = stream;

        // Start processing the video frames
        processFrames();
      })
      .catch(function(error) {
        console.error('Error accessing the webcam:', error);
      });
  } else {
    console.error('getUserMedia API is not supported');
  }
}

// Function to process the video frames
function processFrames() {
  // Create a canvas element for drawing the image
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');

  function processFrame() {
    // Draw the current video frame on the canvas
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // Get the current frame image data
    var frameData = context.getImageData(0, 0, canvas.width, canvas.height);

    // Perform bicep curls exercise using the BicepCurls instance
    var result = bicepCurls.performExercise(frameData);

    // Display the result or take appropriate actions

    // Request the next frame
    requestAnimationFrame(processFrame);
  }

  // Start processing the frames
  requestAnimationFrame(processFrame);
}

