# `fldigi` role

> **Status:** implemented application baseline; detailed operator preference-file automation remains partial.

## Purpose

Configure a HamStack node for FLDIGI-based digital-mode operation, covering the general keyboard/digital modes that do not belong specifically to the WSJT-X workflow.

## Expected starting state

A supported graphical or otherwise suitable Linux host reachable by Ansible. The role may install FLDIGI when that is the appropriate supported deployment method.

## Responsibilities

- Install or configure FLDIGI and its HamStack-specific settings.
- Expose site, operator, audio, and radio-control settings as variables rather than hard-coding them.
- Integrate with shared HamStack rig-control or audio resources where applicable.

## Non-goals

- Own radio hardware definitions that should be reusable by other roles.
- Replace WSJT-X for weak-signal modes that are better handled by the `wsjtx` role.

## Configuration

See the [HamStack configuration reference](../../../docs/configuration.md#role-fldigi) for the public variables owned by this role.

## Supported implementation

The role installs the Debian package and can create an XDG
desktop autostart entry for `hamstack_operator_user`.

Application-specific preference files are intentionally **not** written yet.
The public variables for radio, interface, station identity, and integration
are reserved in the configuration schema; those settings will be applied once
the upstream configuration format is verified against a working HamStack node.
