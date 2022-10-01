document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#nav-home-page-btn').addEventListener('click', () => showPage('home-page'));
    document.querySelector('#nav-upload-btn').addEventListener('click', () => showPage('upload'));
    document.querySelector('#user-page').addEventListener('click', () => showPage('user-page'));

    showPage('home-page')
});


function showPage(page) {
    if (page === 'home-page') {
        document.querySelector('#home-page').style.display = 'block';
        document.querySelector('#upload').style.display = 'none';
        document.querySelector('#user-page').style.display = 'none';
    }
    else if (page === 'upload') {
        document.querySelector('#home-page').style.display = 'none';
        document.querySelector('#upload').style.display = 'block';
        document.querySelector('#user-page').style.display = 'none';
    }
}
