# `voice/allstar`

Configures an **already-installed AllStarLink ASL3 system**. HamStack does not
build, image, or replace the upstream ASL appliance.

## Managed configuration model

For nodes using this role, HamStack is authoritative for the ASL3 configuration
files it owns. The role renders these files from static Jinja templates instead
of attempting to discover, edit, deduplicate, or migrate individual Asterisk
stanzas in place:

- `/etc/asterisk/modules.conf`
- `/etc/asterisk/extensions.conf`
- `/etc/asterisk/rpt.conf`
- `/etc/asterisk/simpleusb.conf`
- `/etc/asterisk/usbradio.conf`
- `/etc/asterisk/rpt_http_registrations.conf`
- `/etc/sa818.conf` when SA818 management is enabled

Ansible creates a backup whenever a managed file changes. A later HamStack run
will overwrite direct edits to the managed files.

### Manual/site-local changes

Do **not** hand-edit the managed files above. Put manual additions or overrides
in their corresponding custom include instead:

| Managed file | Manual/custom location |
| --- | --- |
| `rpt.conf` | `custom/rpt.conf` or `custom/rpt/*.conf` |
| `simpleusb.conf` | `custom/simpleusb.conf` or `custom/simpleusb/*.conf` |
| `usbradio.conf` | `custom/usbradio.conf` or `custom/usbradio/*.conf` |
| `extensions.conf` | `custom/extensions.conf` |
| `modules.conf` | `custom/modules.conf` |
| `rpt_http_registrations.conf` | `custom/rpt_http_registrations.conf` |

The templates load the custom includes **after** HamStack's managed node
configuration so site-local settings can extend or override the managed
baseline without being destroyed on the next run. HamStack creates the custom
include directories but does not modify files placed there.

If an ASL utility such as `simpleusb-tune-menu` writes calibration values into
a managed file, copy those values into HamStack variables or a custom include
before the next playbook run. Otherwise the managed template will restore the
configured HamStack values.

This is deliberately a cattle-style deployment model. A hand-built/multi-node
Asterisk configuration that must remain authoritative should not enable this
role until an explicit non-managed/overlay mode exists.

## Example

```yaml
hamstack_allstar_enabled: true
hamstack_allstar_callsign: N0CALL
hamstack_allstar_node_number: 123456
hamstack_allstar_duplex: 1

hamstack_allstar_channel_driver: simpleusb
hamstack_allstar_simpleusb_devstr: ""
hamstack_allstar_simpleusb_carrierfrom: usbinvert
hamstack_allstar_simpleusb_ctcssfrom: "no"

hamstack_allstar_register: true
```

Store the node password in Vault:

```yaml
vault_hamstack_allstar_node_password: "replace-me"
```

## Calibration boundary

HamStack can place known audio/tuning values into `simpleusb.conf`, but it does
**not** invent calibration data. Leave `rxmixerset`, `txmixaset`, and
`txmixbset` unset until the interface has been measured/tuned. ASL3 provides
`simpleusb-tune-menu` and `asl-find-sound` for that hardware-facing work.

When reproducing a known-good node, capture its per-node settings and express
them in host variables. For example:

```yaml
hamstack_allstar_simpleusb_devstr: ""
hamstack_allstar_simpleusb_rxmixerset: 600
hamstack_allstar_simpleusb_txmixaset: 500
hamstack_allstar_simpleusb_txmixbset: 500
hamstack_allstar_simpleusb_rxboost: "no"
hamstack_allstar_simpleusb_ctcssfrom: "no"
hamstack_allstar_simpleusb_settings:
  plfilter: "no"
```

An empty `devstr` intentionally leaves ASL3 free to auto-select a compatible
USB radio interface.

## Supported channel drivers

- `simpleusb`
- `usbradio` (generic stanza/settings pass-through)
- `hub` (`dahdi/pseudo`, no local radio interface)

Exactly one managed local node stanza is rendered. The stock ASL3 `1999` node
is not carried forward into managed configuration.

## SA818 / DRA818

Set `hamstack_allstar_sa818_enabled: true` to manage the upstream
`/etc/sa818.conf` values used by `sa818-menu`. Example:

```yaml
hamstack_allstar_sa818_enabled: true
hamstack_allstar_sa818_band: UHF
hamstack_allstar_sa818_bandwidth: Wide
hamstack_allstar_sa818_rx_frequency: "446.5000"
hamstack_allstar_sa818_tx_frequency: "446.5000"
hamstack_allstar_sa818_squelch: 1
hamstack_allstar_sa818_volume: 1
hamstack_allstar_sa818_tone: None
hamstack_allstar_sa818_port: /dev/ttyUSB0
hamstack_allstar_sa818_speed: 9600
```

When that saved configuration changes, HamStack runs `sa818-menu --apply` by
default so the module and the menu's saved values remain in sync. Set
`hamstack_allstar_sa818_apply: false` to manage the file without programming
hardware automatically.
