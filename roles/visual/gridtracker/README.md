# `gridtracker`

## Purpose

Install GridTracker2 as the visual companion to WSJT-X/JTDX-style digital mode
operation.

## Supported implementation

- Debian packages on amd64 and arm64;
- a known-good pinned release by default for deterministic fresh installs;
- optional `latest` discovery from the official GridTracker download page;
- explicit package URL/version overrides for reproducible deployments;
- optional XDG desktop autostart for `hamstack_operator_user`.

GridTracker's per-user settings remain operator-owned. Its upstream first-run
configuration and WSJT-X autodetection remain in place.
