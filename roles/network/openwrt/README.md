# `network/openwrt`

Rudimentary native UCI backend for OpenWrt-family network devices, including
GL.iNet routers where their firmware retains the normal OpenWrt UCI model.

The role is executed from the dedicated network-device inventory and does not
require Python on the router. It uses Ansible's raw SSH transport and native
`uci` commands.

Managed primitives:

- hostname;
- static logical LAN interfaces;
- dnsmasq DHCP pools;
- Wi-Fi AP/SSID settings;
- static IPv4 routes;
- simple firewall zones and zone forwarding;
- upstream DNS servers.

The model is deliberately conservative. It does not attempt to discover or
redesign vendor switch topology, DSA bridges, WAN/multi-WAN policy, or GL.iNet
web-UI-specific features. Operators must supply the correct existing device and
radio identifiers for their hardware.

`hamstack_network_extra_settings.uci_commands` is an escape hatch for native UCI
commands that have not yet earned first-class variables.

**Network configuration can disconnect Ansible.** Test on a spare router before
using it against production/event infrastructure.
