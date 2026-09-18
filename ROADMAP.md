# McPlayer Roadmap

## Phase 1

- [x] Dashboard
- [x] Artwork
- [x] Playback API
- [x] Playlist
- [x] Volume slider
- [x] mcplayerd
- [x] Smart Networking
- [x] Offline Mode
- [ ] Bluetooth
- [ ] Backup
- [ ] Plugins
- [ ] OTA Updates


## McPlayerD Daemon

- [x] Create Python application skeleton
- [x] Connect reliably to MPD
- [x] Read playback and song state
- [x] Detect MPD playback/song changes
- [x] Write runtime state to `/run/mcplayer/state.json`
- [x] Run continuously as a systemd service
- [x] Recover automatically after reboot

**Milestone:** v0.1.0 - Daemon Foundation


## Network Observation

- [x] Detect NetworkManager availability
- [x] Read active Wi-Fi connection
- [x] Read active Wi-Fi SSID
- [x] Read Wi-Fi device and state
- [x] Read saved Wi-Fi connections
- [x] Detect usable normal Wi-Fi connection

**Milestone:** v0.2.0 - Network Observation

## Network Resilience

- [x] Detect sustained loss of usable Wi-Fi
- [x] Wait approximately 30 seconds before starting fallback AP
- [x] Start `McPlayer-AP` automatically when no usable Wi-Fi remains
- [x] Keep fallback AP active until explicit user action
- [x] Allow NetworkManager to reconnect to trusted auto-connect networks
- [x] Prevent McPlayerD from periodically switching away from a working connection
- [x] Force AP Mode manually
- [x] Explicitly connect to a selected saved network
- [x] Recover from failed network connection attempts
- [x] Keep MPD, RompR, dashboard, and SSH usable while offline through fallback AP


## Wi-Fi Management

- [x] Scan for nearby Wi-Fi networks
- [x] Display SSID, signal strength, and security
- [x] Connect to saved networks
- [x] Add and connect to WPA/WPA2 networks
- [x] Add and connect to open networks
- [x] Keep Wi-Fi passwords out of command-line arguments
- [x] Remove temporary password files after connection attempts
- [x] Delete incomplete profiles after failed connection attempts
- [x] Default newly added networks to Auto-connect OFF
- [x] Display Auto-connect status for saved networks
- [x] Enable Auto-connect for trusted saved networks
- [x] Disable Auto-connect for saved networks
- [x] Forget saved networks
- [x] Protect `McPlayer-AP` from being forgotten
- [x] Control networking through McPlayerD Unix socket
- [x] Allow Apache/PHP dashboard to communicate with McPlayerD
- [x] Survive browser disconnects during Wi-Fi switching
- [x] Provide standalone browser Wi-Fi management page

### Network Policy

McPlayer follows a sticky network policy:

1. If connected to usable normal Wi-Fi, remain connected.
2. If that network disappears, allow NetworkManager to reconnect to another saved Auto-connect network.
3. If no usable Wi-Fi returns for approximately 30 seconds, start `McPlayer-AP`.
4. Once fallback AP mode starts, remain there until explicit user action.
5. Force AP Mode immediately starts `McPlayer-AP` and remains there until explicit user action.
6. Newly added Wi-Fi networks default to Auto-connect OFF.
7. Auto-connect must be explicitly enabled for networks McPlayer should trust automatically.

### Tested

- [x] Normal home Wi-Fi operation
- [x] Manual Force AP Mode
- [x] Offline dashboard access through `McPlayer-AP`
- [x] Offline RompR access through `McPlayer-AP`
- [x] Offline SSH access through `McPlayer-AP`
- [x] Music playback while offline
- [x] Secure new-network connection
- [x] Open new-network connection
- [x] New networks default to Auto-connect OFF
- [x] Explicit saved-network connection
- [x] Automatic recovery to trusted saved Wi-Fi
- [x] Failed connection cleanup
- [x] Fallback AP recovery
- [x] Forget Network
- [x] Browser network control remains available after network switching

**Known-good commit:** `7d40c53` - Add browser WiFi management


## Remaining Network Work

- [ ] Show the currently active network clearly in the browser UI
- [ ] Show fallback AP mode clearly in the browser UI
- [ ] Improve network-page layout and status messages
- [ ] Replace browser password prompt with an inline password field
- [ ] Integrate network controls into the main `/admin` dashboard
- [ ] Consider HTTPS for local dashboard/password protection
- [ ] Complete final reboot/travel testing