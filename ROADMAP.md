# HamStack roadmap


## Public project baseline

The v0.1.x line establishes the public newcomer path, feature/status catalog, GPLv3
licensing, contribution/security guidance, worked deployment examples, repository QA,
and documented agent/maintainer context.

The canonical public project home, issues, feature requests, and pull requests are at
https://github.com/HamRadioVillage/HamStack.


This roadmap records the intended direction of the project. It is deliberately
capability-oriented rather than date-driven: conference schedules and available
hardware change, while the architecture should remain useful.

Items listed here are plans, not promises that a feature is complete or safe to
deploy. Current implementation state lives in
[`docs/role-status.md`](docs/role-status.md).

## 1. Foundation and operator experience

The public release line keeps the boring pieces that make everything else repeatable:

- bootstrap a freshly installed supported node for Ansible;
- maintain a documented public variable vocabulary;
- keep hardware resources separate from application roles;
- provide a menu-driven local-inventory configurator;
- keep secrets in Ansible Vault;
- make repository QA cheap enough to run before every handoff;
- maintain hardware/reference and architecture documentation;
- validate idempotency on representative nodes.

Ongoing v0.1.x work focuses on widening reference-hardware coverage, preserving idempotency, and converting repeated operator tuning into safe variables only when the automation boundary is well understood. Current implementation status remains tracked separately in `docs/role-status.md`.

## 2. Packet and RF-service maturity

Continue turning the conference packet stack into reusable components:

- complete Graywolf radio/audio/PTT/channel configuration management;
- mature the APRS conference-demo profile, including validated beacon and
  digipeater-rule CRUD;
- continue the variable-driven LinBPQ node/BBS role;
- add the Graywolf KISS -> connected AX.25 -> ENiGMA transport shim;
- preserve offline-first packet/BBS operation;
- mature the Pat-backed Winlink role and validate its selected RF transports.

## 3. Network infrastructure

HamStack should eventually be able to describe and reproduce the small event
network around the radio nodes rather than treating it as mysterious external
plumbing.

Initial backends:

- **OpenWrt / GL.iNet** — HRV's common travel-router family;
- **MikroTik RouterOS** — including the hAP ac lite reference platform.

The intended common network model includes:

- device identity and management addressing;
- bridges/interfaces;
- VLANs;
- DHCP pools;
- DNS forwarding;
- Wi-Fi SSIDs and security;
- static routes;
- simple firewall zones/policy;
- 44Net routing integration.

Conservative backends now exist. OpenWrt/GL.iNet uses native UCI over SSH; RouterOS uses the maintained Ansible RouterOS API modules. The scope should expand only after representative live-device validation and with an out-of-band recovery path.

**AREDN is read-only integration/monitoring** for existing AREDN nodes via its documented sysinfo API; firmware and mesh configuration remain upstream/operator-owned.

## 4. Desktop and supporting infrastructure

HamStack now distinguishes operator desktops and general conference plumbing from
radio/application services.

Desktop roles include development workstations, conference controllers, generic
kiosks, CHIRP, and NetLogger. Infrastructure roles begin with Technitium DNS and
a deliberately minimal HTTP/iPXE netboot service.

The community DNS default is `hamstack.home.arpa`; DHCP and complex split-horizon
policy remain later/manual work until real deployments validate the network model.

## 5. Central service node ("brain")

A HamStack deployment may designate a higher-capacity node as a central service
host. This is a deployment pattern, not a special appliance image.

Likely services include:

- Gatus local status dashboard;
- Blur Deck media service for conference displays;
- CONHAM local/offline display;
- DCDash when an event uses it;
- Meshtastic Web dashboard;
- OpenHamClock;
- OpenWebRX where SDR placement permits;
- GNSS/chrony time service;
- local Cloudlog and/or Wavelog when wanted;
- event-local archives, status, and lightweight service discovery.

A Raspberry Pi 5 with durable storage or an amd64 mini-PC/laptop is a natural
reference platform. Edge radio nodes should remain replaceable and should not
need the central service node for their basic RF function.

## 6. Gatus status dashboard

Gatus is the default local HamStack status surface rather than a bespoke HamStack monitoring application. The role can derive basic node/service checks from inventory and accepts arbitrary native Gatus endpoints.

A future higher-level monitoring or super-console may aggregate one or more HamStack/Gatus deployments; the local role should not block that architecture.

## 7. Blur Deck and CONHAM display services

Blur Deck now uses ReadyMedia/MiniDLNA to publish operator-supplied video to Roku/DLNA clients. Media rendering remains outside the role.

CONHAM Display maintains an atomic last-known-good local mirror of conham.radio and serves it over HTTPS for HamCube/browser kiosk use when WAN connectivity is poor. Future work may consume the upstream Markdown source directly and may generate Roku-friendly presentation media, but the canonical content remains the upstream CONHAM project.

## 8. Meshtastic dashboard

The service role now deploys the official Meshtastic Web client container behind HTTPS. Device connection and application workflow remain upstream Meshtastic behavior.

## 9. Station and logging services

Cloudlog and Wavelog should remain independent, installable service roles.

HamStack's job is to make either platform reproducibly available on a suitable
service node with persistent storage, HTTPS, and normal service lifecycle. An
operator may instead use HRV's existing Cloudlog service, a personal external
Cloudlog/Wavelog instance, or both according to the upstream applications'
normal workflows.

HamStack does **not** need a bespoke logging federation, reconciliation daemon,
or QSO middleware. Import/export, API use, upstream synchronization, and
operator workflow should remain with Cloudlog/Wavelog unless a concrete future
need proves otherwise.

DCDash has a deployment role based on its current Python/Gunicorn/native-TLS service contract.

## 10. Appliance configuration translation

Treat appliance distributions as upstream products and translate HamStack
variables into their native configuration.

Roles are available for:

- **AllStarLink / ASL3** — node identity, native channel-driver selection,
  SimpleUSB/USBRadio baseline, HTTP registration, and service lifecycle;
- **WPSD** — baseline identity, modem selection, frequency/location, and radio
  mode enablement while leaving network/provider workflows in WPSD itself.

Both have been exercised on HRV reference hardware, but site-specific radio/audio
calibration and upstream account/provider workflows remain deployment responsibilities.
HamStack does not become an imaging framework for either project.

## 11. Event profiles and portability

Reusable deployment profiles currently provide starting compositions for:

- central-service-node / HamCube deployment;
- conference control station;
- development workstation.

Planned examples include a small neighborhood demo, a conference packet/BBS
stack, and offline-field or mixed ARM/amd64 deployments.

Profiles should contain no real credentials, private inventory, or event-only
callsigns that leak into generic role defaults.

## 12. Artifact resilience and local software archive

Add an optional `services/artifact-store` capability for software and images
that cannot be reliably fetched from upstream during deployment. The target is a
small, containerized, S3-compatible private object store suitable for a HamCube
or other central service node.

Initial requirements:

- persistent local storage and S3-compatible access;
- Vault-managed credentials and private-by-default buckets;
- versioned object naming plus operator-recorded checksums;
- storage for packages/AppImages, appliance images, ISOs, and firmware;
- no requirement for HA, replication, or lifecycle policy in the initial scope;
- artifact-consuming roles must continue to support controller-local files and
  explicit URLs when no artifact store exists.

A future common artifact-source abstraction may let roles select among a
controller-local file, explicit URL, or an object in the HamStack artifact
store. CHIRP and NetLogger are immediate examples of software whose upstream
delivery path can require operator-supplied artifacts. Garage is a candidate
implementation to evaluate, not yet a committed dependency.

## 13. Secret lifecycle helper

Reduce pointless operator work for credentials that exist only to connect one
managed service to another. A controller-side `hamstack-secrets` helper should
classify secrets as **generated**, **operator-supplied**, or **external**, then
manage the encrypted local Ansible Vault deliberately rather than asking humans
to invent database passwords.

Planned commands:

- `hamstack-secrets ensure` — generate strong random values for missing
  generative secrets and save them into the encrypted local Vault;
- `hamstack-secrets show <name>` — explicitly reveal one requested value;
- `hamstack-secrets rotate <name>` — explicit, service-aware rotation;
- `hamstack-secrets audit` — report required/missing secret names without
  revealing values.

Ordinary managed-host roles must **not** rewrite controller inventory or rotate
credentials behind the operator's back. Existing secrets are reused, generated
values are not printed during normal playbook runs, and rotation is always an
explicit action because changing a database credential without coordinating the
application would break the deployment. Operator-friendly credentials can still
be supplied manually where that is useful.
