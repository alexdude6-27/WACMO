/* WACMO responsive photo viewer: no external dependencies. */
(() => {
    "use strict";

    const dialog = document.getElementById(
        "wacmo-photo-lightbox"
    );

    if (!dialog || typeof dialog.showModal !== "function") {
        return;
    }

    const links = Array.from(
        document.querySelectorAll(".photo-lightbox-trigger")
    );

    if (links.length === 0) {
        return;
    }

    const image = dialog.querySelector("[data-photo-image]");
    const caption = dialog.querySelector("[data-photo-caption]");
    const closeButton = dialog.querySelector("[data-photo-close]");
    const previousButton = dialog.querySelector(
        "[data-photo-previous]"
    );
    const nextButton = dialog.querySelector("[data-photo-next]");

    if (
        !image || !caption || !closeButton ||
        !previousButton || !nextButton
    ) {
        return;
    }

    let group = [];
    let current = 0;
    let opener = null;
    let touchStart = null;

    function showPhoto(index) {
        if (group.length === 0) {
            return;
        }

        current = (index + group.length) % group.length;

        const link = group[current];
        const thumbnail = link.querySelector("img");

        image.src = link.href;
        image.alt = thumbnail
            ? thumbnail.alt
            : "WACMO photograph";

        const label = link.dataset.lightboxCaption ||
            "WACMO photograph";

        caption.textContent =
            `${label} (${current + 1} of ${group.length})`;

        previousButton.hidden = group.length < 2;
        nextButton.hidden = group.length < 2;
    }

    links.forEach((link) => {
        link.addEventListener("click", (event) => {
            if (
                event.defaultPrevented ||
                event.button !== 0 ||
                event.ctrlKey ||
                event.metaKey ||
                event.shiftKey ||
                event.altKey
            ) {
                return;
            }

            event.preventDefault();

            opener = link;

            const selectedGroup =
                link.dataset.lightboxGroup || "";

            group = links.filter(
                (item) =>
                    (item.dataset.lightboxGroup || "") ===
                    selectedGroup
            );

            current = group.indexOf(link);
            showPhoto(current);
            dialog.showModal();
        });
    });

    closeButton.addEventListener("click", () => {
        dialog.close();
    });

    previousButton.addEventListener("click", () => {
        showPhoto(current - 1);
    });

    nextButton.addEventListener("click", () => {
        showPhoto(current + 1);
    });

    dialog.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft") {
            event.preventDefault();
            showPhoto(current - 1);
        } else if (event.key === "ArrowRight") {
            event.preventDefault();
            showPhoto(current + 1);
        }
        // Escape is handled by the native dialog.
    });

    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) {
            dialog.close();
        }
    });

    dialog.addEventListener("touchstart", (event) => {
        if (event.touches.length !== 1) {
            touchStart = null;
            return;
        }

        touchStart = {
            x: event.touches[0].clientX,
            y: event.touches[0].clientY
        };
    }, { passive: true });

    dialog.addEventListener("touchend", (event) => {
        if (
            !touchStart ||
            event.changedTouches.length !== 1
        ) {
            touchStart = null;
            return;
        }

        const dx =
            event.changedTouches[0].clientX - touchStart.x;

        const dy =
            event.changedTouches[0].clientY - touchStart.y;

        touchStart = null;

        if (
            group.length > 1 &&
            Math.abs(dx) >= 45 &&
            Math.abs(dx) > Math.abs(dy) * 1.3
        ) {
            showPhoto(current + (dx < 0 ? 1 : -1));
        }
    }, { passive: true });

    dialog.addEventListener("close", () => {
        image.removeAttribute("src");
        group = [];

        if (opener && opener.isConnected) {
            opener.focus({ preventScroll: true });
        }

        opener = null;
    });
})();
