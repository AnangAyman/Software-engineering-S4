 // Close button functionality
 document.querySelector('.close-button').addEventListener('click', function() {
    alert('Close button clicked');
  });
  
  // Login button functionality
  document.querySelector('.login-button').addEventListener('click', function() {
    alert('Login button clicked');
  });
  
  // Form submission
  document.getElementById('signup-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const age = this.elements['age'].value;
    const name = this.elements['name'].value;
    const email = this.elements['email'].value;
    const password = this.elements['password'].value;
    
    if (!age || !email || !password) {
      alert('Please fill in all required fields');
    } else {
      alert('Account creation form submitted');
      console.log({
        age,
        name,
        email,
        password: '********' // Don't log actual password
      });
    }
  });
  
  // Social login buttons
  document.querySelectorAll('.social-btn').forEach(button => {
    button.addEventListener('click', function() {
      const provider = this.textContent.trim();
      alert(`${provider} login selected`);
    });
  });