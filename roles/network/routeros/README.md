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
API-SSL on port 8729 with certificate validation enabled, so the controller
must trust the router's API-SSL certificate (for example by importing the
router's CA into the controller trust store or by issuing the router a
certificate from a CA the controller already trusts). Set
`hamstack_routeros_api_validate_certs: false` only for a deliberate
self-signed lab deployment; without validation an on-path attacker can capture
the RouterOS administrative credential. Put the password in Vault.

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
