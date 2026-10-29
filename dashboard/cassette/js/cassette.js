
/*
 * McPlayerD Cassette Skin v1.0
 * Playback integration
 */

"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const deck = document.querySelector(".cassette-deck");
    const playButton = document.getElementById("play-btn");
    const stopButton = document.getElementById("stop-btn");
    const previousButton = document.getElementById("prev-btn");
    const nextButton = document.getElementById("next-btn");

    const songTitle = document.getElementById("song-title");
    const artistName = document.getElementById("artist-name");
    const albumName = document.getElementById("album-name");
    const albumArt = document.getElementById("album-art");

    const previewMode = window.location.pathname.endsWith("preview.html");

    const fallbackArt = "assets/default-cover.png";
    const apiBase = "../admin/api/";

    let isPlaying = false;
    let lastArtwork = "";

    function updatePlaybackDisplay() {
        deck.classList.toggle("playing", isPlaying);
        playButton.textContent = isPlaying ? "⏸" : "▶";
        playButton.setAttribute(
            "aria-label",
            isPlaying ? "Pause" : "Play"
        );
    }

    async function refreshStatus() {
        if (previewMode) return;

        try {
            const response = await fetch(
                apiBase + "dashboard.php?t=" + Date.now(),
                { cache: "no-store" }
            );

            if (!response.ok) {
                throw new Error("Status HTTP " + response.status);
            }

            const data = await response.json();

            isPlaying = data.state === "playing";
            updatePlaybackDisplay();

            songTitle.textContent = data.song || "Nothing Playing";
            artistName.textContent = data.artist || "";
            albumName.textContent = data.album || "";

            const artwork = data.artwork || fallbackArt;

            if (artwork !== lastArtwork) {
                lastArtwork = artwork;
                albumArt.src = artwork;
            }
        } catch (error) {
            console.error("Cassette status refresh failed:", error);
        }
    }

    async function sendCommand(action) {
        if (previewMode) {
            if (action === "toggle") {
                isPlaying = !isPlaying;
            } else if (action === "stop") {
                isPlaying = false;
            }

            updatePlaybackDisplay();
            return;
        }

        try {
            const body = new URLSearchParams();
            body.append("action", action);

            const response = await fetch(apiBase + "player.php", {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },
                body
            });

            const data = await response.json();

            if (!response.ok || data.success === false) {
                throw new Error(
                    data.error || "Playback command failed"
                );
            }

            await refreshStatus();
        } catch (error) {
            console.error("Cassette playback error:", error);
        }
    }

    albumArt.addEventListener("error", () => {
        if (!albumArt.src.endsWith("/" + fallbackArt)) {
            albumArt.src = fallbackArt;
        }
    });

    playButton.addEventListener("click", () => {
        sendCommand("toggle");
    });

    stopButton.addEventListener("click", () => {
        sendCommand("stop");
    });

    previousButton.addEventListener("click", () => {
        sendCommand("previous");
    });

    nextButton.addEventListener("click", () => {
        sendCommand("next");
    });

    updatePlaybackDisplay();

    if (!previewMode) {
        refreshStatus();
        setInterval(refreshStatus, 1000);
    }
});
