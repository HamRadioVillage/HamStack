# `digital/js8call`

Installs the current upstream JS8Call Linux AppImage for x86-64 or ARM64 and
creates a desktop launcher for the HamStack operator account.

Version and download URLs are variables; the default is JS8Call
3.0.3, for which upstream publishes both Linux x86-64 and ARM64 AppImages.

The role grants ordinary audio/serial access but does not attempt to configure
station identity, Hamlib rig parameters, audio levels, message macros, or other
operator preferences. Those remain JS8Call configuration.

Accurate host time remains important for JS8 operation; combine this role with
normal NTP or HamStack `services/gps-time` where appropriate.

Upstream: https://js8call.com/downloads.html

The generated desktop launcher uses `APPIMAGE_EXTRACT_AND_RUN=1`, avoiding a
hard dependency on distro-specific FUSE compatibility packages. Radio/audio
configuration remains JS8Call operator configuration.
