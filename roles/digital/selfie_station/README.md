# `selfie_station` role

> **Status:** implemented headless capture/SSTV pipeline based on the HRV reference Selfie Station; TX remains disabled by default.

## Purpose

Reproduce the HamStack SSTV Selfie Station: capture an operator photo on demand, add the configured station/event overlay, and hand the result to the SSTV transmit workflow.

## Expected starting state

A supported Linux host with a camera, trigger device, and the selected SSTV/radio interface available. The reference implementation uses a Raspberry Pi Zero 2 W, Pi Camera, and USB foot pedal, but the role should not require that exact hardware forever.

## Responsibilities

- Deploy and configure the Selfie Station application/scripts.
- Configure camera capture, trigger input, image overlay, file handling, and handoff to the SSTV transmit path.
- Expose callsign/event text and hardware mappings as variables.

## Non-goals

- Own the full generic SSTV receive/archive station; that belongs in `sstv`.
- Hard-code the reference Pi/camera/foot-pedal hardware when an equivalent supported device can satisfy the role.

## Configuration

See the [HamStack configuration reference](../../../docs/configuration.md#role-selfie-station) for the public variables owned by this role.

## Implementation

The role deploys the field-developed headless Python
pipeline as a systemd service:

`foot pedal -> Picamera2 capture -> overlay -> CW ID -> PySSTV WAV -> AIOC PTT/audio`

It installs the Raspberry Pi/Python dependencies, creates a virtual environment
for PySSTV, resolves the trigger and AIOC endpoints from `hamstack_devices`,
and manages `hamstack-selfie-station.service`.

**RF transmission is disabled by default.** Set
`hamstack_selfie_station_transmit_enabled: true` only after validating the
AIOC device, PTT polarity, radio audio level, and generated WAV in dry-run mode.
