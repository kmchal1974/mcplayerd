/******************************************************************************
 * McPlayer Dashboard v2.0
 * app.js
 *
 * Phase 1
 * Core Framework
 ******************************************************************************/

"use strict";

//============================================================
// Dashboard State
//============================================================

const Dashboard = {

    refreshRate: 1000,

    isDraggingVolume: false,

    lastArtwork: "",

    lastPlaylistHash: "",

    lastState: "",

    lastSong: "",

    timer: null

};

//============================================================
// Utility Functions
//============================================================

function $(id) {
    return document.getElementById(id);
}

function setText(id, value) {

    const el = $(id);

    if (!el) return;

    el.textContent = value ?? "--";

}

function postPlayer(action, value = "") {

    const body = new URLSearchParams();

    body.append("action", action);

    if (value !== "")
        body.append("value", value);

    return fetch("api/player.php", {

        method: "POST",

        headers: {
            "Content-Type":
            "application/x-www-form-urlencoded"
        },

        body: body

    })

    .then(r => r.json())

    .catch(err => console.error(err));

}

//============================================================
// Dashboard Refresh
//============================================================

async function refreshDashboard() {

    try {

        const response =
            await fetch(
                "api/dashboard.php?t=" + Date.now()
            );

        const data =
            await response.json();

        updatePlayback(data);

        updateArtwork(data);

        updateProgress(data);

        updateLibrary(data);

        updateSystem(data);

        updateNetwork(data);

        updateActivity(data);

        updatePlaylist(data);

    }

    catch (err) {

        console.error(
            "Dashboard Refresh Failed",
            err
        );

    }

}

//============================================================
// Playback
//============================================================

function updatePlayback(d) {

    setText("song",
        d.song || "Nothing Playing");

    setText("artist",
        d.artist || "");

    setText("album",
        d.album || "");

    //----------------------------------------------------
    // Volume
    //----------------------------------------------------

    setText("volume",
        (d.volume ?? "--"));

    const slider =
        $("volslider");

    if (
        slider &&
        !Dashboard.isDraggingVolume
    ) {

        const vol =
            parseInt(d.volume);

        if (!isNaN(vol))
            slider.value = vol;

    }

    //----------------------------------------------------
    // Play/Pause Button
    //----------------------------------------------------

    const playBtn =
        $("playBtn");

    if (playBtn) {

        if (d.state === "playing") {

            playBtn.innerHTML = "⏸";

            playBtn.onclick =
                () => postPlayer("pause");

        }

        else {

            playBtn.innerHTML = "▶";

            playBtn.onclick =
                () => postPlayer("play");

        }

    }

    updateStateBadge(
        d.state || "stopped"
    );

    //----------------------------------------------------
    // Shuffle State
    //----------------------------------------------------

    const shuffleBtn =
        $("shuffleBtn");

    if (shuffleBtn) {

        shuffleBtn.classList.toggle(
            "active",
            d.random === true
        );

    }

    //----------------------------------------------------
    // Repeat State
    //----------------------------------------------------

    const repeatBtn =
        $("repeatBtn");

    if (repeatBtn) {

        repeatBtn.classList.toggle(
            "active",
            d.repeat === true
        );

    }
}

//============================================================
// Status Badge
//============================================================

function updateStateBadge(state) {

    const badge =
        $("state");

    if (!badge) return;

    state =
        state.toLowerCase();

    badge.innerHTML =
        `<span class="badge ${state}">
            ${state.toUpperCase()}
        </span>`;

}

//============================================================
// Progress
//============================================================

function updateProgress(d) {

    const bar =
        $("progressbar");

    if (bar) {

        bar.style.width =
            (d.percent || 0) + "%";

    }

    setText(
        "elapsed",
        (d.elapsed || "0:00") +
        " / " +
        (d.length || "0:00")
    );

}

//============================================================
// Placeholder Functions
//
// These are implemented in Parts 2–4
//============================================================

function updateArtwork(d) {}

function updatePlaylist(d) {}

function updateLibrary(d) {}

function updateSystem(d) {}

function updateNetwork(d) {}

function updateActivity(d) {}

/******************************************************************************
 * McPlayer Dashboard v2.0
 * Part 2
 * Artwork + Playlist
 ******************************************************************************/

//============================================================
// Album Artwork
//============================================================

function updateArtwork(d) {

    const img = $("albumart");

    if (!img) return;

    //--------------------------------------------------------
    // Determine artwork URL
    //--------------------------------------------------------

    let artwork =
        d.artwork ||
        d.album_art ||
        d.cover ||
        "";

    artwork = artwork.trim();

    if (artwork === "") {

        artwork = "images/default-art.jpg";

    }

    //--------------------------------------------------------
    // Prevent unnecessary reloads
    //--------------------------------------------------------

    if (Dashboard.lastArtwork === artwork)
        return;

    Dashboard.lastArtwork = artwork;

    //--------------------------------------------------------
    // Cache Busting
    //--------------------------------------------------------

    const separator =
        artwork.includes("?") ? "&" : "?";

    //--------------------------------------------------------
    // Fade Out
    //--------------------------------------------------------

    img.style.opacity = 0;

    setTimeout(() => {

        img.src =
            artwork +
            separator +
            "t=" +
            Date.now();

    }, 150);

}

//------------------------------------------------------------
// Image Loaded
//------------------------------------------------------------

window.addEventListener("DOMContentLoaded", () => {

    const img = $("albumart");

    if (!img) return;

    img.addEventListener("load", () => {

        img.style.opacity = 1;

    });

});

//============================================================
// Playlist
//============================================================

function updatePlaylist(d) {

    const div = $("playlist");

    if (!div) return;

    //--------------------------------------------------------
    // Convert Playlist
    //--------------------------------------------------------

    let playlist = [];

    if (Array.isArray(d.playlist)) {

        playlist = d.playlist;

    }

    else {

        playlist =
            (d.playlist || "")
            .split("\n");

    }

    playlist =
        playlist.filter(
            x => x &&
            x.trim() !== ""
        );

    //--------------------------------------------------------
    // Detect Changes
    //--------------------------------------------------------

    const hash =
        playlist.join("|");

    if (
        hash === Dashboard.lastPlaylistHash &&
        Dashboard.lastSong === d.song
    ) {

        return;

    }

    Dashboard.lastPlaylistHash =
        hash;

    Dashboard.lastSong =
        d.song || "";

    //--------------------------------------------------------
    // Empty Playlist
    //--------------------------------------------------------

    if (playlist.length === 0) {

        div.innerHTML =
            "<div class='small'>Playlist Empty</div>";

        return;

    }

    //--------------------------------------------------------
    // Render
    //--------------------------------------------------------

    let html = "";

    playlist.forEach((track, index) => {

        const playing =

            index ===
            d.current_track_index ||

            (
                d.song &&
                track
                    .toLowerCase()
                    .includes(
                        d.song.toLowerCase()
                    )
            );

        html +=

        `<div class="${
            playing
            ? "playingTrack"
            : "track"
        }"

        data-track="${
            index + 1
        }">

            <span class="number">
                ${index + 1}
            </span>

            <span class="trackTitle">
                ${track}
            </span>

        </div>`;

    });

    div.innerHTML = html;

    //--------------------------------------------------------
    // Click-to-Play
    //--------------------------------------------------------

    div.querySelectorAll("[data-track]")

        .forEach(track => {

            track.onclick = () => {

                postPlayer(

                    "playindex",

                    track.dataset.track

                );

            };

        });

    //--------------------------------------------------------
    // Scroll Current Track Into View
    //--------------------------------------------------------

    const current =

        div.querySelector(
            ".playingTrack"
        );

    if (current) {

        current.scrollIntoView({

            behavior: "smooth",

            block: "center"

        });

    }

}

//============================================================
// Playlist Helpers
//============================================================

function clearPlaylistHighlight() {

    document

        .querySelectorAll(".playingTrack")

        .forEach(track => {

            track.classList.remove(

                "playingTrack"

            );

            track.classList.add(

                "track"

            );

        });

}

function highlightCurrentTrack(index) {

    const row =

        document.querySelector(

            `[data-track="${
                index + 1
            }"]`

        );

    if (!row) return;

    row.classList.remove("track");

    row.classList.add("playingTrack");

}

//============================================================
// Artwork Animation
//============================================================

function pulseArtwork() {

    const img = $("albumart");

    if (!img) return;

    img.classList.add("pulse");

    setTimeout(() => {

        img.classList.remove("pulse");

    }, 350);

}

/******************************************************************************
 * McPlayer Dashboard v2.0
 * Part 3
 * Library • System • Network • Activity • Volume • Seek
 ******************************************************************************/

//============================================================
// Library
//============================================================

function updateLibrary(d) {

    setText("songs", d.songs);
    setText("albums", d.albums);
    setText("artists", d.artists);
    setText("lastscan", d.lastscan || "--");

    //--------------------------------------------------------

    const status =
        $("library-status") ||
        $("scanmessage");

    if (status) {

        status.textContent =
            d.updating
                ? "Updating Library..."
                : "Idle";

    }

    //--------------------------------------------------------

    const bar =
        $("scanbar");

    if (bar) {

        bar.style.width =
            d.updating
                ? "100%"
                : "0%";

    }

}

//============================================================
// System
//============================================================

function updateSystem(d) {

    setText("cpu", d.cpu);
    setText("memory", d.memory);
    setText("disk", d.disk);

    setText("musicdisk", d.musicdisk);

    setText("hostname", d.hostname);

    setText("kernel", d.kernel);

    setText("load", d.load);

    setText("uptime", d.uptime);

}

//============================================================
// Network
//============================================================

function updateNetwork(d) {

    setText("ip", d.lan);

    setText("tailscale", d.tailscale);

    setText("ssid", d.ssid);

    setText("signal", d.signal);

    setText("internet", d.internet);

    //--------------------------------------------------------

    const stream =
        $("stream");

    if (stream) {

        if (d.stream) {

            stream.innerHTML =

                `<a href="${d.stream}"
                    target="_blank">

                    ${d.stream}

                </a>`;

        }

        else {

            stream.textContent =
                "--";

        }

    }

}

//============================================================
// Activity
//============================================================

function updateActivity(d) {

    const activity =
        $("activity");

    if (!activity)
        return;

    activity.innerHTML =
        d.activity ||
        "Ready";

}

//============================================================
// Volume Slider
//============================================================

function initializeVolumeSlider() {

    const slider =
        $("volslider");

    if (!slider)
        return;

    //--------------------------------------------------------

    slider.addEventListener(

        "pointerdown",

        () => {

            Dashboard.isDraggingVolume =
                true;

        }

    );

    //--------------------------------------------------------

    slider.addEventListener(

        "pointerup",

        () => {

            Dashboard.isDraggingVolume =
                false;

            postPlayer(

                "volume",

                slider.value

            );

        }

    );

    //--------------------------------------------------------

    slider.addEventListener(

        "change",

        () => {

            postPlayer(

                "volume",

                slider.value

            );

        }

    );

    //--------------------------------------------------------

    slider.addEventListener(

        "input",

        () => {

            setText(

                "volume",

                slider.value + "%"

            );

        }

    );

}

//============================================================
// Click-to-Seek
//============================================================

function initializeSeekBar() {

    const progress =
        document.querySelector(".progress");

    if (!progress)
        return;

    progress.addEventListener(

        "click",

        event => {

            //------------------------------------------------

            const elapsed =
                $("elapsed")
                .textContent
                .split("/");

            if (elapsed.length !== 2)
                return;

            //------------------------------------------------

            const length =

                elapsed[1]
                .trim()
                .split(":");

            if (length.length !== 2)
                return;

            //------------------------------------------------

            const totalSeconds =

                parseInt(length[0]) *
                60 +

                parseInt(length[1]);

            //------------------------------------------------

            const rect =
                progress
                .getBoundingClientRect();

            const percent =

                (event.clientX -
                    rect.left)

                / rect.width;

            //------------------------------------------------

            const seek =

                Math.floor(

                    totalSeconds *

                    percent

                );

            postPlayer(

                "seek",

                seek

            );

        }

    );

}

//============================================================
// Stream Copy
//============================================================

function copyStream() {

    const stream =
        $("stream");

    if (!stream)
        return;

    navigator.clipboard

        .writeText(

            stream.textContent

        )

        .then(() => {

            showToast(

                "Stream URL Copied"

            );

        });

}

//============================================================
// Toast
//============================================================

function showToast(message) {

    let toast =
        $("toast");

    if (!toast) {

        toast =
            document.createElement(
                "div"
            );

        toast.id = "toast";

        toast.style.position =
            "fixed";

        toast.style.bottom =
            "25px";

        toast.style.right =
            "25px";

        toast.style.padding =
            "12px 18px";

        toast.style.background =
            "#222";

        toast.style.color =
            "white";

        toast.style.borderRadius =
            "10px";

        toast.style.opacity =
            0;

        toast.style.transition =
            "opacity .3s";

        document.body
            .appendChild(toast);

    }

    toast.textContent =
        message;

    toast.style.opacity = 1;

    clearTimeout(
        Dashboard.toastTimer
    );

    Dashboard.toastTimer =

        setTimeout(() => {

            toast.style.opacity =
                0;

        }, 1800);

}

/******************************************************************************
 * McPlayer Dashboard v2.0
 * Part 4
 * Initialization & Event Wiring
 ******************************************************************************/

//============================================================
// Playback Controls
//============================================================

function initializeControls() {

    //--------------------------------------------------------
    // Previous
    //--------------------------------------------------------

    const prev = $("prevBtn");

    if (prev)
        prev.onclick = () => postPlayer("previous");

    //--------------------------------------------------------
    // Next
    //--------------------------------------------------------

    const next = $("nextBtn");

    if (next)
        next.onclick = () => postPlayer("next");

    //--------------------------------------------------------
    // Stop
    //--------------------------------------------------------

    const stop = $("stopBtn");

    if (stop)
        stop.onclick = () => postPlayer("stop");

    //--------------------------------------------------------
    // Shuffle
    //--------------------------------------------------------

    const shuffle = $("shuffleBtn");

    if (shuffle) {

        shuffle.onclick = () => {

            postPlayer("shuffle");

            shuffle.classList.toggle("active");

            showToast("Shuffle");

        };

    }

    //--------------------------------------------------------
    // Repeat
    //--------------------------------------------------------

    const repeat = $("repeatBtn");

    if (repeat) {

        repeat.onclick = () => {

            postPlayer("repeat");

            repeat.classList.toggle("active");

            showToast("Repeat");

        };

    }

}

//============================================================
// Keyboard Shortcuts
//============================================================

function initializeKeyboard() {

    document.addEventListener("keydown", e => {

        // Ignore typing in form controls
        if (
            e.target.tagName === "INPUT" ||
            e.target.tagName === "TEXTAREA"
        ) {
            return;
        }

        switch (e.code) {

            case "Space":

                e.preventDefault();

                const playBtn = $("playBtn");

                if (playBtn)
                    playBtn.click();

                break;

            case "ArrowRight":

                postPlayer("next");

                break;

            case "ArrowLeft":

                postPlayer("previous");

                break;

        }

    });

}

//============================================================
// Refresh Timer
//============================================================

function startDashboard() {

    refreshDashboard();

    if (Dashboard.timer)
        clearInterval(Dashboard.timer);

    Dashboard.timer =

        setInterval(

            refreshDashboard,

            Dashboard.refreshRate

        );

}

//============================================================
// Startup
//============================================================

document.addEventListener(

    "DOMContentLoaded",

    () => {

        initializeControls();

        initializeVolumeSlider();

        initializeSeekBar();

        initializeKeyboard();

        startDashboard();

    }

);
