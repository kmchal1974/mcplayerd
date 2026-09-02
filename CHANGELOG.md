## v0.2.0 — Network Observation

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
- Wi-Fi device reported as wlan0
- Connected state detected correctly
- Saved Wi-Fi profiles identified
- Usable Wi-Fi correctly reports True on a normal network
- Existing MPD playback and state updates remain operational
## v0.1.0 — Daemon Foundation

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

2.0.0

Initial public architecture.

Dashboard complete.

RompR repaired.

Artwork fixed.

Playback API.

Volume slider.

Playlist.

Golden Master.
