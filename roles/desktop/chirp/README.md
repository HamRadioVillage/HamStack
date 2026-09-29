# `desktop/chirp`

Installs the maintained CHIRP-next radio programming application on a
Debian-family desktop and grants the operator normal serial-port access.

The default method uses CHIRP's recommended Linux AppImage path on x86_64, but
HamStack does **not** assume the public CHIRP archive is available for
unattended downloads. The public archive may return HTTP 403 to Ansible and
ordinary `curl` clients even when the release artifact is available to a
browser.

Provide either:

- `hamstack_chirp_appimage_src` — a controller-local AppImage path; or
- `hamstack_chirp_appimage_url` — an explicitly reachable/authorized artifact URL.

A controller-local source takes precedence. `hamstack_chirp_appimage_checksum`
may optionally contain `sha256:<digest>` and is verified after installation.
The wheel/pipx method remains available as an explicit alternate path.

HamStack does not manage radio memory images, vendor-specific programming
settings, or CHIRP's own preferences. The capability is simply made available
on the workstation.

Upstream: https://chirpmyradio.com/projects/chirp/wiki/ChirpOnLinux
