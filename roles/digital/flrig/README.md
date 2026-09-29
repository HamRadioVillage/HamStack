# `flrig` role

> **Status:** implemented application baseline; detailed operator preference-file automation remains partial.

## Purpose

Provide HamStack-managed CAT/rig control through FLRIG so other applications and operators can interact with a supported transceiver in a repeatable way.

## Expected starting state

A supported Linux host with access to the radio control interface. The role may install FLRIG where appropriate.

## Responsibilities

- Install or configure FLRIG.
- Manage HamStack-specific radio connection and service settings.
- Make rig-control configuration reproducible across stations that use FLRIG.

## Non-goals

- Own the higher-level digital application using the rig.
- Hard-code a single radio model, serial path, or operator-specific station layout.

## Configuration

See the [HamStack configuration reference](../../../docs/configuration.md#role-flrig) for the public variables owned by this role.

## Supported implementation

The role installs the Debian package and can create an XDG
desktop autostart entry for `hamstack_operator_user`.

Application-specific preference files are intentionally **not** written yet.
The public variables for radio, interface, station identity, and integration
are reserved in the configuration schema; those settings will be applied once
the upstream configuration format is verified against a working HamStack node.

## Known distribution issue

Ubuntu 26.04 (Resolute) currently publishes `flrig 2.0.05-1build1`. Ubuntu bug
2161172 documents an immediate launch crash for that package and has a fix
committed upstream in Ubuntu. HamStack warns when it detects that exact
release/package combination; the role does not silently replace the distro
package with a locally compiled build.

Upstream FLRIG releases may be newer than the distro package.
