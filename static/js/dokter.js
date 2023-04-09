const nextButton = document.querySelector(".next");
const prevButton = document.querySelector(".prev");
const pageNumber = document.querySelector(".page");
const dokterForm = document.querySelector(".dokter-form");
const pasienForm = document.querySelector(".pasien-form");
const rekamMedisForm = document.querySelector(".rekammedis-form");

if (pageNumber !== null) {
    pageNumber.addEventListener("change", (event) => {
        event.preventDefault();
        submitForm();
    });
}

if (nextButton !== null) {
    nextButton.addEventListener("click", () => {
        pageNumber.value++;
        submitForm();
    });
}

if (prevButton !== null) {
    prevButton.addEventListener("click", () => {
        pageNumber.value = parseInt(pageNumber.value) - 1;
        submitForm();
    });
}

function submitForm() {
    if (dokterForm !== null) {
        dokterForm.submit();
    } else if (pasienForm !== null) {
        pasienForm.submit();
    } else if (rekamMedisForm !== null) {
        rekamMedisForm.submit();
    }
}
