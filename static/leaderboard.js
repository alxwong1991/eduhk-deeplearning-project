document.addEventListener("DOMContentLoaded", function () {
    var socket = io();
    var leaderboardButton = document.querySelector(".leaderboard-button");
    var leaderboardModal = document.querySelector(".leaderboard-modal");

    var leaderboardCloseBtn = document.querySelector(".close");
    var leaderboardBody = document.querySelector(".leaderboard-body");

    leaderboardButton.addEventListener("click", openLeaderboardModal);
    leaderboardCloseBtn.addEventListener("click", closeLeaderboardModal);
    window.addEventListener("click", outsideClick);

    socket.on("leaderboard_data", updateLeaderboard);

    function openLeaderboardModal() {
        leaderboardModal.style.display = "block";
        socket.emit("get_leaderboard_data");
    }

    function closeLeaderboardModal() {
        leaderboardModal.style.display = "none";
    }

    function outsideClick(event) {
        if (event.target === leaderboardModal) {
            leaderboardModal.style.display = "none";
        }
    }

    function updateLeaderboard(data) {
        leaderboardBody.innerHTML = "";

        data.forEach(function (row) {
            var newRow = document.createElement("tr");
            var nameCell = document.createElement("td");
            var repsCell = document.createElement("td");

            nameCell.innerText = row.name;
            repsCell.innerText = row.reps;

            newRow.appendChild(nameCell);
            newRow.appendChild(repsCell);

            leaderboardBody.appendChild(newRow);
        });
    }
});