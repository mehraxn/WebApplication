"use strict";

(function () {
    const reducedMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const revealSelector = [
        ".tour-card",
        ".stat-card",
        ".form-section",
        ".dashboard-panel",
        ".admin-guide-block",
        ".detail-section-card",
        ".detail-gallery-card",
        ".simple-calendar",
        ".booking-summary",
        ".booking-form"
    ].join(", ");

    let revealObserver = null;

    function setupNavbarScrollState() {
        const navbar = document.querySelector(".custom-navbar");
        if (!navbar) return;

        let frameRequested = false;

        function updateNavbar() {
            navbar.classList.toggle("navbar-scrolled", window.scrollY > 18);
            frameRequested = false;
        }

        function requestNavbarUpdate() {
            if (frameRequested) return;
            frameRequested = true;
            window.requestAnimationFrame(updateNavbar);
        }

        updateNavbar();
        window.addEventListener("scroll", requestNavbarUpdate, { passive: true });
    }

    function revealAll(elements) {
        elements.forEach(function (element) {
            element.classList.remove("reveal-item");
            element.classList.add("is-visible");
        });
    }

    function setupRevealAnimations() {
        const elements = Array.from(document.querySelectorAll(revealSelector));
        if (!elements.length) return;

        if (reducedMotionQuery.matches || !("IntersectionObserver" in window)) {
            revealAll(elements);
            return;
        }

        elements.forEach(function (element) {
            element.classList.add("reveal-item");
        });

        revealObserver = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;

                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            });
        }, {
            threshold: 0.1,
            rootMargin: "0px 0px -32px"
        });

        elements.forEach(function (element) {
            revealObserver.observe(element);
        });
    }

    function setupHeroCarouselMotion() {
        const carousel = document.getElementById("heroCarousel");
        if (!carousel) return;

        function applyMotionPreference() {
            if (!reducedMotionQuery.matches) return;

            carousel.removeAttribute("data-bs-ride");

            if (window.bootstrap && window.bootstrap.Carousel) {
                const instance = window.bootstrap.Carousel.getInstance(carousel);
                if (instance) instance.pause();
            }
        }

        applyMotionPreference();
        reducedMotionQuery.addEventListener("change", applyMotionPreference);
    }

    function handleMotionPreferenceChange(event) {
        if (!event.matches) return;

        if (revealObserver) {
            revealObserver.disconnect();
            revealObserver = null;
        }

        revealAll(Array.from(document.querySelectorAll(revealSelector)));
    }

    function initializeInterface() {
        document.documentElement.classList.add("js-enabled");
        setupNavbarScrollState();
        setupRevealAnimations();
        setupHeroCarouselMotion();
        reducedMotionQuery.addEventListener("change", handleMotionPreferenceChange);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initializeInterface, { once: true });
    } else {
        initializeInterface();
    }
}());
