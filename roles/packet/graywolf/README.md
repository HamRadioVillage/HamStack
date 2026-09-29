# `graywolf` role

> **Status:** install/service plus API-driven station, audio, modem-channel, PTT, KISS, and AGWPE configuration.

## Purpose

Deploy Graywolf as HamStack's reusable software-modem/TNC layer between radio/audio hardware and higher-level packet applications. Graywolf can be used by itself, as a KISS/AGWPE modem for another application, or underneath the optional `packet/aprs` policy role.

## Responsibilities

- Install an official Graywolf Debian release and manage the service.
- Bootstrap the first Graywolf management user when explicitly enabled.
- Set station identity through the supported REST API.
- Create/update named audio devices and modem-backed or KISS-only channels.
- Configure per-channel PTT.
- Expose KISS interfaces for LinBPQ, Winlink, or other packet clients.
- Configure the global AGWPE listener.

Graywolf keeps its operational configuration in SQLite. HamStack does **not** edit that database directly; API-managed state is converged through Graywolf's management API.

## Boundaries

This role owns Graywolf's modem/TNC plumbing. Higher-level APRS policy remains optional:

- `packet/graywolf`: radio/audio/PTT/channel/KISS/AGWPE and station identity.
- `packet/aprs`: optional iGate, digipeater, beacon, and APRS-specific policy.
- `packet/linbpq`: optional node/BBS consuming Graywolf KISS endpoints.

Graywolf does not tune a conventional radio. `frequency_mhz` may be retained in inventory as operator metadata, but the radio itself must be tuned by CAT, front panel, or another role.

## Configuration

Set `hamstack_graywolf_manage_api: true` to converge operational configuration. API management requires `vault_hamstack_graywolf_password` (or the legacy APRS Graywolf vault value during transition).

Audio devices are referenced by stable HamStack names:

```yaml
hamstack_graywolf_audio_devices:
  - name: packet_rx
    direction: input
    device_path: plughw:CARD=Device,DEV=0
  - name: packet_tx
    direction: output
    device_path: plughw:CARD=Device,DEV=0

hamstack_graywolf_channels:
  - name: packet_2m
    mode: packet
    input_device: packet_rx
    output_device: packet_tx
    modem: afsk1200
    ptt:
      method: cm108
      device_path: /dev/hidraw0
      gpio_pin: 3
    kiss:
      enabled: true
      type: tcp
      listen_address: 127.0.0.1
      port: 6700
      mode: modem
      allow_connected_mode: true
```

See the [HamStack configuration reference](../../../docs/configuration.md#role-graywolf) for the full public variable contract.
