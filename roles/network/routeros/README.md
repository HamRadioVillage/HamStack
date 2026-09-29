# `network/routeros`

MikroTik RouterOS backend using the maintained
`community.routeros` API modules from the Ansible ecosystem. The API path is
chosen over fragile screen/CLI parsing so changes can be structured and
idempotent.

The common-model translation covers:

- system identity;
- managed IP addresses;
- static routes;
- DNS resolver servers.

`hamstack_routeros_native_paths` exposes the same structured API mechanism for
additional RouterOS paths (bridges, DHCP, legacy wireless/wifi, firewall, etc.)
without HamStack prematurely pretending those are identical across every
RouterOS generation. That is particularly relevant to the hAP ac lite and the
RouterOS wireless/wifi package transition.

Prerequisites on the Ansible controller:

- `community.routeros` collection (in `requirements.yml`);
- `librouteros` (in `requirements-controller.txt`).

The router must have the RouterOS API enabled. The default role settings use
API-SSL on port 8729 with certificate validation disabled for lab/event
self-signed deployments. Put the password in Vault.

HamStack translates the common `address`, `interface`/`device`, `target`, `gateway`, `name`, and optional `comment` fields into RouterOS-native address/route entries. Example:

```yaml
hamstack_network_lans:
  - address: 10.73.10.1/24
    interface: bridge
    name: management

hamstack_network_routes:
  - name: 44net
    target: 44.0.0.0/9
    gateway: 10.73.10.254
    comment: hamstack:44net
```

This is intentionally rudimentary network-device support, not a claim that
HamStack can yet regenerate an arbitrary MikroTik from factory defaults.
