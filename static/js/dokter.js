const nextButton = document.querySelector(".next");
const prevButton = document.querySelector(".prev");
const pageNumber = document.querySelector(".page");
const dokterForm = document.querySelector(".dokter-form");
const pasienForm = document.querySelector(".pasien-form");

if (pageNumber !== null) {
    pageNumber.addEventListener("change", (event) => {
        event.preventDefault();
        if (dokterForm !== null) {
            dokterForm.submit();
        } else if (pasienForm !== null) {
            pasienForm.submit();
        }
    });
}

if (nextButton !== null) {
    nextButton.addEventListener("click", () => {
        pageNumber.value++;
        if (dokterForm !== null) {
            dokterForm.submit();
        } else if (pasienForm !== null) {
            pasienForm.submit();
        }
    });
}

if (prevButton !== null) {
    prevButton.addEventListener("click", () => {
        pageNumber.value = parseInt(pageNumber.value) - 1;
        if (dokterForm !== null) {
            dokterForm.submit();
        } else if (pasienForm !== null) {
            pasienForm.submit();
        }
    });
}
