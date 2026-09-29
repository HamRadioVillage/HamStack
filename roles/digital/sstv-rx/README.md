# `sstv-rx` role

> **Status:** implemented and exercised on the HRV reference receive appliance; receiver/antenna choices remain deployment-specific.

## Purpose

Configure a receive-only SSTV demonstration appliance built around an RTL-SDR,
GQRX, and the HamRadioVillage QSSTV fork. This is the HamPi-02-style deployment:
GQRX is the human-operated receiver/tuner and QSSTV is the SSTV decoder/display.

## Expected starting state

A Debian-family desktop-capable host with an RTL-SDR-compatible receiver and a
local display/session. The reference HamPi-02 deployment is a Raspberry Pi 4
connected to a TV for interactive demonstrations.

## Responsibilities

- Install GQRX, RTL-SDR tooling, PulseAudio client utilities, VOLK profiling tools, and the shared HRV QSSTV runtime.
- Seed a first-run GQRX profile with the configured initial frequency and RTL-SDR device.
- Route GQRX audio through a named PulseAudio/PipeWire-Pulse null sink into QSSTV.
- Seed QSSTV to use its PulseAudio backend.
- Optionally autostart GQRX and QSSTV in the configured desktop session.
- Preserve operator tuning/profile changes: the seeded application configs are never overwritten after first creation.

## Non-goals

- Transmit or key a radio.
- Manage camera/trigger workflows; those belong to `selfie_station`.
- Act as a general operator SSTV transmit station; that belongs to `sstv-workstation`.

## Audio and tuning path

```text
RTL-SDR -> GQRX -> hamstack_sstv Pulse sink -> monitor source -> HRV QSSTV
```

GQRX owns tuning, gain, waterfall, and QSY. `hamstack_sstv_rx_frequency_mhz` is
only the initial seed value for a new profile; later Ansible runs do not reset
the operator's current GQRX frequency.

Both applications run with a role-specific `XDG_CONFIG_HOME` under
`~/.config/hamstack-sstv-rx`, keeping appliance settings predictable and
separate from unrelated desktop profiles.

Older `rtl_fm`, `snd-aloop`, and `hamstack-sstv-rx.service` artifacts from earlier
HamStack implementations are removed during convergence.

## Configuration

See the [HamStack configuration reference](../../../docs/configuration.md#role-sstv-rx)
for the public variables owned by this role.
