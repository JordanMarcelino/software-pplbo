const hamburger = document.querySelector(".hamburger");
const mobileNav = document.querySelector(".mobile-nav");
hamburger.addEventListener("click", () => {
    mobileNav.classList.toggle("-translate-x-full");
    mobileNav.classList.toggle("opacity-100");
    hamburger.classList.toggle("hamburger-toggle");
});
