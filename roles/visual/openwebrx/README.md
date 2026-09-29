# `openwebrx`

## Purpose

Publish an OpenWebRX receiver on the LAN while keeping the application's
plaintext port private to its Docker network.

The role runs `jketterl/openwebrx:stable` and a Caddy TLS sidecar. Only HTTPS is
published to the host; the OpenWebRX listener on container port 8073 is not.
Caddy uses its internal CA by default.

`hamstack_openwebrx_device_mappings` is an explicit list of Docker device
mappings, for example:

```yaml
hamstack_openwebrx_device_mappings:
  - /dev/bus/usb:/dev/bus/usb
```

That broad USB mapping is intentionally **not** a default. Receiver profiles and
admin-user provisioning remain upstream/operator-managed so device-specific SDR
configuration is not guessed by HamStack.

### HTTPS-only LAN exposure

OpenWebRX's native HTTP port is kept private to the role's Docker network.
Only the Caddy sidecar publishes a host port, using `tls internal` for HTTPS.
This avoids broadcasting an unencrypted OpenWebRX management/session surface
on a conference LAN.

The role does not create the OpenWebRX administrative account or receiver
profiles automatically. Device pass-through and the persistent settings
directory are prepared; initial OpenWebRX application configuration remains an
upstream/operator workflow.
