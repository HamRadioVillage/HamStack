# `services/gatus`

Deploys Gatus as the default lightweight HamStack status surface. Gatus is the
monitoring product; HamStack does not implement a separate monitoring backend.

The application runs in Docker and is exposed through a Caddy `tls internal`
HTTPS sidecar. SQLite history is persisted under the HamStack data directory by
default.

HamStack can derive basic checks from the inventory:

- ICMP reachability for other HamStack nodes;
- DCDash `/health`;
- OpenHamClock;
- OpenWebRX;
- LinBPQ web service.

Operators can add arbitrary native Gatus endpoints through
`hamstack_gatus_endpoints`. Automatic ICMP discovery can be disabled for any
inventory host by setting the inventory-only per-host variable
`hamstack_gatus_monitor_node: false`; when absent, it defaults to `true`.

This design deliberately leaves room for a future higher-level monitoring or
"super console" to aggregate one or more Gatus/HamStack deployments.

Upstream references:

- https://github.com/TwiN/gatus
- https://github.com/TwiN/gatus/blob/master/config.yaml

For local kiosk use, the Gatus application port is also published only on host
loopback (`hamstack_gatus_loopback_http_port`, default `18080`). Shared/event
LAN access remains HTTPS through the Caddy sidecar.
