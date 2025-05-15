document.addEventListener('DOMContentLoaded', function() {
    const phrases = [
        "Discover your next favorite bubble tea spot 🧋",
        "Share your boba adventures with friends 👥",
        "Find the perfect drink for your mood 🎯",
        "Join our bubble tea community today 🌟",
        "Rate, review, and recommend your favorites ⭐"
    ];

    let currentPhraseIndex = 0;
    const typingText = document.querySelector('.typing-text');

    function typePhrase() {
        const phrase = phrases[currentPhraseIndex];
        typingText.textContent = '';
        let charIndex = 0;

        function typeChar() {
            if (charIndex < phrase.length) {
                typingText.textContent += phrase.charAt(charIndex);
                charIndex++;
                setTimeout(typeChar, 100);
            } else {
                setTimeout(erasePhrase, 2000);
            }
        }

        function erasePhrase() {
            if (typingText.textContent.length > 0) {
                typingText.textContent = typingText.textContent.slice(0, -1);
                setTimeout(erasePhrase, 50);
            } else {
                currentPhraseIndex = (currentPhraseIndex + 1) % phrases.length;
                setTimeout(typePhrase, 500);
            }
        }

        typeChar();
    }

    if (typingText) {
        typePhrase();
    }
}); 