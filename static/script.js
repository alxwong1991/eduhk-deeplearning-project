document.addEventListener("DOMContentLoaded", function () {
    // Socket initialization
    var socket = io();

    // DOM elements
    var saveNameButton = document.querySelector(".save-name-button");
    var startCurlsButton = document.querySelector(".start-curls-button");
    var namePlaceholder = document.querySelector(".name-placeholder");
    var exerciseButtonsContainer = document.querySelector(".exercise-buttons");
    var counterDisplay = document.querySelector(".counter-display");
    var resultContainer = document.getElementById("result-container");

    // Event listeners
    saveNameButton.addEventListener("click", saveName);
    startCurlsButton.addEventListener("click", startBicepCurls);

    // Socket event handlers
    socket.on("update_counter", updateCounter);
    socket.on("exercise_finished", showCompleteMessage);

    // Save name function
    function saveName() {
        var nameInput = document.querySelector(".name-input");
        var name = nameInput.value.trim();

        if (name === "") {
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Please enter your name.",
            });
            return;
        }

        if (!/^[a-zA-Z]+$/.test(name)) {
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Name can only contain alphabetic characters.",
            });
            return;
        }

        socket.emit("save_name", name);

        nameInput.disabled = true;
        saveNameButton.disabled = true;
        exerciseButtonsContainer.style.display = "block";

        namePlaceholder.innerText = name;
    }

    // Start bicep curls function
    function startBicepCurls() {
        socket.emit("start_bicep_curls");
    }

    // Update counter function
    function updateCounter(counter) {
        counterDisplay.textContent = counter;
    }

    // Show complete message function
    function showCompleteMessage(counter) {
        resultContainer.style.display = "block";

        var feedback = getFeedback(counter);
        var completeMessage =
            namePlaceholder.innerText + " did " + counter + " REPS!";
        namePlaceholder.innerText = completeMessage;

        var feedbackElement = createFeedbackElement(feedback.message);
        var imageElement = createImageElement(feedback.image);

        resultContainer.appendChild(feedbackElement);
        resultContainer.appendChild(imageElement);

        hideButton(startCurlsButton);
    }

    // Get feedback based on counter
    function getFeedback(counter) {
        if (counter < 10) {
            return {
                message: "You need to train more weaksauce.",
                image: "weak.jpg",
            };
        } else if (counter < 20) {
            return {
                message: "You're not too bad.",
                image: "not_bad.jpg",
            };
        } else if (counter < 30) {
            return {
                message: "You're strong!",
                image: "strong.jpg",
            };
        } else {
            return {
                message: "You're a GTL!",
                image: "gtl.jpg",
            };
        }
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
});
