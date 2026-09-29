# `44connect`

## Purpose

Configure the Linux side of a **44Net Connect** single-device WireGuard tunnel.
HamStack deliberately does not automate the 44Net portal: the operator requests
and downloads the tunnel configuration from 44Net Connect, then places the
resulting address/peer values in local inventory and private key material in
Ansible Vault.

## Routing policy

HamStack defaults to a **split tunnel**. Only the two currently documented
44Net IPv4 route aggregates (`44.0.0.0/9` and `44.128.0.0/10`) are placed in
WireGuard `AllowedIPs`; normal Internet traffic stays on the host's ordinary
uplink. Set `hamstack_44connect_split_tunnel: false` only when you intentionally
want the configured full-tunnel routes.

## Starting state

A Debian-family system reachable by Ansible and a tunnel already provisioned in
44Net Connect.

## What this role owns

- `wireguard-tools` installation;
- `/etc/wireguard/<interface>.conf`;
- `wg-quick@<interface>` enable/start behavior;
- split/full tunnel route selection.

## Secrets

Store the WireGuard private key in `vault_hamstack_44connect_private_key` and,
when used, the peer preshared key in `vault_hamstack_44connect_preshared_key`.
Do not commit the downloaded 44Net configuration verbatim.
