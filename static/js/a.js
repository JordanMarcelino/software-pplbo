const button_1 = document.getElementById("doc1");
const button_2 = document.getElementById("doc2");
const button_3 = document.getElementById("doc3");
const button_4 = document.getElementById("doc4");

const modalContainer = document.getElementById("modal-container");

const modals = [
  document.getElementById("modal1"),
  document.getElementById("modal2"),
  document.getElementById("modal3"),
  document.getElementById("modal4"),
];

const closeButtons = document.getElementById("close-modal-button");
closeButtons.addEventListener("click", () => {
    modalContainer.classList.add("hidden");
});

button_1.addEventListener("click", () => {
    console.log("test")
    modalContainer.classList.remove("hidden");
    modals[0].classList.remove("hidden");
    modals[1].classList.add("hidden");
    modals[2].classList.add("hidden");
    modals[3].classList.add("hidden");
});

button_2.addEventListener("click", () => {
    modalContainer.classList.remove("hidden");
    modals[0].classList.add("hidden");
    modals[1].classList.remove("hidden");
    modals[2].classList.add("hidden");
    modals[3].classList.add("hidden");
});

button_3.addEventListener("click", () => {
    modalContainer.classList.remove("hidden");
    modals[0].classList.add("hidden");
    modals[1].classList.add("hidden");
    modals[2].classList.remove("hidden");
    modals[3].classList.add("hidden");
});

button_4.addEventListener("click", () => {
    modalContainer.classList.remove("hidden");
    modals[0].classList.add("hidden");
    modals[1].classList.add("hidden");
    modals[2].classList.add("hidden");
    modals[3].classList.remove("hidden");
});
