#!/usr/bin/env python3
"""
HamStack local-inventory configurator.

This intentionally edits only inventory/local/, which is ignored by Git.
It is a convenience layer over the documented YAML configuration model, not a
replacement for that model.
"""

from __future__ import annotations

import argparse
import copy
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print(
        "PyYAML is required. Activate the HamStack development environment or run:\n"
        "  python -m pip install PyYAML",
        file=sys.stderr,
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "inventory" / "example"
LOCAL = ROOT / "inventory" / "local"
HOSTS_FILE = LOCAL / "hosts.yml"
NETWORK_FILE = LOCAL / "network.yml"
SITE_FILE = LOCAL / "group_vars" / "all.yml"
VAULT_DIR = LOCAL / "group_vars" / "all"
VAULT_FILE = VAULT_DIR / "vault.yml"
VAULT_TEMPLATE = VAULT_DIR / "vault.yml.example"
HOST_VARS = LOCAL / "host_vars"
ROLES_DIR = ROOT / "roles"


def load_yaml(path: Path, default: Any) -> Any:
    if not path.exists():
        return copy.deepcopy(default)
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return copy.deepcopy(default) if data is None else data


def atomic_dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = yaml.safe_dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
        prefix=f".{path.name}.",
    ) as handle:
        handle.write("---\n")
        handle.write(payload)
        tmp = Path(handle.name)
    os.replace(tmp, path)


def prompt(label: str, current: Any = None, *, required: bool = False) -> str:
    suffix = ""
    if current not in (None, ""):
        suffix = f" [{current}]"
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if current not in (None, ""):
            return str(current)
        if not required:
            return ""
        print("A value is required.")


def yes_no(label: str, current: bool = False) -> bool:
    default = "Y/n" if current else "y/N"
    while True:
        raw = input(f"{label} [{default}]: ").strip().lower()
        if not raw:
            return current
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Enter y or n.")


def choose(title: str, options: list[str], *, allow_back: bool = True) -> int | None:
    print(f"\n{title}")
    for idx, item in enumerate(options, 1):
        print(f"  {idx}. {item}")
    if allow_back:
        print("  0. Back")
    while True:
        raw = input("> ").strip()
        if allow_back and raw == "0":
            return None
        try:
            idx = int(raw)
        except ValueError:
            print("Enter a menu number.")
            continue
        if 1 <= idx <= len(options):
            return idx - 1
        print("Enter a valid menu number.")


def ensure_local() -> None:
    if LOCAL.exists():
        return
    shutil.copytree(EXAMPLE, LOCAL)
    print(f"Created {LOCAL.relative_to(ROOT)} from inventory/example.")


def site_menu() -> None:
    site = load_yaml(SITE_FILE, {})
    fields = [
        ("hamstack_site_name", "Site/deployment name"),
        ("hamstack_event_name", "Event name (optional)"),
        ("hamstack_callsign", "Primary callsign"),
        ("hamstack_grid_locator", "Grid locator"),
        ("hamstack_country_code", "Country code"),
        ("hamstack_timezone", "Timezone"),
        ("hamstack_locale", "Locale"),
    ]
    for key, label in fields:
        site[key] = prompt(label, site.get(key, ""))
    atomic_dump(SITE_FILE, site)
    print("Saved site settings.")


def hosts_dict() -> dict[str, Any]:
    inventory = load_yaml(HOSTS_FILE, {"all": {"hosts": {}}})
    inventory.setdefault("all", {}).setdefault("hosts", {})
    return inventory


def host_names() -> list[str]:
    return sorted(hosts_dict()["all"]["hosts"].keys())


def host_file(name: str) -> Path:
    return HOST_VARS / f"{name}.yml"


def select_host() -> str | None:
    names = host_names()
    if not names:
        print("No hosts are defined.")
        return None
    idx = choose("Select host", names)
    return None if idx is None else names[idx]


def add_host() -> None:
    inventory = hosts_dict()
    hosts = inventory["all"]["hosts"]

    name = prompt("Inventory hostname", required=True)
    if name in hosts:
        print(f"{name} already exists.")
        return

    address = prompt("IP address or DNS name", required=True)
    ansible_user = prompt("SSH automation user", "hamstack")

    hosts[name] = {
        "ansible_host": address,
        "ansible_user": ansible_user,
    }
    atomic_dump(HOSTS_FILE, inventory)

    data = {
        "hamstack_manage_hostname": False,
        "hamstack_hostname": name,
        "hamstack_operator_user": "",
        "hamstack_devices": {},
        "hamstack_radios": {},
    }
    operator = prompt("Desktop/operator Linux user (optional)")
    if operator:
        data["hamstack_operator_user"] = operator
    atomic_dump(host_file(name), data)

    # Remove the copied example host after the first real host is added.
    if name != "example-node" and "example-node" in hosts:
        if yes_no("Remove the example-node inventory entry", True):
            hosts.pop("example-node", None)
            atomic_dump(HOSTS_FILE, inventory)
            sample = host_file("example-node")
            if sample.exists():
                sample.unlink()

    print(f"Added {name}.")


def edit_host() -> None:
    name = select_host()
    if not name:
        return

    inventory = hosts_dict()
    entry = inventory["all"]["hosts"][name]
    data = load_yaml(host_file(name), {})

    entry["ansible_host"] = prompt("IP address or DNS name", entry.get("ansible_host", ""))
    entry["ansible_user"] = prompt("SSH automation user", entry.get("ansible_user", "hamstack"))
    data["hamstack_manage_hostname"] = yes_no(
        "Manage OS hostname",
        bool(data.get("hamstack_manage_hostname", False)),
    )
    data["hamstack_hostname"] = prompt(
        "Desired OS hostname",
        data.get("hamstack_hostname", name),
    )
    data["hamstack_operator_user"] = prompt(
        "Desktop/operator Linux user (optional)",
        data.get("hamstack_operator_user", ""),
    )

    atomic_dump(HOSTS_FILE, inventory)
    atomic_dump(host_file(name), data)
    print(f"Saved {name}.")


def remove_host() -> None:
    name = select_host()
    if not name:
        return
    if not yes_no(f"Remove {name} from the local inventory", False):
        return
    inventory = hosts_dict()
    inventory["all"]["hosts"].pop(name, None)
    atomic_dump(HOSTS_FILE, inventory)
    path = host_file(name)
    if path.exists() and yes_no(f"Delete {path.relative_to(ROOT)} too", True):
        path.unlink()
    print(f"Removed {name}.")


def hosts_menu() -> None:
    while True:
        options = [f"Add host", "Edit host", "Remove host", "List hosts"]
        choice = choose("Hosts", options)
        if choice is None:
            return
        if choice == 0:
            add_host()
        elif choice == 1:
            edit_host()
        elif choice == 2:
            remove_host()
        else:
            names = host_names()
            print("\n".join(f"  - {x}" for x in names) if names else "No hosts.")


DEVICE_ENDPOINTS = {
    "aioc": ["serial", "audio_capture", "audio_playback"],
    "digirig": ["serial", "audio_capture", "audio_playback"],
    "rtl_sdr": ["usb"],
    "camera": ["video"],
    "hid": ["hid"],
    "gps": ["serial", "pps"],
    "generic_usb_audio": ["audio_capture", "audio_playback"],
    "other": [],
}


def hardware_menu() -> None:
    name = select_host()
    if not name:
        return
    path = host_file(name)
    data = load_yaml(path, {})
    devices = data.setdefault("hamstack_devices", {})
    radios = data.setdefault("hamstack_radios", {})

    while True:
        options = [
            "List devices/radios",
            "Add device",
            "Remove device",
            "Add radio",
            "Remove radio",
        ]
        choice = choose(f"Hardware: {name}", options)
        if choice is None:
            atomic_dump(path, data)
            return

        if choice == 0:
            print("\nDevices:")
            for key, val in devices.items():
                print(f"  {key}: {val.get('type', 'unknown')} — {val.get('description', '')}")
            print("Radios:")
            for key, val in radios.items():
                print(
                    f"  {key}: {val.get('model', 'unknown')} "
                    f"(interface={val.get('interface', '')})"
                )

        elif choice == 1:
            key = prompt("Device resource name", required=True)
            types = list(DEVICE_ENDPOINTS)
            idx = choose("Device type", types)
            if idx is None:
                continue
            dtype = types[idx]
            description = prompt("Description")
            endpoints: dict[str, str] = {}
            for endpoint in DEVICE_ENDPOINTS[dtype]:
                endpoints[endpoint] = prompt(f"{endpoint} path/name (optional)")
            match = {
                "usb_vendor_id": prompt("USB vendor ID (optional)"),
                "usb_product_id": prompt("USB product ID (optional)"),
                "usb_serial": prompt("USB serial (optional)"),
            }
            match = {k: v for k, v in match.items() if v}
            devices[key] = {
                "type": dtype,
                "description": description,
                "match": match,
                "endpoints": endpoints,
                "options": {},
            }
            atomic_dump(path, data)

        elif choice == 2:
            keys = sorted(devices)
            if not keys:
                print("No devices.")
                continue
            idx = choose("Remove device", keys)
            if idx is not None and yes_no(f"Remove {keys[idx]}", False):
                devices.pop(keys[idx], None)
                atomic_dump(path, data)

        elif choice == 3:
            key = prompt("Radio resource name", required=True)
            model = prompt("Radio model", required=True)
            description = prompt("Description")
            interfaces = sorted(devices)
            interface = ""
            if interfaces:
                idx = choose("Interface device", interfaces)
                if idx is not None:
                    interface = interfaces[idx]
            radios[key] = {
                "model": model,
                "description": description,
                "interface": interface,
                "cat": {},
                "ptt": {},
                "options": {},
            }
            atomic_dump(path, data)

        elif choice == 4:
            keys = sorted(radios)
            if not keys:
                print("No radios.")
                continue
            idx = choose("Remove radio", keys)
            if idx is not None and yes_no(f"Remove {keys[idx]}", False):
                radios.pop(keys[idx], None)
                atomic_dump(path, data)



def network_inventory() -> dict[str, Any]:
    inventory = load_yaml(
        NETWORK_FILE,
        {"all": {"children": {"network_devices": {"hosts": {}}}}},
    )
    inventory.setdefault("all", {}).setdefault("children", {}).setdefault(
        "network_devices", {}
    ).setdefault("hosts", {})
    return inventory


def network_devices() -> dict[str, Any]:
    return network_inventory()["all"]["children"]["network_devices"]["hosts"]


def select_network_device() -> str | None:
    names = sorted(network_devices())
    if not names:
        print("No network devices are defined.")
        return None
    idx = choose("Select network device", names)
    return None if idx is None else names[idx]


def add_network_device() -> None:
    inventory = network_inventory()
    devices = inventory["all"]["children"]["network_devices"]["hosts"]

    name = prompt("Inventory device name", required=True)
    if name in devices:
        print(f"{name} already exists.")
        return

    address = prompt("Management IP address or DNS name", required=True)
    platforms = ["openwrt", "routeros"]
    idx = choose("Platform", platforms)
    if idx is None:
        return
    platform = platforms[idx]

    default_user = "root" if platform == "openwrt" else "hamstack"
    devices[name] = {
        "ansible_host": address,
        "ansible_user": prompt("Management username", default_user),
        "hamstack_network_platform": platform,
        "hamstack_network_vendor": prompt(
            "Vendor/family",
            "glinet" if platform == "openwrt" else "mikrotik",
        ),
        "hamstack_network_model": prompt("Model (optional)"),
        "hamstack_network_hostname": prompt("Desired hostname (optional)", name),
        "hamstack_network_lans": [],
        "hamstack_network_wifi": [],
        "hamstack_network_routes": [],
        "hamstack_network_firewall_zones": [],
        "hamstack_network_extra_settings": {},
    }
    atomic_dump(NETWORK_FILE, inventory)
    print(f"Added network device {name}.")


def edit_network_device() -> None:
    name = select_network_device()
    if not name:
        return
    inventory = network_inventory()
    data = inventory["all"]["children"]["network_devices"]["hosts"][name]

    data["ansible_host"] = prompt(
        "Management IP address or DNS name",
        data.get("ansible_host", ""),
    )
    data["ansible_user"] = prompt(
        "Management username",
        data.get("ansible_user", ""),
    )
    data["hamstack_network_vendor"] = prompt(
        "Vendor/family",
        data.get("hamstack_network_vendor", ""),
    )
    data["hamstack_network_model"] = prompt(
        "Model",
        data.get("hamstack_network_model", ""),
    )
    data["hamstack_network_hostname"] = prompt(
        "Desired hostname",
        data.get("hamstack_network_hostname", name),
    )
    atomic_dump(NETWORK_FILE, inventory)
    print(f"Saved {name}.")


def remove_network_device() -> None:
    name = select_network_device()
    if not name:
        return
    if not yes_no(f"Remove network device {name}", False):
        return
    inventory = network_inventory()
    inventory["all"]["children"]["network_devices"]["hosts"].pop(name, None)
    atomic_dump(NETWORK_FILE, inventory)
    print(f"Removed {name}.")


def network_devices_menu() -> None:
    while True:
        options = [
            "Add network device",
            "Edit network device",
            "Remove network device",
            "List network devices",
        ]
        choice = choose("Network devices", options)
        if choice is None:
            return
        if choice == 0:
            add_network_device()
        elif choice == 1:
            edit_network_device()
        elif choice == 2:
            remove_network_device()
        else:
            devices = network_devices()
            if not devices:
                print("No network devices.")
            for name, item in sorted(devices.items()):
                print(
                    f"  - {name}: {item.get('hamstack_network_platform', '?')} "
                    f"{item.get('hamstack_network_model', '')} "
                    f"@ {item.get('ansible_host', '?')}"
                )


def discover_roles() -> list[tuple[str, Path, dict[str, Any], str | None]]:
    found: list[tuple[str, Path, dict[str, Any], str | None]] = []
    for defaults in sorted(ROLES_DIR.rglob("defaults/main.yml")):
        rel = defaults.parent.parent.relative_to(ROLES_DIR).as_posix()
        values = load_yaml(defaults, {})
        enabled = next(
            (
                key
                for key, value in values.items()
                if key.startswith("hamstack_")
                and key.endswith("_enabled")
                and isinstance(value, bool)
            ),
            None,
        )
        found.append((rel, defaults, values, enabled))
    return found


def parse_value(raw: str, current: Any) -> Any:
    if isinstance(current, bool):
        low = raw.lower()
        if low in {"true", "yes", "y", "1", "on"}:
            return True
        if low in {"false", "no", "n", "0", "off"}:
            return False
    try:
        return yaml.safe_load(raw)
    except yaml.YAMLError:
        return raw


def role_menu() -> None:
    name = select_host()
    if not name:
        return
    path = host_file(name)
    data = load_yaml(path, {})
    roles = discover_roles()

    while True:
        labels = []
        for rel, _, defaults, enabled_key in roles:
            state = ""
            if enabled_key:
                state_value = data.get(enabled_key, defaults.get(enabled_key, False))
                state = " [ON]" if state_value else " [off]"
            labels.append(rel + state)
        idx = choose(f"Roles: {name}", labels)
        if idx is None:
            atomic_dump(path, data)
            return

        rel, _, defaults, enabled_key = roles[idx]
        while True:
            actions = []
            if enabled_key:
                actions.append("Toggle enabled")
            actions += ["Edit role variable", "Show current overrides"]
            action = choose(f"Role {rel}", actions)
            if action is None:
                break

            offset = 0
            if enabled_key:
                if action == 0:
                    current = bool(data.get(enabled_key, defaults[enabled_key]))
                    data[enabled_key] = not current
                    print(f"{enabled_key} = {data[enabled_key]}")
                    atomic_dump(path, data)
                    continue
                offset = 1

            if action == offset:
                keys = [k for k in defaults if k.startswith("hamstack_")]
                key_idx = choose("Variable", keys)
                if key_idx is None:
                    continue
                key = keys[key_idx]
                current = data.get(key, defaults[key])
                print(f"Default/current value: {current!r}")
                raw = input(
                    "New YAML value (blank = leave unchanged; complex values may be "
                    "entered as inline YAML): "
                ).strip()
                if raw:
                    data[key] = parse_value(raw, current)
                    atomic_dump(path, data)
            else:
                overrides = {
                    key: value
                    for key, value in data.items()
                    if key in defaults
                }
                print(yaml.safe_dump(overrides, sort_keys=False).rstrip() or "(none)")


def vault_menu() -> None:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    ansible_vault = shutil.which("ansible-vault")
    if not ansible_vault:
        print(
            "ansible-vault is not in PATH. Activate the HamStack Ansible "
            "environment first."
        )
        return

    if VAULT_FILE.exists():
        subprocess.run([ansible_vault, "edit", str(VAULT_FILE)], check=False)
        return

    if not VAULT_TEMPLATE.exists():
        print(f"Vault template not found: {VAULT_TEMPLATE}")
        return

    if not yes_no("Create an encrypted site Vault from the template", True):
        return

    VAULT_FILE.write_text(VAULT_TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run([ansible_vault, "encrypt", str(VAULT_FILE)], check=False)
    if result.returncode != 0:
        print("Vault encryption failed; deleting the temporary plaintext vault.")
        VAULT_FILE.unlink(missing_ok=True)
        return
    subprocess.run([ansible_vault, "edit", str(VAULT_FILE)], check=False)


def validate() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not LOCAL.exists():
        errors.append("inventory/local does not exist; run the configurator first.")
    else:
        inventory = hosts_dict()
        hosts = inventory["all"]["hosts"]
        if not hosts:
            errors.append("No hosts are defined.")
        if "example-node" in hosts:
            warnings.append("example-node is still present in the local inventory.")

        site = load_yaml(SITE_FILE, {})
        if site.get("hamstack_callsign") in {"", "N0CALL", None}:
            warnings.append("hamstack_callsign is still unset/N0CALL.")

        for name in hosts:
            path = host_file(name)
            if not path.exists():
                errors.append(f"Missing host_vars file for {name}.")
                continue
            data = load_yaml(path, {})
            devices = data.get("hamstack_devices", {}) or {}
            radios = data.get("hamstack_radios", {}) or {}
            for radio_name, radio in radios.items():
                interface = (radio or {}).get("interface", "")
                if interface and interface not in devices:
                    errors.append(
                        f"{name}: radio {radio_name} references unknown "
                        f"device {interface}."
                    )


    if NETWORK_FILE.exists():
        try:
            net_inventory = network_inventory()
            net_devices = net_inventory["all"]["children"]["network_devices"]["hosts"]
            for name, item in net_devices.items():
                platform = (item or {}).get("hamstack_network_platform", "")
                if platform not in {"openwrt", "routeros"}:
                    errors.append(
                        f"{name}: unsupported hamstack_network_platform {platform!r}."
                    )
                if not (item or {}).get("ansible_host"):
                    errors.append(f"{name}: missing ansible_host.")
        except Exception as exc:
            errors.append(f"Network inventory validation failed: {exc}")

    try:
        discover_roles()
    except Exception as exc:  # defensive: YAML/schema problems should surface.
        errors.append(f"Role-default discovery failed: {exc}")

    print("\nValidation")
    for item in warnings:
        print(f"  WARNING: {item}")
    for item in errors:
        print(f"  ERROR: {item}")
    if not warnings and not errors:
        print("  Local inventory structure looks sane.")

    # Optional deeper Ansible parser check.
    ansible_playbook = shutil.which("ansible-playbook")
    if ansible_playbook and LOCAL.exists() and not VAULT_FILE.exists():
        result = subprocess.run(
            [
                ansible_playbook,
                "-i",
                str(HOSTS_FILE),
                str(ROOT / "playbooks" / "site.yml"),
                "--syntax-check",
            ],
            cwd=ROOT,
            check=False,
        )
        if result.returncode:
            errors.append("ansible-playbook --syntax-check failed.")
    elif VAULT_FILE.exists():
        print(
            "  NOTE: encrypted Vault present; automatic syntax-check skipped "
            "to avoid prompting for the Vault password."
        )

    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure HamStack inventory/local")
    parser.add_argument("--init", action="store_true", help="create inventory/local and exit")
    parser.add_argument("--validate", action="store_true", help="validate local configuration and exit")
    args = parser.parse_args()

    if args.init:
        ensure_local()
        return 0
    if args.validate:
        return validate()

    ensure_local()

    while True:
        options = [
            "Site settings",
            "Hosts",
            "Host hardware/resources",
            "Role configuration",
            "Network devices",
            "Secrets / Ansible Vault",
            "Validate configuration",
            "Exit",
        ]
        choice = choose("HamStack configurator", options, allow_back=False)
        assert choice is not None

        if choice == 0:
            site_menu()
        elif choice == 1:
            hosts_menu()
        elif choice == 2:
            hardware_menu()
        elif choice == 3:
            role_menu()
        elif choice == 4:
            network_devices_menu()
        elif choice == 5:
            vault_menu()
        elif choice == 6:
            validate()
        else:
            print("Configuration lives under inventory/local/.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
