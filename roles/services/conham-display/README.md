# `services/conham-display`

Maintains a last-known-good local copy of `conham.radio` for conference use when
WAN connectivity is unreliable.

The role mirrors the **rendered site** with `wget`, including linked page
assets, and serves the successful mirror locally through a Caddy HTTPS
container. Refreshes are staged and switched atomically: a failed fetch leaves
the previous local copy untouched.

The selected conference page is an operator/display concern; for example a
HamCube Chromium kiosk can open:

```text
https://<hamcube>:8446/dc
```

The upstream CONHAM content is maintained separately from HamStack. A future
enhancement can consume the Markdown/source repository directly once its build
contract is captured. Roku rendering is also intentionally separate: Roku is a
media client, while the canonical CONHAM representation remains local HTML.
