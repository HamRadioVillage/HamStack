#!/usr/bin/env python3
"""Fast, offline repository QA for HamStack development."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment
from yaml.constructor import ConstructorError

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def error(msg: str) -> None:
    ERRORS.append(msg)
    print(f"ERROR: {msg}")


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found unhashable key ({exc})",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def check_yaml() -> None:
    for path in sorted(list(ROOT.rglob("*.yml")) + list(ROOT.rglob("*.yaml"))):
        if ".venv" in path.parts or "inventory/local" in path.as_posix():
            continue
        try:
            yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        except Exception as exc:
            error(f"YAML parse failed: {path.relative_to(ROOT)}: {exc}")


def check_jinja() -> None:
    env = Environment()
    for path in sorted(ROOT.rglob("*.j2")):
        try:
            env.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            error(f"Jinja parse failed: {path.relative_to(ROOT)}: {exc}")


def check_python() -> None:
    for path in sorted((ROOT / "scripts").glob("*.py")):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)],
            capture_output=True,
            text=True,
        )
        if result.returncode:
            error(f"Python compile failed: {path.relative_to(ROOT)}: {result.stderr.strip()}")


def check_shell() -> None:
    for path in sorted((ROOT / "scripts").glob("*.sh")):
        result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
        if result.returncode:
            error(f"Shell syntax failed: {path.relative_to(ROOT)}: {result.stderr.strip()}")


def check_markdown_links() -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    paths = (
        list(ROOT.glob("*.md"))
        + list((ROOT / "docs").rglob("*.md"))
        + list((ROOT / "roles").rglob("README.md"))
    )
    for path in sorted(paths):
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                error(f"Broken Markdown link: {path.relative_to(ROOT)} -> {target}")


def check_role_layout() -> None:
    for path in (ROOT / "roles").rglob("main.yml"):
        rel = path.relative_to(ROOT / "roles")
        if path.parent.name not in {"tasks", "defaults", "handlers", "meta", "vars"}:
            error(f"Suspicious role-root main.yml: roles/{rel}")


def check_variable_reference() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate-variable-reference.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        error(result.stdout.strip() or result.stderr.strip() or "Variable reference is stale")


def _implemented_roles() -> set[str]:
    status = ROOT / "docs" / "role-status.md"
    if not status.exists():
        return set()
    text = status.read_text(encoding="utf-8")
    section = text.split("## Implemented or runnable roles", 1)
    if len(section) != 2:
        return set()
    body = section[1].split("## ", 1)[0]
    return set(re.findall(r"^- `([^`]+)`", body, flags=re.MULTILINE))


def _role_path(role: str) -> Path:
    if role == "common":
        return ROOT / "roles" / "common"
    return ROOT / "roles" / role


def _is_fail_fast_stub(tasks_path: Path) -> bool:
    try:
        data = yaml.load(tasks_path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except Exception:
        return False
    if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
        return False
    return "ansible.builtin.fail" in data[0] or "fail" in data[0]


def check_role_documentation_consistency() -> None:
    for role in sorted(_implemented_roles()):
        role_path = _role_path(role)
        tasks = role_path / "tasks" / "main.yml"
        readme = role_path / "README.md"
        if not tasks.exists():
            error(f"Role status marks {role!r} implemented but {tasks.relative_to(ROOT)} is missing")
            continue
        if _is_fail_fast_stub(tasks):
            error(f"Role status marks {role!r} implemented but its task file is only a fail-fast stub")
        if readme.exists():
            lower = readme.read_text(encoding="utf-8").lower()
            for stale in (
                "design intent / implementation pending",
                "schema/inventory placeholder only",
                "initial implementation in progress",
            ):
                if stale in lower:
                    error(f"Role status marks {role!r} implemented but README still says {stale!r}")


def check_deprecated_paths() -> None:
    scans = [ROOT / "README.md", ROOT / "docs", ROOT / "scripts", ROOT / "playbooks", ROOT / "roles"]
    forbidden = [
        "inventory/local/group_vars/vault.yml",
        "inventory/example/group_vars/vault.example.yml",
        "examples/dc34-linbpq.yml",
        "roles/services/hamstack-dashboard",
        "hamstack_dashboard_",
    ]
    paths: list[Path] = []
    for root in scans:
        if root.is_file():
            paths.append(root)
        elif root.exists():
            paths.extend(p for p in root.rglob("*") if p.is_file())
    for path in paths:
        if path.resolve() == (ROOT / "scripts" / "qa.py").resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in forbidden:
            if token in text:
                error(f"Deprecated path/reference {token!r} in {path.relative_to(ROOT)}")

    deprecated_files = [
        ROOT / "group_vars" / "all" / "vault.yml.example",
        ROOT / "inventory" / "example" / "group_vars" / "vault.example.yml",
        ROOT / "roles" / "packet" / "graywolf" / "main.yml",
    ]
    for path in deprecated_files:
        if path.exists():
            error(f"Deprecated duplicate/stray file exists: {path.relative_to(ROOT)}")


def check_public_placeholders() -> None:
    placeholders = ("<RAW_URL>", "<HAMSTACK_RAW_URL>")
    paths = [ROOT / "README.md", ROOT / "docs", ROOT / "scripts", ROOT / "roles"]
    for base in paths:
        candidates = [base] if base.is_file() else [p for p in base.rglob("*") if p.is_file()]
        for path in candidates:
            if path.resolve() == (ROOT / "scripts" / "qa.py").resolve():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for placeholder in placeholders:
                if placeholder in text:
                    error(f"Public placeholder {placeholder!r} remains in {path.relative_to(ROOT)}")


def check_published_port_defaults() -> None:
    """Reject duplicate defaults for host-published web/TLS listeners."""
    published: dict[int, list[str]] = {}
    suffixes = ("_https_port", "_http_port", "_web_port")
    # Some applications expose a web/TLS listener through a generic *_port name.
    # Keep these explicit so the checker does not mistake remote-service ports,
    # UDP listeners, or container-internal ports for host-published web services.
    explicit_listener_names = {
        "hamstack_dcdash_port",
    }
    for defaults in sorted((ROOT / "roles").rglob("defaults/main.yml")):
        try:
            data = yaml.load(defaults.read_text(encoding="utf-8"), Loader=UniqueKeyLoader) or {}
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        for name, value in data.items():
            is_published_listener = name.endswith(suffixes) or name in explicit_listener_names
            if not is_published_listener or not isinstance(value, int) or value <= 0:
                continue
            published.setdefault(value, []).append(name)
    for port, names in sorted(published.items()):
        if len(names) > 1:
            error(f"Duplicate host-published default port {port}: {', '.join(sorted(names))}")


def check_vault_contract() -> None:
    """Keep code, the public Vault template, and secret-variable docs aligned."""
    template = ROOT / "inventory" / "example" / "group_vars" / "all" / "vault.yml.example"
    config = ROOT / "docs" / "configuration.md"

    try:
        template_data = yaml.load(template.read_text(encoding="utf-8"), Loader=UniqueKeyLoader) or {}
    except Exception as exc:
        error(f"Unable to parse Vault template {template.relative_to(ROOT)}: {exc}")
        return
    if not isinstance(template_data, dict):
        error(f"Vault template must contain a mapping: {template.relative_to(ROOT)}")
        return

    template_names = {name for name in template_data if name.startswith("vault_hamstack_")}
    documented_names = set(re.findall(r"^\| `(vault_hamstack_[A-Za-z0-9_]+)` \|", config.read_text(encoding="utf-8"), re.MULTILINE))

    code_names: set[str] = set()
    vault_pattern = re.compile(r"\bvault_hamstack_[A-Za-z0-9_]+\b")
    for base in (ROOT / "roles", ROOT / "playbooks"):
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            try:
                code_names.update(vault_pattern.findall(path.read_text(encoding="utf-8")))
            except UnicodeDecodeError:
                continue

    for name in sorted(code_names - template_names):
        error(f"Vault variable used by code but missing from vault.yml.example: {name}")
    for name in sorted(template_names - code_names):
        error(f"Vault variable present in vault.yml.example but unused by roles/playbooks: {name}")
    for name in sorted(template_names - documented_names):
        error(f"Vault variable present in vault.yml.example but missing from docs/configuration.md: {name}")
    for name in sorted(documented_names - template_names):
        error(f"Vault variable documented but missing from vault.yml.example: {name}")


def check_repository_contract_files() -> None:
    required = [
        ROOT / "LICENSE",
        ROOT / "AGENTS.md",
        ROOT / "CHANGELOG.md",
        ROOT / "RELEASE_NOTES.md",
        ROOT / ".github" / "copilot-instructions.md",
        ROOT / ".github" / "workflows" / "qa.yml",
        ROOT / ".gitattributes",
        ROOT / "FEATURES.md",
        ROOT / "docs" / "getting-started.md",
        ROOT / "docs" / "concepts.md",
        ROOT / "docs" / "first-deployment.md",
        ROOT / "scripts" / "bootstrap-node.sh",
        ROOT / "scripts" / "bootstrap-workstation.sh",
        ROOT / "playbooks" / "profiles" / "hamcube.yml",
        ROOT / "playbooks" / "profiles" / "control-station.yml",
        ROOT / "playbooks" / "profiles" / "dev-workstation.yml",
        ROOT / "inventory" / "example" / "group_vars" / "all" / "vault.yml.example",
    ]
    for path in required:
        if not path.exists():
            error(f"Required repository contract file is missing: {path.relative_to(ROOT)}")


def main() -> int:
    check_yaml()
    check_jinja()
    check_python()
    check_shell()
    check_markdown_links()
    check_role_layout()
    check_variable_reference()
    check_role_documentation_consistency()
    check_deprecated_paths()
    check_public_placeholders()
    check_published_port_defaults()
    check_vault_contract()
    check_repository_contract_files()
    if ERRORS:
        print(f"\nHamStack QA failed with {len(ERRORS)} error(s).")
        return 1
    print("HamStack QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
