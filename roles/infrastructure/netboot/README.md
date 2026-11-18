# `infrastructure/netboot`

Provides a deliberately small **authenticated HTTPS/iPXE content service** for
HamStack.

The role serves a generated `boot.ipxe` menu and an operator-managed web root.
It is useful once a machine is already capable of executing an iPXE script.
The container exposes TLS only: `hamstack_netboot_tls_certificate_path` and
`hamstack_netboot_tls_private_key_path` identify certificate and key source files
that already exist on the managed host. HamStack copies them into the role's
root-owned `tls` directory on each run and authoritatively manages those copies.
The source files and certificate lifecycle remain operator-owned.

The supported scope intentionally does **not** run DHCP, proxy-DHCP, or TFTP. Those
features can be added after the basic workflow is exercised on real conference
networks. Avoiding an accidental second DHCP server is a feature.

Boot clients must retrieve the initial menu through its `https://` endpoint,
trust the server certificate, support iPXE image signatures, and contain the
certificate that signs boot artifacts in their iPXE trust store. The generated
menu permanently enables image trust before displaying entries. It fetches and
verifies every detached signature before executing a chained script or booting a
kernel/initrd pair. Plain HTTP and unsigned entry URLs are rejected during the
Ansible run.

Entries may either chain another signed iPXE script or specify signed
kernel/initrd/arguments:

```yaml
hamstack_netboot_tls_certificate_path: /etc/hamstack/netboot/server.crt
hamstack_netboot_tls_private_key_path: /etc/hamstack/netboot/server.key
hamstack_netboot_entries:
  - id: rescue
    label: Signed rescue environment
    kernel: https://netboot.example.invalid:8089/rescue/vmlinuz
    kernel_signature: https://netboot.example.invalid:8089/rescue/vmlinuz.sig
    initrd: https://netboot.example.invalid:8089/rescue/initrd.img
    initrd_signature: https://netboot.example.invalid:8089/rescue/initrd.img.sig
    args: ip=dhcp
  - id: installer
    label: Signed installer menu
    chain: https://boot.example.invalid/installer.ipxe
    chain_signature: https://boot.example.invalid/installer.ipxe.sig
```

`hamstack_netboot_https_port` is the published TLS port. It defaults to the
legacy-named `hamstack_netboot_http_port` value so existing port overrides remain
effective; no plaintext listener is created. Operators can copy ISO-derived
kernels, rescue environments, Debian installer assets, or custom material into
the persistent web root as needed, together with their detached signatures.
