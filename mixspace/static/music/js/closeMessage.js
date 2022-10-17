document.addEventListener('DOMContentLoaded', function() {
    messages = document.querySelectorAll('.close');
    messages.forEach(message => {
        message.addEventListener('click', function() {
            const parent = message.parentElement;
            parent.style.display = 'none';
        })
    });
})