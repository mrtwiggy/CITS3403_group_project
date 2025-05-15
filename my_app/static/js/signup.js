document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const submitButton = document.getElementById('submit-btn');

    const lengthCheck = document.getElementById('length-check');
    const uppercaseCheck = document.getElementById('uppercase-check');
    const lowercaseCheck = document.getElementById('lowercase-check');
    const numberCheck = document.getElementById('number-check');
    const specialCheck = document.getElementById('special-check');
    const passwordMatch = document.getElementById('password-match');

    function updateRequirement(element, isValid) {
        const icon = element.querySelector('svg');
        if (isValid) {
            element.classList.remove('text-gray-500');
            element.classList.add('text-green-500');
            icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>';
        } else {
            element.classList.remove('text-green-500');
            element.classList.add('text-gray-500');
            icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>';
        }
    }

    function validatePassword() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // Check length
        updateRequirement(lengthCheck, password.length >= 6);

        // Check uppercase
        updateRequirement(uppercaseCheck, /[A-Z]/.test(password));

        // Check lowercase
        updateRequirement(lowercaseCheck, /[a-z]/.test(password));

        // Check number
        updateRequirement(numberCheck, /[0-9]/.test(password));

        // Check special character
        updateRequirement(specialCheck, /[!@#$%^&*(),.?":{}|<>]/.test(password));

        // Check if passwords match
        updateRequirement(passwordMatch, password === confirmPassword && password !== '');

        // Enable submit button if all requirements are met
        const allRequirementsMet = 
            password.length >= 6 &&
            /[A-Z]/.test(password) &&
            /[a-z]/.test(password) &&
            /[0-9]/.test(password) &&
            /[!@#$%^&*(),.?":{}|<>]/.test(password) &&
            password === confirmPassword &&
            password !== '';

        submitButton.disabled = !allRequirementsMet;
        if (allRequirementsMet) {
            submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
            submitButton.classList.add('hover:bg-pink-500');
        } else {
            submitButton.classList.add('opacity-50', 'cursor-not-allowed');
            submitButton.classList.remove('hover:bg-pink-500');
        }
    }

    passwordInput.addEventListener('input', validatePassword);
    confirmPasswordInput.addEventListener('input', validatePassword);
}); 