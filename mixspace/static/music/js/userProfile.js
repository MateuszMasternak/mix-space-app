document.addEventListener('DOMContentLoaded', function () {
    const followForm = document.querySelector('#followForm');
    if (followForm) {
        showFollowButton(followForm);
        followForm.addEventListener('submit', (e) => follow(followForm, e));
    }
})

function showFollowButton(followForm) {
    const pathArray = window.location.pathname.split('/');
    const path = `/follow/${pathArray[2]}`;
    fetch(path)
    .then((response) => response.json())
    .then((data) => {
        const btn = followForm.querySelector('button');
        if (btn) {
            btn.remove();
        }
        button = document.createElement('button');
        if (data['is_followed'] === true) {
            button.classList.add('btn', 'btn-outline-danger', 'unfollowButton');
            button.textContent = 'Unfollow';
        }
        else if (data['is_followed'] === false) {
            button.classList.add('btn', 'btn-outline-primary', 'followButton');
            button.textContent = 'Follow';   
        }
        button.id = 'followButton';
        button.type = 'submit';
        followForm.append(button);
    })
}

function follow(followForm, e) {
    e.preventDefault();
    const pathArray = window.location.pathname.split('/');
    const path = `/follow/${pathArray[2]}`;
    formData = new FormData(followForm);
    fetch(path, {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then(() => {
        showFollowButton(followForm);
    })
}