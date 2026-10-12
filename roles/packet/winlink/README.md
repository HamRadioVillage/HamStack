# `packet/winlink`

The first HamStack Winlink implementation is **Pat** (`la5nta/pat`). Pat is a
Linux-friendly Winlink client with CLI and mobile-friendly web interfaces and
native support for multiple transports.

The role installs an upstream Pat `.deb`, creates persistent mailbox/config
storage, renders a baseline Pat JSON configuration, and optionally runs `pat
http` as a hardened systemd service.

Transport configuration is deliberately additive/operator-driven. Telnet is the
minimal default; AX.25, AGWPE, serial TNC, ARDOP, VARA, PACTOR, Hamlib, and GPSd
values are exposed without HamStack pretending every station has the same radio
stack.

The Winlink secure-login password can be stored as:

```yaml
vault_hamstack_winlink_password: '...'
```

## Package verification

The Pat `.deb` is downloaded into the root-owned HamStack package cache
(`hamstack_winlink_package_cache_dir`) and its SHA-256 digest is checked
against `hamstack_winlink_package_checksums` before installation. When
`hamstack_winlink_version` changes, add the matching upstream release digests
for each architecture; set `hamstack_winlink_require_checksum: false` only for
a deliberate, unverified install.

Pat upstream: https://github.com/la5nta/pat
