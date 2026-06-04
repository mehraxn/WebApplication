document.addEventListener("DOMContentLoaded", function () {
    const selectedDateInput = document.getElementById("selectedDate");
        const selectedTimeInput = document.getElementById("selectedTime");
        const selectedSlotPreview = document.getElementById("selectedSlotPreview");
        const availableDateCards = document.querySelectorAll(".available-reservation-day");
        const reservationMonthMenu = document.getElementById("reservationMonthMenu");
        const reservationMonthTrigger = document.getElementById("reservationMonthTrigger");
        const reservationMonthTriggerText = document.getElementById("reservationMonthTriggerText");
        const reservationMonthOptions = document.querySelectorAll(".reservation-month-option");
        const reservationCalendarCards = document.querySelectorAll(".reservation-calendar-card");
        const reservationForm = document.getElementById("reservationForm");
        const extraPeopleSelect = document.getElementById("extraPeople");
        const extraPeopleNameList = document.getElementById("extraPeopleNameList");
        const openLoginRequiredModal = document.getElementById("openLoginRequiredModal");
        const loginRequiredModal = document.getElementById("loginRequiredModal");
        const closeLoginRequiredModal = document.getElementById("closeLoginRequiredModal");

        function updateVisibleCalendars(startKey, endKey) {

            reservationCalendarCards.forEach(function (calendarCard) {
                const calendarKey = calendarCard.dataset.calendarKey;
                const shouldShow = calendarKey === startKey || calendarKey === endKey;
                calendarCard.classList.toggle("active-reservation-calendar-card", shouldShow);
            });
        }

        reservationMonthTrigger.addEventListener("click", function () {
            const menuIsOpen = reservationMonthMenu.classList.toggle("open-reservation-month-menu");
            reservationMonthTrigger.setAttribute("aria-expanded", menuIsOpen ? "true" : "false");
        });

        reservationMonthOptions.forEach(function (button) {
            if (button.classList.contains("selected-reservation-month-option")) {
                updateVisibleCalendars(button.dataset.start, button.dataset.end);
            }

            button.addEventListener("click", function () {
                reservationMonthOptions.forEach(function (otherButton) {
                    otherButton.classList.remove("selected-reservation-month-option");
                });

                button.classList.add("selected-reservation-month-option");
                reservationMonthTriggerText.textContent = button.dataset.label;
                reservationMonthMenu.classList.remove("open-reservation-month-menu");
                reservationMonthTrigger.setAttribute("aria-expanded", "false");
                updateVisibleCalendars(button.dataset.start, button.dataset.end);
            });
        });

        document.addEventListener("click", function (event) {
            if (!reservationMonthMenu.contains(event.target)) {
                reservationMonthMenu.classList.remove("open-reservation-month-menu");
                reservationMonthTrigger.setAttribute("aria-expanded", "false");
            }
        });

        availableDateCards.forEach(function (button) {
            button.addEventListener("click", function () {
                availableDateCards.forEach(function (otherButton) {
                    otherButton.classList.remove("selected-reservation-day");
                });

                button.classList.add("selected-reservation-day");

                const selectedDate = button.dataset.date;
                const selectedTime = button.dataset.time;

                selectedDateInput.value = selectedDate;
                selectedTimeInput.value = selectedTime;

                selectedSlotPreview.textContent = "Selected: " + selectedDate + " at " + selectedTime;
            });
        });

        reservationForm.addEventListener("submit", function (event) {
            if (!selectedDateInput.value || !selectedTimeInput.value) {
                event.preventDefault();
                selectedSlotPreview.textContent = "Please select one available date before confirming.";
            }
        });

        if (openLoginRequiredModal && loginRequiredModal) {
            openLoginRequiredModal.addEventListener("click", function () {
                loginRequiredModal.classList.add("show-login-required-modal");
                loginRequiredModal.setAttribute("aria-hidden", "false");
            });
        }

        if (closeLoginRequiredModal && loginRequiredModal) {
            closeLoginRequiredModal.addEventListener("click", function () {
                loginRequiredModal.classList.remove("show-login-required-modal");
                loginRequiredModal.setAttribute("aria-hidden", "true");
            });
        }

        if (loginRequiredModal) {
            loginRequiredModal.addEventListener("click", function (event) {
                if (event.target.classList.contains("login-required-modal-backdrop")) {
                    loginRequiredModal.classList.remove("show-login-required-modal");
                    loginRequiredModal.setAttribute("aria-hidden", "true");
                }
            });
        }

        function renderExtraPeopleFields() {
            const count = Number(extraPeopleSelect.value || 0);
            extraPeopleNameList.innerHTML = "";

            for (let index = 1; index <= count; index += 1) {
                const fieldWrapper = document.createElement("div");
                fieldWrapper.className = "extra-person-field";

                const label = document.createElement("label");
                label.className = "form-label";
                label.setAttribute("for", "extraPerson" + index);
                label.textContent = "Extra participant " + index + " full name";

                const input = document.createElement("input");
                input.type = "text";
                input.id = "extraPerson" + index;
                input.name = "extra_person_" + index;
                input.className = "form-control";
                input.required = true;
                input.placeholder = "Full name";

                fieldWrapper.appendChild(label);
                fieldWrapper.appendChild(input);
                extraPeopleNameList.appendChild(fieldWrapper);
            }
        }

        extraPeopleSelect.addEventListener("change", renderExtraPeopleFields);
        renderExtraPeopleFields();
});
