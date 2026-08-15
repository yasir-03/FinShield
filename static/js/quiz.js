// Quiz page: countdown timer, live progress bar, auto-submit on time-up
document.addEventListener("DOMContentLoaded", () => {
    const totalQuestions = typeof TOTAL_QUESTIONS !== "undefined" ? TOTAL_QUESTIONS : 0;
    const timePerQuestion = typeof TIME_PER_QUESTION !== "undefined" ? TIME_PER_QUESTION : 30;
    let secondsLeft = totalQuestions * timePerQuestion;

    const timeDisplay = document.getElementById("timeDisplay");
    const quizForm = document.getElementById("quizForm");
    const progressBar = document.getElementById("quizProgressBar");
    const answeredCountEl = document.getElementById("answeredCount");
    const radios = document.querySelectorAll(".quiz-radio");

    function formatTime(totalSeconds) {
        const m = Math.floor(totalSeconds / 60).toString().padStart(2, "0");
        const s = Math.floor(totalSeconds % 60).toString().padStart(2, "0");
        return `${m}:${s}`;
    }

    function updateTimerDisplay() {
        if (!timeDisplay) return;
        timeDisplay.textContent = formatTime(secondsLeft);
        const timerBox = document.getElementById("quizTimer");
        if (secondsLeft <= 30 && timerBox) {
            timerBox.style.background = "rgba(239, 68, 68, 0.25)";
        }
    }

    function updateProgress() {
        const answeredQuestions = new Set();
        radios.forEach((radio) => {
            if (radio.checked) answeredQuestions.add(radio.dataset.qindex);
        });
        const answered = answeredQuestions.size;
        if (answeredCountEl) answeredCountEl.textContent = answered;
        if (progressBar && totalQuestions > 0) {
            const pct = Math.round((answered / totalQuestions) * 100);
            progressBar.style.width = pct + "%";
        }
    }

    radios.forEach((radio) => radio.addEventListener("change", updateProgress));
    updateProgress();
    updateTimerDisplay();

    if (secondsLeft > 0) {
        const interval = setInterval(() => {
            secondsLeft -= 1;
            updateTimerDisplay();
            if (secondsLeft <= 0) {
                clearInterval(interval);
                if (quizForm) quizForm.submit();
            }
        }, 1000);
    }

    if (quizForm) {
        quizForm.addEventListener("submit", () => {
            const submitBtn = document.getElementById("submitQuizBtn");
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
            }
        });
    }
});
