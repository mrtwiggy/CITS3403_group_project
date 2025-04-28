/* to be filled with js for user authentication*/

// UI toggle for login/signup forms on index.html
document.addEventListener('DOMContentLoaded', function() {
    const showLoginBtn = document.getElementById('show-login');
    const showSignupBtn = document.getElementById('show-signup');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    if (showLoginBtn && showSignupBtn && loginForm && signupForm) {
        showLoginBtn.addEventListener('click', function() {
            loginForm.classList.remove('hidden');
            signupForm.classList.add('hidden');
            showLoginBtn.classList.add('text-pink-500', 'border-pink-400');
            showLoginBtn.classList.remove('text-gray-400');
            showSignupBtn.classList.remove('text-pink-500', 'border-pink-400');
            showSignupBtn.classList.add('text-gray-400');
        });

        showSignupBtn.addEventListener('click', function() {
            loginForm.classList.add('hidden');
            signupForm.classList.remove('hidden');
            showSignupBtn.classList.add('text-pink-500', 'border-pink-400');
            showSignupBtn.classList.remove('text-gray-400');
            showLoginBtn.classList.remove('text-pink-500', 'border-pink-400');
            showLoginBtn.classList.add('text-gray-400');
        });
    }
});

// Example: (keep your Firebase or other login logic here)
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = loginForm.querySelector('input[type="email"]').value.trim();
            const password = loginForm.querySelector('input[type="password"]').value;

            if (email === 'admin@admin.com' && password === 'root') {
                localStorage.setItem('loggedIn', 'true');
                window.location.href = 'pages/profile.html';
            } else {
                let error = document.getElementById('login-error');
                if (!error) {
                    error = document.createElement('div');
                    error.id = 'login-error';
                    error.className = 'text-red-500 mt-2 text-center';
                    loginForm.appendChild(error);
                }
                error.textContent = 'Invalid email or password.';
            }
        });
    }
});