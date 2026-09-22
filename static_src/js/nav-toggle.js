/**
 * Classic collapsible hamburger menu for the header nav.
 * Self-wiring: no-ops if the page has no [data-nav-toggle], so it's safe
 * to include on every page via base.html.
 */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        var toggle = document.querySelector("[data-nav-toggle]");
        var nav = document.querySelector("[data-nav]");
        if (!toggle || !nav) {
            return;
        }

        toggle.addEventListener("click", function () {
            var isOpen = nav.classList.toggle("is-open");
            toggle.classList.toggle("is-open", isOpen);
            toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
        });

        // Tapping a link closes the menu instead of leaving it open
        // underneath the page you just navigated to.
        nav.addEventListener("click", function (event) {
            if (event.target.tagName === "A") {
                closeNav();
            }
        });

        // Rotating back to a desktop-sized viewport shouldn't leave the
        // menu stuck open (or stuck closed via display:none) if it was
        // toggled at a narrow width.
        window.addEventListener("resize", function () {
            if (window.innerWidth > 720) {
                closeNav();
            }
        });

        function closeNav() {
            nav.classList.remove("is-open");
            toggle.classList.remove("is-open");
            toggle.setAttribute("aria-expanded", "false");
        }
    });
})();
