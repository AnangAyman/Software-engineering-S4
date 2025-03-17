// Select elements
const leftNav = document.querySelector('.nav-left');
const rightNav = document.querySelector('.nav-right');
const container = document.querySelector('.carousel-container');

function cycleRight() {
  const firstItem = container.firstElementChild;
  container.appendChild(firstItem.cloneNode(true)); 
  container.removeChild(firstItem);
}

function cycleLeft() {
  const lastItem = container.lastElementChild;
  container.insertBefore(lastItem.cloneNode(true), container.firstElementChild); 
  container.removeChild(lastItem);
}

leftNav.addEventListener('click', () => {
  cycleLeft();
  resetAutoCycle();
});

rightNav.addEventListener('click', () => {
  cycleRight();
  resetAutoCycle();
});

function autoCycle() {
  cycleRight();
}

let autoCycleInterval = setInterval(autoCycle, 3000);

function resetAutoCycle() {
  clearInterval(autoCycleInterval);
  autoCycleInterval = setInterval(autoCycle, 3000);
}

// document.querySelector('.btn-primary').addEventListener('click', function() {
//   location.href = '../signin/signin.html';
// });

// document.querySelector('.btn-secondary').addEventListener('click', function() {
//   location.href ='../login/login.html';
// });