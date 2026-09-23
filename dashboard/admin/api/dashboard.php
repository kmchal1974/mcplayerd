<?php
header('Content-Type: application/json');
header('X-Content-Type-Options: nosniff');

require_once("../config.php");
require_once("../includes/artwork.php");

// ----------------------------------------------------
// PLAYER & ACTIVE TRACK QUEUE
// ----------------------------------------------------
$current = trim(shell_exec("mpc current"));
$status = shell_exec("mpc status");

// Fix: Read element 1 from the regex match array cleanly
preg_match('/\[(.*?)\]/', $status, $stateMatch);
$state = strtolower($stateMatch[1] ?? "stopped");

preg_match('/(\d+:\d+)\/(\d+:\d+)/', $status, $timesMatch);
$elapsed = $timesMatch[1] ?? "0:00";
$length = $timesMatch[2] ?? "0:00";

preg_match('/\(([0-9]+)%\)/', $status, $percentMatch);
$percent = intval($percentMatch[1] ?? 0);

preg_match('/volume:\s*([0-9]+%)/', $status, $volMatch);
$volume = $volMatch[1] ?? "--";

// NEW: Extract random and repeat flags from mpc status (checks if they are "on")
$random = false;
if (preg_match('/random:\s*(on|off)/', $status, $randomMatch)) {
    $random = ($randomMatch[1] === 'on');
}

$repeat = false;
if (preg_match('/repeat:\s*(on|off)/', $status, $repeatMatch)) {
    $repeat = ($repeatMatch[1] === 'on');
}

$artist = trim(shell_exec("mpc --format '%artist%' current"));
$album = trim(shell_exec("mpc --format '%album%' current"));
$artwork = getAlbumArtwork();

// Fix: Correctly grab the capture group index
$current_track_index = null;
if (preg_match('/ #(\d+)\/\d+/', $status, $indexMatch)) {
    $current_track_index = intval($indexMatch[1]) - 1;
}

// ----------------------------------------------------
// PLAYLIST GENERATION
// ----------------------------------------------------
$raw_playlist = shell_exec('mpc playlist -f "%artist% - %title%"');
if (empty($raw_playlist)) {
    $playlist = [];
} else {
    $playlist_lines = explode("\n", trim($raw_playlist));
    $playlist = array_values(array_filter(array_map('trim', $playlist_lines)));
}

// ----------------------------------------------------
// LIBRARY
// ----------------------------------------------------
$stats = shell_exec("mpc stats");
preg_match('/Songs:\s+(\d+)/', $stats, $songsMatch);
$songs = $songsMatch[1] ?? "--";

preg_match('/Albums:\s+(\d+)/', $stats, $albumsMatch);
$albums = $albumsMatch[1] ?? "--";

preg_match('/Artists:\s+(\d+)/', $stats, $artistsMatch);
$artists = $artistsMatch[1] ?? "--";

// ----------------------------------------------------
// DATABASE STATUS
// ----------------------------------------------------
$updating = strpos(shell_exec("mpc"), "Updating DB") !== false;
preg_match('/DB Updated:\s+(.*)/', $stats, $lastscanMatch);
$lastscan = trim($lastscanMatch[1] ?? "--");

// ----------------------------------------------------
// SYSTEM METRICS
// ----------------------------------------------------
$tempRaw = @file_get_contents('/sys/class/thermal/thermal_zone0/temp');
$tempF = "--";
if ($tempRaw !== false) {
    $tempC = $tempRaw / 1000;
    $tempF = round(($tempC * 9 / 5) + 32, 1) . "°F";
}

$memory = trim(shell_exec("free -m | awk '/Mem:/ {print $3\" MB / \"$2\" MB\"}'"));
$disk = trim(shell_exec("df -h / | awk 'END{print $5}'"));
$musicdisk = trim(shell_exec("df -h /mnt/music | awk 'END{print $5}'"));
$uptime = trim(shell_exec("uptime -p"));
$hostname = trim(shell_exec("hostname"));
$kernel = trim(shell_exec("uname -r"));
$load = trim(shell_exec("cut -d' ' -f1 /proc/loadavg"));

// ----------------------------------------------------
// NETWORK
// ----------------------------------------------------
$lan = trim(shell_exec("hostname -I | awk '{print $1}'"));
$tailscale = trim(shell_exec("tailscale ip -4 2>/dev/null"));
$ssid = trim(shell_exec("iwgetid -r"));
if ($ssid == "") {
    $ssid = "Offline";
}

$signal = trim(shell_exec("iwconfig wlan0 2>/dev/null | grep -o '[0-9]\\+/70' | head -1"));
if ($signal != "") {
    list($a, $b) = explode("/", $signal);
    $signal = round(($a / $b) * 100) . "%";
} else {
    $signal = "--";
}

exec("ping -c1 8.8.8.8 >/dev/null 2>&1", $o, $internet);
$internet = ($internet == 0) ? "Online" : "Offline";
$stream = "http://" . $lan . ":8000";

// ----------------------------------------------------
// ACTIVITY LOGGING
// ----------------------------------------------------
$activity = "Ready";
$logfile = "../logs/activity.log";
if (file_exists($logfile)) {
    $lines = file($logfile);
    $activity = implode("<br>", array_slice($lines, -10));
}

// ----------------------------------------------------
// RENDER RESPONSE
// ----------------------------------------------------
echo json_encode([
    "song"                => $current,
    "artist"              => $artist,
    "album"               => $album,
    "state"               => $state,
    "elapsed"             => $elapsed,
    "length"              => $length,
    "percent"             => $percent,
    "volume"              => $volume,
    "random"              => $random, // Added
    "repeat"              => $repeat, // Added
    "songs"               => $songs,
    "albums"              => $albums,
    "artists"             => $artists,
    "cpu"                 => $tempF,
    "memory"              => $memory,
    "disk"                => $disk,
    "musicdisk"           => $musicdisk,
    "uptime"              => $uptime,
    "hostname"            => $hostname,
    "kernel"              => $kernel,
    "load"                => $load,
    "lan"                 => $lan,
    "tailscale"           => $tailscale,
    "ssid"                => $ssid,
    "signal"              => $signal,
    "internet"            => $internet,
    "stream"              => $stream,
    "playlist"            => $playlist,
    "current_track_index" => $current_track_index,
    "updating"            => $updating,
    "lastscan"            => $lastscan,
    "activity"            => $activity,
    "artwork"             => $artwork
], JSON_PRETTY_PRINT);
