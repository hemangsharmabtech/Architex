document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (response.ok) {
            // Redirect to the floor plan page on successful login
            window.location.href = '/floor_plan';
        } else {
            // Display error message if login fails
            document.getElementById('error-message').textContent = result.message || 'Invalid credentials. Please try again or sign up.';
        }
    } catch (error) {
        console.error('Error during login:', error);
        document.getElementById('error-message').textContent = 'An error occurred. Please try again later.';
    }
});
