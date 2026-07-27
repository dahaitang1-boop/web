#!/usr/bin/env python3
"""Refuse to publish private data.

This is the load-bearing guard for ~/web. It is wired in three places so that
no single bypass works:

  1. .githooks/pre-commit          -> --staged
  2. .github/workflows/scan.yml    -> whole tree, on push and PR
  3. package.json "build"          -> whole tree, before astro build

(3) is the one that matters: `git commit --no-verify` still cannot deploy,
because Cloudflare runs the build script and the build script runs this first.

Design rules:
  - The verdict is an exit code, never a judgement call under time pressure.
  - Deny by default. A false positive is fixed by allowlisting the specific
    value with a written reason, never by loosening a regex.
  - Patterns are public (scripts/deny-patterns.toml). Exact secret values are
    NOT stored here in any form -- see the note on deny-literals.local below.

Exit codes: 0 clean, 1 findings, 2 configuration error.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "scripts" / "deny-patterns.toml"
ALLOWLIST = ROOT / "scripts" / "allowlist.txt"

# Identifying rules (a case number, names) that the public rule file must not
# carry. Gitignored; merged in when present. Absent on CI by design — the
# generic vocabulary rules still run there, and these values can only ever
# enter the repo from this machine, where the local layer IS present.
CONFIG_LOCAL = ROOT / "scripts" / "deny-patterns.local.toml"

# Exact-value layer. Deliberately gitignored and LOCAL ONLY.
#
# Why not commit digests: the values worth protecting here (phone numbers,
# a 14-digit membership number, an IBAN) are low-entropy. A published sha256
# of a 14-digit number is brute-forceable in hours, so committing digests
# would leak the very values it claims to protect. CI therefore runs on the
# regex rules alone; this file is a local belt-and-braces layer.
LITERALS = ROOT / "scripts" / "deny-literals.local"

BINARY_SNIFF = 8192
MAX_BYTES = 8 * 1024 * 1024


def norm(s: str) -> str:
    """Normalise a candidate for comparison: letters and digits only."""
    return re.sub(r"[^0-9a-z]", "", s.lower())


def die(msg: str) -> None:
    print(f"scan_secrets: configuration error: {msg}", file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------- config --


def load_config() -> dict:
    if not CONFIG.is_file():
        die(f"missing {CONFIG}")
    with CONFIG.open("rb") as fh:
        cfg = tomllib.load(fh)
    if not cfg.get("rule"):
        die("no [[rule]] entries defined")
    if CONFIG_LOCAL.is_file():
        with CONFIG_LOCAL.open("rb") as fh:
            local = tomllib.load(fh)
        cfg["rule"].extend(local.get("rule", []))
    for rule in cfg["rule"]:
        for key in ("name", "regex", "why"):
            if not rule.get(key):
                die(f"rule {rule.get('name', '<unnamed>')!r} is missing {key!r}")
        flags = re.MULTILINE
        if "i" in rule.get("flags", ""):
            flags |= re.IGNORECASE
        try:
            rule["_rx"] = re.compile(rule["regex"], flags)
        except re.error as exc:
            die(f"rule {rule['name']!r} has an invalid regex: {exc}")
    return cfg


def load_allowlist() -> set[str]:
    """Approved literals. Every entry must carry a written reason."""
    if not ALLOWLIST.is_file():
        die(f"missing {ALLOWLIST}")
    approved: set[str] = set()
    for lineno, raw in enumerate(ALLOWLIST.read_text("utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        value, sep, reason = line.partition("#")
        value, reason = value.strip(), reason.strip()
        if not value:
            continue
        if not sep or not reason:
            die(
                f"{ALLOWLIST.name}:{lineno}: {value!r} has no reason. "
                "Every allowlist entry must say why it is safe to publish."
            )
        approved.add(norm(value))
    return approved


def load_literals() -> set[str]:
    if not LITERALS.is_file():
        return set()
    out: set[str] = set()
    for raw in LITERALS.read_text("utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if len(line) == 64 and all(c in "0123456789abcdef" for c in line):
            out.add(line)
    return out


# ---------------------------------------------------------------- files --


def glob_hit(rel: str, patterns: list[str]) -> bool:
    base = rel.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(base, p) for p in patterns)


def candidate_files(staged: bool, excludes: list[str]) -> list[Path]:
    if staged:
        res = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM", "-z"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        names = [n for n in res.stdout.split("\0") if n]
        paths = [ROOT / n for n in names]
    else:
        paths = [p for p in ROOT.rglob("*") if p.is_file()]

    out = []
    for p in paths:
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if glob_hit(rel, excludes):
            continue
        out.append(p)
    return sorted(out)


def read_text(path: Path) -> str | None:
    """Return decoded text, or None when the file is binary or oversized."""
    try:
        if path.stat().st_size > MAX_BYTES:
            return None
        head = path.open("rb").read(BINARY_SNIFF)
    except OSError:
        return None
    if b"\x00" in head:
        return None
    try:
        return path.read_text("utf-8", errors="replace")
    except OSError:
        return None


# ----------------------------------------------------------------- scan --


def redact(s: str) -> str:
    s = s.replace("\n", "\\n")
    if len(s) <= 8:
        return s[0] + "…" + s[-1] if len(s) > 2 else "…"
    return f"{s[:4]}…{s[-3:]} ({len(s)} chars)"


def scan_text(text: str, rules: list[dict], approved: set[str], literals: set[str]):
    """Return a list of (line, rule_name, why, matched_text)."""
    raw: list[tuple[int, int, dict, str]] = []
    allowed_spans: list[tuple[int, int]] = []

    for rule in rules:
        for m in rule["_rx"].finditer(text):
            hit = m.group(0)
            if norm(hit) in approved:
                allowed_spans.append(m.span())
            else:
                raw.append((m.start(), m.end(), rule, hit))

    findings = []
    for start, end, rule, hit in raw:
        # A generic rule often fires *inside* an allowlisted value: the
        # 7-digit rule matches the tail of an approved hut phone number.
        # Suppress anything fully contained in an approved span.
        if any(a <= start and end <= b for a, b in allowed_spans):
            continue
        line = text.count("\n", 0, start) + 1
        findings.append((line, rule["name"], rule["why"], hit))

    if literals:
        for m in re.finditer(r"[0-9][0-9 \-/()]{4,}[0-9]|[A-Za-z0-9._%+\-]{8,}", text):
            token = norm(m.group(0))
            if not token:
                continue
            if hashlib.sha256(token.encode()).hexdigest() in literals:
                line = text.count("\n", 0, m.start()) + 1
                findings.append(
                    (line, "known-literal", "exact value on the local deny list", m.group(0))
                )

    findings.sort()
    return findings


# ----------------------------------------------------------------- main --


def add_literal() -> int:
    """Record a secret's digest without it passing through argv or history."""
    import getpass

    value = getpass.getpass("value to deny (not echoed): ").strip()
    if not value:
        print("nothing entered; aborted", file=sys.stderr)
        return 2
    digest = hashlib.sha256(norm(value).encode()).hexdigest()
    label = input("short label for your own reference (no secret data): ").strip()
    with LITERALS.open("a", encoding="utf-8") as fh:
        if LITERALS.stat().st_size == 0:
            fh.write("# LOCAL ONLY - never commit. See scan_secrets.py for why.\n")
        fh.write(f"{digest}  # {label or 'unlabelled'}\n")
    LITERALS.chmod(0o600)
    print(f"recorded. {LITERALS.name} now holds {len(load_literals())} literal(s).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Block private data from reaching the public site.")
    ap.add_argument("--staged", action="store_true", help="scan staged files only (pre-commit)")
    ap.add_argument("--add-literal", action="store_true", help="add an exact value to the local deny list")
    ap.add_argument("-q", "--quiet", action="store_true", help="print nothing when clean")
    args = ap.parse_args()

    if args.add_literal:
        LITERALS.touch(mode=0o600, exist_ok=True)
        return add_literal()

    cfg = load_config()
    meta = cfg.get("meta", {})
    rules = cfg["rule"]
    approved = load_allowlist()
    literals = load_literals()
    deny_segments = set(meta.get("deny_path_segments", []))
    excludes = list(meta.get("exclude_paths", []))

    files = candidate_files(args.staged, excludes)
    findings: list[tuple[str, int, str, str, str]] = []
    path_violations: list[str] = []
    skipped_binary: list[str] = []

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        bad = deny_segments.intersection(path.relative_to(ROOT).parts)
        if bad:
            path_violations.append(f"{rel}  (forbidden directory: {'/'.join(sorted(bad))})")
            continue
        text = read_text(path)
        if text is None:
            skipped_binary.append(rel)
            continue
        # Per-rule exclude: a rule may opt out of files where its pattern is
        # structurally noisy (digit runs in a lockfile, coordinates in SVG).
        applicable = [r for r in rules if not glob_hit(rel, r.get("exclude", []))]
        for line, name, why, hit in scan_text(text, applicable, approved, literals):
            findings.append((rel, line, name, why, hit))

    if not findings and not path_violations:
        if not args.quiet:
            scope = "staged files" if args.staged else "working tree"
            print(
                f"scan_secrets: clean — {len(files)} file(s) in {scope}, "
                f"{len(rules)} rule(s), {len(approved)} allowlisted value(s)."
            )
            if skipped_binary:
                print(
                    f"  note: {len(skipped_binary)} binary file(s) not scanned "
                    f"(review by hand): {', '.join(skipped_binary[:5])}"
                    + (" …" if len(skipped_binary) > 5 else "")
                )
        return 0

    print("\n  ✋ scan_secrets: BLOCKED — private data must not reach the public site.\n", file=sys.stderr)

    for v in path_violations:
        print(f"  {v}", file=sys.stderr)
    if path_violations:
        print("", file=sys.stderr)

    by_rule: dict[str, list] = {}
    for rel, line, name, why, hit in findings:
        by_rule.setdefault(name, []).append((rel, line, why, hit))

    for name in sorted(by_rule):
        items = by_rule[name]
        print(f"  [{name}] {items[0][2]}", file=sys.stderr)
        for rel, line, _why, hit in items[:12]:
            print(f"      {rel}:{line}  {redact(hit)}", file=sys.stderr)
        if len(items) > 12:
            print(f"      … and {len(items) - 12} more", file=sys.stderr)
        print("", file=sys.stderr)

    print(
        "  Fix by removing the value. If it is genuinely public (a hut's own\n"
        "  phone number) add it to scripts/allowlist.txt WITH a reason.\n"
        "  Never loosen a regex to make this go away.\n",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
