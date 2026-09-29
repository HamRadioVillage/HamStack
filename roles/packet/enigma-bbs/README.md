# `enigma-bbs`

## Purpose

Deploy an ENiGMA½ BBS suitable for HamStack experimentation and event use.

## Supported deployment

The supported IP deployment runs the official ENiGMA Docker image and exposes:

- Telnet directly on the configured Telnet port;
- SSH directly on the configured SSH port;
- WebSocket through a Caddy TLS sidecar as **WSS**, using Caddy's internal CA.

ENiGMA's Docker image performs important first-run work before the BBS can
start: it seeds the stock config/art/mod trees and `oputil.js config new` creates
the system `config.hjson` plus board-specific menu files under `config/menus/`.
HamStack therefore seeds those upstream-owned trees and drives the interactive
upstream configuration wizard with Ansible's `expect` module so each prompt is
answered only after it appears. The runtime tree is marked initialized only
after the system config and at least one generated menu file exist.

HamStack does not replace that generated system config. It renders a small
HamStack-owned overlay and merges those managed values into the upstream-generated
`config.hjson` with ENiGMA's own bundled HJSON/lodash runtime. This preserves the
wizard-created menu/message-area configuration while keeping HamStack's network
and service settings authoritative. It also avoids pre-creating `config.hjson`,
suppressing ENiGMA's bootstrap, or trying to pipe answers into a TTY-oriented
wizard.

An SSH host key from the older HamStack layout is preserved during migration so
existing deployments do not silently rotate SSH identity. Database, logs,
filebase, art, mods, config, and mail data persist on the host.

Convergence verifies the generated menu tree, merged system config, and SSH key
inside the running container, then waits five seconds and confirms PM2's `main`
process still has an online PID. This prevents a Docker-published port from being
mistaken for a healthy BBS when the application itself is crash-looping.

## RF/KISS status

The Graywolf KISS → AX.25 session → ENiGMA transport shim is **not currently
supported**. Keep `hamstack_enigma_bbs_packet_transport: none`. RF transport can be
added later without changing the BBS service model established here.

## First login

ENiGMA promotes the first account created through the normal login flow to its
sysop group. Account provisioning is intentionally left to the upstream BBS.

### Transport boundary

The supported deployment deliberately stops at IP access:

- Telnet is exposed directly on the configured Telnet port.
- SSH is exposed directly on the configured SSH port.
- WebSocket access is exposed to the LAN only as **WSS** through a Caddy
  sidecar using Caddy's internal CA.
- ENiGMA's plain WebSocket port remains private to the Docker network.

The future RF feature is a transport shim that terminates a connected AX.25
session arriving from a Graywolf KISS endpoint and bridges it into ENiGMA.
`hamstack_enigma_bbs_packet_transport` remains `none` until that shim exists.

Future custom menus/themes should be modeled as explicit HamStack-managed files
or persistent paths rather than replacing the entire upstream config directory.
