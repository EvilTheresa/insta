async function makeRequest(url, method = 'POST') {
    const csrfToken = document.body.getAttribute('data-csrf-token');
    let response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
    });
    if (response.ok) {
        return await response.json();
    } else {
        let errorText = await response.text();
        let error = new Error(`HTTP Error: ${response.status}: ${errorText}`);
        console.error(error);
        throw error;
    }
}

async function onClick(event) {
    event.preventDefault();
    let button = event.currentTarget;
    let postId = button.getAttribute('data-post-id');


    let url = `/api/post/${postId}/toggle_like/`;
    try {
        let response = await makeRequest(url);
        button.innerHTML = response.liked ? '<i class="bi bi-heart"></i>' : '<i class="bi bi-heart-fill"></i>';
        let likesCounter = document.querySelector(`.likes-count[data-post-id="${postId}"]`);
        console.log(likesCounter);
        if (likesCounter) {
            likesCounter.innerText = `Likes: ${response.likes_count}`;
        }
    } catch (error) {
        console.error('Error toggling like:', error);
    }
}


function onLoad() {
    let buttons = document.querySelectorAll('[data-js="like-button"]');
    for (let button of buttons) {
        button.addEventListener("click", onClick);
    }
}

document.addEventListener('DOMContentLoaded', onLoad);
