# `services/cloudlog`

Deploys a local Cloudlog server using the upstream-supported style rather than
HamStack inventing an unofficial production container: Linux + Apache + PHP +
MariaDB/MySQL.

The role installs the runtime, checks out the requested Cloudlog ref, keeps the
application source root-owned, grants `www-data` write access only to Cloudlog's
known runtime/upload/config paths, creates a local database/user, and exposes
only an HTTPS Apache virtual host using a self-signed certificate. It
intentionally leaves Cloudlog's own `/install` wizard and application-level
station/user/logging configuration to Cloudlog.

Use `vault_hamstack_cloudlog_database_password` for the database secret. During
the web installer, the database host is `localhost` and the database/user names
come from the role variables.

HamStack does not implement log reconciliation or provider middleware.

Upstream project requirements state Linux, Apache (or compatible web server),
PHP, and MySQL; upstream does not provide production Docker support:
https://github.com/magicbug/Cloudlog
