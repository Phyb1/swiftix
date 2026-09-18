/**
 * Minimal, dependency-free carousel.
 * Auto-wires every [data-carousel] on the page, so it works if you
 * add a second carousel elsewhere without touching this file.
 */
(function () {
    "use strict";

    var AUTOPLAY_MS = 5000;
    var prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    function initCarousel(root) {
        var track = root.querySelector("[data-carousel-track]");
        var slides = Array.prototype.slice.call(track.children);
        var prevBtn = root.querySelector("[data-carousel-prev]");
        var nextBtn = root.querySelector("[data-carousel-next]");
        var dotsWrap = root.querySelector("[data-carousel-dots]");
        var count = slides.length;
        var index = 0;
        var timer = null;

        if (count <= 1) {
            if (prevBtn) prevBtn.hidden = true;
            if (nextBtn) nextBtn.hidden = true;
            return;
        }

        // Lay the track out as one wide flex row: count * 100% wide,
        // each slide 100/count % — then we just translateX by index.
        track.style.width = count * 100 + "%";
        slides.forEach(function (slide) {
            slide.style.width = 100 / count + "%";
        });

        var dots = slides.map(function (_, i) {
            var dot = document.createElement("button");
            dot.type = "button";
            dot.className = "carousel-dot";
            dot.setAttribute("aria-label", "Go to slide " + (i + 1));
            dot.addEventListener("click", function () {
                goTo(i);
                restartAutoplay();
            });
            dotsWrap.appendChild(dot);
            return dot;
        });

        function render() {
            track.style.transform = "translateX(-" + (index * (100 / count)) + "%)";
            dots.forEach(function (dot, i) {
                dot.classList.toggle("active", i === index);
            });
        }

        function goTo(i) {
            index = (i + count) % count;
            render();
        }

        function next() {
            goTo(index + 1);
        }

        function prev() {
            goTo(index - 1);
        }

        function startAutoplay() {
            if (prefersReducedMotion) return;
            timer = window.setInterval(next, AUTOPLAY_MS);
        }

        function stopAutoplay() {
            if (timer) window.clearInterval(timer);
        }

        function restartAutoplay() {
            stopAutoplay();
            startAutoplay();
        }

        if (nextBtn) {
            nextBtn.addEventListener("click", function () {
                next();
                restartAutoplay();
            });
        }
        if (prevBtn) {
            prevBtn.addEventListener("click", function () {
                prev();
                restartAutoplay();
            });
        }

        root.addEventListener("keydown", function (e) {
            if (e.key === "ArrowRight") { next(); restartAutoplay(); }
            if (e.key === "ArrowLeft") { prev(); restartAutoplay(); }
        });

        root.addEventListener("mouseenter", stopAutoplay);
        root.addEventListener("mouseleave", startAutoplay);
        root.addEventListener("focusin", stopAutoplay);
        root.addEventListener("focusout", startAutoplay);

        // Basic touch swipe support.
        var touchStartX = null;
        root.addEventListener("touchstart", function (e) {
            touchStartX = e.changedTouches[0].clientX;
            stopAutoplay();
        }, { passive: true });
        root.addEventListener("touchend", function (e) {
            if (touchStartX === null) return;
            var delta = e.changedTouches[0].clientX - touchStartX;
            if (delta > 40) prev();
            else if (delta < -40) next();
            touchStartX = null;
            startAutoplay();
        });

        render();
        startAutoplay();
    }

    document.addEventListener("DOMContentLoaded", function () {
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-carousel]"),
            initCarousel
        );
    });
})();

