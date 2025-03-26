function showCorrectAnswer() {
  document.querySelector('.correct-answer').style.display = 'block';
}

document.addEventListener("DOMContentLoaded", function() {
  document.querySelector('.option.o').addEventListener('click', showCorrectAnswer);
});
