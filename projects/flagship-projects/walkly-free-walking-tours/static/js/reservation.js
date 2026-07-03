"use strict";

let modalTrigger = null;

function getFocusableElements(loginModal) {
    return Array.from(loginModal.querySelectorAll(
        "a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex='-1'])"
    ));
}

function showLoginRequiredModal(loginModal, trigger) {
    modalTrigger = trigger || document.activeElement;
    loginModal.classList.add("show-login-required-modal");
    loginModal.setAttribute("aria-hidden", "false");
    document.body.classList.add("reservation-modal-open");

    window.requestAnimationFrame(function () {
        const closeButton = loginModal.querySelector("#closeLoginRequiredModal");
        if (closeButton) closeButton.focus();
    });
}

function hideLoginRequiredModal(loginModal) {
    loginModal.classList.remove("show-login-required-modal");
    loginModal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("reservation-modal-open");

    if (modalTrigger) {
        modalTrigger.focus();
        modalTrigger = null;
    }
}

function keepFocusInsideModal(event, loginModal) {
    if (event.key !== "Tab") return;

    const focusableElements = getFocusableElements(loginModal);
    if (!focusableElements.length) return;

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    if (event.shiftKey && document.activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
    } else if (!event.shiftKey && document.activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
    }
}

function setupLoginRequiredModal() {
    const openModalButton = document.querySelector("#openLoginRequiredModal");
    const closeModalButton = document.querySelector("#closeLoginRequiredModal");
    const loginModal = document.querySelector("#loginRequiredModal");

    if (!loginModal) {
        return;
    }

    if (openModalButton) {
        openModalButton.addEventListener("click", function () {
            showLoginRequiredModal(loginModal, openModalButton);
        });
    }

    if (closeModalButton) {
        closeModalButton.addEventListener("click", function () {
            hideLoginRequiredModal(loginModal);
        });
    }

    loginModal.addEventListener("click", function (event) {
        if (event.target.classList.contains("login-required-modal-backdrop")) {
            hideLoginRequiredModal(loginModal);
        }
    });

    document.addEventListener("keydown", function (event) {
        if (loginModal.getAttribute("aria-hidden") === "true") return;

        if (event.key === "Escape") {
            event.preventDefault();
            hideLoginRequiredModal(loginModal);
            return;
        }

        keepFocusInsideModal(event, loginModal);
    }, true);
}

document.addEventListener("DOMContentLoaded", function () {
    setupLoginRequiredModal();
});
