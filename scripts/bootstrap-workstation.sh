#!/usr/bin/env bash
set -Eeuo pipefail

mode="controller"
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
HamStack workstation bootstrap

Prepares a Debian-family machine to run the HamStack controller or development
profile from an already-provided/unzipped source tree.

Usage:
  ./scripts/bootstrap-workstation.sh [--mode controller|dev] [--repo PATH]

The script installs only enough host tooling to create the repository-local
Python virtual environment, installs HamStack's Python requirements and Ansible
collections, then prints the profile command to run.

It does not clone/update a Git repository and should be run as the normal
operator account (it invokes sudo only for apt).
EOF
}

die() { printf '[hamstack-workstation] ERROR: %s\n' "$*" >&2; exit 1; }
log() { printf '[hamstack-workstation] %s\n' "$*"; }

while (($#)); do
  case "$1" in
    --mode)
      [[ $# -ge 2 ]] || die '--mode requires a value'
      mode="$2"; shift 2 ;;
    --repo)
      [[ $# -ge 2 ]] || die '--repo requires a value'
      repo="$(cd "$2" && pwd)"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

[[ "$mode" == controller || "$mode" == dev ]] || die '--mode must be controller or dev'
[[ $EUID -ne 0 ]] || die 'run this script as the normal operator user, not root'
command -v apt-get >/dev/null 2>&1 || die 'this bootstrap currently requires apt'
[[ -f "$repo/requirements-controller.txt" ]] || die "not a HamStack source tree: $repo"

log 'Installing workstation bootstrap prerequisites.'
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  ca-certificates curl openssh-client python3 python3-pip python3-venv rsync unzip

python3 -m venv "$repo/.venv"
"$repo/.venv/bin/python" -m pip install --upgrade pip
if [[ "$mode" == dev ]]; then
  "$repo/.venv/bin/pip" install -r "$repo/requirements-dev.txt"
  profile='dev-workstation.yml'
  role_user_var='hamstack_dev_user'
  role_repo_var='hamstack_dev_repo_path'
else
  "$repo/.venv/bin/pip" install -r "$repo/requirements-controller.txt"
  profile='control-station.yml'
  role_user_var='hamstack_controller_user'
  role_repo_var='hamstack_controller_repo_path'
fi
"$repo/.venv/bin/ansible-galaxy" collection install -r "$repo/requirements.yml"

cat <<EOF

HamStack ${mode} bootstrap complete.

Activate the environment:
  source "$repo/.venv/bin/activate"

Then converge this workstation:
  ansible-playbook -i 'localhost,' -c local \\
    "$repo/playbooks/profiles/$profile" \\
    -e hamstack_profile_hosts=localhost \\
    -e hamstack_operator_user="$USER" \\
    -e $role_user_var="$USER" \\
    --ask-become-pass

EOF
