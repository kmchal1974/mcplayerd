
/*
 * McPlayerD Cassette Skin v1.0
 * Visual prototype — playback animation only
 * No backend connections
 */

"use strict";

document.addEventListener("DOMContentLoaded", () => {

    const deck = document.querySelector(".cassette-deck");
    const playButton = document.getElementById("play-btn");
    const stopButton = document.getElementById("stop-btn");

    let isPlaying = false;

    function updateCassette() {

        deck.classList.toggle("playing", isPlaying);

        playButton.textContent = isPlaying ? "⏸" : "▶";

        playButton.setAttribute(
            "aria-label",
            isPlaying ? "Pause demonstration" : "Play demonstration"
        );
    }

    playButton.addEventListener("click", () => {

        isPlaying = !isPlaying;
        updateCassette();

    });

    stopButton.addEventListener("click", () => {

        isPlaying = false;
        updateCassette();

    });

    updateCassette();

});
