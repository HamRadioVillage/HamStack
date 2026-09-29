# `linbpq`

## Purpose

Deploy a LinBPQ AX.25 node/BBS with Graywolf as the modem/PTT layer.

The role's model came from a real multi-band conference deployment, but the
configuration is intentionally **site-neutral**. Callsigns, SSIDs, aliases,
KISS ports, service ports, node behavior, applications, user text, and per-port
timing are inventory variables.

## Identity model

A deployment may supply complete callsigns:

```yaml
hamstack_linbpq_node_callsign: N0CALL-7
hamstack_linbpq_bbs_callsign: N0CALL-1
```

or derive them from the site callsign:

```yaml
hamstack_callsign: N0CALL

hamstack_linbpq_node_ssid: 7
hamstack_linbpq_node_alias: NODE

hamstack_linbpq_bbs_enabled: true
hamstack_linbpq_bbs_ssid: 1
hamstack_linbpq_bbs_alias: BBS
```

No node or BBS SSID is forced by the role.

## Installation policy

HamStack does not redistribute LinBPQ. Set `hamstack_linbpq_install: true` and
provide a compatible upstream `hamstack_linbpq_binary_url`, or preinstall the
binary and leave `hamstack_linbpq_install: false`.

## Graywolf / KISS model

Each item in `hamstack_linbpq_ports` describes a KISS TCP endpoint. The common
case is Graywolf bound to loopback:

```yaml
hamstack_linbpq_ports:
  - portnum: 1
    id: 70cm packet
    kiss_host: 127.0.0.1
    kiss_port: 6700

  - portnum: 2
    id: 2m packet
    kiss_host: 127.0.0.1
    kiss_port: 6701
```

Shared defaults such as `TXDELAY`, `PERSIST`, `PACLEN`, and `DIGIFLAG` live in
`hamstack_linbpq_port_defaults`; any port can override them individually.

Graywolf owns modem timing/PTT by default, so the generated configuration uses
`KISSOPTIONS=NOPARAMS` unless changed explicitly.

## Node and service behavior

`hamstack_linbpq_node_options` exposes the normal node-routing and session
values as a dictionary rather than hard-coding one event's settings.

Telnet/FBB/Web service ports, prompts, anonymous access, session limits, and the
IP-service BPQ port number are variables as well.

SYSOP/user credentials belong in:

```yaml
vault_hamstack_linbpq_telnet_users:
  - username: n0call
    password: CHANGE_ME
    callsign: N0CALL
    sysop: true
```

stored in the encrypted site Vault.

## Escape hatches

`hamstack_linbpq_extra_settings` emits additional top-level `KEY=VALUE` options.

`hamstack_linbpq_raw_config_append` exists for upstream features that the role
does not model yet. Prefer adding a proper variable to the role when a setting
becomes generally useful.

## Web-management assets

The generated BPQ configuration can enable the HTTP management port, but
HamStack does not currently redistribute or automatically fetch LinBPQ HTML
assets. If the selected upstream build expects separate HTML pages, install
those from the upstream distribution alongside the binary before relying on
the web UI.
