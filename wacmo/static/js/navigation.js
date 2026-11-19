"use strict";

document.documentElement.classList.add("has-js");

document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".menu-toggle");
    const navigation = document.getElementById("site-navigation");

    if (!button || !navigation) return;

    button.hidden = false;

    const close = () => {
        button.setAttribute("aria-expanded", "false");
        navigation.classList.remove("is-open");
    };

    button.addEventListener("click", () => {
        const opening =
            button.getAttribute("aria-expanded") !== "true";

        button.setAttribute(
            "aria-expanded", String(opening)
        );

        navigation.classList.toggle("is-open", opening);
    });

    navigation.addEventListener("click", (event) => {
        if (event.target.closest("a")) close();
    });

    document.addEventListener("keydown", (event) => {
        if (
            event.key === "Escape"
            && button.getAttribute("aria-expanded") === "true"
        ) {
            close();
            button.focus();
        }
    });
});
