# McPlayer — Project Source of Truth

**Version:** 2.0.0
**Status:** Golden Master
**Last Updated:** July 2026

---

# Project Vision

McPlayer is a self-contained, high-fidelity digital music appliance built on Raspberry Pi hardware.

The goal is to provide a reliable music server that behaves like a commercial audio component rather than a Linux computer.

A user should be able to:

* Turn it on.
* Connect from any phone, tablet, or computer.
* Browse and play music.
* Continue listening whether Internet is available or not.

Linux should never be exposed to the end user.

---

# Design Philosophy

McPlayer is an appliance.

The Raspberry Pi is simply the hardware platform.

The operating system exists only to support McPlayer.

Every feature should improve:

* reliability
* simplicity
* recoverability
* maintainability

---

# Hardware

Current Platform

* Raspberry Pi Zero 2 W
* 512 GB microSD
* External DAC
* USB Power
* Wi-Fi

Primary Output

High-quality stereo audio through the DAC.

Primary Control

Responsive web interface.

No dedicated display is required.

---

# Operating System

* Raspberry Pi OS Lite
* Debian Bookworm
* 64-bit

System should remain as lightweight as possible.

---

# Current Core Components

## MPD

Responsible only for:

* playback
* queue
* database
* audio output

MPD should not contain application logic.

---

## Apache / PHP

Hosts:

* Admin Dashboard
* REST API
* RompR

---

## RompR

Purpose:

* Library management
* Album browsing
* Metadata management
* Playlist management

Current Status

✔ Fully operational

Library rebuilt successfully.

Artwork repaired.

---

## Tailscale

Provides secure remote administration.

Allows McPlayer to be managed from anywhere without exposing ports.

---

# Optional Components

Currently Installed

* Icecast

Current Status

Installed but not actively used.

Future Possibilities

* Internet streaming
* Broadcast mode
* Multi-listener streaming

Because it is not part of the active playback path, it is considered optional.

---

# Dashboard

Location

/var/www/html/admin

Purpose

Real-time control and monitoring of McPlayer.

Current Features

✓ Album artwork

✓ Playback controls

✓ Playlist

✓ Volume slider

✓ Progress bar

✓ Library statistics

✓ Scan status

✓ Network status

✓ System health

✓ Stream information

✓ Activity feed

---

# REST API

Location

/var/www/html/admin/api

Current Endpoints

dashboard.php

player.php

playlist.php

network.php

status.php

system.php

Future Endpoints

daemon.php

wifi.php

bluetooth.php

backup.php

settings.php

plugins.php

---

# Current Stable Features

Artwork refresh

✔

Volume slider

✔

Playback controls

✔

Playlist display

✔

Library rebuild

✔

RompR repaired

✔

System monitoring

✔

Responsive dashboard

✔

---

# Current Architecture

```
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

The dashboard currently communicates directly with PHP APIs.

---

# Future Architecture

```
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

All application logic will move into mcplayerd.

PHP becomes a presentation layer.

---

# mcplayerd

mcplayerd becomes the operating system of McPlayer.

Responsibilities

Playback

Queue management

Volume

Shuffle

Repeat

Metadata cache

Album artwork cache

Network monitoring

Automatic Wi-Fi management

Automatic hotspot mode

Bluetooth management

Library monitoring

Backup management

Health monitoring

Logging

Plugin management

REST services

System automation

The web dashboard should never directly manage Linux services.

Everything flows through mcplayerd.

---

# Smart Networking

Primary Goal

McPlayer should always be reachable.

Normal Operation

Join known Wi-Fi.

Serve dashboard.

Provide playback.

Remote access through Tailscale.

Offline Operation

If no known Wi-Fi exists:

Automatically create

McPlayer

Wi-Fi access point.

Phone connects directly.

Dashboard becomes available.

Music continues normally.

When known Wi-Fi returns:

Reconnect automatically.

Disable hotspot.

Resume normal operation.

No user intervention required.

---

# Offline Operation

McPlayer must function without Internet.

The following features must continue working:

Music library

Playback

Album artwork

Playlist

Volume

Search

Dashboard

System controls

Only remote Internet access should be unavailable.

---

# Backup Philosophy

Every stable milestone should produce a complete backup.

Preferred backup methods

Full SD image

Project archive

Configuration export

Future

mcplayerd will include integrated backup functionality.

---

# Development Principles

Preserve existing functionality.

Avoid breaking APIs.

Build independent modules.

Fail safely.

Prefer daemon-based control.

Keep the interface responsive.

Design for unattended operation.

Every subsystem should restart independently.

Every major change should be reversible.

---

# Long-Term Roadmap

Phase 1

mcplayerd

Phase 2

Smart Networking

Phase 3

Offline Mode

Phase 4

Bluetooth

Phase 5

Integrated Backup

Phase 6

Plugin Framework

Phase 7

Automatic Updates

Phase 8

Optional Mobile Application

---

# Golden Master

McPlayer Version 2.0 represents the baseline system.

Known Working Components

✓ Dashboard

✓ MPD

✓ RompR

✓ Artwork

✓ Library

✓ Playback

✓ Volume

✓ Playlist

✓ Tailscale

This version should always remain recoverable.

---

# Mission Statement

McPlayer is an open, self-contained, appliance-grade music system designed to deliver a polished listening experience with the flexibility of open-source software and the reliability expected from dedicated commercial audio hardware.

The long-term objective is for users to think about their music—not the operating system running underneath it.
