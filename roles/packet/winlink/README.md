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

Pat upstream: https://github.com/la5nta/pat
