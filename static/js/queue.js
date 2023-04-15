const cards = document.querySelectorAll(".card");
const selectedCardInput = document.querySelector("#selected-dokter");

cards.forEach(function (card) {
    card.addEventListener("click", function () {
        if (this.classList.contains("selected")) {
            this.classList.remove("selected");
            selectedCardInput.value = "";
        } else {
            cards.forEach(function (c) {
                c.classList.remove("selected");
            });
            this.classList.add("selected");
            selectedCardInput.value = this.getAttribute("data-value");
        }
    });
});
