# Interactive configurator

`scripts/configure.py` is a small terminal-menu helper for creating and editing
a local HamStack inventory after cloning the repository.

It is intentionally **not** a second configuration system. The YAML files under
`inventory/local/` remain authoritative; the configurator simply writes those
same documented variables.

## Start

```bash
python3 scripts/configure.py
```

On first run it copies `inventory/example/` to `inventory/local/`.

The menu can then:

- configure site identity and localization;
- add/edit/remove inventory hosts;
- register shared hardware resources such as AIOCs, DigiRigs, cameras, GPS
  devices, HID triggers, and RTL-SDRs;
- register radios and associate them with shared interfaces;
- discover HamStack roles from their `defaults/main.yml` files;
- enable/disable roles per host;
- edit simple role variables or enter complex values as inline YAML;
- create/edit the site Ansible Vault;
- perform local consistency checks.

## Non-interactive helpers

Create only the local inventory:

```bash
python3 scripts/configure.py --init
```

Validate an existing local inventory:

```bash
python3 scripts/configure.py --validate
```

When Ansible is available and no encrypted Vault would require an interactive
password, validation also attempts `ansible-playbook --syntax-check`.

## Secrets

The configurator never attempts to parse an encrypted Vault itself.

When asked to create one, it copies the tracked secret-variable template to:

```text
inventory/local/group_vars/all/vault.yml
```

and immediately invokes `ansible-vault encrypt`. If encryption fails, the
temporary plaintext Vault file is deleted.

Existing Vaults are opened with `ansible-vault edit`.

## Advanced configuration

The menu is intended to make the common path approachable, not to hide YAML.
Every generated file can be edited normally afterward.

For nested or unusual role variables, either enter an inline YAML value in the
role-variable editor or edit the host/site variable file directly and use
[configuration.md](configuration.md) as the reference.

## Network devices

The configurator maintains routers separately from ordinary Linux nodes. The
**Network devices** menu writes `inventory/local/network.yml` and currently
supports the `openwrt` and `routeros` platform labels.

Both backends have deliberately conservative implementations. The
menu exists to create the separate network-device inventory; operators can then
apply it with `playbooks/network.yml` and edit the YAML directly for advanced
settings. Validate network changes on spare hardware before event cutover.
