
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>McPlayerD Cassette Player</title>

    <link rel="stylesheet" href="css/cassette.css">
    <script defer src="js/cassette.js"></script>
</head>

<body>

<main class="cassette-app">

    <!-- VINTAGE CASSETTE RECORDER -->
    <section class="cassette-deck">

        <!-- SPEAKER GRILLE / TRACK INFORMATION -->
        <div class="speaker-grille">
            <div class="branding">McPlayerD</div>

            <div class="track-display">
                <div id="song-title">Never Meant to Know</div>
                <div id="artist-name">Tally Hall</div>
                <div id="album-name">Good &amp; Evil</div>
            </div>
        </div>

        <!-- CASSETTE COMPARTMENT -->
        <div class="cassette-compartment">

            <div class="cassette-tape">

                <div class="tape-label">
                    <img
                        id="album-art"
                        src="assets/default-cover.png"
                        alt="Album Artwork">
                </div>

                <div class="tape-reels">

                    <div class="reel left-reel"></div>
                    <div class="reel right-reel"></div>

                </div>

            </div>

        </div>

        <!-- VU METERS -->
        <div class="vu-section">
            <div class="vu-meter">VU LEFT</div>
            <div class="vu-meter">VU RIGHT</div>
        </div>

        <!-- PLAYBACK CONTROLS -->
        <div class="transport-controls">

            <button id="prev-btn">⏮</button>
            <button id="play-btn">▶</button>
            <button id="stop-btn">■</button>
            <button id="next-btn">⏭</button>

        </div>

    </section>

    <!-- MANAGEMENT CONSOLE -->
    <section class="management-console">

        <nav class="main-tabs">
            <button>Music</button>
            <button>Queue</button>
            <button>Playlists</button>
            <button>Bluetooth</button>
            <button>Network</button>
            <button>Setup</button>
            <button>System</button>
        </nav>

        <div class="tab-content">
            <h2>Music Library</h2>

            <nav class="music-tabs">
                <button id="folders-tab" type="button">Folders</button>
                <button id="artists-tab" type="button">Artists</button>
                <button id="albums-tab" type="button">Albums</button>
                <button>Songs</button>
            </nav>
        </div>
        <div id="music-browser" class="music-browser">
            Select Artists to browse your music library.
        </div>
    </section>

</main>

</body>
</html>
