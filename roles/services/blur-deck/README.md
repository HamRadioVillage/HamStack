# `services/blur-deck`

Publishes a directory of conference video media with ReadyMedia/MiniDLNA for
Roku Media Player and other DLNA clients.

The role intentionally stays dumb: it installs ReadyMedia, owns a media
directory, optionally copies a supplied MP4 into it, and manages the DLNA
service. Rendering/generating the Blur Deck itself remains outside the role.

This keeps the service reusable for the existing Blur Deck and for future roles
that may generate Roku-consumable media.

Upstream ReadyMedia supports video-only media directories (`media_dir=V,...`),
a configurable `friendly_name`, interface binding, and inotify scanning.
