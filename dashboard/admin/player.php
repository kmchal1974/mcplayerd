<?php
header("Content-Type: application/json");
header("X-Content-Type-Options: nosniff");

require_once("../config.php");

$action = $_POST['action'] ?? '';
$value  = $_POST['value'] ?? '';

switch ($action) {
    case "previous":
    case "play":
    case "pause":
    case "next":
        $socketPath = '/run/mcplayer/player-control.sock';
        $socket = socket_create(AF_UNIX, SOCK_STREAM, 0);

        if ($socket === false) {
            http_response_code(500);
            echo json_encode([
                "success" => false,
                "error" => "Could not create player control socket"
            ]);
            exit;
        }

        if (!socket_connect($socket, $socketPath)) {
            http_response_code(500);
            echo json_encode([
                "success" => false,
                "error" => "Could not connect to McPlayerD"
            ]);
            socket_close($socket);
            exit;
        }

        $request = json_encode([
            "action" => $action
        ]);

        socket_write(
            $socket,
            $request,
            strlen($request)
        );

        $response = socket_read(
            $socket,
            8192
        );

        socket_close($socket);

        if ($response === false || $response === '') {
            http_response_code(500);
            echo json_encode([
                "success" => false,
                "error" => "No response from McPlayerD"
            ]);
            exit;
        }

        $mcplayerResponse = json_decode($response, true);

        if (
            !is_array($mcplayerResponse) ||
            !($mcplayerResponse['ok'] ?? false)
        ) {
            http_response_code(500);
            echo json_encode([
                "success" => false,
                "error" => $mcplayerResponse['error']
                    ?? "McPlayerD player command failed"
            ]);
            exit;
        }

        break;

     case "toggle":   shell_exec("mpc toggle"); break;
    case "stop":     shell_exec("mpc stop"); break;

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
