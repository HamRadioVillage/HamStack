## What changed

Describe the change and the HamStack role/capability it affects.

## Why

Explain the problem being solved or the behavior being added.

## Validation

- [ ] `python3 scripts/qa.py`
- [ ] `yamllint .`
- [ ] `ansible-lint`
- [ ] Relevant playbook(s) pass `ansible-playbook --syntax-check`
- [ ] A second Ansible run was checked for unexpected changes when live hardware/software was exercised

Tested hardware/OS and commands used:

## Release/user impact

Note changed defaults, ports, variables, hardware assumptions, manual migration steps, or known limitations. If none, say so.

## Documentation and secrets

- [ ] Public variable changes are reflected in examples/docs and `docs/variables.md` is regenerated
- [ ] No real credentials, private inventory, event-only secrets, or sensitive artifacts are included
- [ ] Upstream-derived code/configuration retains required attribution and licensing information
