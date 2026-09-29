# `services/dcdash`

Deploys the current DCDash application onto a Debian-family HamStack service
node. The role is based on the DCDash 2.9 deployment contract supplied to the
HamStack project: Python 3.11–3.12, Flask/Gunicorn, SQLite/WAL, native TLS on
8450, `/etc/default/dcdash`, and an application-scoped hardened systemd unit.

The role validates the DCDash 2.9 Python runtime contract (Python 3.11 or 3.12).

HamStack deliberately does **not** reproduce DCDash's standalone deployment
script's host-wide UFW, fail2ban, SSH-policy, hostname, or Avahi changes. Those
belong to host/network policy, not an application role on a multifunction
HamCube.

The application source remains separate from HamStack. Point
`hamstack_dcdash_source_repo` at the desired DCDash git repository/ref and put
`vault_hamstack_dcdash_admin_password` in the local Vault.

The role verifies the application's public `/health` endpoint after startup.
