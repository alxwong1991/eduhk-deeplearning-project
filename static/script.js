document.addEventListener("DOMContentLoaded", function () {
    var socket = io();
    var saveNameButton = document.querySelector(".save-name-button");
    var startCurlsButton = document.querySelector(".start-curls-button");
    var namePlaceholder = document.querySelector(".name-placeholder");
    // var feedbackPlaceholder = document.querySelector(".feedback-placeholder");
    var exerciseButtonsContainer = document.querySelector(".exercise-buttons");
    // var saveDataButton = document.querySelector(".save-data-button");
    var counterDisplay = document.querySelector("counter-display");
    var resultContainer = document.getElementById("result-container");

    saveNameButton.addEventListener("click", saveName);
    startCurlsButton.addEventListener("click", startBicepCurls);
    // saveDataButton.addEventListener("click", saveData);

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
        counterDisplay.innerHTML = counter;
    }

    function showCompleteMessage(counter) {
        resultContainer.style.display = "block";

        var feedbackMessage = "";
        var feedbackImage = "";

        if (counter < 10) {
            feedbackMessage = "You need to train more weaksauce.";
            feedbackImage = "weak.jpg";
        } else if (counter >= 10 && counter < 20) {
            feedbackMessage = "You're not too bad.";
            feedbackImage = "not_bad.jpg";
        } else if (counter >= 20 && counter < 30) {
            feedbackMessage = "You're strong!";
            feedbackImage = "strong.jpg";
        } else if (counter >= 30) {
            feedbackMessage = "You're a GTL!";
            feedbackImage = "gtl.jpg";
        }

        var completeMessage = namePlaceholder.innerText + " did " + counter + " REPS!";
        namePlaceholder.innerText = completeMessage;

        var feedbackElement = document.createElement("p");
        feedbackElement.classList.add("feedback-placeholder");
        feedbackElement.innerText = feedbackMessage;
        resultContainer.insertBefore(feedbackElement, imageElement);
    
        var imageElement = document.createElement("img");
        imageElement.src = "../static/assets/" + feedbackImage;
        imageElement.classList.add("result-image");
        resultContainer.appendChild(imageElement);

        var saveDataButton = document.createElement("button");
        saveDataButton.classList.add("save-data-button");
        saveDataButton.innerText = "Save Data";
        resultContainer.appendChild(saveDataButton);

        hideButton(startCurlsButton);
    }

    function hideButton(button) {
        button.style.display = "none";
    }

    // function saveData() {
    //     var name = namePlaceholder.innerText;
    //     var reps = document.getElementById("counter-display").innerText;

    //     var data = {
    //         name: name,
    //         reps: reps,
    //     };

    //     socket.emit("save_data", data);
    // }
});
