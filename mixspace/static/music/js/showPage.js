document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#nav-home-page-btn').addEventListener('click', () => showPage('home-page'));
    document.querySelector('#nav-log-in-btn').addEventListener('click', () => showPage('log-in'));
    document.querySelector('#nav-sing-up-btn').addEventListener('click', () => showPage('sign-up'));
    document.querySelector('#nav-upload-btn').addEventListener('click', () => showPage('upload'));
    document.querySelector('#user-page').addEventListener('click', () => showPage('user-page'));

    document.querySelector('#upload-to-register-btn').addEventListener('click', () => showPage('sign-up', p="Only loged in users can upload files."))

    showPage('home-page')
});


function showPage(page, p='') {
    if (page === 'home-page') {
        document.querySelector('#home-page').style.display = 'block';
        document.querySelector('#log-in').style.display = 'none';
        document.querySelector('#sign-up').style.display = 'none';
        document.querySelector('#upload').style.display = 'none';
        document.querySelector('#user-page').style.display = 'none';
    }
    else if (page === 'log-in') {
        document.querySelector('#home-page').style.display = 'none';
        document.querySelector('#log-in').style.display = 'block';
        document.querySelector('#sign-up').style.display = 'none';
        document.querySelector('#upload').style.display = 'none';
        document.querySelector('#user-page').style.display = 'none';
    }
    else if (page === 'sign-up') {
        document.querySelector('#home-page').style.display = 'none';
        document.querySelector('#log-in').style.display = 'none';
        document.querySelector('#sign-up').style.display = 'block';
        document.querySelector('#upload').style.display = 'none';
        document.querySelector('#user-page').style.display = 'none';
        if (p !== '') {
            document.querySelector('#upload-info').innerHTML = p;
            document.querySelector('#upload-info').style.display = 'block';
        }
        else {
            document.querySelector('#upload-info').style.display = 'none';
        }
    }
    else if (page === 'upload') {
        document.querySelector('#home-page').style.display = 'none';
        document.querySelector('#log-in').style.display = 'none';
        document.querySelector('#sign-up').style.display = 'none';
        document.querySelector('#upload').style.display = 'block';
        document.querySelector('#user-page').style.display = 'none';
    }
}
