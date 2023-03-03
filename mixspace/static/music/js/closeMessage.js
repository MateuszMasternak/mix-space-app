document.addEventListener('DOMContentLoaded', function() {
    let messages = document.querySelectorAll('.close');
    messages.forEach(message => {
        message.addEventListener('click', function() {
            const parent = message.parentElement;
            parent.remove();
        })
    });
})