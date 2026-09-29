# `aprs`

## Purpose

Turn a generic Graywolf installation into a configurable **conference APRS demo
station**. The generic `graywolf` role owns installation/service lifecycle and
reusable radio/channel resources. This role owns APRS behavior on top of it.

## Safety-minded defaults

The role sets the station identity, but iGate, digipeater, and beacon
transmission are all opt-in. Graywolf simulation mode defaults on for the APRS
profile. If iGate is enabled, RF→APRS-IS is the default direction while
APRS-IS→RF stays disabled unless explicitly requested.

## Managed APRS behavior

- station callsign/SSID through Graywolf's REST API;
- iGate enable/server/filter/direction/channel settings;
- digipeater enable/callsign/dedup settings;
- simulation-mode convergence as part of iGate configuration.

Beacon CRUD and digipeater-rule CRUD are documented but deliberately fail fast
when requested until their identity/update behavior has been validated on a live
Graywolf node. This prevents an Ansible rerun from accidentally creating
multiple on-air beacons or duplicate digi rules.

## Starting state

Graywolf must already be installed, running, and have its audio/radio channel
configured. Supply that channel's Graywolf numeric ID with
`hamstack_aprs_graywolf_channel_id` when APRS behavior needs an RF channel.

## APRS-IS identity

Graywolf derives the APRS-IS passcode from the station callsign, so HamStack does not store a separate APRS-IS passcode for this backend.

### Graywolf authentication

Graywolf's configuration API is session-authenticated. Set
`hamstack_aprs_graywolf_username` and place the corresponding password in
`vault_hamstack_graywolf_password`. The older
`vault_hamstack_aprs_graywolf_password` name remains a compatibility fallback
for existing private inventories.

On a fresh Graywolf database, HamStack can create the first management user
when `hamstack_aprs_graywolf_manage_first_user` is `true` (the default). If a
user already exists, HamStack logs in with the supplied credentials and does
not attempt to replace it.

Conference-demo defaults are intentionally conservative: simulation mode is
on, iGate and digipeating are off, IS-to-RF gating is off, and beacon creation
is off. Every one of those features has a documented variable so a deployment
can opt in deliberately.
