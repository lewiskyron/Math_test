window.onload = function() {
    // Start the timer as soon as the game page loads
    startTimer();
};

function startTimer() {
    var startTime = new Date();
    var timerDisplay = document.getElementById('timer');

    // Update the timer every second
    setInterval(function() {
        var currentTime = new Date();
        var elapsed = currentTime - startTime;
        var seconds = Math.floor(elapsed / 1000);
        if (timerDisplay) {
            timerDisplay.textContent = `Time: ${seconds} seconds`;
        }
    }, 1000);
}
