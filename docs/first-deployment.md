# First deployment example: one node with Gatus

This walkthrough intentionally does something boring.

The goal is not to build a complete conference stack. It is to prove the
controller, inventory, target bootstrap, container runtime, role execution, and
idempotency path with one small service.

The example deploys Gatus to a Debian-family target.

## Example layout

```text
controller laptop
    |
    | SSH / Ansible
    v
hamstack-demo
    |
    +-- common baseline
    +-- Gatus
```

Assumptions used below:

```text
target hostname: hamstack-demo
target address: 192.168.50.25
Ansible user: hamstack
site callsign: N0CALL   <-- replace this
timezone: America/Chicago
```

Use values appropriate for your station.

## 1. Prepare the controller

From the unpacked HamStack repository:

```bash
bash ./scripts/bootstrap-workstation.sh --mode controller
source .venv/bin/activate
```

Create the local inventory:

```bash
python3 scripts/configure.py --init
```

## 2. Configure the target host

Edit `inventory/local/hosts.yml`:

```yaml
---
all:
  hosts:
    hamstack-demo:
      ansible_host: 192.168.50.25
      ansible_user: hamstack
```

Rename the example host-variable file:

```bash
mv inventory/local/host_vars/example-node.yml \
   inventory/local/host_vars/hamstack-demo.yml
```

For this demonstration, replace the contents of that host-variable file with:

```yaml
---
hamstack_manage_hostname: true
hamstack_hostname: hamstack-demo

hamstack_devices: {}
hamstack_radios: {}

hamstack_gatus_enabled: true
hamstack_gatus_tls_host: hamstack-demo
hamstack_gatus_https_port: 8443
```

Edit `inventory/local/group_vars/all.yml` and set at least:

```yaml
hamstack_site_name: My HamStack
hamstack_callsign: YOURCALL
hamstack_timezone: America/Chicago
```

Replace `YOURCALL` with your real callsign where one is appropriate for your
deployment.

## 3. Bootstrap the target

Install your controller SSH public key on the target through
`scripts/bootstrap-node.sh`.

For example, if your controller key is:

```text
ssh-ed25519 AAAA... operator@example
```

run on the target:

```bash
sudo bash ./scripts/bootstrap-node.sh \
  --authorized-key "ssh-ed25519 AAAA... operator@example"
```

## 4. Confirm SSH and Ansible

From the controller:

```bash
ssh hamstack@192.168.50.25
ansible all -m ping
```

Do not proceed until both work reliably.

## 5. Apply the common baseline

```bash
ansible-playbook playbooks/bootstrap.yml
```

Then immediately run it again:

```bash
ansible-playbook playbooks/bootstrap.yml
```

Investigate unexpected changes or failures before continuing.

## 6. Deploy Gatus

Run:

```bash
ansible-playbook playbooks/site.yml
```

The Gatus role installs the shared HamStack container runtime as needed,
generates its configuration, and exposes Gatus through HTTPS.

Open:

```text
https://192.168.50.25:8443/
```

The role uses an internally generated certificate. Your browser may
need to trust/accept the local certificate according to your environment.

## 7. Run the play again

```bash
ansible-playbook playbooks/site.yml
```

The second run is important. A role that continually reports changes without an
underlying configuration change needs investigation.

## 8. Add the next capability

Once the simple path works, enable one additional role and repeat the process.

Good next steps include:

- `visual/openhamclock`;
- `services/conham-display`;
- `packet/graywolf` on suitable hardware;
- one of the deployment profiles.

Do not enable ten unrelated services at once during your first troubleshooting
session.

## What this example proved

If the walkthrough succeeds, you have exercised:

- controller setup;
- private inventory;
- SSH automation account;
- privilege escalation;
- common baseline;
- Ansible collections;
- Docker/container runtime;
- one real HamStack role;
- a second idempotency run.

That is the foundation for the more interesting radio work.
