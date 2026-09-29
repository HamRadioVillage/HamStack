# `voice/wpsd`

Configures the baseline identity/radio settings of an **already-imaged WPSD
system**. HamStack does not download or flash WPSD.

This role intentionally follows WPSD's appliance boundary. The operator first
writes a supported WPSD image, boots it, gets networking/SSH working, and then
HamStack can apply a reproducible initial baseline.

The public WPSD manual documents the initial fields HamStack manages:

- hostname;
- node callsign;
- DMR/CCS7 ID when DMR is used;
- NXDN ID when NXDN is used;
- simplex/duplex mode;
- RX/TX radio frequency;
- modem type;
- basic location information;
- enabled radio modes;
- optional modem RX/TX offsets;
- optional WPSD OLED display configuration.

References:

- https://manual.wpsd.radio/install_software/
- https://manual.wpsd.radio/initial_startup/
- https://manual.wpsd.radio/modes/dmr/
- https://manual.wpsd.radio/profiles/

WPSD's own public scripts also use `/etc/mmdvmhost`,
`/etc/dstar-radio.mmdvmhost`, and `/etc/WPSD-Dashboard-Config.ini` as native
configuration/state files.

## Example

```yaml
hamstack_wpsd_enabled: true
hamstack_wpsd_callsign: N0CALL

hamstack_wpsd_modem: "mmdvmhshat"
hamstack_wpsd_frequency_mhz: 446.500
hamstack_wpsd_duplex: false

hamstack_wpsd_display: oled
hamstack_wpsd_oled_type: 3
hamstack_wpsd_oled_screensaver: true
hamstack_wpsd_oled_scroll: true

hamstack_wpsd_dmr_id: 1234567
hamstack_wpsd_modes:
  - dmr
  - ysf
```

Use the exact modem token expected by the WPSD Configuration page (for example, `mmdvmhshat` for the GPIO MMDVM_HS_Hat detected on HamStar-class hardware). The upstream manual recommends
running:

```bash
sudo wpsd-detectmodem
```

when the correct modem type is not known.

For duplex/repeater use, set separate RX/TX frequencies:

```yaml
hamstack_wpsd_duplex: true
hamstack_wpsd_rx_frequency_mhz: 438.250
hamstack_wpsd_tx_frequency_mhz: 439.950
```

## DMR custom masters

HamStack can optionally own WPSD's `[DMR Network Custom]` definition. This is
intended for stable community/private masters where a reproducible node should
connect directly without depending on BrandMeister or another public-network
account. It remains opt-in; ordinary WPSD network selection stays under WPSD.

WPSD uses DMRGateway as its normal DMR routing layer. When
`hamstack_wpsd_manage_dmr_custom_network` is enabled, HamStack points
MMDVMHost at the local DMRGateway and manages the custom-master section of
`/etc/dmrgateway`. WPSD's main Configuration page is still another config
writer and may regenerate this file; re-running HamStack restores the managed
values.

For the Ham Radio Village URF478 DMR master, use:

```yaml
hamstack_wpsd_dmr_id: 1234567
hamstack_wpsd_modes:
  - dmr

hamstack_wpsd_manage_dmr_custom_network: true
hamstack_wpsd_dmr_custom_network_name: HRV_URF478
hamstack_wpsd_dmr_custom_network_address: urf.hamvillage.org
hamstack_wpsd_dmr_custom_network_port: 62030
hamstack_wpsd_dmr_custom_network_auto_rewrites: false
hamstack_wpsd_dmr_custom_network_exclusive: true
hamstack_wpsd_dmr_custom_network_rules:
  - option: TGRewrite0
    value: "2,4001,2,4001,1"
```

Store the custom-master password in `inventory/local/group_vars/all/vault.yml`:

```yaml
vault_hamstack_wpsd_dmr_custom_network_password: "replace-with-the-master-password"
```

That gives a radio programmed for **TG 4001 / TS2** a direct, unprefixed path
to the HRV master. Exclusive mode also disables the standard BrandMeister,
DMR+/FreeDMR, TGIF, SystemX, crossover, and XLX DMRGateway network sections so
the appliance has one intentionally managed DMR destination. The password is
Vault-only; routing rules remain explicit public variables so a site can adapt
them if its URFd policy changes.

HamStack still does **not** attempt to clone the rest of WPSD's provider UI:
BrandMeister/TGIF account management, arbitrary multi-network policy, hostfile
editors, profiles, and dashboard/SSH passwords remain operator configuration.

## OLED displays

Set `hamstack_wpsd_display: oled` to manage the MMDVMHost OLED section. Type 3
is the common 0.96-inch OLED and supports scrolling; Type 6 is the 1.3-inch
OLED and WPSD forces scrolling off. HamStack also invokes WPSD's native
`.wpsd-display-driver-helper` whenever display settings change so the required
display driver state follows the rendered MMDVMHost configuration.
