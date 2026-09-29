#!/usr/bin/env bash
set -Eeuo pipefail

HAMSTACK_BOOTSTRAP_VERSION="0.1.0"

hamstack_user="${HAMSTACK_USER:-hamstack}"
authorized_key="${HAMSTACK_AUTHORIZED_KEY:-}"
authorized_key_file=""
copy_key_from=""
passwordless_sudo=true
start_ssh=true

log() {
  printf '[hamstack-bootstrap] %s\n' "$*"
}

warn() {
  printf '[hamstack-bootstrap] WARNING: %s\n' "$*" >&2
}

die() {
  printf '[hamstack-bootstrap] ERROR: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'EOF'
HamStack node bootstrap

Prepares a supported vanilla Linux node so it can be managed by Ansible.

Usage:
  sudo ./bootstrap-node.sh [options]

  curl -fsSL https://raw.githubusercontent.com/HamRadioVillage/HamStack/v0.1.0/scripts/bootstrap-node.sh \
    | sudo bash -s -- [options]

Options:
  --user USER
      Automation account to create/use. Default: hamstack

  --authorized-key "PUBLIC_KEY"
      Add one SSH public key to the automation account.

  --authorized-key-file PATH
      Add public key(s) from a file already present on the target node.

  --copy-key-from USER
      Copy public key(s) from USER's ~/.ssh/authorized_keys.

  --no-passwordless-sudo
      Do not grant the automation account passwordless sudo.
      If HamStack needs privilege escalation, the operator must provide
      another become mechanism to Ansible.

  --no-start-ssh
      Install the SSH server if necessary, but do not enable/start it.

  -h, --help
      Show this help.

Environment:
  HAMSTACK_USER
      Alternate default for --user.

  HAMSTACK_AUTHORIZED_KEY
      Alternate way to provide one SSH public key.

Behavior:
  * Currently supports Debian-family systems with apt.
  * Installs only the target-side prerequisites HamStack needs:
      python3, python3-apt, sudo, openssh-server, ca-certificates
  * Creates or reuses the automation account.
  * Grants passwordless sudo by default.
  * Does not disable password authentication.
  * Does not change PermitRootLogin.
  * Does not install Ansible on the target.
  * Safe to run repeatedly.

If no SSH key option is supplied and the script is invoked with sudo, the
script will try to copy the invoking user's existing authorized_keys file.
EOF
}

while (($#)); do
  case "$1" in
    --user)
      [[ $# -ge 2 ]] || die "--user requires a value"
      hamstack_user="$2"
      shift 2
      ;;
    --authorized-key)
      [[ $# -ge 2 ]] || die "--authorized-key requires a value"
      authorized_key="$2"
      shift 2
      ;;
    --authorized-key-file)
      [[ $# -ge 2 ]] || die "--authorized-key-file requires a value"
      authorized_key_file="$2"
      shift 2
      ;;
    --copy-key-from)
      [[ $# -ge 2 ]] || die "--copy-key-from requires a value"
      copy_key_from="$2"
      shift 2
      ;;
    --no-passwordless-sudo)
      passwordless_sudo=false
      shift
      ;;
    --no-start-ssh)
      start_ssh=false
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "Unknown argument: $1 (use --help)"
      ;;
  esac
done

[[ ${EUID} -eq 0 ]] || die "Run this script as root or through sudo."

[[ "$hamstack_user" =~ ^[a-z_][a-z0-9_-]*[$]?$ ]] \
  || die "Invalid Linux user name: ${hamstack_user}"

if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  source /etc/os-release
else
  die "Cannot identify the operating system: /etc/os-release is missing."
fi

if ! command -v apt-get >/dev/null 2>&1; then
  die "Bootstrap v${HAMSTACK_BOOTSTRAP_VERSION} currently supports Debian-family systems with apt only."
fi

log "HamStack bootstrap v${HAMSTACK_BOOTSTRAP_VERSION}"
log "Detected ${PRETTY_NAME:-${ID:-unknown}}"

required_packages=(
  python3
  python3-apt
  sudo
  openssh-server
  ca-certificates
)

missing_packages=()
for package in "${required_packages[@]}"; do
  if ! dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q '^install ok installed$'; then
    missing_packages+=("$package")
  fi
done

if ((${#missing_packages[@]})); then
  log "Installing target prerequisites: ${missing_packages[*]}"
  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y --no-install-recommends "${missing_packages[@]}"
else
  log "Target prerequisites are already installed."
fi

if id "$hamstack_user" >/dev/null 2>&1; then
  log "Automation user ${hamstack_user} already exists."
else
  log "Creating automation user ${hamstack_user}."
  useradd --create-home --shell /bin/bash "$hamstack_user"
fi

if getent group sudo >/dev/null 2>&1; then
  usermod -aG sudo "$hamstack_user"
else
  die "Expected sudo group does not exist on this system."
fi

sudoers_file="/etc/sudoers.d/90-hamstack-ansible"
if [[ "$passwordless_sudo" == true ]]; then
  tmp_sudoers="$(mktemp)"
  trap 'rm -f "${tmp_sudoers:-}"' EXIT
  printf '%s ALL=(ALL:ALL) NOPASSWD: ALL\n' "$hamstack_user" > "$tmp_sudoers"
  chmod 0440 "$tmp_sudoers"

  if ! visudo -cf "$tmp_sudoers" >/dev/null; then
    die "Generated sudoers configuration failed validation."
  fi

  install -o root -g root -m 0440 "$tmp_sudoers" "$sudoers_file"
  rm -f "$tmp_sudoers"
  trap - EXIT
  log "Configured passwordless sudo for ${hamstack_user}."
else
  if [[ -e "$sudoers_file" ]]; then
    rm -f "$sudoers_file"
    log "Removed HamStack-managed passwordless sudo configuration."
  fi
fi

user_home="$(getent passwd "$hamstack_user" | cut -d: -f6)"
[[ -n "$user_home" ]] || die "Could not determine home directory for ${hamstack_user}."
user_group="$(id -gn "$hamstack_user")"

install -d -o "$hamstack_user" -g "$user_group" -m 0700 "${user_home}/.ssh"
authorized_keys_path="${user_home}/.ssh/authorized_keys"
touch "$authorized_keys_path"
chown "$hamstack_user:$user_group" "$authorized_keys_path"
chmod 0600 "$authorized_keys_path"

append_keys_from_file() {
  local source_file="$1"
  [[ -r "$source_file" ]] || die "Cannot read SSH key file: ${source_file}"

  local added=0
  while IFS= read -r key_line || [[ -n "$key_line" ]]; do
    [[ -z "$key_line" ]] && continue
    [[ "$key_line" =~ ^[[:space:]]*# ]] && continue

    if ! grep -Fqx -- "$key_line" "$authorized_keys_path"; then
      printf '%s\n' "$key_line" >> "$authorized_keys_path"
      added=$((added + 1))
    fi
  done < "$source_file"

  chown "$hamstack_user:$user_group" "$authorized_keys_path"
  chmod 0600 "$authorized_keys_path"
  log "Added ${added} new SSH public key(s) for ${hamstack_user}."
}

key_configured=false

if [[ -n "$authorized_key" ]]; then
  tmp_key="$(mktemp)"
  trap 'rm -f "${tmp_key:-}"' EXIT
  printf '%s\n' "$authorized_key" > "$tmp_key"
  append_keys_from_file "$tmp_key"
  rm -f "$tmp_key"
  trap - EXIT
  key_configured=true
elif [[ -n "$authorized_key_file" ]]; then
  append_keys_from_file "$authorized_key_file"
  key_configured=true
else
  if [[ -z "$copy_key_from" && -n "${SUDO_USER:-}" && "${SUDO_USER}" != "root" ]]; then
    copy_key_from="${SUDO_USER}"
  fi

  if [[ -n "$copy_key_from" ]]; then
    source_home="$(getent passwd "$copy_key_from" | cut -d: -f6 || true)"
    source_keys="${source_home}/.ssh/authorized_keys"

    if [[ -n "$source_home" && -s "$source_keys" ]]; then
      log "Copying authorized SSH key(s) from ${copy_key_from}."
      append_keys_from_file "$source_keys"
      key_configured=true
    else
      warn "No authorized_keys file found for ${copy_key_from}; no SSH key was installed."
    fi
  fi
fi

if [[ "$key_configured" != true ]]; then
  warn "No SSH public key was configured for ${hamstack_user}."
  warn "Add one before attempting key-based Ansible access."
fi

if [[ "$start_ssh" == true ]]; then
  if command -v systemctl >/dev/null 2>&1; then
    if systemctl list-unit-files ssh.service >/dev/null 2>&1; then
      systemctl enable --now ssh.service
      log "SSH service is enabled and running."
    elif systemctl list-unit-files sshd.service >/dev/null 2>&1; then
      systemctl enable --now sshd.service
      log "SSHD service is enabled and running."
    else
      warn "Could not identify an SSH systemd unit to enable."
    fi
  elif command -v service >/dev/null 2>&1; then
    service ssh start || service sshd start || warn "Could not start the SSH service."
  else
    warn "No supported service manager found; verify that sshd is running."
  fi
fi

install -d -o root -g root -m 0755 /etc/hamstack
cat > /etc/hamstack/bootstrap <<EOF
bootstrap_version=${HAMSTACK_BOOTSTRAP_VERSION}
automation_user=${hamstack_user}
bootstrapped_at=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
EOF
chmod 0644 /etc/hamstack/bootstrap

python_version="$(python3 --version 2>&1 || true)"
host_name="$(hostname -f 2>/dev/null || hostname)"
host_addresses="$(hostname -I 2>/dev/null | xargs || true)"

cat <<EOF

HamStack bootstrap complete.

  Host:             ${host_name}
  Address(es):      ${host_addresses:-unknown}
  Automation user: ${hamstack_user}
  Python:           ${python_version:-unknown}
  Passwordless sudo: ${passwordless_sudo}

Next, add this node to inventory/local/hosts.yml on your Ansible control host
and test it with:

  ansible all -m ping

Then apply the HamStack baseline with:

  ansible-playbook playbooks/bootstrap.yml

EOF
