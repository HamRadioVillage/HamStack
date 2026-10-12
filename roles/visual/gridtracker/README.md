# `gridtracker`

## Purpose

Install GridTracker2 as the visual companion to WSJT-X/JTDX-style digital mode
operation.

## Supported implementation

- Debian packages on amd64 and arm64;
- a known-good pinned release by default for deterministic fresh installs;
- optional `latest` discovery from the official GridTracker download page;
- explicit package URL/version overrides for reproducible deployments;
- optional XDG desktop autostart for `hamstack_operator_user`;
- optional SHA-256 verification through `hamstack_gridtracker_package_checksum`.

Package URLs must use HTTPS. The downloaded package is cached under the
root-owned HamStack package cache using its upstream filename, so changing
`hamstack_gridtracker_version` installs the new package rather than a stale
cached copy. GridTracker does not publish signed packages; supply
`hamstack_gridtracker_package_checksum` (`sha256:<digest>`) for reproducible,
verified installs.

GridTracker's per-user settings remain operator-owned. Its upstream first-run
configuration and WSJT-X autodetection remain in place.
