# `infrastructure/technitium-dns`

Deploys the official Technitium DNS Server container as HamStack infrastructure.

The role provides persistent configuration/log storage, DNS on TCP/UDP 53,
HTTPS administration with Technitium's self-signed TLS support, initial admin
credentials from Vault, recursive/forwarder bootstrap settings, an optional
primary local zone, and a HamStack-rendered RFC 1035 zone fragment for managed
service records.

The community-oriented default namespace is `hamstack.home.arpa`, following the
special-use home-network namespace defined by RFC 8375. Both the server name and
zone are variables.

When `hamstack_technitium_dns_manage_zonefile` is enabled, the role renders a
zone fragment under the Technitium data directory and imports it with
Technitium's authoritative-zone API. By default it creates A records for enabled
local HamStack services whose configured TLS hostname belongs to the managed
zone, plus the Technitium server name itself. Automatic records point to the host's default interface address unless
`hamstack_technitium_dns_auto_address` overrides it.

Additional records can be declared directly:

```yaml
hamstack_technitium_dns_records:
  - name: files
    type: A
    value: 192.168.73.20
    ttl: 300
  - name: docs
    type: CNAME
    value: files.hamstack.home.arpa.
```

The import overwrites matching record sets but does not wipe unrelated/manual
records from the zone. DHCP, split-horizon policy, complex views/apps, and
record deletion/reconciliation remain later work.

Required Vault value:

```yaml
vault_hamstack_technitium_admin_password: 'use-a-real-secret'
```

Upstream: https://technitium.com/dns/
