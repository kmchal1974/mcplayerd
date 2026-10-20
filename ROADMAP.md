# McPlayer Roadmap

**Project:** McPlayerD — Raspberry Pi Music Player
**Repository:** https://github.com/kmchal1974/mcplayerd
**Roadmap updated:** October 20, 2026
**Latest stable release:** v0.6.0 (`b9fb812`)
**Development policy:** GitHub is the source of truth. Develop on feature branches, verify changes before merging, and do not treat unfinished work as released.

## Milestone Overview

| Milestone | Scope | Status |
| --- | --- | --- |
| v0.1.0 | Daemon Foundation | Complete |
| v0.2.0 | Network Observation | Complete |
| v0.4.0 | Network Resilience and Wi-Fi Management | Complete |
| v0.5.0 | Player Control | Complete |
| v0.6.0 | Library & Playlist Management | **Stable release** |
| v0.7.0 | Bluetooth Support | Remote controls working; audio output shelved; **not released** |
| v0.8.0 | Backup & Recovery | Planned / development track |
| Cassette Admin interface | Visual redesign and music browsing improvements | Separate development track; release number TBD |
| v0.9.0 | Plugins | Proposed |
| v0.10.0 | OTA Updates | Proposed |

## Phase 1

- [x] Dashboard
- [x] Artwork
- [x] Playback API
- [x] Playlist
- [x] Volume slider
- [x] mcplayerd
- [x] Smart Networking
- [x] Offline Mode
- [ ] Bluetooth (full scope not complete; remote controls working)
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

- [x] List saved playlists
- [x] Load a saved playlist into the queue
- [x] Save the current queue as a new named playlist
- [x] Update an existing playlist from the current queue
- [x] Delete a saved playlist with confirmation
- [x] Manage saved playlists through McPlayerD

### Architecture

- [x] Route library browsing operations through McPlayerD
- [x] Route new library, queue, and playlist operations through McPlayerD
- [x] Keep RompR functional alongside the Admin dashboard
- [x] Avoid direct `mpc` commands for new Admin library and playlist features

### Tested

- [x] Browse Artist -> Album -> Tracks from the Admin dashboard
- [x] Build a queue from library selections
- [x] Play library selections from the Admin dashboard
- [x] Remove and reorder queued tracks
- [x] Save a new playlist
- [x] Load a saved playlist
- [x] Modify a loaded playlist and explicitly save the changes
- [x] Delete a saved playlist
- [x] RompR remains operational

**Milestone:** v0.6.0 - Library & Playlist Management

## Bluetooth Support

**Milestone:** v0.7.0 - Bluetooth Support (**partially working; paused; not released**)
**Development branch:** `feature/bluetooth-v0.7.0`
**Status review:** October 19, 2026

### Bluetooth Remote Controls — Working

- [x] Pair and trust Stadia Bluetooth controller
- [x] Detect Stadia controller through Linux HID input
- [x] Play/pause using the A button
- [x] Previous/next track using D-pad left/right
- [x] Volume up/down using D-pad up/down
- [x] Route playback commands through McPlayerD
- [x] Run Bluetooth controller listener in the background
- [x] Detect controller disconnection and reconnection
- [x] Recover automatically when BlueZ reports a connection but HID input is missing
- [x] Limit automatic recovery attempts to prevent repeated reconnection loops
- [x] Verify all controls after automatic HID recovery
- [x] Re-test Stadia controller successfully after October 19 Bluetooth audio troubleshooting

**Verified controller commit previously documented:** `4cfaa22` - Add limited Stadia Bluetooth HID recovery.
**Controller:** `Stadia9NZK-19fd` — paired, bonded, trusted, not blocked; HID recognized.
**Decision:** Preserve working controller implementation and button mappings. Bluetooth audio output need not be enabled for the controller to work.

### Bluetooth Audio Output — Experimental / Shelved

- [x] Inspect Bluetooth and audio architecture during troubleshooting
- [x] Configure BlueALSA A2DP source and sink
- [x] Configure and test an MPD Bluetooth Audio output
- [x] Test JBL Vibe Beam earbuds and onn. Rugged Speaker M
- [x] Test direct ALSA playback independently of MPD
- [x] Test playback with DAC and WAN outputs temporarily disabled
- [x] Investigate buffering, SBC bitrate, 44.1/48 kHz audio, Wi-Fi coexistence, system resources, firmware, drivers, and transport logs
- [x] Restore BlueALSA override file to the standard A2DP source/sink configuration
- [x] Leave Bluetooth Audio MPD output disabled
- [ ] Establish reliable, uninterrupted Bluetooth audio playback
- [ ] Establish safe, tested audio-output selection and switching
- [ ] Verify normal DAC playback with a final listening test

**Finding:** Playback was choppy with both Bluetooth devices. Direct ALSA playback was also choppy, so the problem is not isolated to MPD. Lower SBC bitrate and 44.1 kHz source audio improved some tests without resolving the problem. Forced 44.1 kHz negotiation was achieved but also produced a stalled, silent test. Inspected logs showed successful codec negotiation without an explicit transport error. CPU and memory checks did not show obvious exhaustion. **Root cause is undetermined.**

**Decision:** Shelve Bluetooth audio output rather than risk the working DAC, networking, or remote controls. An external USB Bluetooth adapter is a possible future experiment; it has **not** been tested.

**Final verified `mpc outputs` status:**

| MPD output | State |
| --- | --- |
| Output 1 — IQaudIO DAC | Enabled |
| Output 2 — WAN Stream | Enabled |
| Output 3 — Bluetooth Audio | Disabled |

**BlueALSA override:** `/etc/systemd/system/bluealsa.service.d/override.conf` contains:

```ini
[Service]
ExecStart=
ExecStart=/usr/bin/bluealsa -p a2dp-source -p a2dp-sink
```

Experimental `--sbc-quality=low` and `--a2dp-force-audio-cd` options were removed from the file. **BlueALSA was not restarted after the restoration**, so the file's settings will take effect at its next restart. `bluealsa-aplay` remains intentionally disabled. The observed `hciuart.service` state of `inactive (dead)` was not established as a fault and should not be changed without evidence.

### Bluetooth Audio Input — Deferred

- [ ] Design Bluetooth audio input architecture
- [ ] Implement Bluetooth audio input
- [ ] Test Bluetooth audio input
- [ ] Verify existing MPD playback and audio output remain functional

### Bluetooth Admin Management — Future

- [ ] Display Bluetooth status in the Admin dashboard
- [ ] Enable/disable Bluetooth
- [ ] Scan for available Bluetooth devices
- [ ] Display paired and available devices
- [ ] Pair, connect, disconnect, and forget devices
- [ ] Provide a separate enable/disable setting for Bluetooth remote controls
- [ ] Integrate Bluetooth management with the planned Admin dashboard redesign

### Architecture Requirements and Release Safeguards

- Preserve existing PCM512x DAC playback.
- Preserve MPD, RompR, Admin dashboard, WAN streaming, SSH, Wi-Fi, fallback AP, and Force AP Mode.
- Keep Bluetooth operations separate from Wi-Fi network management.
- Avoid unnecessary changes to Broadcom firmware, Bluetooth UART, Wi-Fi drivers, and networking services.
- Support user-directed Bluetooth device management.
- Keep Bluetooth optional so failures do not stop McPlayerD.
- Preserve the development order: remote controls, then audio output, then audio input, if work resumes.
- [ ] Confirm DAC playback with an actual listening test.
- [ ] Verify current Bluetooth branch, clean working tree, and controller code pushed to GitHub.
- [ ] Review any tracked audio experiments before merging.
- [ ] Do not mark v0.7.0 released or merge unfinished Bluetooth audio into stable v0.6.0.

## Backup & Recovery

**Planned milestone:** v0.8.0 — Backup & Recovery
**Development track:** `feature/backup-v0.8.0` (verify branch state before editing)

Three **distinct deliverables** are required; a personal backup is not a public installer.

### 1. Personal Configuration Backup

- [ ] Inventory configuration and user data required to restore a personal McPlayerD installation
- [ ] Back up McPlayerD settings, MPD configuration, playlists, and relevant playback state
- [ ] Back up applicable RompR preferences and user data safely
- [ ] Include network profiles and other personal configuration only in the private backup
- [ ] Protect passwords, Wi-Fi credentials, and other secrets in storage and during export
- [ ] Exclude music files and regenerable caches by default
- [ ] Provide verification and a documented restore procedure
- [ ] Test restoring onto a suitable installation

### 2. Full SD-Card Image Backup

- [ ] Define a full-card image workflow for disaster recovery
- [ ] Include operating system, installed software, configuration, and music
- [ ] Plan for the capacity and storage requirements of a large microSD card
- [ ] Document image creation, integrity verification, and restoration
- [ ] Test that a restored image can boot and operate
- [ ] Clearly label full images as **private** because they can contain personal credentials

### 3. Clean Distributable Installation

- [ ] Build a reproducible installation image or package for other users
- [ ] Exclude the original owner's accounts, passwords, saved Wi-Fi networks, SSH keys, tokens, and machine-specific secrets
- [ ] On first boot, offer a temporary setup access point when needed
- [ ] Provide browser-based first-run setup accessible from a phone or computer
- [ ] Require the new owner to create their own username and password
- [ ] Let the new owner select Wi-Fi and enter their own network password
- [ ] Complete initial setup without requiring Linux command-line access
- [ ] Secure or retire temporary setup credentials after provisioning
- [ ] Verify no original owner's personal data survives in the distributable output
- [ ] Test the clean installation on a freshly prepared card/device

### Backup Development Safeguards

- Do not upload private backups, credentials, or full personal SD images to public GitHub.
- Do not alter the stable player's data or configuration during initial inventory work.
- Implement and verify one small step at a time; keep recovery testing separate from normal playback.

## Cassette-Themed Admin Interface

**Development track:** `feature/cassette-skin-v1` (separate Git worktree)
**Milestone/version:** To be determined; do not mark complete until tested.

### Cassette Deck Design

- [ ] Design a cassette tape recorder viewed from above
- [ ] Place current track and album information in the upper speaker-grille area
- [ ] Display album artwork in the center of the cassette
- [ ] Animate cassette reels during playback and stop them when playback stops
- [ ] Provide cassette-deck-inspired playback controls
- [ ] Make the design responsive on phones, tablets, and desktop browsers
- [ ] Let the large cassette deck scroll out of view on phones while keeping a compact playback bar available
- [ ] Keep an optional VU-meter control in the design; real audio-driven meters are **not** a v1.0 blocker

### Music Browsing and Navigation

- [ ] Preserve artist → album → tracks browsing
- [ ] Add filesystem folder browsing, similar to RompR, without forcing genre-based navigation
- [ ] Add collapsible/expandable Music, Folder, and Playlist sections
- [ ] Add Back/breadcrumb navigation when drilling into artists, albums, and folders
- [ ] Allow adding individual songs and complete albums to the queue
- [ ] Keep saved playlists and queue controls accessible
- [ ] Preserve existing McPlayerD player-control architecture and RompR compatibility

### Admin Sections

- [ ] Music
- [ ] Setup
- [ ] Bluetooth
- [ ] Network
- [ ] System Controls

**Safeguard:** Develop and test the cassette interface independently of the Bluetooth and Backup branches. Do not imply the skin is already implemented or released.

## Plugins

**Proposed milestone:** v0.9.0 — Plugins

- [ ] Define plugin interfaces and lifecycle
- [ ] Decide how plugins are installed, enabled, disabled, and updated
- [ ] Isolate plugin failures from core music playback and networking
- [ ] Define plugin permissions and security boundaries
- [ ] Create a small example plugin and test it

## OTA Updates

**Proposed milestone:** v0.10.0 — OTA Updates

- [ ] Design a safe update mechanism using verified releases
- [ ] Protect user settings, playlists, and network configuration during updates
- [ ] Provide clear update status and failure reporting in the Admin dashboard
- [ ] Plan rollback or recovery from interrupted/failed updates
- [ ] Test updates and recovery before offering them to users

## Development and Release Rules

- GitHub is the source of truth; use separate branches for unfinished features.
- Review `git status`, current branch, and diffs before committing or merging.
- Test changes on the Raspberry Pi before declaring a release complete.
- Preserve stable v0.6.0 while Bluetooth, Backup, and Cassette work remain in development.
- Never commit private network profiles, credentials, tokens, or personal backup images.
- Do not treat roadmap checkboxes or a documentation commit as proof that hardware testing, a merge, or a release occurred.
