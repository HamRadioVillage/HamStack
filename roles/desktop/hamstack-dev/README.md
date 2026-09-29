# `desktop/hamstack-dev`

Prepares a Debian-family laptop, mini-PC, or Raspberry Pi as a **HamStack
development environment**.

The role intentionally has no IDE opinion. It installs the language/controller
prerequisites, creates a repository-local Python virtual environment, installs
`requirements-dev.txt`, and installs the Ansible collections declared by the
repository.

HamStack source control is outside this role. The expected starting point is an
already-provided/unzipped HamStack tree (default `~/hamstack`). It will not
clone, pull, reset, commit, or otherwise mutate Git history.

This role is useful for contributors who want a Linux-native HamStack workspace
without requiring the project to prescribe their editor or source-sharing
workflow.
