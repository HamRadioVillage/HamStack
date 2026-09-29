# Network-device support

HamStack treats routers and network appliances separately from normal Linux
radio nodes.

The supported backends are:

- `openwrt` — OpenWrt-family systems, including GL.iNet travel routers;
- `routeros` — MikroTik RouterOS, including the hAP ac lite reference device.

Both have deliberately conservative backends. OpenWrt uses native UCI over raw SSH; RouterOS uses the maintained `community.routeros` API modules. Test on spare hardware and keep an out-of-band recovery path before relying on either for event cutover.

## Separate inventory

Do not place router appliances in the normal `inventory/local/hosts.yml`.
Doing so would make the Linux `site.yml` play try to apply `common` and other
node roles to a router.

Network devices live in:

```text
inventory/local/network.yml
```

Example:

```yaml
all:
  children:
    network_devices:
      hosts:
        event-router:
          ansible_host: 192.168.8.1
          ansible_user: root
          hamstack_network_platform: openwrt
          hamstack_network_vendor: glinet
          hamstack_network_model: travel-router

        event-mikrotik:
          ansible_host: 192.168.88.1
          ansible_user: hamstack
          hamstack_network_platform: routeros
          hamstack_network_vendor: mikrotik
          hamstack_network_model: hAP ac lite
```

The interactive configurator can create this inventory.

Apply the network inventory with:

```bash
ansible-playbook -i inventory/local/network.yml playbooks/network.yml
```

## Common logical model

Where practical, HamStack should expose the same logical vocabulary to both
backends:

```yaml
hamstack_network_hostname: event-router

hamstack_network_lans:
  - name: radio
    address: 10.73.20.1/24
    device: br-radio
    dhcp:
      enabled: true
      start: 100
      limit: 100

hamstack_network_wifi:
  - ssid: HRV
    network: radio
    security: wpa2

hamstack_network_routes: []
hamstack_network_firewall_zones: []
```

The backend then translates that model into platform-native configuration.
Platform-specific escape hatches can exist when the common model is
insufficient.

## Backend direction

### OpenWrt / GL.iNet

The implementation should configure the underlying OpenWrt system using native
UCI/ubus/service primitives rather than automating the vendor web UI.

GL.iNet-specific behavior may require explicit compatibility handling, but the
backend should remain useful for generic OpenWrt where practical.

### MikroTik RouterOS

The implementation should use RouterOS-native automation rather than treating
the router like a generic Debian machine. The hAP ac lite is a reference target.

## Current supported scope

The OpenWrt backend directly translates a conservative UCI subset: hostname,
static interfaces, DHCP pools, Wi-Fi AP definitions, DNS forwarders, static
routes, and simple firewall zones/forwardings. It deliberately does not try to
discover or redesign a device's DSA/switch topology, so the operator supplies
the actual interface/radio identifiers for the target router.

The RouterOS backend directly manages identity, HamStack-tagged IP addresses,
HamStack-tagged static routes, and DNS. Additional RouterOS-native paths can be
provided through `hamstack_routeros_native_paths`; this is the intended
native-path escape hatch for DHCP, bridges/VLANs, Wi-Fi, and firewall policy
until those common-model translations have been validated across RouterOS
versions and both legacy wireless and newer Wi-Fi stacks.

RouterOS API modules execute on the Ansible controller and require
`librouteros`, supplied by `requirements-controller.txt`. API-SSL on port 8729
is the default HamStack connection model.

Both backends can change the management network underneath the active Ansible
session. Test on spare hardware and keep a recovery path. Advanced policy
routing, multi-WAN, captive portals, mesh control, and elaborate firewall mangle
rules remain later work. AREDN monitoring exists separately; AREDN firmware and
mesh configuration remain outside the current automation boundary.
