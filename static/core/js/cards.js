document.addEventListener('DOMContentLoaded', function() {

    const pathArray = window.location.pathname.split('/');
    if (pathArray[1] !== 'core-player') {
        // Click on a track's card will redirect to the player
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            const trackId = card.querySelector('#trackId').innerHTML;
            card.addEventListener('click', (e) => redirect(card, trackId, e));
        });

        // Click on a heart icon or a likes count will change a like status
        const likeForms = document.querySelectorAll('#likeForm');
        likeForms.forEach(form => {
            const unspecifiedLikeBtn = form.querySelector('#unspecifiedLikeButton');
            const unactiveBtn = form.querySelector('#unactiveLikeButton');
            if (unspecifiedLikeBtn) {
                unspecifiedLikeBtn.addEventListener('click', () => like(form));
                showLikeInfo(form, false);
            }
            else if (unactiveBtn) {
                showLikeInfo(form, false);
            }
        })

        // Delete track
        const deleteForms = document.querySelectorAll('#deleteForm');
        deleteForms.forEach(form => {
            const deleteBtn = form.querySelector('#deleteBtn');
            const trackId = form.querySelector('#trackId').innerHTML;
            deleteBtn.addEventListener('click', () => deleteTrack(form, trackId));
        });
    }
    else {
        // Change a like status for the core player
        const likeForm = document.querySelector('#likeForm-player');
        const unspecifiedLikeBtn = likeForm.querySelector('#unspecifiedLikeButton');
        const unactiveBtn = likeForm.querySelector('#unactiveLikeButton');
        if (unspecifiedLikeBtn) {
            unspecifiedLikeBtn.addEventListener('click', () => like(likeForm, true, true));
            showLikeInfo(likeForm, false, true);
        } else if (unactiveBtn) {
            showLikeInfo(likeForm, false, true);
        }
    }

})

function redirect(card, trackId, e) {
    let pass = true;
    const likeForm = card.querySelector('#likeForm');
    const unlikeBtn = card.querySelector('path');
    const likeBtn = card.querySelector('.bi-heart');
    const likesCount = card.querySelector('#likesCount');
    const heartBox = card.querySelector('#heart');
    const deleteBtn = card.querySelector('#deleteBtn');
    if (likeForm === e.target || unlikeBtn === e.target || likeBtn === e.target || likesCount === e.target || heartBox === e.target || deleteBtn === e.target) {
        pass = 'false';
    }

    if (pass === true) {
        const url = `/music-player/${trackId}`;
        window.location.replace(url);
    }
}

function showLikeInfo(likeForm, update=true, player=false) {
    const trackId = likeForm.querySelector('#trackId').innerHTML;
    const path = `/like/${trackId}`;
    fetch(path)
    .then((response) => response.json())
    .then((data) => {
        // Update a likes count
        const likes = likeForm.querySelector('#likesCount');
        const likesPlayer = likeForm.querySelector('#likesCount-player');
        if (likes) {
            likes.innerHTML = '';
            likes.innerHTML = data['likes_count'];
        }
        else {
            likesPlayer.innerHTML = '';
            likesPlayer.innerHTML = data['likes_count'];
        }

        // Update an icon or delete a track's card if the liked page is open,
        // but firstly checks if the icon update is needed
        if (update) {
            const btn = likeForm.querySelector('#likeButton');
            if (btn) {
                // If like is given
                swapForUnlike(likeForm, player)
            }
            else {
                // If unlike is given
                const currentPath = window.location.pathname.split('/');
                if (currentPath[1] === 'liked') {
                    // Delete a track's card
                    likeForm.parentElement.parentElement.parentElement.remove();
                }
                else {
                    swapForLike(likeForm, player);
                }
            }
        }
        else {
            if (data['is_liked']) {
                swapForUnlike(likeForm, player);
            } else {
                swapForLike(likeForm, player);
            }
        }
    })
}

function like(likeForm, update=true, player=false) {
    const trackId = likeForm.querySelector('#trackId').innerHTML;
    const path = `/like/${trackId}`;
    formData = new FormData(likeForm);
    fetch(path, {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then(() => {
        showLikeInfo(likeForm, update, player);
    })
}

function deleteTrack(deleteForm, trackId) {
    const path = `/delete/${trackId}`;
    formData = new FormData(deleteForm);
    fetch(path, {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then(() => {
        deleteForm.parentElement.remove();
    })
}

function swapForUnlike(likeForm, player) {
    const heart = likeForm.querySelector('#heart');
    heart.innerHTML = '';
    if (player) {
        heart.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16" id="unlikeButton"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>';
        const unlikeBtn = likeForm.querySelector('#unlikeButton');
        unlikeBtn.addEventListener('click', () => like(likeForm, true, true));
    } else {
        heart.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16" id="unlikeButton"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>';
        const unlikeBtn = likeForm.querySelector('#unlikeButton');
        unlikeBtn.addEventListener('click', () => like(likeForm));
    }
}

function swapForLike(likeForm, player) {
    const heart = likeForm.querySelector('#heart');
    heart.innerHTML = '';
    if (player) {
        heart.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16" id="likeButton"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/></svg>';
        const likeBtn = likeForm.querySelector('#likeButton');
        likeBtn.addEventListener('click', () => like(likeForm, true, true));
    } else {
        heart.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16" id="likeButton"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/></svg>';
        const likeBtn = likeForm.querySelector('#likeButton');
        likeBtn.addEventListener('click', () => like(likeForm));
    }
}