# Contributing to HamStack

Thanks for helping build HamStack.

HamStack is an open-source Ham Radio Village project intended to be useful
across different hardware, neighborhoods, stations, clubs, and event
deployments. Contributions should avoid assuming that one person's shack layout
is the universal architecture.

The canonical public repository, issues, feature requests, and pull requests are hosted at
https://github.com/HamRadioVillage/HamStack.

Bug reports, feature requests, documentation improvements, hardware support,
new roles, and pull requests are welcome.

For general project coordination, the preferred contact is **`@shoot3r` on the
HRV Discord**.

## Before you start

Read [AGENTS.md](AGENTS.md) for the repository architecture, role taxonomy, automation
boundaries, and expectations shared by human and AI-assisted contributors.


For a small fix, submit a pull request.

For a new role, major behavioral change, new hardware assumption, or repository-wide design change, open an issue first so the approach can be discussed before a large amount of work is done.

## Development setup

Create a virtual environment and install the development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
ansible-galaxy collection install -r requirements.yml
```

Run the fast repository QA and linters before submitting:

```bash
python scripts/qa.py
yamllint .
ansible-lint
```

The fast check is intentionally offline and does not substitute for live-device
validation. See [docs/qa.md](docs/qa.md) for the complete repository and hardware
validation workflow.

If you add or rename role defaults, regenerate the exhaustive variable index with:

```bash
python scripts/generate-variable-reference.py
```

## Role expectations

A HamStack role should:

- document its supported starting state and prerequisites;
- expose site-specific values as variables instead of hard-coding them;
- avoid embedding secrets in tracked files;
- be reasonably idempotent;
- use Ansible modules instead of shell commands where practical;
- include handlers for service restarts where appropriate;
- avoid making assumptions about unrelated HamStack roles;
- clearly document any action that may affect transmitting equipment.

When practical, test a role by running it twice. The second run should not report changes unless the underlying state actually changed.

## Naming

Prefer clear, lowercase role and variable names.

For variables, use a role-specific prefix where practical, for example:

```yaml
hamstack_timezone: America/Chicago
hamstack_allstar_node_number: 12345
```

Do not rename upstream projects merely to make the taxonomy prettier.

## Pull requests

Keep pull requests focused. A PR that adds or changes one role is easier to review than a PR that changes six unrelated subsystems.

A good pull request explains:

- what changed;
- why it changed;
- what hardware and OS were tested;
- what command or playbook was used to test it;
- whether a second idempotency run was clean;
- any known limitations.

## Secrets and personal configuration

Never commit real passwords, tokens, private keys, hotspot credentials, service credentials, or private inventory data.

Use clearly fake example values in documentation and examples.

## Be kind to future maintainers

If a configuration choice is weird for a good reason, document the reason. Six months from now, "why the hell is this here?" is a bug report waiting to happen.

## Licensing of contributions

HamStack is licensed under the GNU General Public License, version 3.

By submitting a contribution for inclusion in HamStack, you represent that you
have the right to submit it under the project's GPLv3 license. Do not submit
code, configuration, documentation, media, or other material copied from a
source whose license is incompatible with redistribution in HamStack.

Third-party software that HamStack installs or configures remains under that
software's own license. If a contribution copies or substantially derives a
configuration/template from an upstream project, preserve required attribution
and license notices and identify the upstream source in the role documentation.
