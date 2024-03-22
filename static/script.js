document.addEventListener("DOMContentLoaded", function () {
    var socket = io();
    var saveNameButton = document.querySelector(".save-name-button");
    var startCurlsButton = document.querySelector(".start-curls-button");
    var namePlaceholder = document.querySelector(".name-placeholder");
    var feedbackPlaceholder = document.querySelector(".feedback-placeholder");
    var exerciseButtonsContainer = document.querySelector(".exercise-buttons");
    var saveDataButton = document.querySelector(".save-data-button");

    saveNameButton.addEventListener("click", saveName);
    startCurlsButton.addEventListener("click", startBicepCurls);
    saveDataButton.addEventListener("click", saveData);

    socket.on("update_counter", updateCounter);
    socket.on("exercise_finished", showCompleteMessage);

    function saveName() {
        var nameInput = document.querySelector(".name-input");
        var name = nameInput.value.trim();

        if (name === "") {
            alert("Please enter your name.");
            return;
        }

        socket.emit("save_name", name);

        nameInput.disabled = true;
        saveNameButton.disabled = true;
        exerciseButtonsContainer.style.display = "block";

        namePlaceholder.innerText = name;
    }

    function startBicepCurls() {
        socket.emit("start_bicep_curls");
    }

    function updateCounter(counter) {
        var counterDisplay = document.querySelector("counter-display");
        counterDisplay.innerHTML = counter;
    }

    function showCompleteMessage(counter) {
        var counterContainer = document.querySelector("counter-container");
        counterContainer.style.display = "block";

        var feedbackMessage = "";

        if (counter < 10) {
            feedbackMessage = "You need to train more.";
        } else if (counter >= 10 && counter < 20) {
            feedbackMessage = "You're not too bad.";
        } else if (counter >= 20 && counter < 30) {
            feedbackMessage = "You're strong!";
        }

        var completeMessage =
            namePlaceholder.innerText + " did " + counter + " REPS";
        namePlaceholder.innerText = completeMessage;
        feedbackPlaceholder.innerText = feedbackMessage;

        saveDataButton.style.display = "block";
        hideButton(startCurlsButton);

        // Show counter-container items
        document.querySelector(".counter-container").style.display = "block";
    }

    function hideButton(button) {
        button.style.display = "none";
    }

    function saveData() {
        var name = namePlaceholder.innerText;
        var reps = document.getElementById("counter-display").innerText;

        var data = {
            name: name,
            reps: reps,
        };

        socket.emit("save_data", data);
    }
});