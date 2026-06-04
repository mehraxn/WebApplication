document.addEventListener("DOMContentLoaded", function () {
    const completedTourDate = document.getElementById("completedTourDate");
        const completedTourId = document.getElementById("completedTourId");

        if (completedTourDate && completedTourId) {
            completedTourDate.addEventListener("change", function () {
                const selectedOption = completedTourDate.options[completedTourDate.selectedIndex];
                completedTourId.value = selectedOption.dataset.tourId || "";
            });
        }
});
