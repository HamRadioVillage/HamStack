# `sstv-workstation` role

> **Status:** implemented QSSTV workstation baseline; detailed per-user audio/PTT preferences remain operator-configured.

## Purpose

Configure a general-purpose operator SSTV workstation for receiving, composing,
decoding, displaying, archiving, and eventually transmitting SSTV through a
normal radio/audio/PTT interface.

This is the "show how an SSTV station actually works" role. It is deliberately
separate from both the receive-only RTL-SDR appliance and the purpose-built
Selfie Station.

## Expected starting state

A Debian-family desktop-capable host with an operator login/session. RX/TX
hardware may be described through `hamstack_radios` and `hamstack_devices` as
the radio-control implementation grows.

## Responsibilities

- Install the supported interactive SSTV application stack.
- Autostart QSSTV in the selected operator desktop session when requested.
- Own workstation-level receive/transmit intent, frequency, mode, image storage,
  and future audio/PTT mapping.
- Remain suitable for a conventional human-operated SSTV demonstration station.

## Non-goals

- Implement the RTL-SDR-only appliance; use `sstv-rx` for that.
- Own camera/trigger/meme-generation logic; use `selfie_station` for that.
- Hard-code one radio or USB audio/PTT implementation.

## Configuration

See the [HamStack configuration reference](../../../docs/configuration.md#role-sstv-workstation)
for the public variables owned by this role.

## Implementation

The role uses the **HamRadioVillage QSSTV fork** on Debian-family systems. HamStack builds the HRV source with the shared `digital/qsstv-runtime` helper rather than installing Debian's `qsstv` package, then can autostart `/usr/local/bin/qsstv` in the desktop session of `hamstack_sstv_workstation_user`, which defaults to `hamstack_operator_user`.

Transmit intent remains disabled by default. The role does not yet generate
QSSTV's per-user preference database, so audio device selection, detailed
receive/transmit settings, and radio/PTT mapping remain operator-configured until those settings have a stable, portable automation contract.
