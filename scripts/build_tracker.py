#!/usr/bin/env python3
"""Render the tracker table in README.md from roadmap.yml + techniques/*/meta.yml."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
START, END = "<!-- TRACKER:START -->", "<!-- TRACKER:END -->"

STATUS = {
    "done": "✅ done",
    "review": "🧪 review",
    "wip": "🔄 in progress",
    "import": "📥 import",
    "planned": "⬜ planned",
}
ORDER = list(STATUS)
RULES = [("auditd", "auditd.rules"), ("Sigma", "sigma.yml"),
         ("Elastic", "elastic.esql"), ("Splunk", "splunk.spl")]


def mitre_url(tid: str) -> str:
    return "https://attack.mitre.org/techniques/" + tid.replace(".", "/") + "/"


def cell(path: Path, rel: str) -> str:
    if not path.exists():
        return "—"
    mark = "📝" if "TODO" in path.read_text(encoding="utf-8") else "✅"
    return f"[{mark}]({rel})"


def load():
    items = {}
    for entry in yaml.safe_load((ROOT / "roadmap.yml").read_text(encoding="utf-8")) or []:
        items[entry["id"]] = {**entry, "dir": None}
    for meta in sorted((ROOT / "techniques").glob("*/meta.yml")):
        if meta.parent.name.startswith("_"):
            continue
        data = yaml.safe_load(meta.read_text(encoding="utf-8")) or {}
        tid = data.get("id")
        if not tid:
            continue
        items[tid] = {**items.get(tid, {}), **data, "dir": meta.parent}
    return items


def sort_key(tid: str):
    return [int(p) for p in re.findall(r"\d+", tid)]


def render(items) -> str:
    head = ("| Technique | Status | Tactic | Simulation | Playbook | "
            + " | ".join(name for name, _ in RULES) + " |")
    sep = "|" + "---|" * (5 + len(RULES))
    rows = [head, sep]
    for tid in sorted(items, key=sort_key):
        it = items[tid]
        name = f"[{tid}]({mitre_url(tid)}) {it.get('name', '')}"
        status = STATUS.get(it.get("status", "planned"), it.get("status", ""))
        d = it["dir"]
        if d is not None:
            rel = d.relative_to(ROOT).as_posix()
            name = f"[{tid}]({mitre_url(tid)}) [{it.get('name', '')}]({rel}/)"
            sim = cell(d / "simulate.md", f"{rel}/simulate.md")
            pb = cell(d / "playbook.md", f"{rel}/playbook.md")
            rules = [cell(d / "rules" / f, f"{rel}/rules/{f}") for _, f in RULES]
        else:
            sim = pb = "—"
            rules = ["—"] * len(RULES)
        rows.append(f"| {name} | {status} | {it.get('tactic', '')} | {sim} | {pb} | "
                    + " | ".join(rules) + " |")

    counts = {s: sum(1 for i in items.values() if i.get("status") == s) for s in ORDER}
    total = len(items)
    done = counts["done"]
    filled = round(20 * done / total) if total else 0
    bar = "█" * filled + "░" * (20 - filled)
    summary = (f"**Progress:** `{bar}` {done}/{total} done · "
               + " · ".join(f"{STATUS[s].split()[0]} {counts[s]}" for s in ORDER))
    return summary + "\n\n" + "\n".join(rows)


def main():
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit("README.md is missing the TRACKER markers")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    README.write_text(f"{before}{START}\n{render(load())}\n{END}{after}", encoding="utf-8")
    print("README.md tracker updated")


if __name__ == "__main__":
    main()
