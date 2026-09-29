# HamStack QA and validation

HamStack separates **repository QA** from **live integration validation**. Passing
static checks means the tree is internally consistent; it does not certify that a
radio, router, appliance image, USB interface, or upstream service behaves the
way a real deployment expects.

## Fast offline QA

Run from the repository root:

```bash
python3 scripts/qa.py
```

The fast check validates:

- YAML parsing, including duplicate mapping keys;
- Jinja syntax;
- Python compilation and shell syntax;
- local Markdown links;
- Ansible role layout;
- generated `docs/variables.md` freshness;
- unresolved public URL placeholders;
- duplicate defaults for host-published HTTP(S)/web ports, including generic
  listener variables explicitly registered by QA;
- consistency between Vault variables used by code, the public Vault template,
  and the secret-variable reference;
- deprecated/duplicate repository paths;
- obvious disagreement between `docs/role-status.md`, role READMEs, and
  fail-fast placeholder tasks.

Regenerate the variable reference after changing role defaults:

```bash
python3 scripts/generate-variable-reference.py
```

## Controller-side QA

With the development requirements installed:

```bash
yamllint .
ansible-lint
```

When Ansible is available, use syntax checks against representative inventory or
localhost/profile runs before touching hardware. The interactive configurator's
`--validate` mode also attempts an Ansible syntax check when it can do so without
requiring an encrypted Vault prompt.

## Configurator smoke test

Use a disposable copy of the tree so QA does not create a real deployment
inventory in a working checkout:

```bash
python3 scripts/configure.py --init
python3 scripts/configure.py --validate
```

Expected example-inventory warnings such as `N0CALL` are not substitutes for
errors in the configurator itself.

## Public release gate

Before importing or mirroring a repository **with Git history** into a public host,
scan the real Git clone (all refs/history), not only an exported working tree. Use a
history-aware secret scanner such as Gitleaks or TruffleHog and investigate any
credential/private-key findings before publication. A clean current tree does not prove
that deleted historical content is safe to publish.

Also verify Git tracks directly-invoked scripts as executable:

```bash
git ls-files --stage scripts/
```

Scripts intended to be launched as `./scripts/<name>` should normally be mode `100755`.
ZIP exports do not reliably preserve or demonstrate Git's executable-bit metadata.

## Live integration validation

Before documenting a role as reference-hardware exercised, test the parts of its
contract that static analysis cannot prove:

1. Start from the documented upstream OS/appliance state.
2. Apply the role once and confirm the intended service/application works.
3. Apply it a second time and investigate unexpected changes.
4. Reboot and confirm enabled services survive.
5. Exercise failure/recovery paths appropriate to the role.
6. Confirm the role does not overwrite operator/upstream configuration outside
   the boundary documented in its README.

Network roles additionally need an out-of-band recovery path because a correct
configuration change can still disconnect the active Ansible session. RF roles
that can transmit should be validated with transmit disabled or into a suitable
load/test arrangement until hardware, audio levels, PTT behavior, and regulatory
settings are confirmed.

## What a passing QA result means

`HamStack QA passed.` means the repository passed the fast offline checks above.
It does **not** imply live-device certification. Current implementation and
hardware-validation caveats are tracked in [role-status.md](role-status.md).
