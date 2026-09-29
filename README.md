# HamStack

**HamStack** is an open-source Ham Radio Village (HRV) project for building
reproducible amateur-radio, conference, station, and lab infrastructure with
Ansible.

It is intentionally hardware-flexible. A deployment may use Raspberry Pis, x86
mini-PCs, laptops, upstream appliance images, travel routers, or other
appropriate systems.

The core contract is simple:

> Give HamStack a reachable machine and describe what that machine should do.

HamStack grew out of Ham Radio Village conference infrastructure and DEF CON
experiments with packet radio, SSTV, AllStar, 44Net, local services, displays,
and interactive radio demos. The reference deployment is a test bed, not a
hardware prescription.

## Start here

If this is your first time seeing HamStack:

1. Read the [feature overview](FEATURES.md).
2. Read [Getting started](docs/getting-started.md).
3. If the terminology is unfamiliar, read [HamStack concepts](docs/concepts.md).
4. Try the [one-node first deployment](docs/first-deployment.md).
5. Use [role status](docs/role-status.md) to understand current implementation
   and validation limits.

Additional background:

- [Project history](docs/history.md)
- [Architecture](docs/architecture.md)
- [Reference hardware](docs/hardware.md)
- [Deployment profiles](docs/profiles.md)
- [Roadmap](ROADMAP.md)

## What HamStack does

HamStack provides composable roles for radio applications, packet/BBS systems,
voice/hotspot appliances, shared conference services, station displays,
operator workstations, DNS/netboot infrastructure, and selected network
devices.

Examples include Graywolf, APRS, LinBPQ, Pat/Winlink, AllStarLink, WPSD,
FLDIGI/FLRIG/WSJT-X/JS8Call, SSTV, CHIRP, OpenWebRX, OpenHamClock, DCDash,
Gatus, Cloudlog/Wavelog, CONHAM mirroring, Technitium DNS, 44Net Connect,
OpenWrt/GL.iNet, and RouterOS.

See [FEATURES.md](FEATURES.md) for the current capability and maturity matrix.

## What HamStack is not

HamStack generally does **not** provide custom appliance images.

For normal Linux roles, install a supported operating system, make networking
and SSH work, and HamStack begins there. For upstream appliances such as WPSD
or AllStarLink, install the supported upstream image first and let HamStack
configure the portion it owns.

HamStack also does not try to replace every upstream application's own UI or
workflow. A role should automate the stable, repeatable infrastructure boundary
and leave product-specific operator workflows upstream when that is the safer
choice.

## Project status

HamStack v0.1.x is an **alpha-quality public release line**. The repository contains
deployable roles across radio, packet, service, desktop, infrastructure, and
network-device families, and representative HRV Raspberry Pi and x86 deployment paths
have been exercised on real hardware.

Alpha does not mean every radio, interface, router, or appliance combination is
certified. Site-specific audio calibration, device mapping, application preferences,
frequencies, talkgroups, credentials, and other operator settings may still require
manual adjustment. HamStack treats those boundaries as part of the public contract
rather than hiding them behind speculative automation.

The baseline rule remains deliberately boring: start from the role's documented
upstream state, apply it, verify the capability, and run it again to investigate
unexpected changes. Current implementation boundaries are tracked in
[docs/role-status.md](docs/role-status.md), and the validation workflow is in
[docs/qa.md](docs/qa.md). See [RELEASE_NOTES.md](RELEASE_NOTES.md) for the current
release summary and [CHANGELOG.md](CHANGELOG.md) for version history.

## Role layout

A role does not necessarily install the upstream project it configures.

For example, the `wpsd` role assumes a supported WPSD image has already been installed and is reachable. The role then configures that node for use as part of a HamStack deployment. Other roles may install software when installation is naturally part of that role.

Each role should document its supported starting state.


## Role families

HamStack keeps different operational concerns separate:

- `desktop/` — operator/developer workstations and kiosk/presentation clients;
- `digital/` — radio-mode applications, signaling/decoding workflows, and related operator tools;
- `infrastructure/` — non-radio deployment plumbing such as DNS and netboot;
- `network/` — 44Net and network-device/integration backends;
- `packet/` — packet/APRS/BBS/Winlink capabilities;
- `services/` — shared web/data/event services;
- `visual/` — displays and tools that visualize station, receiver, propagation, telemetry, or other amateur-radio data;
- `voice/` — AllStar/WPSD voice-digital appliance configuration.

Deployment profiles compose these roles without turning a machine identity such
as HamCube into a mega-role.

## Requirements

For the first supported path:

- Linux control host with Ansible
- A target Linux system reachable through SSH
- Python available on normal Linux targets (network appliances use their platform-native transport)
- Privilege escalation (`sudo`) where required

Clone the canonical repository, then install controller dependencies and Ansible
collections:

```bash
git clone https://github.com/HamRadioVillage/HamStack.git
cd HamStack
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-controller.txt
ansible-galaxy collection install -r requirements.yml
```

Contributors can install the superset of QA/development tools instead:

```bash
python -m pip install -r requirements-dev.txt
```

## Bootstrap a target node

A freshly installed target may need Python, SSH, sudo, and an automation account before Ansible can manage it. HamStack includes a small idempotent bootstrap script for supported Debian-family systems.

From a checked-out copy on the target:

```bash
sudo bash ./scripts/bootstrap-node.sh --copy-key-from "$USER"
```

For the v0.1.0 release, the bootstrap can also be fetched from the canonical GitHub
repository. Pinning the release tag avoids executing a moving branch as root:

```bash
curl -fsSL https://raw.githubusercontent.com/HamRadioVillage/HamStack/v0.1.0/scripts/bootstrap-node.sh | sudo bash
```

See [docs/bootstrap.md](docs/bootstrap.md) for SSH-key options, the safer inspect-then-run workflow, passwordless-sudo behavior, and appliance-image caveats.


## Bootstrap a control or development workstation

When a Debian-family workstation already has an unpacked HamStack source tree,
bootstrap its local controller environment with:

```bash
bash ./scripts/bootstrap-workstation.sh --mode controller
# or
bash ./scripts/bootstrap-workstation.sh --mode dev
```

The script creates the repository-local virtual environment and installs the
matching Python requirements and Ansible collections. It deliberately does not
clone, pull, push, or otherwise own a Git workflow. See
[docs/bootstrap.md](docs/bootstrap.md).

## Quick start

The easiest first-run path is the interactive configurator:

```bash
python3 ./scripts/configure.py
```

It can create `inventory/local/`, configure site identity, add hosts, register
shared hardware, enable roles, and launch Ansible Vault for secrets.

The non-interactive inventory initializer remains available:

```bash
bash ./scripts/init-local-inventory.sh
```

Or manually:

```bash
cp -R inventory/example inventory/local
```

Then edit:

- `inventory/local/hosts.yml` for your real hosts;
- `inventory/local/group_vars/all.yml` for site-wide identity and defaults;
- `inventory/local/group_vars/all/vault.yml` for encrypted site secrets;
- `inventory/local/host_vars/<hostname>.yml` for attached hardware and per-node role settings.

`inventory/local/` is ignored by Git.

Test connectivity:

```bash
ansible all -m ping
```

Apply the baseline:

```bash
ansible-playbook playbooks/bootstrap.yml
```

Run it a second time. A healthy baseline should complete without failures and without unnecessary changes.

Apply the roles enabled in your local inventory:

```bash
ansible-playbook playbooks/site.yml
```

See [docs/configuration.md](docs/configuration.md) for the HamStack configuration schema, shared hardware-resource model, role variables, and Vault variable names.

## Configuration and secrets

HamStack's public variable vocabulary is documented in [docs/configuration.md](docs/configuration.md).

Do not commit passwords, API keys, private keys, callsign credentials, node passwords, or other secrets. Real deployment data belongs under the gitignored `inventory/local/` tree, and credentials should be stored in an encrypted `inventory/local/group_vars/all/vault.yml` created with Ansible Vault.

## Containerized LAN services

HamStack containerized web services are designed not to publish their upstream plaintext HTTP listeners directly onto an event LAN. Current OpenHamClock and OpenWebRX roles use a Caddy sidecar with an internal CA and publish HTTPS only; the application port remains on a private Docker network.

LinBPQ's variable model was derived from a real multi-band conference deployment, but the tracked defaults and examples are intentionally site-neutral.

## Deployment profiles

HamStack roles are composable capabilities. Thin deployment profiles for a
central HamCube/service node, conference control station, and development
workstation live under `playbooks/profiles/`. See
[docs/profiles.md](docs/profiles.md).

## Network devices

Routers and network appliances use a separate inventory and playbook so they do
not receive ordinary Linux-node roles. Conservative backends exist for GL.iNet/OpenWrt and MikroTik RouterOS; validate
changes on spare hardware and keep an out-of-band recovery path before using them for
an event cutover:

```bash
ansible-playbook -i inventory/local/network.yml playbooks/network.yml
```

See [docs/network-devices.md](docs/network-devices.md).

## Radio responsibility

HamStack configures software and systems. Operators and deploying organizations remain responsible for ensuring that transmitting equipment is operated lawfully and appropriately for their jurisdiction, license privileges, band plans, and event environment.

## Role implementation status

See [docs/role-status.md](docs/role-status.md) for the current implementation matrix,
validation notes, and intentionally operator-owned functionality.


## Development QA

Before handing a branch to another operator or starting hardware validation, run:

```bash
python3 scripts/qa.py
yamllint .
ansible-lint
```

The fast QA script checks YAML/Jinja/Python/shell syntax, local Markdown links, role/documentation consistency, deprecated inventory paths, and whether the generated complete variable index is current. See [docs/qa.md](docs/qa.md) for the static and live-validation workflow.

## Community and contact

HamStack is developed for and maintained with the Ham Radio Village community.
The canonical public repository, issue tracker, feature-request workflow, and
pull requests are hosted through the **Ham Radio Village GitHub organization**.

Bug reports, feature requests, documentation improvements, hardware support,
new roles, and pull requests are welcome.

For general project questions or coordination, the preferred contact is
**`@shoot3r` on the HRV Discord**.

See [CONTRIBUTING.md](CONTRIBUTING.md) before making a substantial change or
adding a new role.

## Security

Please do not post credentials, private deployment information, or exploitable
details in a public issue. See [SECURITY.md](SECURITY.md) for the reporting
process.

## License

HamStack is free software licensed under the **GNU General Public License,
version 3 (GPLv3)**. Commercial use, consulting, hosting, tested/prebuilt
deployments, and other paid services are permitted subject to the GPLv3 terms.

See [LICENSE](LICENSE) for the complete license text.

For details on the interactive setup helper, see
[docs/configurator.md](docs/configurator.md).
