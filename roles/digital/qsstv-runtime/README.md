# `qsstv-runtime` support role

> **Status:** internal shared source-build helper for HamStack SSTV roles.

This is not a standalone deployment capability and is intentionally absent from
`playbooks/site.yml`. `digital/sstv-rx` and `digital/sstv-workstation` invoke it
when they need QSSTV.

HamStack uses the HamRadioVillage QSSTV fork rather than the Debian `qsstv`
package. The HRV source currently identifies itself as QSSTV 9.5.11 and
builds with qmake. Its README documents the Debian-family
build dependencies that this helper installs.

The helper checks out `hamstack_qsstv_source_repo` at
`hamstack_qsstv_source_ref`, builds into a disposable cache directory, installs
the binary under `/opt/hamstack/qsstv`, and exposes it as
`/usr/local/bin/qsstv`. The distro package is removed by default so the broken
or incompatible `/usr/bin/qsstv` cannot accidentally win path selection.

The default ref is `main` because the HRV repository currently has no HamStack-
validated release tag. Sites requiring immutable rebuilds should pin
`hamstack_qsstv_source_ref` to a tested commit hash.
