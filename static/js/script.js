document.addEventListener("DOMContentLoaded", function () {
    // DOM elements
    var saveNameButton = document.querySelector(".save-name-button");
    // var startCurlsButton = document.querySelector(".start-curls-button");
    // var namePlaceholder = document.querySelector(".name-placeholder");
    var exerciseButtonsContainer = document.querySelector(".exercise-buttons");

    // Event listeners
    saveNameButton.addEventListener("click", saveName);
    startCurlsButton.addEventListener("click", startBicepCurls);

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
});