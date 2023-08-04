document.addEventListener('DOMContentLoaded', function() {
    let username  = document.querySelector('.su-nick-input');
    if (username) {
        username.addEventListener('focus', () => show('username-form-text'))
        username.addEventListener('blur', () => hide('username-form-text'))
    }
    let password  = document.querySelector('.su-pass-input');
    if (password) {
        password.addEventListener('focus', () => show('password-form-text'))
        password.addEventListener('blur', () => hide('password-form-text'))
    }

    let title  = document.querySelector('.u-title-input');
    if (title) {
        title.addEventListener('focus', () => show('title-form-text'))
        title.addEventListener('blur', () => hide('title-form-text'))
    }
})

function show(infoClass) {
    document.querySelector(`.${infoClass}`).style.display = 'block';
}

function hide(infoClass) {
    document.querySelector(`.${infoClass}`).style.display = 'none';
}
