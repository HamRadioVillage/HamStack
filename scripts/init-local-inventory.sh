#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="${repo_root}/inventory/example"
target_dir="${repo_root}/inventory/local"

if [[ -e "${target_dir}" ]]; then
  echo "Refusing to overwrite ${target_dir}" >&2
  echo "Remove it yourself if you intentionally want to start over." >&2
  exit 1
fi

cp -R "${source_dir}" "${target_dir}"

cat <<'EOF'
Created inventory/local from inventory/example.

Next:
  1. Edit inventory/local/hosts.yml.
  2. Rename inventory/local/host_vars/example-node.yml to match your host.
  3. Edit inventory/local/group_vars/all.yml.
  4. Create inventory/local/group_vars/all/vault.yml with ansible-vault if you need secrets.
     Template: inventory/local/group_vars/all/vault.yml.example
  5. Run: ansible all -m ping

inventory/local is ignored by Git.
EOF
