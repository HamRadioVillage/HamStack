# Changelog

All notable public HamStack releases are recorded here.

HamStack uses semantic versioning while the public interface is still evolving. During
the `0.x` line, role variables and implementation boundaries may change between minor
releases when needed to establish a durable public contract.

## [0.1.0] - 2026-09-28

Initial public alpha release.

### Added

- Composable Ansible role families for digital modes, packet/APRS/BBS, voice/hotspot
  appliances, visual tools, shared services, desktops, infrastructure, and network
  integrations.
- Local inventory model with Ansible Vault support and shared hardware-resource
  definitions.
- Interactive configurator plus non-interactive inventory/bootstrap helpers.
- Deployment profiles for a HamCube/service node, conference control station, and
  contributor workstation.
- Packet stack support including Graywolf, APRS, LinBPQ, Pat/Winlink, and an IP-access
  ENiGMA BBS deployment.
- Digital/operator support including FLDIGI, FLRIG, WSJT-X, JS8Call, FT8Web, SSTV,
  CHIRP, NetLogger, UniPager, and multimon-ng.
- Appliance configuration for preinstalled AllStarLink ASL3 and WPSD systems.
- Shared/event services including Gatus, DCDash, Blur Deck, CONHAM display mirroring,
  Meshtastic Web, Cloudlog, Wavelog, GPS-backed time, OpenHamClock, and OpenWebRX.
- Network/infrastructure roles for 44Net Connect, Technitium DNS, basic iPXE content,
  read-only AREDN integration, OpenWrt/GL.iNet, and RouterOS.
- Offline repository QA, variable-reference generation, contributor guidance, security
  guidance, architecture documentation, and agent/maintainer instructions.

### Release expectations

- v0.1.0 is an alpha-quality public release, not a certification of every supported
  radio, interface, router, or appliance combination.
- Representative HRV hardware and deployment paths have been exercised; site-specific
  radio/audio calibration, device mapping, and application preferences may still need
  operator adjustment.
- Transmit-capable paths use conservative defaults and require the deploying operator
  to validate RF, PTT, audio, licensing, and local operating requirements.
