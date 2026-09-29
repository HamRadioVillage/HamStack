# `network/aredn`

Read-only integration for **already-running AREDN nodes**.

HamStack does not flash firmware or own mesh RF/tunnel/LQM configuration. The
role periodically queries AREDN's documented `/a/sysinfo` JSON API, validates a
minimal response, and keeps last-known-good JSON snapshots on a normal HamStack
Linux node.

Optional API flags can include link information, advertised services, and LQM.
Polling defaults to a conservative two-minute interval so management traffic is
not needlessly sprayed across the mesh.

When Gatus is enabled, HamStack can also derive basic AREDN reachability/API
checks from `hamstack_aredn_nodes`.

Upstream API documentation:
https://docs.arednmesh.org/en/latest/arednHow-toGuides/devtools.html
