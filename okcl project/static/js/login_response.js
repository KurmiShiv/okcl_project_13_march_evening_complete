// Get the form element
const loginForm = document.querySelector('form');

// Add a submit event listener to the form
loginForm.addEventListener('submit', async(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Get the input values from the form fields
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const role = document.getElementById('role').value;

  // Send an AJAX request to the server to validate the credentials
  const res = await fetch('http://127.0.0.1:5500/login',{
    method : 'POST',
    headers:{
       
    }
  })
});
