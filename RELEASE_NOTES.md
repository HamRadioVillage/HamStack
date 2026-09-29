# HamStack v0.1.0 release notes

**Release date:** 2026-09-28
**Release type:** Initial public alpha

HamStack v0.1.0 is the first public release of the Ham Radio Village Ansible framework
for reproducible amateur-radio, conference, station, and lab infrastructure.

The project grew out of HRV conference deployments and experiments with packet radio,
SSTV, AllStar, WPSD/DMR, 44Net, local services, displays, logging tools, and portable
operator stations. v0.1.0 turns those patterns into composable roles and documented
configuration instead of prescribing one fixed hardware image.

## What is ready to use

This release includes deployable roles across:

- digital-mode and operator applications;
- packet, APRS, BBS, and Winlink services;
- AllStarLink and WPSD appliance configuration;
- SSTV receive/workstation/Selfie Station workflows;
- conference and station web/display services;
- local DNS, basic netboot, status, and time infrastructure;
- 44Net and selected network-device integrations;
- controller, contributor, and kiosk workstations.

Representative HRV Raspberry Pi and x86 deployments have been exercised during the
v0.1.0 development cycle, including fresh-install/redeploy workflows. Real deployments
should still expect some site-specific adjustment for radio audio levels, PTT polarity,
device enumeration, application preferences, frequencies, talkgroups, credentials, and
other station-specific settings.

## Alpha means alpha

v0.1.0 establishes the public structure and operating model; it does not freeze every
variable or promise universal hardware compatibility. Advanced functions that HamStack
cannot safely own yet intentionally remain with the upstream application or operator.
Those boundaries are documented rather than hidden behind placeholder automation.

Several alpha-line defaults intentionally follow upstream moving releases or branches
where that matches the upstream project. Sites that require immutable rebuilds should
pin the documented image, version, package URL, or source-ref variables in inventory.

Network-device roles are intentionally conservative. Test changes on spare hardware and
keep an out-of-band recovery path before using them for an event cutover.

Transmit-capable roles default to conservative behavior. Operators remain responsible
for validating their hardware, audio/PTT path, licensing, band plan, and local rules
before transmitting.

## Start here

Repository: https://github.com/HamRadioVillage/HamStack

For a first deployment, follow:

1. `README.md`
2. `docs/getting-started.md`
3. `docs/first-deployment.md`
4. `docs/role-status.md`
5. the README for each enabled role

Run repository QA before and after local modifications:

```bash
python3 scripts/qa.py
```

Contributions, bug reports, feature requests, documentation fixes, and new hardware
support are welcome. See `CONTRIBUTING.md`. General coordination is available through
`@shoot3r` on the HRV Discord.
