# `openhamclock`

## Purpose

Publish OpenHamClock as a LAN service without exposing the application's plain
HTTP listener directly onto an event network.

The role runs the official OpenHamClock container on a private Docker network
and fronts it with a Caddy sidecar. Only HTTPS is published to the host. Caddy
uses its internal CA (`tls internal`) by default, so clients will see an
untrusted certificate until that CA is imported/trusted.

OpenHamClock's application listener remains container-internal on port 3000.
The default LAN endpoint is `https://<inventory-hostname>:8449`.

HamStack passes the deployment callsign, grid locator, timezone, and optional
coordinates into the upstream container environment, then layers
`hamstack_openhamclock_environment` on top for operator overrides. Application
data is persisted from `/data` into the HamStack data directory.

### HTTPS-only LAN exposure

The application container is attached only to a private Docker network and does
not publish its native HTTP port on the host. Caddy is the only LAN-facing
component and publishes HTTPS with `tls internal`.

HamStack also enables OpenHamClock server-side settings sync and stores the
settings file under the persistent `/data` volume. The application is told to
trust proxy headers because all browser traffic reaches it through Caddy.

Clients will need to trust Caddy's local root CA if they should see the
certificate as trusted rather than merely encrypted/self-signed.
