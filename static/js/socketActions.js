// Socket initialization
var socket = io();

// DOM elements
var counterDisplay = document.querySelector(".counter-display");
var resultContainer = document.getElementById("result-container");
var namePlaceholder = document.querySelector(".name-placeholder");
var startCurlsButton = document.querySelector(".start-curls-button");

// Socket event handlers
socket.on("display_countdown", displayCountdown);
socket.on("update_counter", updateCounter);
socket.on("exercise_finished", showCompleteMessage);
socket.on("display_alert", displayAlert);

// Display countdown function
function displayCountdown(countdown) {
    Swal.fire({
        title: "Get ready!",
        text: "The exercise will start in " + countdown + " seconds.",
        icon: "info",
        timer: countdown * 1000,
        showConfirmButton: false,
        allowOutsideClick: false,
        onBeforeOpen: () => {
            Swal.showLoading();
        }
    });
}

// Update counter function
function updateCounter(counter) {
    counterDisplay.textContent = counter;
}

function showCompleteMessage(counter) {
    resultContainer.style.display = "block";

    var feedback = getFeedback(counter);
    var completeMessage =
        namePlaceholder.innerText + " did " + counter + " reps!";
    namePlaceholder.innerText = completeMessage;

    var feedbackElement = createFeedbackElement(feedback.message);
    var imageElement = createImageElement(feedback.image);

    resultContainer.appendChild(feedbackElement);
    resultContainer.appendChild(imageElement);

    hideButton(startCurlsButton);
}

// Get feedback based on counter
function getFeedback(counter) {
    switch (true) {
        case counter < 10:
            return {
                message: "You need to train more weaksauce.",
                image: "weak.jpg",
            };
        case counter < 20:
            return {
                message: "You're not too bad.",
                image: "not_bad.jpg",
            };
        case counter < 30:
            return {
                message: "You're strong!",
                image: "strong.jpg",
            };
        default:
            return {
                message: "You're a GTL!",
                image: "gtl.jpg",
            };
    }
}

// Display Swal.fire alert function
function displayAlert(alertData) {
    Swal.fire({
        title: alertData.title,
        text: alertData.text,
        icon: alertData.icon
    });
}

// Create feedback element
function createFeedbackElement(message) {
    var feedbackElement = document.createElement("p");
    feedbackElement.classList.add("feedback-placeholder");
    feedbackElement.textContent = message;
    return feedbackElement;
}

// Create image element
function createImageElement(image) {
    var imageElement = document.createElement("img");
    imageElement.src = "../static/assets/" + image;
    imageElement.classList.add("result-image");
    return imageElement;
}

// Hide button
function hideButton(button) {
    button.style.display = "none";
}