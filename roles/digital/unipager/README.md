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

## Repository trust

UniPager installation is fail-closed until
`hamstack_unipager_repo_key_checksum` is set to the independently verified
SHA-256 digest of the repository signing key, in `sha256:<64-hex-digest>`
form. Do not derive the checksum from `hamstack_unipager_repo_key_url` during
the playbook run: the checksum is the trust anchor that prevents that origin
from substituting both a signing key and packages. A key rotation requires an
explicit reviewed checksum update.

## Current upstream packaging status

HamStack points at the currently documented `https://hampager.de/debian`
repository and key. On Ubuntu 26.04, APT rejects that repository because the
upstream signing key is expired (`EXPKEYSIG 275E586934BE1547`). HamStack
intentionally does **not** mark the repository trusted or allow unauthenticated
packages to bypass that failure. No digest is shipped for the expired key, so
fresh installs remain upstream-blocked until a valid signing key/repository
signature is published and its digest is independently reviewed.

Upstream: https://github.com/rwth-afu/UniPager
