# Bootstrapping a HamStack node

HamStack normally begins after a machine has a supported operating system, working networking, and SSH reachability. A freshly installed system may still be missing the small set of components Ansible needs.

`scripts/bootstrap-node.sh` primes that system.

## What the bootstrap does

Bootstrap v0.1 currently targets Debian-family systems that use `apt`.

It:

- installs `python3`, `python3-apt`, `sudo`, `openssh-server`, and `ca-certificates` when missing;
- creates or reuses a dedicated `hamstack` automation account;
- adds that account to the `sudo` group;
- grants the account passwordless sudo by default;
- installs an SSH public key when one is supplied or available from the invoking sudo user;
- enables and starts the SSH server;
- records bootstrap metadata in `/etc/hamstack/bootstrap`.

It does **not** install Ansible on the target. Ansible runs from the HamStack control machine.

It also does not alter `PasswordAuthentication`, `PermitRootLogin`, firewall policy, hostname, networking, or application configuration.

The script is intended to be idempotent and may be run more than once.

## From a checked-out repository

On the target node:

```bash
sudo bash ./scripts/bootstrap-node.sh --copy-key-from "$USER"
```

If the account you are currently using already has the SSH public key that the HamStack control machine will use, this is the simplest path.

## Curl bootstrap

A published release can be run directly from GitHub. Prefer a release-tag or commit-pinned URL rather than a moving branch:

```bash
curl -fsSL https://raw.githubusercontent.com/HamRadioVillage/HamStack/v0.1.0/scripts/bootstrap-node.sh \
  | sudo bash
```

When invoked through `sudo`, the script automatically attempts to copy the invoking user's existing `~/.ssh/authorized_keys` into the `hamstack` account.

To explicitly provide a public key:

```bash
curl -fsSL https://raw.githubusercontent.com/HamRadioVillage/HamStack/v0.1.0/scripts/bootstrap-node.sh \
  | sudo bash -s -- \
      --authorized-key 'ssh-ed25519 AAAA... operator@example'
```

Or copy keys from a specific existing account:

```bash
curl -fsSL https://raw.githubusercontent.com/HamRadioVillage/HamStack/v0.1.0/scripts/bootstrap-node.sh \
  | sudo bash -s -- --copy-key-from pi
```

For a published release, prefer a URL pinned to a release tag or commit rather than a moving branch.

## Safer inspect-then-run workflow

`curl | sudo bash` is convenient, but it executes whatever the URL serves with root privileges. Operators who want to inspect the script first should use:

```bash
curl -fsSL https://raw.githubusercontent.com/HamRadioVillage/HamStack/v0.1.0/scripts/bootstrap-node.sh \
  -o /tmp/hamstack-bootstrap.sh

less /tmp/hamstack-bootstrap.sh

sudo bash /tmp/hamstack-bootstrap.sh --copy-key-from "$USER"
```

## Automation account

The default automation account is:

```text
hamstack
```

Choose another account with:

```bash
sudo bash ./scripts/bootstrap-node.sh --user ansible
```

or:

```bash
curl -fsSL https://raw.githubusercontent.com/HamRadioVillage/HamStack/v0.1.0/scripts/bootstrap-node.sh \
  | sudo bash -s -- --user ansible
```

The inventory must use the same account:

```yaml
all:
  hosts:
    example-node:
      ansible_host: 192.0.2.10
      ansible_user: hamstack
```

## Passwordless sudo

HamStack grants the automation account passwordless sudo by default because many roles need privilege escalation and unattended automation should not require an interactive password.

To opt out:

```bash
sudo bash ./scripts/bootstrap-node.sh --no-passwordless-sudo
```

HamStack will remove the sudoers file that this bootstrap script manages. The operator must then configure an alternative Ansible become method.

The managed sudoers file is:

```text
/etc/sudoers.d/90-hamstack-ansible
```

## SSH keys

The bootstrap supports three explicit methods:

```text
--authorized-key "PUBLIC_KEY"
--authorized-key-file /path/to/file
--copy-key-from USER
```

If none is specified and the script was invoked using `sudo`, it tries to copy the invoking user's existing `authorized_keys`.

The script never generates a private key and never copies a private key to the target.

## Appliance images

Some HamStack roles target upstream appliance-style distributions such as WPSD or AllStarLink. Those roles may have their own supported starting-state requirements.

Do not assume this generic bootstrap is appropriate for every appliance image. Follow the role's README when an upstream image has special filesystem, user-management, or package-management behavior.

## After bootstrapping

On the HamStack control machine:

```bash
bash ./scripts/init-local-inventory.sh
```

Edit `inventory/local/hosts.yml`, then verify connectivity:

```bash
ansible all -m ping
```

Finally:

```bash
ansible-playbook playbooks/bootstrap.yml
```

At that point the machine is under HamStack management and the regular Ansible roles take over.

## Workstation bootstrap

For a Debian-family development or control workstation that already has an
unpacked HamStack tree, run:

```bash
bash ./scripts/bootstrap-workstation.sh --mode controller
# or
bash ./scripts/bootstrap-workstation.sh --mode dev
```

This creates the repository `.venv`, installs the matching requirements and
Ansible collections, and prints the local profile command. It deliberately does
not clone or update the repository.
