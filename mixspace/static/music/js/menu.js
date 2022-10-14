document.addEventListener('DOMContentLoaded', function() {
    const pathArray = window.location.pathname.split('/');
    const home = document.querySelector('#nav-home-page-btn');
    const upload = document.querySelector('#nav-upload-btn');
    const following = document.querySelector('#nav-following-btn');
    const liked = document.querySelector('#nav-liked-btn');
    const logIn = document.querySelector('#nav-log-in-btn');
    const signUp = document.querySelector('#nav-sign-up-btn');
    const myProfile = document.querySelector('#nav-my-profile-btn');
    if (pathArray[1] === 'log-in') {
        home.classList.remove('active');
        home.ariaCurrent = '';
        logIn.classList.add('active');
        logIn.ariaCurrent = 'page';
    }
    else if (pathArray[1] === 'sign-up') {
        home.classList.remove('active');
        home.ariaCurrent = '';
        signUp.classList.add('active');
        signUp.ariaCurrent = 'page';
    }
    else if (pathArray[1] === 'upload') {
        home.classList.remove('active');
        home.ariaCurrent = '';
        upload.classList.add('active');
        upload.ariaCurrent = 'page';
    }
    else if (pathArray[1] === 'user') {
        home.classList.remove('active');
        home.ariaCurrent = '';
        myProfile.classList.add('active');
        myProfile.ariaCurrent = 'page';
    }
    else if (pathArray[1] === 'following') {
        home.classList.remove('active');
        home.ariaCurrent = '';
        following.classList.add('active');
        following.ariaCurrent = 'page';
    }
    else if (pathArray[1] === 'liked') {
        home.classList.remove('active');
        home.ariaCurrent = '';
        liked.classList.add('active');
        liked.ariaCurrent = 'page';
    }
})
