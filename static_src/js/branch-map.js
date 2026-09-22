/**
 * Renders pins (from the locations app's branch_map_widget template tag)
 * onto a Leaflet/OpenStreetMap map. Self-wiring: no-ops if the page has
 * no #branch-map element, so it's safe to load on any page.
 */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        var mapEl = document.getElementById("branch-map");
        var dataEl = document.getElementById("branch-map-pins");
        if (!mapEl || !dataEl || typeof L === "undefined") {
            return;
        }

        var pins = JSON.parse(dataEl.textContent);
        if (!pins.length) {
            return;
        }

        var map = L.map(mapEl, { scrollWheelZoom: false });
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution: "&copy; OpenStreetMap contributors",
        }).addTo(map);

        var markers = pins.map(function (pin) {
            var marker = L.marker([pin.lat, pin.lng]).addTo(map);
            marker.bindPopup(
                "<strong>" + escapeHtml(pin.name) + "</strong><br>" +
                escapeHtml(pin.address) + "<br>" +
                '<a href="' + pin.directions_url + '" target="_blank" rel="noopener">Get directions</a>'
            );
            return marker;
        });

        if (markers.length === 1) {
            map.setView(markers[0].getLatLng(), 15);
        } else {
            map.fitBounds(L.featureGroup(markers).getBounds().pad(0.3));
        }

        // Scroll-zoom is off by default so the map doesn't hijack page
        // scrolling; a tap/click inside it opts back in.
        mapEl.addEventListener("click", function () {
            map.scrollWheelZoom.enable();
        }, { once: true });

        function escapeHtml(str) {
            var div = document.createElement("div");
            div.textContent = str;
            return div.innerHTML;
        }
    });
})();
