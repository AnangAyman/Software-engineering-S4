document.querySelector('.close-button').addEventListener('click', function() {
    alert('Close button clicked');
});

document.querySelector('.sign-up').addEventListener('click', function(){
    location.href = '../signin/signin.html';
    }
)

document.querySelector('.login-button').addEventListener('click', function() {
    const email = document.querySelector('input[type="text"]').value;
    const password = document.querySelector('input[type="password"]').value;
    
    if (email && password) {
        alert('Login attempted with: ' + email);
    } else {
        alert('Please fill in all fields');
    }
});

document.querySelectorAll('.social-button').forEach(button => {
    button.addEventListener('click', function() {
        const provider = this.textContent.trim();
        alert(provider + ' login selected');
    });
});

