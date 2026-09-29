# HamStack deployment architecture

HamStack is built around capabilities rather than fixed node identities. A node
number or computer model does not determine what that machine must do.

## Edge nodes

Edge nodes are machines close to radios, cameras, SDRs, or other physical
hardware. They should remain reconstructable and as independent as practical.

Examples include:

- AllStar nodes;
- WPSD hotspots;
- Graywolf/LinBPQ packet nodes;
- SSTV receive/transmit stations;
- the Selfie Station;
- rig-control/digital-mode workstations.

A failure of the central service node should not prevent an edge node from
performing its core local RF job.

## Central service node

Larger deployments may designate one machine as the **central service node** or
"brain." This is a composition of normal HamStack roles, not a separate OS or
magic appliance.

Good candidates are a Raspberry Pi 5 with durable storage or an amd64 system
with enough memory/storage for several containers and archives.

Likely central roles include:

- `services/gatus`;
- `services/blur-deck`;
- `services/conham-display`;
- DCDash;
- `services/meshtastic-dashboard`;
- local Cloudlog/Wavelog services when enabled;
- gps/chrony time service;
- OpenHamClock;
- selected archives and event-facing web services.

Stateful services belong here more naturally than on disposable radio-edge
nodes.

## Network infrastructure devices

Routers and switches are not ordinary HamStack Linux nodes.

HamStack models them in a separate network-device inventory and applies them
through a dedicated network playbook. Current network backends are:

- OpenWrt-family devices, including GL.iNet;
- MikroTik RouterOS, including hAP ac lite.

They should not receive the `common` Linux-node role, and HamStack should not
assume Python is present on the device.

See [network-devices.md](network-devices.md).

## Display clients

Display devices such as Roku TVs are consumers, not general HamStack compute
nodes.

For Blur Deck, the architecture is:

```text
central service node
        |
        | renders / stores blurdeck.mp4
        v
ReadyMedia / DLNA service
        |
        +---- Roku TV / Roku Media Player
        |
        +---- Roku TV / Roku Media Player
```

This replaces the earlier pattern of dedicating a Raspberry Pi HDMI output to
each display.

## Dashboard boundary

The HamStack dashboard is intended to show **ham-radio/deployment status**, not
become a general-purpose unauthenticated sysadmin panel.

It should favor:

- read-only status;
- role/service health;
- radio/demo state;
- event-facing information;
- HTTPS on shared LANs.

Credentials, generic shell/admin controls, and sensitive host-management data
do not belong on the public/event dashboard.

## Operator workstations and profiles

HamStack now separates shared service nodes from privileged operator desktops.
The **control station** is the lead volunteer's Ansible controller and consumes a
locally provided HamStack tree. The **development workstation** adds contributor
and QA tooling. Neither role implies a Git hosting workflow.

A generic `desktop/kiosk` role provides the browser/display primitive used by
HamCube and future exam/presentation stations.

Infrastructure such as Technitium DNS and netboot is similarly separated from
radio-service roles. See [profiles.md](profiles.md).
