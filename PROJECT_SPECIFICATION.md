# McPlayer — Project Source of Truth

**Specification version:** 2.1.0 (proposed update)
**Specification status:** Development reference; historical Golden Master 2.0 baseline retained
**Last updated:** October 22, 2026
**Project:** McPlayerD — Raspberry Pi Music Player
**Repository:** https://github.com/kmchal1974/mcplayerd
**Latest stable software release:** v0.6.0 (`b9fb812`)

> **Version distinction:** The original *McPlayer Project Source of Truth* was labeled **Version 2.0.0 — Golden Master** in July 2026. That was a specification/baseline designation, **not** evidence that McPlayerD software v2.0.0 was released. McPlayerD software release numbers follow the GitHub roadmap and tags.

---

## Original July 2026 Technical Baseline — Detailed Requirements

The following sections preserve the detailed inventories, diagrams, responsibilities, and safeguards from the original July 2026 Golden Master specification. They are historical design requirements, not assertions that every item is implemented. Where they conflict with the updated requirements later in this document, the updated requirements govern.

### Original core component responsibilities

**MPD** — responsible only for:

- playback
- queue
- database
- audio output

MPD should not contain application logic.

**Apache / PHP** hosts:

- Admin Dashboard
- REST API
- RompR

**RompR** purposes:

- Library management
- Album browsing
- Metadata management
- Playlist management

July 2026 recorded status: fully operational; library rebuilt successfully; artwork repaired. This is a historical status report, not a guarantee about subsequent issues.

**Tailscale** provides secure remote administration, allowing McPlayer to be managed without exposing public ports.

**Icecast** was installed but not actively used in the July baseline. Future possibilities included Internet streaming, broadcast mode, and multi-listener streaming. Icecast was optional because it was not part of the active playback path at that time.

### Original dashboard feature inventory

**Location:** `/var/www/html/admin`

**Purpose:** Real-time control and monitoring of McPlayer.

The original specification marked these dashboard features as present:

- Album artwork
- Playback controls
- Playlist
- Volume slider
- Progress bar
- Library statistics
- Scan status
- Network status
- System health
- Stream information
- Activity feed

### Original PHP API inventory

**Location:** `/var/www/html/admin/api`

**Listed as current in July 2026:**

- `dashboard.php`
- `player.php`
- `playlist.php`
- `network.php`
- `status.php`
- `system.php`

**Listed as future in July 2026:**

- `daemon.php`
- `wifi.php`
- `bluetooth.php`
- `backup.php`
- `settings.php`
- `plugins.php`

These are original inventory/design claims. Confirm actual files and behavior before asserting current implementation.

### Original stable feature checklist

The July baseline marked each of these working:

- Artwork refresh
- Volume slider
- Playback controls
- Playlist display
- Library rebuild
- RompR repaired
- System monitoring
- Responsive dashboard

### Original current architecture diagram (July 2026)

```text
Music Library
      │
      ▼
     MPD
      │
      ├──────── DAC
      │
      ├──────── RompR
      │
      └──────── Dashboard API
```

The dashboard was described as communicating directly with PHP APIs.

### Original future architecture diagram (July 2026)

```text
Dashboard
      │
 REST API
      │
      ▼
  mcplayerd
      │
 ┌────┼───────────────┐
 │    │               │
 ▼    ▼               ▼
MPD Network      Library
 │
 ▼
Audio Output
```

Original direction: all application logic should move into McPlayerD; PHP becomes a presentation layer. The transition is incremental and partially implemented as documented below.

### Original McPlayerD responsibility inventory

The original specification described McPlayerD as the application control layer, responsible for:

- Playback
- Queue management
- Volume
- Shuffle
- Repeat
- Metadata cache
- Album artwork cache
- Network monitoring
- Automatic Wi-Fi management
- Automatic hotspot mode
- Bluetooth management
- Library monitoring
- Backup management
- Health monitoring
- Logging
- Plugin management
- REST services
- System automation

**Design requirement:** The web dashboard should never directly manage Linux services; application operations should flow through McPlayerD. This is a target architecture, not a claim that all existing legacy PHP code has already been migrated.

**Networking clarification:** The July 2026 requirement to automatically reconnect to a known Wi-Fi network and disable the hotspot whenever that network returns is **superseded** by the sticky, user-directed AP behavior documented in *Smart Networking — Current Policy* below. The rest of the offline-access objective remains intact.

### Original offline-operation checklist

Without Internet, the following must continue working:

- Music library
- Playback
- Album artwork
- Playlist
- Volume
- Search
- Dashboard
- System controls

Only remote Internet access should be unavailable.

### Original backup philosophy

Every stable milestone should produce a complete backup. Original preferred methods were a full SD image, project archive, and configuration export. The three specific deliverables defined later under *Backup & Recovery — v0.8.0* expand this requirement.

### Original development principles

- Preserve existing functionality.
- Avoid breaking APIs.
- Build independent modules.
- Fail safely.
- Prefer daemon-based control.
- Keep the interface responsive.
- Design for unattended operation.
- Every subsystem should restart independently.
- Every major change should be reversible.

### Original long-term roadmap

1. mcplayerd
2. Smart Networking
3. Offline Mode
4. Bluetooth
5. Integrated Backup
6. Plugin Framework
7. Automatic Updates
8. Optional Mobile Application

The updated roadmap later in this document records the implementation milestones and additional cassette-interface development track.

### Original Golden Master checklist

The July 2026 Golden Master recorded these as known working:

- Dashboard
- MPD
- RompR
- Artwork
- Library
- Playback
- Volume
- Playlist
- Tailscale

**Original safeguard:** This baseline should always remain recoverable.

---

## Project Vision

McPlayer is a self-contained, high-fidelity digital music appliance built on Raspberry Pi hardware.

The goal is a reliable music server that behaves like a commercial audio component rather than a Linux computer. A user should be able to:

- Turn it on.
- Connect from any phone, tablet, or computer.
- Browse and play music.
- Continue listening whether Internet is available or not.

**Linux should never be exposed to the end user during normal operation or initial setup of a distributable installation.**

## Design Philosophy

McPlayer is an appliance. The Raspberry Pi is simply the hardware platform; the operating system exists to support McPlayer. Every feature should improve reliability, simplicity, recoverability, or maintainability.

## Hardware

**Current platform:**

- Raspberry Pi Zero 2 W
- 512 GB microSD card
- IQaudIO-compatible PCM512x external DAC
- USB power
- Onboard Wi-Fi and Bluetooth

**Primary output:** High-quality stereo audio through the DAC.

**Primary control:** Responsive browser-based interface; no dedicated display required.

## Operating System

- Raspberry Pi OS Lite, Debian Bookworm, 64-bit
- Lightweight, headless operation
- NetworkManager manages Wi-Fi

## Core Components

### MPD

MPD is responsible for playback, queue, music database, and audio outputs. Application orchestration belongs in McPlayerD rather than MPD.

### Apache / PHP

Hosts the Admin dashboard, PHP API endpoints, and RompR. The Admin UI should delegate new application control operations to McPlayerD through supported interfaces rather than directly manipulating Linux services.

### RompR

Used for music library browsing, metadata, artwork, and playlist management. Preserve RompR alongside the Admin dashboard.

**Status note:** RompR is operational as part of the v0.6.0 baseline, but a later collection/database issue was investigated separately. Do not interpret the July 2026 statement “Library rebuilt successfully” as proof that all subsequent collection issues are resolved.

### Tailscale

Provides secure remote administration without opening public inbound ports. It is not required for offline playback.

### Optional components

Icecast was documented as installed but not actively used in the July 2026 baseline. Internet streaming, broadcast mode, and multi-listener streaming remain optional possibilities. Verify present configuration before relying on them.

## Admin Dashboard

**Location:** `/var/www/html/admin`

Existing dashboard capabilities documented in the original specification include artwork, playback controls, playlist, volume, progress, library statistics, scan and network status, system health, stream information, and activity feed. The v0.5.0 and v0.6.0 milestones additionally document McPlayerD-based playback and library/playlist management.

**Do not assume every legacy dashboard endpoint already uses McPlayerD.** The existing `admin/api/player.php` has used direct `mpc` calls; new features should avoid unnecessary duplication or rewrites of working behavior.

## PHP API

**Location:** `/var/www/html/admin/api`

The original specification lists these existing endpoints: `dashboard.php`, `player.php`, `playlist.php`, `network.php`, `status.php`, `system.php`.

Originally proposed endpoints: `daemon.php`, `wifi.php`, `bluetooth.php`, `backup.php`, `settings.php`, `plugins.php`.

This list records the original design intent; **verify actual files before describing an endpoint as implemented**.

## Implemented Architecture and Milestones

The original July 2026 architecture described a future transition from direct PHP control to a McPlayerD daemon. That transition is underway and partially implemented.

```text
Browser: Admin dashboard / RompR
          |
       PHP APIs
          |
   McPlayerD control sockets (for supported operations)
          |
   MPD / NetworkManager / system services
          |
    PCM512x DAC and other configured outputs
```

- **v0.1.0 — Daemon Foundation:** McPlayerD Python service, MPD state observation, runtime state file, and systemd recovery.
- **v0.2.0 — Network Observation:** NetworkManager and Wi-Fi status detection.
- **v0.4.0 — Network Resilience and Wi-Fi Management:** Browser-based Wi-Fi management, fallback AP, Force AP Mode, and explicit network selection.
- **v0.5.0 — Player Control:** Playback and queue controls through McPlayerD.
- **v0.6.0 — Library & Playlist Management:** Library browsing, queue changes, and saved playlists through McPlayerD. **Latest stable release:** `b9fb812`.

**Architecture principle:** Preserve existing working PHP, RompR, MPD, and daemon integrations. Move additional application logic into McPlayerD incrementally and only after testing. The dashboard should not directly manage Linux services when a safe daemon interface is available.

## McPlayerD Responsibilities

**Implemented or substantially established:**

- MPD observation and playback state
- Playback commands, volume, shuffle, repeat, and queue control
- Library browsing and saved playlist operations
- Network monitoring and user-directed Wi-Fi / fallback AP control
- Runtime state and service supervision

**Future, partial, or requiring verification:**

- Expanded metadata and artwork caching
- Bluetooth device and audio management
- Integrated backup and restore
- Additional health monitoring and logging
- Plugin management
- OTA update management
- Expanded API/services and automation

## Smart Networking — Current Policy

**Primary goal:** McPlayer should remain reachable without unnecessary network switching.

1. On usable normal Wi-Fi, remain connected.
2. If the connection disappears, NetworkManager may reconnect to another trusted saved network with Auto-connect enabled.
3. If no usable Wi-Fi returns for approximately 30 seconds, start the fallback McPlayer access point.
4. Once fallback AP starts, **stay in AP mode until explicit user action**. Do not periodically search and switch away.
5. **Force AP Mode** starts and maintains the AP even when known Wi-Fi networks are nearby, until the override is turned off or the user deliberately changes modes.
6. New Wi-Fi networks default to **Auto-connect OFF**; users explicitly enable it for trusted networks.
7. The user can scan, choose a saved network, add a new network, connect, or forget a network through browser controls.
8. Protect the fallback AP profile from accidental deletion. Preserve password-handling and failed-connection cleanup safeguards.

The earlier July 2026 requirement to automatically disable the hotspot whenever known Wi-Fi returns is **superseded** by this tested, sticky network policy.

## Offline Operation

Without Internet, local music playback, artwork, library browsing, playlists, volume, search, dashboard, and appropriate system controls should remain available. Remote Internet-based administration may be unavailable. The fallback AP provides local access when no usable network is present or when deliberately forced.

## Bluetooth — v0.7.0 (Unreleased)

**Development branch:** `feature/bluetooth-v0.7.0`

### Bluetooth remote controls — working

The paired/trusted Google Stadia Bluetooth controller has verified HID playback control, button mappings, and reconnection/recovery behavior. Previously documented recovery commit: `4cfaa22`. Preserve the working implementation and keep controller input independent of Bluetooth audio output.

### Bluetooth audio output — experimental, shelved

- BlueALSA A2DP and an MPD Bluetooth Audio output were configured and tested.
- JBL Vibe Beam earbuds and onn. Rugged Speaker M both experienced choppy playback.
- Direct ALSA playback was also choppy, so the issue is not isolated to MPD.
- Buffering, SBC settings, sample rates, interference, system resources, and transport were investigated; **root cause remains undetermined**.
- An external USB Bluetooth adapter is an **untested** possible future experiment.
- Final reported MPD outputs: **IQaudIO DAC enabled; WAN Stream enabled; Bluetooth Audio disabled**.
- A final **DAC listening test remains outstanding**.
- The BlueALSA override was restored to `-p a2dp-source -p a2dp-sink`, but BlueALSA was not restarted after restoration; `bluealsa-aplay` remains intentionally disabled.

**Decision:** Shelve unreliable Bluetooth audio output rather than risk working DAC, networking, or Stadia controller functionality. Do not modify Broadcom firmware, UART, or Wi-Fi drivers without evidence.

### Bluetooth audio input and Admin controls — future

Bluetooth audio input has **not** started. Future Admin management may include status, scanning, pairing, connecting/disconnecting, forgetting devices, and independent remote-control enable/disable.

**Development order:** Remote controls first, then audio output, then audio input. Do not merge or release incomplete v0.7.0 as though all Bluetooth functions work.

## Backup & Recovery — v0.8.0 (Planned / Development Track)

**Branch:** `feature/backup-v0.8.0` (verify current branch state before work).

Three separate deliverables are mandatory:

### 1. Personal configuration backup

- Export the user's McPlayerD settings, relevant MPD configuration, playlists, and applicable RompR settings/data.
- Include personal network configuration only when intentionally creating a **private** backup.
- Protect credentials, Wi-Fi passwords, tokens, and other secrets.
- Exclude music and regenerable caches by default, unless explicitly selected.
- Provide verification and a documented, tested restore procedure.

### 2. Full SD-card image backup

- Capture a complete disaster-recovery image including OS, installed software, configuration, and music.
- Account for the large 512 GB microSD and storage requirements.
- Document image integrity checking and restoration.
- Test that a restored image boots and works.
- Clearly mark full images **private**, since they may contain personal accounts and credentials.

### 3. Clean distributable installation image or package

- Produce a reproducible installation that **any new owner can use** without the original owner's credentials or saved Wi-Fi networks.
- Exclude personal logins, Wi-Fi profiles, SSH keys, API tokens, private preferences, and machine-specific secrets.
- Provide a **first-run setup experience** accessible from a phone, tablet, or computer, using a temporary setup AP when needed.
- Require the new owner to create their own **username and password** and enter their own **Wi-Fi credentials**.
- Complete initial setup without requiring Linux commands or SSH.
- Secure or retire temporary provisioning credentials and verify that no private information remains.
- Test on a fresh card/device before distribution.

**Safety:** Never upload private backups or personal full-card images to public GitHub. A private restore backup must never be mistaken for a clean public installer. Work in small, reversible, tested steps.

## Cassette-Themed Admin Interface — Separate Development Track

**Branch/worktree:** `feature/cassette-skin-v1`; release number to be determined.

- Design a cassette recorder viewed from above, with a speaker grille at the top.
- Show track/album information in the upper grille and **album artwork in the cassette center**.
- Animate cassette reels during playback; stop animation when playback stops.
- Use cassette-deck-style playback controls.
- Make phone and iPad layouts responsive; on phones, let the large cassette deck scroll away while a compact playback bar remains accessible.
- Keep real audio-driven VU meters a future enhancement, **not a v1.0 blocker**; allow an optional VU-meter control concept.
- Support filesystem **folder browsing like RompR**, not genre-only navigation, alongside Artist → Album → Tracks.
- Add Back/breadcrumb navigation, collapsible Music/Folder/Playlist sections, queueing of tracks and albums, and saved-playlist controls.
- Organize Admin sections around **Music, Setup, Bluetooth, Network, and System Controls**.
- Preserve McPlayerD controls, MPD, and RompR compatibility. Develop independently from Bluetooth and Backup.

## Plugins — v0.9.0 (Proposed)

- Define plugin interfaces, lifecycle, installation, enable/disable, and updates.
- Establish permissions and security boundaries.
- Ensure plugin failures cannot interrupt core playback or networking.
- Build and test a minimal example plugin before expanding the framework.

## OTA Updates — v0.10.0 (Proposed)

- Design a verified release/update mechanism.
- Preserve settings, playlists, credentials, and networking during updates.
- Show update progress and errors in the Admin dashboard.
- Plan rollback/recovery for interrupted updates.
- Test recovery thoroughly before exposing updates to general users.

## Long-Term Roadmap

1. Daemon foundation — complete.
2. Smart Networking and Offline Mode — implemented; some UI and travel testing remains.
3. Player Control and Library/Playlist Management — complete through stable v0.6.0.
4. Bluetooth v0.7.0 — remote controls working; audio output shelved; unreleased.
5. Backup & Recovery v0.8.0 — planned/development track.
6. Cassette-themed Admin redesign — separate worktree; release number TBD.
7. Plugin Framework v0.9.0 — proposed.
8. OTA Updates v0.10.0 — proposed.
9. Optional mobile application — longer-term possibility.

## Development Principles and Release Safeguards

- GitHub is the source of truth. Develop features on branches and verify before merging.
- Preserve working functionality, APIs, networking, DAC playback, MPD, RompR, Admin, and SSH.
- Favor modularity, safe failure, reversibility, and responsive browser controls.
- Avoid breaking changes and speculative low-level system modifications.
- Test on the Raspberry Pi before declaring a software release complete.
- Keep secrets, private Wi-Fi profiles, and backup images out of public GitHub.
- Keep stable **v0.6.0** recoverable while later features remain under development.

## Historical Golden Master

The July 2026 **McPlayer Project Source of Truth v2.0.0** identified a *Golden Master* baseline with Dashboard, MPD, RompR, artwork, library, playback, volume, playlists, and Tailscale. Preserve that historical reference. It does not override the verified McPlayerD GitHub release history, whose latest stable release is **v0.6.0**.

## Mission Statement

McPlayer is an open, self-contained, appliance-grade music system designed to deliver a polished listening experience with the flexibility of open-source software and the reliability expected from dedicated commercial audio hardware.

The long-term objective is for users to think about their music—not the operating system running underneath it.
