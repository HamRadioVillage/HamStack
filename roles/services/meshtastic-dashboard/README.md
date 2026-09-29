# `services/meshtastic-dashboard`

Deploys the **official Meshtastic Web client** using its published container
image. HamStack does not implement its own Meshtastic dashboard.

The upstream client listens on container port 8080. HamStack keeps that listener
private and exposes it through the normal Caddy `tls internal` HTTPS sidecar.
Device selection and connection (HTTP/Bluetooth/Web Serial as supported by the
browser/client) remain normal Meshtastic Web behavior.

Upstream reference: https://meshtastic.org/docs/software/web-client/
