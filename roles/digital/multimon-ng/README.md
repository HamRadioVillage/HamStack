# `digital/multimon-ng`

Installs the Debian `multimon-ng` decoder and provides a predictable HamStack
wrapper for selecting decoders such as POCSAG 512/1200/2400.

The role does not invent the radio/audio front end. Operators may pipe raw audio
or demodulated samples into `/usr/local/bin/hamstack-multimon-ng`, or provide a
`hamstack_multimon_ng_source_command` (for example an SDR/audio pipeline) and
enable the optional managed service.

The managed service runs as the unprivileged `hamstack_multimon_ng_user`
account (default `hamstack-multimon`, a member of `audio` and `plugdev`) under
a restricted systemd sandbox, because the decoder parses over-the-air data.
The source command therefore needs its audio or SDR device to be accessible to
that account; Debian's `rtl-sdr` udev rules grant `plugdev` access to
RTL-SDR dongles. Set `hamstack_multimon_ng_manage_user: false` to run under
an account the operator manages, and add groups through
`hamstack_multimon_ng_user_groups` when other devices are needed. The decoded
output file is owned by the service account with mode `0640`.

Transmit capability is not involved; this role is receive/decoder plumbing.
