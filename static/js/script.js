const hamburger = document.querySelector(".hamburger");
const mobileNav = document.querySelector(".mobile-nav");
const pfp = document.querySelector(".pfp");
const pfpList = document.querySelector(".pfp-list");

if (hamburger !== null) {
    hamburger.addEventListener("click", () => {
        mobileNav.classList.toggle("-translate-x-full");
        mobileNav.classList.toggle("opacity-100");
        hamburger.classList.toggle("hamburger-toggle");
    });
}

if (pfp !== null) {
    pfp.addEventListener("click", () => {
        pfpList.classList.toggle("opacity-0");
        pfpList.classList.toggle("translate-x-full");
    });
}
