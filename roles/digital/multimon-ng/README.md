# `digital/multimon-ng`

Installs the Debian `multimon-ng` decoder and provides a predictable HamStack
wrapper for selecting decoders such as POCSAG 512/1200/2400.

The role does not invent the radio/audio front end. Operators may pipe raw audio
or demodulated samples into `/usr/local/bin/hamstack-multimon-ng`, or provide a
`hamstack_multimon_ng_source_command` (for example an SDR/audio pipeline) and
enable the optional managed service.

Transmit capability is not involved; this role is receive/decoder plumbing.
