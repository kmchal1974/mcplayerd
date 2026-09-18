# Changelog

## v0.4.0 - Network Management

Reworked McPlayer networking around a sticky connection policy and added browser-based Wi-Fi management.

### Added

- Browser-based Wi-Fi management page
- Nearby Wi-Fi scanning
- Saved-network listing
- Signal-strength and security display
- Connection to selected saved networks
- WPA/WPA2 network setup
- Open network setup
- Per-network Auto-connect controls
- Forget Network control
- Protection against forgetting the `McPlayer-AP` fallback profile
- McPlayerD network-control Unix socket
- PHP bridge between the dashboard and McPlayerD
- Secure temporary password-file handling for Wi-Fi credentials
- Cleanup of incomplete profiles after failed connection attempts

### Changed

- Replaced automatic preferred-network switching with a sticky network policy.
- McPlayer now remains on a usable normal Wi-Fi connection instead of periodically searching for a stronger saved network.
- NetworkManager may automatically reconnect to another saved Auto-connect network if the current network disappears.
- If no usable normal Wi-Fi returns for approximately 30 seconds, McPlayerD starts `McPlayer-AP`.
- Once fallback AP mode starts, McPlayer remains there until explicit user action.
- Force AP Mode remains in AP mode until explicit user action.
- Newly added Wi-Fi networks default to Auto-connect OFF.
- Trusted networks can be explicitly enabled for Auto-connect.

### Fixed

- Prevented periodic Wi-Fi scanning/switching from destabilizing the fallback AP on the Raspberry Pi Zero 2 W.
- Prevented browser disconnects during Wi-Fi switching from terminating the McPlayerD network-control thread.
- Increased Wi-Fi connection timeout to allow authentication and DHCP to complete.
- Failed Wi-Fi connection attempts now remove incomplete NetworkManager profiles.

### Verified

- Normal home Wi-Fi operation
- Manual Force AP Mode
- Fallback AP operation with no usable normal Wi-Fi
- Dashboard access while offline through `McPlayer-AP`
- RompR access while offline through `McPlayer-AP`
- SSH access while offline through `McPlayer-AP`
- Music playback while offline
- Secure new-network connection
- Open new-network connection
- New networks default to Auto-connect OFF
- Explicit saved-network connection
- Automatic recovery to trusted Auto-connect Wi-Fi
- Failed connection cleanup
- Forget Network
- Browser network control after Wi-Fi switching

**Known-good implementation commit:** `7d40c53` - Add browser WiFi management

**Milestone documentation commit:** `1c3047a` - Document network management milestone


## v0.3.0 - Network Resilience

Initial implementation of automatic Wi-Fi switching and fallback-AP recovery.

### Added

- Automatic preferred-network switching
- Automatic fallback-AP recovery
- Signal-strength comparison between saved Wi-Fi networks
- Automatic switching when another known network was meaningfully stronger

### Historical Note

The automatic preferred-network switching and automatic recovery away from the fallback AP introduced in v0.3.0 were later replaced by the sticky network policy in v0.4.0.

Real-world testing showed that periodic scanning and switching could destabilize `McPlayer-AP` while the Raspberry Pi Zero 2 W was using its single Wi-Fi radio as an access point.


## v0.2.0 - Network Observation

Added read-only NetworkManager awareness to McPlayerD.

### Added

- NetworkManager availability detection
- Active Wi-Fi connection detection
- Active SSID detection
- Wi-Fi device detection
- Wi-Fi device state detection
- Saved Wi-Fi connection discovery
- Usable Wi-Fi detection
- Exclusion of the McPlayer fallback access point from normal usable Wi-Fi

### Verified

- NetworkManager detected correctly on Raspberry Pi
- Active Wi-Fi network identified correctly
- Wi-Fi device reported as `wlan0`
- Connected state detected correctly
- Saved Wi-Fi profiles identified
- Usable Wi-Fi correctly reports True on a normal network
- Existing MPD playback and state updates remain operational


## v0.1.0 - Daemon Foundation

Initial working McPlayerD daemon foundation.

### Added

- Python McPlayerD application package
- MPD connection using python-mpd2
- Playback and current-song state reading
- MPD change detection using idle notifications
- Atomic runtime state output to `/run/mcplayer/state.json`
- Automatic MPD reconnection
- Continuous daemon operation
- systemd service integration
- Automatic startup after reboot

### Verified

- Local MPD playback remains operational
- RompR and existing McPlayer dashboard remain operational
- State updates when playback changes
- McPlayerD automatically starts after a Raspberry Pi reboot


## 2.0.0 - Initial Architecture

Initial public architecture.

### Completed

- Dashboard
- RompR repair
- Artwork fixes
- Playback API
- Volume slider
- Playlist

**Milestone:** Golden Master