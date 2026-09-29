# `desktop/hamstack-controller`

Prepares the lead operator's Debian-family control station for **consuming and
pushing HamStack playbooks**.

It installs only the controller prerequisites, creates a local virtual
environment from `requirements-controller.txt`, and installs the repository's
Ansible collections. It does not install an IDE, monitoring bookmarks, or a GUI
management suite.

The HamStack tree is assumed to have been delivered out-of-band (for example as
a ZIP file) and unpacked locally. The role never clones, pulls, resets, or
publishes repository changes.

Secrets remain operator-managed. The control station can point Ansible at a
Vault password file or SSH keys, but this role does not manufacture or copy
private credentials.
