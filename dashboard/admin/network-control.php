<?php

header('Content-Type: application/json');

$allowedActions = [
    'force_ap',
    'automatic',
    'connect_saved',
    'list_saved',
    'scan_wifi',
    'add_network',
    'enable_autoconnect',
    'disable_autoconnect',
    'forget_network' 
];

$action = $_POST['action'] ?? '';

if (!in_array($action, $allowedActions, true)) {
    http_response_code(400);

    echo json_encode([
        'ok' => false,
        'error' => 'Invalid action'
    ]);

    exit;
}

$socketPath = '/run/mcplayer/network-control.sock';

$socket = socket_create(AF_UNIX, SOCK_STREAM, 0);

if ($socket === false) {
    http_response_code(500);

    echo json_encode([
        'ok' => false,
        'error' => 'Could not create control socket'
    ]);

    exit;
}

if (!socket_connect($socket, $socketPath)) {
    http_response_code(500);

    echo json_encode([
        'ok' => false,
        'error' => 'Could not connect to McPlayerD'
    ]);

    socket_close($socket);
    exit;
}

$requestData = [
    'action' => $action
];

if ($action === 'connect_saved') {
    $connection = $_POST['connection'] ?? '';

    if ($connection === '') {
        http_response_code(400);

        echo json_encode([
            'ok' => false,
            'error' => 'Missing connection'
        ]);

        socket_close($socket);
        exit;
    }

    $requestData['connection'] = $connection;
}
if (
    $action === 'enable_autoconnect' ||
    $action === 'disable_autoconnect' ||
    $action === 'forget_network'
) {
    $connection = $_POST['connection'] ?? '';

    if ($connection === '') {
        http_response_code(400);

        echo json_encode([
            'ok' => false,
            'error' => 'Missing connection'
        ]);

        socket_close($socket);
        exit;
    }

    $requestData['connection'] = $connection;
}
if ($action === 'add_network') {
    $ssid = $_POST['ssid'] ?? '';
    $password = $_POST['password'] ?? '';

    if ($ssid === '') {
        http_response_code(400);

        echo json_encode([
            'ok' => false,
            'error' => 'Missing SSID'
        ]);

        socket_close($socket);
        exit;
    }


    $requestData['ssid'] = $ssid;
    $requestData['password'] = $password;
}

$request = json_encode($requestData);

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
        'ok' => false,
        'error' => 'No response from McPlayerD'
    ]);

    exit;
}

echo $response;
