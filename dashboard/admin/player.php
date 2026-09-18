<?php
header("Content-Type: application/json");
header("X-Content-Type-Options: nosniff");

require_once("../config.php");

$action = $_POST['action'] ?? '';
$value  = $_POST['value'] ?? '';

switch ($action) {
    case "previous": shell_exec("mpc prev"); break;
    case "play":     shell_exec("mpc play"); break;
    case "pause":    shell_exec("mpc pause"); break;
    case "toggle":   shell_exec("mpc toggle"); break;
    case "stop":     shell_exec("mpc stop"); break;
    case "next":     shell_exec("mpc next"); break;

    case "volume":
        $v = max(0, min(100, intval($value)));
        shell_exec("mpc volume $v");
        break;

    case "seek":
        $s = intval($value);
        shell_exec(sprintf("mpc seek %d", $s));
        break;

    case "shuffle":
        if ($value === '') {
            shell_exec("mpc random");
        } else {
            $status = ($value === 'true' || $value === '1' || $value === 'on') ? "on" : "off";
            shell_exec("mpc random $status");
        }
        break;

    case "repeat":
        if ($value === '') {
            shell_exec("mpc repeat");
        } else {
            $status = ($value === 'true' || $value === '1' || $value === 'on') ? "on" : "off";
            shell_exec("mpc repeat $status");
        }
        break;

    case "clear":
        shell_exec("mpc clear");
        break;

    case "add":
        if ($value !== '') {
            $file = escapeshellarg($value);
            shell_exec("mpc add $file");
        }
        break;

    case "clear_add":
        if ($value !== '') {
            $file = escapeshellarg($value);
            shell_exec("mpc clear && mpc add $file && mpc play");
        }
        break;

    case "playindex":
        $track = max(1, intval($value));
        shell_exec("mpc play " . escapeshellarg($track));
        break;

    default:
        http_response_code(400);
        echo json_encode([
            "success" => false,
            "error" => "Unknown player action requested: " . htmlspecialchars($action)
        ]);
        exit;
}

// ----------------------------------------------------
// FETCH FRESH AFTERMATH STATE FOR THE FRONTEND
// ----------------------------------------------------
$statusString = shell_exec("mpc status");

// 1. Extract the clean layout playback status state
preg_match('/\[(.*?)\]/', $statusString, $stateMatch);
$currentState = strtolower($stateMatch[1] ?? "stopped");

// 2. Extract current track numerical position tracking index
$currentTrackIndex = null;
if (preg_match('/#(\d+)\/\d+/', $statusString, $indexMatch)) {
    $currentTrackIndex = intval($indexMatch[1]) - 1; // 0-indexed alignment
}

// 3. Extract the active volume metrics
preg_match('/volume:\s*([0-9]+%)/', $statusString, $volMatch);
$currentVolume = $volMatch[1] ?? "--";

// Send high-utility data directly back to JavaScript for partial layout paints
echo json_encode([
    "success"   => true,
    "action"    => $action,
    "playback"  => [
        "state"               => $currentState,
        "volume"              => $currentVolume,
        "current_track_index" => $currentTrackIndex
    ]
], JSON_PRETTY_PRINT);
