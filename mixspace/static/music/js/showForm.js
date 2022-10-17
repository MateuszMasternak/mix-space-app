document.addEventListener('DOMContentLoaded', function () {
    const avatarForm = document.querySelector('#avatarForm');
    const image = document.querySelector('#avatar');
    if (avatarForm) {
        image.addEventListener('click', function() {
            if (avatarForm.style.display === 'none') {
                avatarForm.style.display = 'block';
            }
            else {
                avatarForm.style.display = 'none';
            }
        })
    }
})