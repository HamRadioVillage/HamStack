# `desktop/netlogger`

Installs the existing NetLogger application on a Debian-family HamStack desktop.

NetLogger's public download workflow currently asks the operator to select a
platform and provide identifying/contact information before receiving the
package. HamStack intentionally does not automate around that workflow.
Provide either a controller-side `.deb` with `hamstack_netlogger_package_src`
or a direct HTTPS package URL you are authorized to use. When using a URL,
`hamstack_netlogger_package_checksum` (`sha256:<digest>`) verifies the package
before it is installed as root.

Once installed, net definitions, operator preferences, LoTW setup, and ordinary
net workflow remain NetLogger configuration.

Upstream: https://netlogger.org/download.php
