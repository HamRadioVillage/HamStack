# `digital/ft8web`

Provides a **local/offline-oriented mirror** of OK1CDJ's FT8Web browser client
and serves it over local HTTPS.

FT8Web is a browser/PWA application using browser audio and Web Serial. HTTPS is
important for modern browser hardware APIs, so HamStack serves the local copy
through a Caddy internal-CA TLS sidecar. Caddy receives certificates for the
inventory hostname, the managed `ansible_host` address when present, and any
additional names listed in `hamstack_ft8web_tls_extra_names`.

The mirror refresh uses a transactional last-known-good directory swap. The
nginx container bind-mounts the stable FT8Web data parent and serves the
`current` child, so atomic refreshes remain visible without recreating the
container. If a refresh fails, the previous local copy remains in service.

This is intentionally pragmatic rather than a fork of FT8Web. If upstream later
publishes a cleaner self-host build artifact/repository contract, the role can
switch sources without changing the HamStack-facing capability.

Upstream application: https://ft8web.ok1cdj.com/
