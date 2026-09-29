# `digital/unipager`

Installs UniPager, the RWTH amateur-radio group's POCSAG transmitter controller,
using its documented Debian/Raspbian repository.

UniPager exposes its configuration UI on port 8073 and browser websocket traffic
on 8055. Actual transmitter type, pager network, GPIO/serial hardware, and RF
settings remain UniPager configuration.

**Safety boundary:** `hamstack_unipager_autostart` defaults to `false`. Merely
enabling/installing this role does not intentionally leave the pager
transmitter controller running. The operator must explicitly opt in after the
hardware and RF configuration are understood.

## Current upstream packaging status

HamStack points at the currently documented `https://hampager.de/debian`
repository and key. On Ubuntu 26.04, APT rejects that repository because the
upstream signing key is expired (`EXPKEYSIG 275E586934BE1547`). HamStack
intentionally does **not** mark the repository trusted or allow unauthenticated
packages to bypass that failure. Fresh installs remain upstream-blocked until a
valid signing key/repository signature is published.

Upstream: https://github.com/rwth-afu/UniPager
