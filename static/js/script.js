document.addEventListener("DOMContentLoaded", function () {
    // DOM elements
    var saveNameButton = document.querySelector(".save-name-button");
    var exerciseButtonsContainer = document.querySelector(".exercise-buttons");

    // Event listeners
    saveNameButton.addEventListener("click", saveName);
    startCurlsButton.addEventListener("click", startBicepCurls);

    // Save name function
    function saveName() {
        var nameInput = document.querySelector(".name-input");
        var name = nameInput.value.trim();

        if (name === "") {
            showErrorAlert("Please enter your name.");
            return;
        }
    
        if (/\s/.test(name)) {
            showErrorAlert("Name cannot contain spaces.");
            return;
        }
    
        if (!/^[a-zA-Z]+$/.test(name)) {
            showErrorAlert("Name can only contain alphabetic characters.");
            return;
        }

        showSuccessAlert("Name has been successfully saved!")

        socket.emit("save_name", name);

        nameInput.disabled = true;
        saveNameButton.disabled = true;
        exerciseButtonsContainer.style.display = "block";

        namePlaceholder.innerText = name;
    }

    function showErrorAlert(message) {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: message,
        });
    }

    function showSuccessAlert(message) {
        Swal.fire({
            icon: "success",
            title: "Success!",
            text: message
        })
    }

    // Start bicep curls function
    function startBicepCurls() {
        socket.emit("start_bicep_curls");
    }
});