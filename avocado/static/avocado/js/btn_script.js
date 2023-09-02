const imageButton = document.querySelector('.image-button');

imageButton.addEventListener('mousedown', function() {
  this.classList.add('pressed');
});

imageButton.addEventListener('mouseup', function() {
  this.classList.remove('pressed');
});
