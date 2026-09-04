Phase 1
========

[x] Dashboard

[x] Artwork

[x] Playback API

[x] Playlist

[x] Volume slider

[ ] mcplayerd

[ ] Smart Networking

[ ] Offline Mode

[ ] Bluetooth

[ ] Backup

[ ] Plugins

[ ] OTA Updates

### McPlayerD Daemon

- [x] Create Python application skeleton
- [x] Connect reliably to MPD
- [x] Read playback and song state
- [x] Detect MPD playback/song changes
- [x] Write runtime state to `/run/mcplayer/state.json`
- [x] Run continuously as a systemd service
- [x] Recover automatically after reboot

**Milestone:** v0.1.0 — Daemon Foundation

### Network Observation

- [x] Detect NetworkManager availability
- [x] Read active Wi-Fi connection
- [x] Read active Wi-Fi SSID
- [x] Read Wi-Fi device and state
- [x] Read saved Wi-Fi connections
- [x] Detect usable normal Wi-Fi connection

**Milestone:** v0.2.0 — Network Observation

✓ 3D-E Automatic preferred-network switching

✓ 3D-F Automatic fallback-AP recovery