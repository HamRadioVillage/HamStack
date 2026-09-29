# `wsjtx` role

> **Status:** implemented application baseline; detailed operator preference-file automation remains partial.

## Purpose

Configure a HamStack station for WSJT-X operation, including the weak-signal digital modes and station integration that belong to the WSJT-X application.

## Expected starting state

A supported Linux host with the required display/audio/radio interfaces available. The role may install WSJT-X when that matches the supported platform.

## Responsibilities

- Install or configure WSJT-X.
- Manage site-specific station, audio, CAT, and operating parameters as variables.
- Integrate cleanly with companion roles such as `flrig` and `gridtracker` without requiring them.

## Non-goals

- Provide general-purpose rig control for unrelated applications.
- Own visual/logging companion applications that have their own HamStack roles.

## Configuration

See the [HamStack configuration reference](../../../docs/configuration.md#role-wsjtx) for the public variables owned by this role.

## Supported implementation

The role installs the Debian package and can create an XDG
desktop autostart entry for `hamstack_operator_user`.

Application-specific preference files are intentionally **not** written yet.
The public variables for radio, interface, station identity, and integration
are reserved in the configuration schema; those settings will be applied once
the upstream configuration format is verified against a working HamStack node.
