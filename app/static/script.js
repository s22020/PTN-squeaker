let posts = document.querySelectorAll(".post-content");

posts.forEach(post => post.addEventListener("click", (event) => {
    let link = event.target.querySelector(".permalink");
    window.location.href = link.href;
}));