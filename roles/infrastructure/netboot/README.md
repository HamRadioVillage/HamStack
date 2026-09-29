# `infrastructure/netboot`

Provides a deliberately small **HTTP/iPXE content service** for HamStack.

The role serves a generated `boot.ipxe` menu and an operator-managed web root.
It is useful once a machine is already capable of executing an iPXE script.

The supported scope intentionally does **not** run DHCP, proxy-DHCP, or TFTP. Those
features can be added after the basic workflow is exercised on real conference
networks. Avoiding an accidental second DHCP server is a feature.

Entries may either chain another iPXE URL or specify kernel/initrd/arguments.
Operators can copy ISO-derived kernels, rescue environments, Debian installer
assets, or custom material into the persistent web root as needed.
