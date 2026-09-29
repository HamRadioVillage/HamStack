# Security Policy

## Reporting a vulnerability

Please do **not** publish credentials, exploitable configuration details,
private inventory, or sensitive deployment information in a public GitHub
issue.

The preferred initial security contact is **`@shoot3r` on the Ham Radio Village
Discord**.

When making initial contact, identify the message as a HamStack security report
and avoid sending live credentials or unnecessary private deployment data until
an appropriate private exchange is established.

If a vulnerability primarily belongs to an upstream project that HamStack
installs or configures, report it to that upstream project unless HamStack's
integration creates or materially worsens the issue.

## What is in scope

Security reports involving HamStack are welcome, including issues involving:

- automation that unexpectedly weakens host security;
- privilege escalation or unsafe sudo behavior;
- secret/Vault handling;
- generated configuration that exposes credentials;
- unsafe default network exposure;
- unintended transmit-enabling behavior;
- container or service isolation caused by HamStack configuration;
- repository examples that contain real or sensitive deployment data.

## Secrets

HamStack repositories must not contain real secrets.

Do not commit:

- passwords;
- API tokens;
- private keys;
- radio-network credentials;
- node passwords;
- private deployment inventory;
- other credentials or sensitive operator data.

If a secret is committed accidentally, treat it as compromised and rotate it.
Removing it from the latest commit is not sufficient by itself.

Use encrypted Ansible Vault data under the gitignored `inventory/local/` tree
for supported secret variables.

## Public issue hygiene

A public issue may describe the existence and impact of a security problem after
it is safe to do so, but it should not contain working credentials, personal
deployment information, or unnecessary exploit details that put active systems
at risk.
