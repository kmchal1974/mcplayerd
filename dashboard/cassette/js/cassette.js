
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

// ============================================================
// Music Library — Artist Browser
// ============================================================

const artistsTab = document.getElementById("artists-tab");
const foldersTab = document.getElementById("folders-tab");
const musicBrowser = document.getElementById("music-browser");
const albumsTab = document.getElementById("albums-tab");

async function loadArtists() {
    if (!musicBrowser) return;

    musicBrowser.textContent = "Loading artists...";

    try {
        const body = new URLSearchParams();
        body.append("action", "list_artists");

        const response = await fetch(apiBase + "player.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body
        });

        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }

        const data = await response.json();

        if (!data.success || !Array.isArray(data.artists)) {
            throw new Error("Invalid artist list response");
        }

        musicBrowser.replaceChildren();

        data.artists.forEach(artist => {
            const row = document.createElement("div");

            row.className = "track";
            row.textContent = artist;

            row.addEventListener("click", () => loadAlbums(artist));

            musicBrowser.appendChild(row);
        });

        if (data.artists.length === 0) {
            musicBrowser.textContent = "No artists found.";
        }

    } catch (error) {
        console.error("Cassette artist browser error:", error);
        musicBrowser.textContent = "Unable to load artists.";
    }
}

async function loadTracks(artist, album, source = "artists", directory = null) {
    if (!musicBrowser) return;

    musicBrowser.textContent = `Loading tracks for ${album}...`;

    try {
        const body = new URLSearchParams();

        if (directory !== null) {
            body.append("action", "list_compilation_tracks");
            body.append("album", album);
            body.append("directory", directory);
        } else {
            body.append("action", "list_tracks");
            body.append("artist", artist);
            body.append("album", album);
        }     

        const response = await fetch(apiBase + "player.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body
        });

        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }

        const data = await response.json();

        if (!data.success || !Array.isArray(data.tracks)) {
            throw new Error("Invalid track list response");
        }

        musicBrowser.replaceChildren();

        const backButton = document.createElement("button");
        backButton.textContent = "← Back to Albums";
        backButton.addEventListener("click", () => {
            if (source === "albums") {
                loadAllAlbums();
            } else {
                loadAlbums(artist);
            }
        });
        musicBrowser.appendChild(backButton);

        const playAlbumButton = document.createElement("button");
        playAlbumButton.type = "button";
        playAlbumButton.textContent = "Play Album";

        playAlbumButton.addEventListener("click", async () => {
            playAlbumButton.disabled = true;

            try {
                const body = new URLSearchParams();
                body.append("action", "play_album");
                body.append("artist", artist);
                body.append("album", album);

                if (directory !== null) {
                    body.append("directory", directory);
                }
                const response = await fetch(apiBase + "player.php", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || "Unable to play album");
                }

                await refreshStatus();

            } catch (error) {
                console.error("Cassette Play Album Failed:", error);
                alert("Unable to play album.");
            } finally {
                playAlbumButton.disabled = false;
            }
        });

        musicBrowser.appendChild(playAlbumButton);

        const queueAlbumButton = document.createElement("button");
        queueAlbumButton.type = "button";
        queueAlbumButton.textContent = "Add Album to Queue";

        queueAlbumButton.addEventListener("click", async () => {
            queueAlbumButton.disabled = true;

            try {
                const body = new URLSearchParams();
                body.append("action", "add_album");
                body.append("artist", artist);
                body.append("album", album);

                if (directory !== null) {
                    body.append("directory", directory);
                }

                const response = await fetch(apiBase + "player.php", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || "Unable to add album");
                }

                queueAlbumButton.textContent = "Album Added!";

                setTimeout(() => {
                    queueAlbumButton.textContent = "Add Album to Queue";
                }, 1500);

            } catch (error) {
                console.error("Cassette Add Album Failed:", error);
                queueAlbumButton.textContent = "Failed";
            } finally {
                queueAlbumButton.disabled = false;
            }
        });

musicBrowser.appendChild(queueAlbumButton);

        data.tracks.forEach(track => {
            const row = document.createElement("div");
            row.className = "track";

            const number = track.track || "";
            const title = track.title || track.file || "";

        const trackLabel = document.createElement("span");
        trackLabel.textContent = `${number} ${title}`.trim();

        const playButton = document.createElement("button");
        playButton.type = "button";
        playButton.textContent = "Play";

        playButton.addEventListener("click", async () => {
            const body = new URLSearchParams();
            body.append("action", "play_track");
            body.append("value", track.file);

            try {
                const response = await fetch(apiBase + "player.php", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || "Unable to play track");
                }

                await refreshStatus();

            } catch (error) {
                console.error("Cassette Play Track Failed:", error);
            }
        });

const queueButton = document.createElement("button");
queueButton.type = "button";
queueButton.textContent = "Add to Queue";

queueButton.addEventListener("click", async () => {
    queueButton.disabled = true;

    const body = new URLSearchParams();
    body.append("action", "add_track");
    body.append("value", track.file);

    try {
        const response = await fetch(apiBase + "player.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body
        });

        const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || "Unable to add track");
                }

                queueButton.textContent = "Added!";
                setTimeout(() => {
                    queueButton.textContent = "Add to Queue";
                }, 1500);

            } catch (error) {
                console.error("Cassette Add to Queue Failed:", error);
                queueButton.textContent = "Failed";
            } finally {
                queueButton.disabled = false;
            }
        });

        row.appendChild(trackLabel);
        row.appendChild(playButton);
        row.appendChild(queueButton);
        musicBrowser.appendChild(row);
        });

        if (data.tracks.length === 0) {
            musicBrowser.append("No tracks found.");
        }

    } catch (error) {
        console.error("Cassette track browser error:", error);
        musicBrowser.textContent = "Unable to load tracks.";
    }
}

async function loadAlbums(artist) {
    if (!musicBrowser) return;

    musicBrowser.textContent = `Loading albums for ${artist}...`;

    try {
        const body = new URLSearchParams();
        body.append("action", "list_albums");
        body.append("value", artist);

        const response = await fetch(apiBase + "player.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body
        });

        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }

        const data = await response.json();

        if (!data.success || !Array.isArray(data.albums)) {
            throw new Error("Invalid album list response");
        }

        musicBrowser.replaceChildren();

        const backButton = document.createElement("button");
        backButton.textContent = "← Back to Artists";
        backButton.addEventListener("click", loadArtists);
        musicBrowser.appendChild(backButton);

        data.albums.forEach(album => {
            const row = document.createElement("div");
            row.className = "track";
            row.textContent = album;

            row.addEventListener("click", () => {
                loadTracks(artist, album);
        });

        musicBrowser.appendChild(row);
        });

        if (data.albums.length === 0) {
            musicBrowser.append("No albums found.");
        }

    } catch (error) {
        console.error("Cassette album browser error:", error);
        musicBrowser.textContent = "Unable to load albums.";
    }
}

    if (artistsTab) {
        artistsTab.addEventListener("click", loadArtists);
    }

    // Music Library — All Albums Browser
    async function loadAllAlbums() {
        if (!musicBrowser) return;

        musicBrowser.textContent = "Loading albums...";

        try {
            const body = new URLSearchParams();
            body.append("action", "list_all_albums");

            const response = await fetch(apiBase + "player.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body
            });

            if (!response.ok) {
                throw new Error("HTTP " + response.status);
            }

            const data = await response.json();

            if (!data.success || !Array.isArray(data.albums)) {
                throw new Error("Invalid album response");
            }

            musicBrowser.replaceChildren();

        data.albums.forEach(item => {
            const row = document.createElement("div");
            row.className = "track";
            row.textContent = item.album + " — " + item.artist;
            row.style.cursor = "pointer";

            row.addEventListener("click", () => {
                if (item.compilation === true) {
                    loadTracks(
                        item.artist,
                        item.album,
                        "albums",
                        item.directory
                    );
                } else {
                    loadTracks(item.artist, item.album, "albums");
                }
            });
            
            musicBrowser.appendChild(row);
        });         

            if (data.albums.length === 0) {
                musicBrowser.textContent = "No albums found.";
            }

        } catch (error) {
            console.error("Cassette Albums Browser Error:", error);
            musicBrowser.textContent = "Unable to load albums.";
        }
    }

    if (albumsTab) {
        albumsTab.addEventListener("click", loadAllAlbums);
    }

    if (!previewMode) {
        refreshStatus();
        setInterval(refreshStatus, 1000);
    }
    
   // Play or queue all tracks directly inside a folder
async function queueFolder(entries, playNow = false) {
    const tracks = entries.filter(entry => entry.type === "file");

    if (tracks.length === 0) {
        alert("No tracks found in this folder.");
        return;
    }

    try {
        for (let i = 0; i < tracks.length; i++) {
            const body = new URLSearchParams();

            // Start playback with the first track when requested
            const action = playNow && i === 0
                ? "play_track"
                : "add_track";

            body.append("action", action);
            body.append("value", tracks[i].path);

            const response = await fetch(apiBase + "player.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "Unable to queue folder");
            }
        }

        if (playNow) {
            await refreshStatus();
        }

    } catch (error) {
        console.error("Folder playback failed:", error);
        alert("Unable to queue all folder tracks.");
    }
}
    // Music Library — Folder Browser
async function loadFolders(path = "") {
    if (!musicBrowser) return;

    musicBrowser.textContent = "Loading folders...";

    try {
        const body = new URLSearchParams();
        body.append("action", "list_directory");
        body.append("path", path);

        const response = await fetch(apiBase + "player.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body
        });

        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }

        const data = await response.json();

        if (!data.success || !Array.isArray(data.entries)) {
            throw new Error("Invalid directory response");
        }

        musicBrowser.replaceChildren();

// Folder playback controls
if (path !== "") {
    const folderTracks = data.entries.filter(
        entry => entry.type === "file"
    );

    if (folderTracks.length > 0) {
        const controls = document.createElement("div");
        controls.className = "folder-controls";

        const playFolderButton = document.createElement("button");
        playFolderButton.type = "button";
        playFolderButton.textContent = "Play Folder";

        playFolderButton.addEventListener("click", async () => {
            playFolderButton.disabled = true;

            try {
                await queueFolder(data.entries, true);
            } finally {
                playFolderButton.disabled = false;
            }
        });

        const addFolderButton = document.createElement("button");
        addFolderButton.type = "button";
        addFolderButton.textContent = "Add Folder to Queue";

        addFolderButton.addEventListener("click", async () => {
            addFolderButton.disabled = true;

            try {
                await queueFolder(data.entries, false);
            } finally {
                addFolderButton.disabled = false;
            }
        });

        controls.appendChild(playFolderButton);
        controls.appendChild(addFolderButton);
        musicBrowser.appendChild(controls);
    }
}

        // Show a Back button when inside a folder
        if (path !== "") {
            const backButton = document.createElement("button");
            backButton.type = "button";
            backButton.textContent = "← Back";

            backButton.addEventListener("click", () => {
                const parentPath = path.includes("/")
                    ? path.substring(0, path.lastIndexOf("/"))
                    : "";

                loadFolders(parentPath);
            });

            musicBrowser.appendChild(backButton);
        }

        // Display folders and allow navigation
        data.entries.forEach(entry => {
            if (entry.type !== "directory") return;

            const row = document.createElement("div");
            row.className = "track";
            row.textContent = "📁 " + entry.name;
            row.style.cursor = "pointer";

            row.addEventListener("click", () => {
                loadFolders(entry.path);
            });

            musicBrowser.appendChild(row);
        });

        // Display music files within the current folder
        data.entries.forEach(entry => {
            if (entry.type !== "file") return;

            const row = document.createElement("div");
            row.className = "track";

        const trackLabel = document.createElement("span");
        trackLabel.textContent = "♫ " + (entry.title || entry.name);

        const playButton = document.createElement("button");
        playButton.type = "button";
        playButton.textContent = "Play";

        playButton.addEventListener("click", async () => {
            playButton.disabled = true;

            try {
                const body = new URLSearchParams();
                body.append("action", "play_track");
                body.append("value", entry.path);

                const response = await fetch(apiBase + "player.php", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || "Unable to play track");
                }

                await refreshStatus();

            } catch (error) {
                console.error("Folder track playback failed:", error);
                alert("Unable to play track.");
            } finally {
                playButton.disabled = false;
            }
        });

        const queueButton = document.createElement("button");
        queueButton.type = "button";
        queueButton.textContent = "Add to Queue";

        queueButton.addEventListener("click", async () => {
            queueButton.disabled = true;

            try {
                const body = new URLSearchParams();
                body.append("action", "add_track");
                body.append("value", entry.path);

                const response = await fetch(apiBase + "player.php", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || "Unable to add track");
                }

            } catch (error) {
                console.error("Folder track queue failed:", error);
                alert("Unable to add track to queue.");
            } finally {
                queueButton.disabled = false;
            }
        });

        row.appendChild(trackLabel);
        row.appendChild(playButton);
        row.appendChild(queueButton);
        musicBrowser.appendChild(row);
        });

        if (data.entries.length === 0) {
            musicBrowser.textContent = "This folder is empty.";
        }

    } catch (error) {
        console.error("Cassette Folder Browser Error:", error);
        musicBrowser.textContent = "Unable to load folders.";
    }
}

if (foldersTab) {
    foldersTab.addEventListener("click", () => loadFolders(""));
}
});
