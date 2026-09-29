# HamStack agent and maintainer guide

This file is the repository-level operating context for humans and coding agents.
Read it before making architectural, taxonomy, inventory, or role changes.

HamStack is an open-source Ham Radio Village project for reproducible amateur-radio,
conference, station, and lab infrastructure with Ansible. It is intentionally
hardware-flexible and favors small composable roles over machine-specific mega-roles.

## Design rules that are intentional

1. **Role families describe function, not presentation.**
   - `digital/` contains radio-mode applications and signaling/decoding workflows,
     including SSTV.
   - `packet/` contains packet/APRS/BBS/Winlink capabilities.
   - `voice/` contains AllStar/WPSD voice/digital appliance configuration.
   - `visual/` is reserved for tools whose primary purpose is visualizing station,
     receiver, propagation, telemetry, or similar amateur-radio data.
   - `services/`, `desktop/`, `network/`, and `infrastructure/` keep their documented
     meanings in `README.md` and `docs/architecture.md`.
   Do not move a role merely because its application has a GUI or produces an image.

2. **Capabilities are composable.** A Raspberry Pi, laptop, HamCube, or other node is
   a deployment target, not a reason to create a giant role for that machine. Profiles
   may compose roles, but roles should remain independently useful where practical.

3. **Respect upstream appliance boundaries.** HamStack does not generally build or
   replace WPSD, AllStarLink, AREDN, or other upstream appliance images. A role may
   configure the documented portion it owns. Do not expand ownership into upstream
   workflows without an explicit design decision and documentation update.

4. **Managed versus operator-owned state must be explicit.** If a role renders a file
   authoritatively, document that fact and provide a safe extension point when
   practical. Do not silently overwrite operator or upstream state outside the role's
   documented boundary.

5. **Inventory expresses deployment intent.** Site identity, attached hardware,
   frequencies, callsigns, node numbers, talkgroups, service endpoints, and other
   deployment-specific values belong in inventory variables rather than role forks or
   hard-coded task values.

6. **Secrets do not belong in tracked files.** Real passwords, API keys, hotspot
   credentials, private keys, and similar values belong in the gitignored local
   inventory and Ansible Vault. Examples must use clearly fake values.

7. **Prefer boring, observable Ansible.** Do not add abstractions solely to reduce a
   few repeated lines. Prefer understandable modules, templates, handlers, and
   variables that are easy to debug on a Pi or laptop in the field.

8. **Idempotency matters.** A second run should be boring unless underlying state
   changed. Avoid tasks that report changes on every run without a concrete reason.

9. **Do not make unrelated RF changes.** Never change frequencies, callsigns, node
   numbers, talkgroups, network destinations, PTT mappings, radio-interface mappings,
   or transmit-enable defaults as collateral cleanup.

10. **Transmit-safe defaults win.** New or uncertain transmit paths should default to
    disabled until the operator explicitly enables them. Do not infer regulatory or
    station-specific RF settings.

## Public role contract

For a normal public role, expect to review all of the following when behavior changes:

- `roles/<family>/<role>/defaults/main.yml`
- tasks/templates/handlers used by the role
- the role `README.md`
- `playbooks/site.yml` when role enablement changes
- `inventory/example/host_vars/example-node.yml` for useful public examples
- `inventory/example/group_vars/all/vault.yml.example` when the secret surface changes
- `docs/configuration.md` when the documented schema changes
- generated `docs/variables.md` when role defaults change
- `docs/role-status.md` and `FEATURES.md` when capability or maturity changes

Host-published HTTP(S)/web defaults must remain unique across composable roles. If a
public default port changes, update any Gatus-derived fallback checks and regenerate the
variable reference. Generic listener variables such as `hamstack_dcdash_port` must also
be registered in the QA listener set. `scripts/qa.py` rejects duplicate published
defaults and Vault-schema drift.

Internal support roles such as `digital/qsstv-runtime` may intentionally be absent from
`playbooks/site.yml`; their README must say so.

## Hardware and validation claims

Repository QA and real-device validation are different. Do not claim a role is
hardware-validated merely because YAML, lint, syntax, templates, or a container test
passed. When documenting hardware validation, state what was actually exercised and
keep site-specific tuning/calibration limitations visible.

Minor hand tuning of radio audio, application preferences, device enumeration, and
site-specific settings is expected during the v0.1.x alpha line unless the role
explicitly promises to manage those values.

## Before submitting a change

Run at minimum:

```bash
python3 scripts/qa.py
```

For contributor changes, also run when the tools are installed:

```bash
yamllint .
ansible-lint
```

If role defaults changed, regenerate and verify the variable reference:

```bash
python3 scripts/generate-variable-reference.py
python3 scripts/generate-variable-reference.py --check
```

For hardware-facing changes, record the target OS/appliance, hardware tested, the
playbook used, whether a second run was clean, and what still required operator tuning.

## Documentation style

Write documentation as durable public project documentation, not as a diary of the
implementation process. Prefer statements such as "HamStack manages X and leaves Y to
the operator" over "we still need to test Y later." Put future work in `ROADMAP.md` and
current limitations in the relevant role README or `docs/role-status.md`.

## Canonical project location

- Repository: https://github.com/HamRadioVillage/HamStack
- General project coordination: `@shoot3r` on the HRV Discord
- License: GNU GPL version 3
