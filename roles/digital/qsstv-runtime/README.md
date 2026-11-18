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

Source checkout, qmake, make, and runtime-library inspection run as the locked
`hamstack_qsstv_build_user` account. HamStack accepts only regular artifacts
owned by that account, stages them without following source symlinks, verifies
their SHA-256 digests, and then atomically moves them into root-owned install
locations. Upstream build logic therefore does not receive root authority.

The default ref remains `main` because the HRV repository currently has no
HamStack-validated release tag, but `hamstack_qsstv_update_source` defaults to
`false`: the branch is resolved for an initial checkout and later convergence
does not follow it. To update an existing checkout, first review and set
`hamstack_qsstv_source_ref` to the full 40-character commit ID, then set
`hamstack_qsstv_update_source: true`. The role verifies that exact commit before
building it and rejects automatic updates from branches, tags, or short IDs.
