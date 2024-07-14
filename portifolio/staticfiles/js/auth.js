document.addEventListener('DOMContentLoaded', function() {
    console.log("auth.js is working!");

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const loginValue = document.getElementById('login').value;
            const passwordValue = document.getElementById('password').value;
            const errorMessage = document.getElementById('errorMessage');

            if (loginValue && passwordValue) {
                // Simulate a login process. Replace this with actual authentication logic.
                if (loginValue === "test@example.com" && passwordValue === "password") {
                    console.log("Login successful");
                    errorMessage.style.display = 'none';
                    window.location.href = './dashboard.html'; // Redirect on successful login
                } else {
                    console.log("Login failed: wrong username or password");
                    errorMessage.textContent = "Invalid username or password. Please try again.";
                    errorMessage.style.display = 'block';
                    alert("Invalid username or password. Please try again.");
                }
            } else {
                console.log("Please fill in all fields");
                errorMessage.textContent = "Please fill in all fields.";
                errorMessage.style.display = 'block';
                alert("Please fill in all fields.");
            }
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const firstName = document.getElementById('firstName').value;
            const lastName = document.getElementById('lastName').value;
            const countryCode = document.getElementById('countryCode').value;
            const phone = document.getElementById('phone').value;
            const email = document.getElementById('email').value;
            const dob = document.getElementById('dob').value;
            const gender = document.getElementById('gender').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
	        //const errorMessage = document.getElementById('registerErrorMessage');

            if (firstName && lastName && countryCode && phone && email && dob && gender && password && confirmPassword) {
                if (password === confirmPassword) {
                    console.log("Register form submitted with:", firstName, lastName, countryCode, phone, email, dob, gender, password);
                    alert("Registration successful!");
                    window.location.href = 'dashboard.html';
                    // Implement your registration logic here by sending data to your server for registration
                } else {
                    console.log("Passwords do not match");
                    alert("Passwords do not match. Please try again.");
                }
            } else {
                console.log("Please fill in all fields");
                alert("Please fill in all fields.");
            }
        });
    }
});
