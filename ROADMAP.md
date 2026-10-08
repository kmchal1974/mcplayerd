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

## Player Control

- [x] Control MPD through the McPlayerD Unix socket
- [x] Play
- [x] Pause
- [x] Toggle play/pause
- [x] Previous track
- [x] Next track
- [x] Stop
- [x] Volume control
- [x] Seek within the current track
- [x] Shuffle control
- [x] Synchronize dashboard shuffle state with MPD
- [x] Repeat control
- [x] Synchronize dashboard repeat state with MPD
- [x] Clear the current playlist
- [x] Play a selected track from the current playlist
- [x] Route active dashboard playback controls through McPlayerD

### Tested

- [x] Play and pause through McPlayerD
- [x] Previous and next track
- [x] Stop playback
- [x] Volume control
- [x] Seek control
- [x] Shuffle control and RompR synchronization
- [x] Repeat control and RompR synchronization
- [x] Clear playlist
- [x] Dashboard playlist click-to-play
- [x] Dashboard playback controls remain functional through McPlayerD

**Milestone:** v0.5.0 - Player Control

## Library & Playlist Management

### Library Browser

- [x] Read album artists from the MPD library
- [x] Browse albums for a selected artist
- [x] Browse tracks for a selected album
- [x] Display the music library in the Admin dashboard

### Queue Management

- [x] Add a selected track to the current queue
- [x] Add a selected album to the current queue
- [x] Play a selected track immediately
- [x] Play a selected album immediately
- [x] Remove an individual track from the current queue
- [x] Reorder tracks in the current queue
- [x] Manage the queue through McPlayerD

### Saved Playlists

- [ ] List saved playlists
- [ ] Load a saved playlist into the queue
- [ ] Save the current queue as a new named playlist
- [ ] Update an existing playlist from the current queue
- [ ] Delete a saved playlist with confirmation
- [ ] Manage saved playlists through McPlayerD

### Architecture

- [x] Route library browsing operations through McPlayerD
- [ ] Route new library, queue, and playlist operations through McPlayerD
- [ ] Keep RompR functional alongside the Admin dashboard
- [ ] Avoid direct `mpc` commands for new Admin library and playlist features

### Tested

- [x] Browse Artist -> Album -> Tracks from the Admin dashboard
- [ ] Build a queue from library selections
- [ ] Play library selections from the Admin dashboard
- [ ] Remove and reorder queued tracks
- [ ] Save a new playlist
- [ ] Load a saved playlist
- [ ] Modify a loaded playlist and explicitly save the changes
- [ ] Delete a saved playlist
- [ ] RompR remains operational

**Milestone:** v0.6.0 - Library & Playlist Management
