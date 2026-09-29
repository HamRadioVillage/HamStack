# HamStack concepts

You do not need to understand the entire repository before using HamStack. Five
ideas explain most of it.

## Controller

The **controller** is the computer that runs Ansible.

This is normally a laptop or mini-PC used by the operator or lead volunteer.
The controller has the HamStack source tree and your private inventory. It
connects to managed Linux nodes over SSH and to supported network appliances
through their platform-specific management interface.

Ansible normally does **not** run on every radio node.

## Node

A **node** is a computer or appliance that provides one or more HamStack
capabilities.

Examples:

- a Raspberry Pi running Graywolf and LinBPQ;
- a Pi running SSTV;
- a pre-imaged WPSD hotspot;
- a HamCube central service/display node;
- an x86 mini-PC running shared services.

A node's hostname or model does not determine its job. Inventory does.

## Role

A **role** represents one capability.

Examples:

```text
packet/graywolf
services/gatus
visual/openwebrx
voice/allstar
desktop/chirp
```

Roles are intentionally composable. One computer may run several roles when
that combination makes operational sense.

A role does not necessarily install an upstream operating system or appliance.
For example, the WPSD role expects a supported WPSD image to already exist.

## Resource

A **resource** is physical or logical hardware that roles may share.

Examples:

```text
AIOC
DigiRig
radio
GPS/PPS receiver
RTL-SDR
camera
USB foot pedal
serial port
audio interface
```

Resources live primarily in host inventory. A radio application can refer to a
named resource instead of hard-coding `/dev/ttyUSB0` everywhere.

## Profile

A **profile** is a useful composition of roles for a recognizable deployment
shape.

Current examples include:

- HamCube;
- conference control station;
- development workstation.

Profiles provide a baseline, not a law. Inventory variables can change or
disable individual components.

## Inventory

Your inventory is the description of **your** HamStack deployment.

Real deployment data belongs under:

```text
inventory/local/
```

That tree is ignored by Git.

The common split is:

```text
inventory/local/hosts.yml
    Which Linux nodes exist and how Ansible reaches them.

inventory/local/group_vars/all.yml
    Site-wide defaults such as callsign, timezone, event name.

inventory/local/host_vars/<hostname>.yml
    Hardware resources and role settings for one node.

inventory/local/group_vars/all/vault.yml
    Encrypted credentials/secrets when required.

inventory/local/network.yml
    Routers/network appliances managed through the network playbook.
```

## Upstream software boundary

HamStack is configuration/deployment automation, not a replacement for every
upstream project it uses.

Depending on the role, HamStack may:

- install a package;
- deploy a container;
- configure an already-installed application;
- configure a pre-imaged appliance;
- expose a conservative baseline and leave advanced application workflow to the
  upstream UI.

Each role README documents its boundary.

## Controller versus HamCube

These are deliberately different jobs.

**Control station**

- privileged operator workstation;
- holds the HamStack tree and private inventory;
- runs Ansible;
- used by the lead operator to change the deployment.

**HamCube / central service node**

- provides shared services and displays;
- can run Gatus, CONHAM, Blur Deck, DNS, OpenHamClock, and similar roles;
- should continue doing its service job without an operator sitting at it.

The central service node is useful, but edge RF nodes should remain as
independent as practical.

## Implementation status

HamStack distinguishes repository implementation from field validation.

**Implemented** means code exists, static QA passes, and the role has a defined
automation boundary.

It does **not** mean every combination of hardware and upstream version has been
certified. See [`qa.md`](qa.md) and [`role-status.md`](role-status.md).
