# `services/wavelog`

Deploys a local Wavelog instance using the upstream-recommended Docker model:
Wavelog plus MariaDB with persistent storage. HamStack adds its normal private
Docker network and Caddy HTTPS sidecar rather than publishing the application's
port directly on a conference LAN.

After deployment, finish Wavelog's normal web installer at `/install`; use
`hamstack-wavelog-db` as the database hostname and the Vault-backed database
password configured for this role.

HamStack does not implement QSO federation, synchronization, or bespoke logging
middleware. External Wavelog/Cloudlog use and later import/export remain
operator/application workflows.

Upstream reference:
https://docs.wavelog.org/getting-started/installation/docker/
