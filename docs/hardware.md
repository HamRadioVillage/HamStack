# Model and reference hardware

HamStack is intentionally hardware-flexible. This document records the
**reference hardware and capability classes used to develop the project**; it is
not a mandatory shopping list.

Support labels used here are intentionally conservative:

- **Reference** — used in the HamStack/HRV development environment or directly
  represented by a current role.
- **Expected** — architecturally suitable, but not necessarily field-validated
  by the project on every model.
- **Specialized** — useful for a narrow role rather than a general multi-role
  node.
- **Not recommended** — technically possible in some cases, but a poor default
  for that workload.

## Compute platforms

| Platform | Status | Good fits | Constraints / notes |
| --- | --- | --- | --- |
| Raspberry Pi 5 + durable storage | Reference / service-node candidate | HamStack dashboard, Blur Deck, Meshtastic dashboard, OpenHamClock, containers, archives, shared services | Natural central "brain" platform; the reference HamCube uses a Pi 5 with NVMe-capable storage. Keep RF edge nodes independently useful. |
| Raspberry Pi 4 | Reference | AllStar, Graywolf, LinBPQ, APRS, SSTV RX/workstation, OpenHamClock, lightweight OpenWebRX, general services | Primary ARM reference platform. Desktop roles need a desktop-capable OS/session. Container-heavy or SDR-heavy combinations should be sized and tested. |
| Raspberry Pi 3 | Reference | Graywolf, LinBPQ, packet/BBS, lightweight headless services | Useful reuse target for lighter roles. Avoid assuming it has the headroom of a Pi 4 for several GUI/container/SDR workloads at once. |
| Raspberry Pi Zero 2 W | Reference / specialized | Selfie Station, small headless services, appliance roles supported by their upstream image | Excellent single-purpose node. Not the default target for multi-container stacks or desktop applications. |
| Pi Zero-family hotspot hardware | Reference / specialized | WPSD when supported by the upstream WPSD image | HamStack begins after the WPSD image is installed. Exact hardware support follows WPSD upstream. |
| amd64 Linux mini-PC/laptop | Expected / first-class target | GridTracker 2, FLDIGI, FLRIG, WSJT-X, OpenWebRX, OpenHamClock, packet roles, local services | Preferred when desktop software, containers, or heavier SDR workloads need more headroom. |
| generic arm64 Debian-family SBC | Expected | Most headless/container roles and GridTracker 2 where upstream packages exist | GPIO, camera, audio, and device paths may require board-specific integration. |
| older/smaller ARM boards | Specialized | One lightweight role at a time | Treat as deployment-specific until tested. |

A role README may impose tighter requirements than this table.

## Reference radio interfaces and peripherals

### AIOC

The All-In-One Cable (AIOC) is a first-class HamStack shared device resource.
A single AIOC may be consumed by different roles on the same host at different
times, so it belongs in `hamstack_devices`, not inside a Graywolf- or SSTV-only
configuration structure.

Reference uses include:

- Graywolf packet modem/PTT;
- SSTV audio/PTT;
- the Selfie Station transmit path;
- general sound-card/PTT experiments.

Useful endpoints include serial/PTT, capture audio, and playback audio.

### DigiRig

DigiRig-style USB interfaces are a natural fit for HF digital roles such as
FLRIG, FLDIGI, and WSJT-X. HamStack models them as shared devices so CAT/audio
resources can be referenced by more than one application.

### AllStar radio interfaces

The reference AllStar environment has used a USB radio interface with an
SA-818-family radio module. SHARI/CM108-style interfaces are also consistent
with the role model. The AllStar role is expected to translate inventory
variables into the native ASL configuration after a supported ASL image is
installed.

### RTL-SDR

RTL-SDR devices are reference receive hardware for SDR and OpenWebRX work.
OpenWebRX can be CPU-intensive depending on receiver count, sample rate, and
demodulation workload; amd64 or a Pi 4-class system is a safer starting point
than a Pi Zero.

### GNSS / PPS

HamStack's `gps-time` role expects a named GPS/GNSS device resource and can also
consume a PPS endpoint. The GNSS receiver is a stratum-0 reference source;
chrony on the HamStack host serves time to explicitly allowed client networks.

### Camera and HID trigger

The Selfie Station reference hardware uses:

- Raspberry Pi Camera;
- a USB HID foot pedal;
- an AIOC;
- a radio capable of transmitting the generated SSTV audio.

These are independent named devices in inventory rather than hard-coded device
paths.

## Reference radios

HamStack generally configures the computer-side infrastructure rather than the
radio firmware itself. Radios used or discussed in the reference environment
include:

| Radio | Typical HamStack use |
| --- | --- |
| QRZ-1 | VHF/UHF packet and event-demo radio |
| Quansheng UV-K5 | VHF/UHF experimentation and packet |
| Xiegu G90 | HF digital-mode / rig-control work |
| truSDX | Lightweight HF experimentation |
| zBitX | Experimental HF platform |

These entries are **reference context, not an automatic compatibility
guarantee**. A role that requires CAT, audio, PTT, or specific serial behavior
must document and validate those interfaces.

## Network and display infrastructure

The reference environment uses small GL.iNet/OpenWrt routers and has long used
MikroTik hardware, including the hAP ac lite. HamStack now reserves separate
network-device backends for both families rather than treating routers as
ordinary Linux radio nodes.

| Device family | Status | Intended HamStack use |
| --- | --- | --- |
| GL.iNet / OpenWrt | Reference / conservative backend | Portable event router, DHCP/DNS, Wi-Fi, VLANs, static routes, basic firewall policy |
| MikroTik hAP ac lite / RouterOS | Reference / conservative backend | Event routing/switching/Wi-Fi and infrastructure automation |
| AREDN-capable network hardware | Integration | Read-only node/status monitoring through the AREDN sysinfo API; firmware/configuration remains upstream-managed |
| Roku TV / Roku player | Reference display client | Blur Deck playback from the central DLNA media service; not treated as a general HamStack compute node |

Current network direction is:

- Linux nodes may establish a **44Net Connect WireGuard tunnel**;
- 44Net is split-routed by default rather than becoming the node's general
  Internet default route;
- routers use a separate `network.yml` inventory and `playbooks/network.yml`;
- AREDN integration is currently read-only monitoring/status; firmware and mesh configuration remain upstream-managed.

See [network-devices.md](network-devices.md) and
[architecture.md](architecture.md).

## Role-to-platform guidance

| Role family | Pi Zero 2 W | Pi 3 | Pi 4 | amd64 / larger arm64 |
| --- | --- | --- | --- | --- |
| common/bootstrap | Yes | Yes | Yes | Yes |
| Graywolf / LinBPQ | Possible single-purpose | Good | Good | Good |
| APRS demo profile | Possible single-purpose | Good | Good | Good |
| Selfie Station | Reference | Good | Good | Possible with camera changes |
| WPSD | Upstream-dependent reference use | Upstream-dependent | Upstream-dependent | Upstream-dependent |
| AllStar | Not preferred | Expected | Reference | Expected |
| FLDIGI / FLRIG / WSJT-X | Not recommended | Limited | Good with desktop | Good |
| GridTracker 2 | No | Not initial target | arm64 build where available | Reference initial targets: amd64/arm64 |
| OpenHamClock container | Not recommended | Possible | Good | Good |
| OpenWebRX | Not recommended | Light use only | Good for modest workloads | Preferred for heavier SDR workloads |
| local Cloudlog/Wavelog server | Not recommended | Limited | Possible | Preferred |
| central service/dashboard node | Not recommended | Limited | Good | Preferred |
| Blur Deck media service | Not recommended | Possible | Good | Good |
| Meshtastic dashboard | Not recommended | Possible | Good | Good |

The matrix is guidance, not a scheduler. HamStack will increasingly add runtime
assertions where a role has a hard architecture or operating-system
requirement.

## Desktop and controller systems

Debian-family laptops, mini-PCs, and Raspberry Pi systems can fill workstation
roles independent of the radio-node numbering scheme:

- **development workstation** — local HamStack source tree plus development/QA dependencies;
- **control station** — lean Ansible controller used by the lead operator;
- **kiosk station** — Chromium presentation surface for Gatus, CONHAM, DCDash, FT8Web, exams, or other web applications.

These are capabilities/profiles rather than specific hardware products.
