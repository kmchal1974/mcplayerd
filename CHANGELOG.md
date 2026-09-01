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
