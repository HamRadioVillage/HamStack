# HamStack coding instructions

Read `/AGENTS.md` before proposing or editing code. It is the canonical repository-level
architecture and maintainer guide.

In particular:

- preserve HamStack's functional role taxonomy;
- preserve composability rather than creating machine-specific mega-roles;
- respect upstream appliance and operator-owned configuration boundaries;
- keep RF identity/frequency/network choices explicit in inventory;
- keep secrets out of tracked files;
- prefer clear, idempotent Ansible over speculative abstraction;
- update examples and documentation with public variable/capability changes;
- do not claim hardware validation that was not actually performed;
- run `python3 scripts/qa.py` before considering a repository-wide change complete.
