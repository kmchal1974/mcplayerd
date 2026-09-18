<?php
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>McPlayer Network Control</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
            background: #111;
            color: #eee;
        }

        h1 {
            margin-bottom: 8px;
        }

        .card {
            background: #222;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }

        button {
            display: block;
            width: 100%;
            padding: 15px;
            margin: 12px 0;
            font-size: 18px;
            cursor: pointer;
        }

        #status {
            margin-top: 20px;
            padding: 12px;
            background: #333;
            border-radius: 6px;
            min-height: 24px;
        }
    </style>
</head>

<body>

<h1>McPlayer Network</h1>

<div class="card">
    <h2>Network Mode</h2>

    <button onclick="networkAction('force_ap')">
        Force AP Mode
    </button>

    <button onclick="networkAction('automatic')">
        Return to Automatic
    </button>
    <hr>

    <h2>Saved Networks</h2>

    <div id="saved-networks">
        Loading saved networks...
    </div>

    <hr>

    <h2>Nearby Networks</h2>

    <button onclick="scanNetworks()">
        Scan for Networks
    </button>

    <div id="nearby-networks">
        Press Scan for Networks
    </div>

    <div id="status">
        Ready
    </div>
</div>

<script>
async function networkAction(action) {
    const status = document.getElementById('status');

    if (action === 'force_ap') {
        status.textContent =
            'Switching to McPlayer AP. You may lose this connection.';
    } else {
        status.textContent =
            'Returning to automatic network mode. You may lose this connection.';
    }

    const body = new URLSearchParams();
    body.append('action', action);

    try {
        const response = await fetch(
            'network-control.php',
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/x-www-form-urlencoded'
                },
                body: body.toString()
            }
        );

        const result = await response.json();

        if (result.ok) {
            status.textContent =
                'Command accepted. Network connection may change.';
        } else {
            status.textContent =
                'Network command failed: ' +
                (result.error || 'Unknown error');
        }

    } catch (error) {
        status.textContent =
            'Connection changed. Reconnect to McPlayer if necessary.';
    }
}

async function connectSaved(connection) {
    const status = document.getElementById('status');

    status.textContent =
        'Connecting to ' + connection + '...';

    const body = new URLSearchParams();

    body.append('action', 'connect_saved');
    body.append('connection', connection);

    try {
        const response = await fetch(
            'network-control.php',
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/x-www-form-urlencoded'
                },
                body: body.toString()
            }
        );

        const result = await response.json();

        if (result.ok) {
            status.textContent =
                'Connecting to ' + connection +
                '. Your browser connection may change.';
        } else {
            status.textContent =
                'Connection failed: ' +
                (result.error || 'Unknown error');
        }

    } catch (error) {
        status.textContent =
            'Network changed. Reconnect to McPlayer if necessary.';
    }
}

async function setAutoconnect(connectionName, enabled) {
    const status =
        document.getElementById('status');

    const body =
        new URLSearchParams();

    body.append(
        'action',
        enabled
            ? 'enable_autoconnect'
            : 'disable_autoconnect'
    );

    body.append(
        'connection',
        connectionName
    );

    status.textContent =
        'Updating auto-connect...';

    try {
        const response = await fetch(
            'network-control.php',
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/x-www-form-urlencoded'
                },
                body: body.toString()
            }
        );

        const result =
            await response.json();

        if (result.ok) {
            status.textContent =
                'Auto-connect updated.';

            loadSavedNetworks();
        } else {
            status.textContent =
                'Update failed: ' +
                (result.error || 'Unknown error');
        }

    } catch (error) {
        status.textContent =
            'Update failed.';
    }
}
async function forgetNetwork(connectionName, ssid) {
    const status =
        document.getElementById('status');

    const confirmed = confirm(
        'Forget saved network "' +
        ssid +
        '"?'
    );

    if (!confirmed) {
        return;
    }

    const body =
        new URLSearchParams();

    body.append(
        'action',
        'forget_network'
    );

    body.append(
        'connection',
        connectionName
    );

    status.textContent =
        'Forgetting ' + ssid + '...';

    try {
        const response = await fetch(
            'network-control.php',
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/x-www-form-urlencoded'
                },
                body: body.toString()
            }
        );

        const result =
            await response.json();

        if (result.ok) {
            status.textContent =
                ssid + ' has been forgotten.';

            loadSavedNetworks();
        } else {
            status.textContent =
                'Forget failed: ' +
                (result.error || 'Unknown error');
        }

    } catch (error) {
        status.textContent =
            'Forget failed.';
    }
}
async function loadSavedNetworks() {
    const container =
        document.getElementById('saved-networks');

    const body = new URLSearchParams();
    body.append('action', 'list_saved');

    try {
        const response = await fetch(
            'network-control.php',
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/x-www-form-urlencoded'
                },
                body: body.toString()
            }
        );

        const result = await response.json();

        if (!result.ok) {
            container.textContent =
                'Could not load saved networks.';
            return;
        }

        container.innerHTML = '';

        result.networks.forEach(function(network) {
            const item =
                document.createElement('div');

            let signalText;

            if (network.signal === null) {
                signalText = 'Not in range';
            } else {
                signalText = network.signal + '%';
            }

            const autoText =
                network.autoconnect
                    ? 'Auto-connect ON'
                    : 'Auto-connect OFF';

            const label =
                document.createElement('div');

            label.textContent =
                network.ssid +
                ' — ' +
                signalText +
                ' — ' +
                autoText;

            item.appendChild(label);

            const connectButton =
                document.createElement('button');

            connectButton.textContent =
                'Connect';

            connectButton.onclick = function() {
                connectSaved(network.name);
            };

            item.appendChild(connectButton);

            const autoButton =
                document.createElement('button');

            if (network.autoconnect) {
                autoButton.textContent =
                    'Disable Auto-connect';

                autoButton.onclick = function() {
                    setAutoconnect(
                        network.name,
                        false
                    );
                };
            } else {
                autoButton.textContent =
                    'Enable Auto-connect';

                autoButton.onclick = function() {
                    setAutoconnect(
                        network.name,
                        true
                    );
                };
            }

            item.appendChild(autoButton);

            const forgetButton =
                document.createElement('button');

            forgetButton.textContent =
                'Forget';

            forgetButton.onclick = function() {
                forgetNetwork(
                    network.name,
                    network.ssid
                 );
            };

            item.appendChild(forgetButton);

            container.appendChild(item);
        });

        if (result.networks.length === 0) {
            container.textContent =
                'No saved Wi-Fi networks found.';
        }

    } catch (error) {
        container.textContent =
            'Could not contact McPlayerD.';
    }
}

async function scanNetworks() {
    const status =
        document.getElementById('status');

    const container =
        document.getElementById('nearby-networks');

    status.textContent = 'Scanning...';
    container.textContent = 'Scanning...';

    try {
        const scanResponse = await fetch(
            'network-control.php',
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/x-www-form-urlencoded'
                },
                body: 'action=scan_wifi'
            }
        );

        const scanResult =
            await scanResponse.json();

        if (!scanResult.ok) {
            container.textContent =
                'Wi-Fi scan failed.';

            status.textContent = 'Ready';
            return;
        }

        const savedResponse = await fetch(
            'network-control.php',
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/x-www-form-urlencoded'
                },
                body: 'action=list_saved'
            }
        );

        const savedResult =
            await savedResponse.json();

        const savedSsids = new Set();

        if (savedResult.ok) {
            for (const network of savedResult.networks) {
                savedSsids.add(network.ssid);
            }
        }

        container.innerHTML = '';

        for (const network of scanResult.networks) {
            const item =
                document.createElement('div');

            const securityText =
                network.security || 'Open';

            const label =
                document.createElement('div');

            label.textContent =
                network.ssid +
                ' — ' +
                network.signal +
                '% — ' +
                securityText;

            item.appendChild(label);

            if (savedSsids.has(network.ssid)) {
                const savedLabel =
                    document.createElement('span');

                savedLabel.textContent = 'Saved';

                item.appendChild(savedLabel);
            } else {
                const connectButton =
                    document.createElement('button');

                connectButton.textContent =
                    'Connect';

                connectButton.onclick =
                    function() {
                        connectNewNetwork(
                            network.ssid,
                            network.security
                        );
                    };

                item.appendChild(connectButton);
            }

            container.appendChild(item);
        }

        status.textContent = 'Ready';

    } catch (error) {
        container.textContent =
            'Wi-Fi scan failed.';

        status.textContent = 'Ready';
    }
}

async function connectNewNetwork(ssid, security) {
    const status =
        document.getElementById('status');

    let password = '';

    if (security && security.trim() !== '') {
        password = prompt(
            'Enter Wi-Fi password for ' + ssid
        );

        if (password === null) {
            return;
        }

        if (password === '') {
            status.textContent =
                'Password required.';
            return;
        }
    }

    const body = new URLSearchParams();

    body.append('action', 'add_network');
    body.append('ssid', ssid);
    body.append('password', password);

    status.textContent =
        'Connecting to ' + ssid + '...';

    try {
        const response = await fetch(
            'network-control.php',
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/x-www-form-urlencoded'
                },
                body: body.toString()
            }
        );

        const result = await response.json();

        if (result.ok) {
            status.textContent =
                'Connecting to ' + ssid +
                '. Your browser connection may change.';
        } else {
            status.textContent =
                'Connection failed: ' +
                (result.error || 'Unknown error');
        }

    } catch (error) {
        status.textContent =
            'Network changed. Reconnect to McPlayer if necessary.';
    }
}

loadSavedNetworks();
</script>
</body>
</html>
