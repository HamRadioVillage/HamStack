# Getting started with HamStack

This is the shortest supported path from "I downloaded HamStack" to "Ansible is
managing a node."

If you are new to Ansible, the important idea is that HamStack normally runs
from one **controller** computer and connects to one or more **target nodes**.

## What you need

For the easiest first deployment:

- a Debian-family Linux controller or workstation;
- an unpacked copy of the HamStack repository on that controller;
- a Debian-family target such as a Raspberry Pi, mini-PC, VM, or laptop;
- working IP networking between the controller and target;
- an SSH public key from the controller;
- sudo/root access on the target for initial bootstrap.

Some roles support other operating systems or upstream appliances. Start with
ordinary Debian-family Linux while learning the layout.

## 1. Prepare the controller

From the unpacked HamStack directory:

```bash
bash ./scripts/bootstrap-workstation.sh --mode controller
```

This installs the local controller prerequisites, creates a repository-local
Python virtual environment, installs the controller Python dependencies, and
installs the required Ansible collections.

It does **not** clone, pull, commit, or push Git repositories.

Activate the environment when working with HamStack:

```bash
source .venv/bin/activate
```

## 2. Create your local inventory

Run the interactive configurator:

```bash
python3 scripts/configure.py --init
python3 scripts/configure.py
```

Or copy the example inventory manually:

```bash
cp -R inventory/example inventory/local
```

Real deployment configuration belongs under `inventory/local/`, which is
ignored by Git.

At minimum:

1. replace `example-node` in `inventory/local/hosts.yml`;
2. set the node's real IP address or DNS name;
3. rename `inventory/local/host_vars/example-node.yml` to match your hostname;
4. set your callsign and timezone in
   `inventory/local/group_vars/all.yml`;
5. enable the role(s) you actually want in that host's variables.

Do not enable every role just because it exists.

## 3. Bootstrap a fresh target

The target needs Python, SSH, sudo, and an account Ansible can use.

On the controller, display your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

If you use another key, substitute that file.

On the target, from an unpacked HamStack copy:

```bash
sudo bash ./scripts/bootstrap-node.sh \
  --authorized-key "ssh-ed25519 AAAA...your-controller-key..."
```

The default automation account is `hamstack`.

The bootstrap script deliberately does not change firewall policy, disable
password authentication, install Ansible on the target, or configure any radio
software.

See [`bootstrap.md`](bootstrap.md) for other key-install options.

## 4. Test connectivity

Back on the controller:

```bash
ansible all -m ping
```

If this fails, solve SSH/inventory connectivity before running larger
playbooks.

Useful direct test:

```bash
ssh hamstack@<target-address>
```

## 5. Apply the common baseline

Run:

```bash
ansible-playbook playbooks/bootstrap.yml
```

Run it a second time:

```bash
ansible-playbook playbooks/bootstrap.yml
```

A healthy second run should have no failures and should not report unnecessary
changes.

## 6. Apply enabled roles

Once your host variables enable the desired capabilities:

```bash
ansible-playbook playbooks/site.yml
```

Again, run it a second time while validating a new deployment.

## 7. Secrets

If a role needs credentials, create an encrypted Vault:

```bash
ansible-vault create inventory/local/group_vars/all/vault.yml
```

The tracked example at:

```text
inventory/example/group_vars/all/vault.yml.example
```

shows the secret variable names HamStack currently knows about.

Never commit real passwords, API keys, node passwords, private keys, or private
deployment inventory.

## 8. Network appliances

OpenWrt/GL.iNet and RouterOS devices use a separate inventory:

```text
inventory/local/network.yml
```

Apply those with:

```bash
ansible-playbook -i inventory/local/network.yml playbooks/network.yml
```

These backends are intentionally conservative implementations. Test
on spare hardware before changing an event router.

## 9. Deployment profiles

If your machine matches one of the standard deployment shapes, you can start
with a profile:

```text
playbooks/profiles/hamcube.yml
playbooks/profiles/control-station.yml
playbooks/profiles/dev-workstation.yml
```

Profiles provide sensible defaults and remain overrideable through inventory.

See [`profiles.md`](profiles.md).

## 10. Validate the repository

Before sharing changes or starting a hardware-validation cycle:

```bash
python3 scripts/qa.py
yamllint .
ansible-lint
```

See [`qa.md`](qa.md) for the distinction between static QA and live-device
validation.

## Where to go next

- [`../FEATURES.md`](../FEATURES.md) — what HamStack can do;
- [`concepts.md`](concepts.md) — terminology and architecture;
- [`first-deployment.md`](first-deployment.md) — a small worked example;
- [`configuration.md`](configuration.md) — public configuration model;
- [`variables.md`](variables.md) — exhaustive generated variable reference;
- [`hardware.md`](hardware.md) — reference hardware/capability guidance;
- [`role-status.md`](role-status.md) — implementation boundaries;
- [`../ROADMAP.md`](../ROADMAP.md) — future direction.

## Help and project contact

HamStack is an open-source Ham Radio Village project. The canonical public
repository, issues, feature requests, and pull requests are maintained through
the HRV GitHub organization.

Feature requests, bug reports, documentation improvements, hardware support,
and pull requests are welcome.

For general project questions or coordination, the preferred contact is
**`@shoot3r` on the Ham Radio Village Discord**.
