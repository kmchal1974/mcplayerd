<?php require_once("config.php"); ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= htmlspecialchars(MCP_NAME, ENT_QUOTES, 'UTF-8') ?> Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
    <script defer src="js/app.js"></script>
</head>
<body>
    <header>
        <img src="<?= htmlspecialchars(LOGO_IMAGE, ENT_QUOTES, 'UTF-8') ?>" alt="McPlayer Logo">
        <h1><?= htmlspecialchars(MCP_NAME, ENT_QUOTES, 'UTF-8') ?></h1>
        <p>High Fidelity Music Server</p>
    </header>

    <div class="container">
        <div class="grid">

        <!-- NOW PLAYING -->
            <div class="card">
                <h2>Now Playing</h2>
                <img id="albumart" class="album" src="<?= htmlspecialchars(DEFAULT_ARTWORK, ENT_QUOTES, 'UTF-8') ?>" alt="Album Artwork">
                <h3 id="song">Loading...</h3>
                <div id="artist" class="small"></div>
                <div id="album" class="small"></div>
                <br>
                <div class="progress">
                    <div id="progressbar" class="progress-bar"></div>
                </div>
                <br>
                <div id="elapsed">0:00 / 0:00</div>
            </div>

            <!-- PLAYBACK -->
            <div class="card">
                <h2>Playback</h2>
                <div id="state">
                    <span class="badge stopped">Loading...</span>
                </div>
                <br>
                <div class="player-controls">
                    <button id="prevBtn" class="control-btn" aria-label="Previous">⏮</button>
                    <button id="playBtn" class="control-btn" aria-label="Play">▶</button>
                    <button id="stopBtn" class="control-btn" aria-label="Stop">⏹</button>
                    <button id="nextBtn" class="control-btn" aria-label="Next">⏭</button>
                </div>
                <br>
                <div class="player-options">
                    <button id="shuffleBtn" class="option-btn">🔀 Shuffle</button>
                    <button id="repeatBtn" class="option-btn">🔁 Repeat</button>
                </div>
                <br>
                <div class="value" id="volume">--</div>
                <input id="volslider" type="range" min="0" max="100" value="50">
            </div>

            <!-- PLAYLIST -->
            <div class="card">
                <h2>Playlist</h2>
                <div id="playlist" class="playlist">Loading Playlist...</div>
            </div>

            <!-- LIBRARY SUMMARY -->
            <div class="card">
                <h2>Library</h2>
                <table>
                    <tr>
                        <td>Songs</td>
                        <td id="songs">--</td>
                    </tr>
                    <tr>
                        <td>Albums</td>
                        <td id="albums">--</td>
                    </tr>
                    <tr>
                        <td>Artists</td>
                        <td id="artists">--</td>
                    </tr>
                    <tr>
                        <td>Status</td>
                        <td><div id="library-status">Idle</div></td>
                    </tr>
                    <tr>
                        <td>Last Scan</td>
                        <td id="lastscan">--</td>
                    </tr>
                </table>
            </div>

            <!-- LIBRARY SCAN PROGRESS -->
            <div class="card">
                <h2>Library Scan</h2>
                <div id="scanmessage">Idle</div>
                <br>
                <div style="background:#555;height:12px;border-radius:8px;overflow:hidden;">
                    <div id="scanbar" style="height:12px; width:0%; background:#4CAF50; transition: width 0.3s ease;"></div>
                </div>
            </div>

            <!-- SYSTEM DETAILS -->
            <div class="card">
                <h2>System</h2>
                <table>
                    <tr><td>CPU Load</td><td id="load">--</td></tr>
                    <tr><td>Music Drive</td><td id="musicdisk">--</td></tr>
                    <tr><td>Hostname</td><td id="hostname">--</td></tr>
                    <tr><td>Kernel</td><td id="kernel">--</td></tr>
                    <tr><td>CPU</td><td id="cpu">--</td></tr>
                    <tr><td>Memory</td><td id="memory">--</td></tr>
                    <tr><td>Disk</td><td id="disk">--</td></tr>
                    <tr><td>Uptime</td><td id="uptime">--</td></tr>
                </table>
            </div>

            <!-- NETWORK CONTROLS -->
            <div class="card">
                <h2>Network</h2>
                <table>
                    <tr><td>Mode</td><td id="mode">--</td></tr>
                    <tr><td>LAN IP</td><td id="ip">--</td></tr>
                    <tr><td>Tailscale</td><td id="tailscale">--</td></tr>
                    <tr><td>WiFi</td><td id="ssid">--</td></tr>
                    <tr><td>Signal</td><td id="signal">--</td></tr>
                    <tr><td>Internet</td><td id="internet">--</td></tr>
                    <tr><td>MPD Stream</td><td id="stream">--</td></tr>
                </table>
                <br>
                <a href="<?= htmlspecialchars(ICECAST_URL, ENT_QUOTES, 'UTF-8') ?>" target="_blank" style="color: #1f6feb; text-decoration: none; font-weight: bold;">🎵 Open Stream</a>
                <br><br>
                <button onclick="copyStream()">Copy Stream URL</button>
            </div>

            <!-- ACTIVITY FEED -->
            <div class="card">
                <h2>Activity</h2>
                <div id="activity">Waiting...</div>
            </div>

            <!-- SYSTEM BACKEND ACTIONS -->
            <div class="card">
                <h2>System Controls</h2>
                <form action="control.php" method="post">
                    <button type="submit" class="success" name="cmd" value="update">Update Library</button>
                    <button type="submit" class="success" name="cmd" value="rescan">Rescan Music</button>
                    <button type="submit" name="cmd" value="clear">Clear Playlist</button>
                    <button type="submit" name="cmd" value="restartmpd">Restart MPD</button>
                    <button type="submit" class="warning" name="cmd" value="reboot">Reboot</button>
                    <button type="submit" class="danger" name="cmd" value="shutdown">Shutdown</button>
                </form>
            </div>

        </div>
    </div>

    <footer>
        <?= htmlspecialchars(MCP_NAME, ENT_QUOTES, 'UTF-8') ?> Version <?= htmlspecialchars(MCP_VERSION, ENT_QUOTES, 'UTF-8') ?> Build <?= htmlspecialchars(MCP_BUILD, ENT_QUOTES, 'UTF-8') ?>
        <br>
        <?= htmlspecialchars(DEVICE_NAME, ENT_QUOTES, 'UTF-8') ?> • <?= htmlspecialchars(DAC_NAME, ENT_QUOTES, 'UTF-8') ?>
    </footer>
</body>
</html>
