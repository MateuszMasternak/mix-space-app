document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#nav-home-page-btn').addEventListener('click', () => showPage('home-page'));
    document.querySelector('#nav-upload-btn').addEventListener('click', () => showPage('upload'));
    document.querySelector('#nav-my-profile-btn').addEventListener('click', () => showPage('user-page'));

    showPage('home-page')
});


function showPage(page, loggedIn=false) {
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
    else if (page === 'user-page') {
        document.querySelector('#home-page').style.display = 'none';
        document.querySelector('#upload').style.display = 'none';
        document.querySelector('#user-page').style.display = 'block';

        username = document.querySelector('#get-current-user').innerHTML;
        showUser(username);
    }
}


function showUser(username) {
    const path = `/show-user/${username}`
    fetch(path)
        .then((response) => response.json())
        .then((data) => {
            document.querySelector('#user-page').innerHTML = '';
            const element = document.createElement('article');
            element.innerHTML = `<h1 class="h1-pos">${data['username']}</h1>`;
            element.innerHTML += '<div class="default-avatar"></div>';
            document.querySelector('#user-page').append(element);
        })
}