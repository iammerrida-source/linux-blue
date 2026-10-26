#!/usr/bin/env python3
"""Scaffold techniques/<ID>-<slug>/ from the template, pre-filled from roadmap.yml.

usage: python3 scripts/new_technique.py T1543.002 [slug]
"""
from pathlib import Path
import re
import shutil
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "techniques" / "_template"


def slugify(text: str) -> str:
    text = text.split(":")[-1]
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    tid = sys.argv[1].upper()
    roadmap = {e["id"]: e for e in yaml.safe_load((ROOT / "roadmap.yml").read_text()) or []}
    entry = roadmap.get(tid, {})
    name = entry.get("name", "Technique name")
    tactic = entry.get("tactic", "")
    slug = sys.argv[2] if len(sys.argv) > 2 else slugify(name) or "technique"

    dest = ROOT / "techniques" / f"{tid}-{slug}"
    if dest.exists():
        raise SystemExit(f"{dest.relative_to(ROOT)} already exists")
    shutil.copytree(TEMPLATE, dest)

    url_path = tid.replace(".", "/")
    for f in dest.rglob("*"):
        if f.is_file():
            t = f.read_text(encoding="utf-8")
            t = (t.replace("TXXXX/XXX", url_path)
                  .replace("TXXXX.XXX", tid)
                  .replace("txxxx.xxx", tid.lower())
                  .replace("lb_txxxx", "lb_" + tid.lower().replace(".", "_"))
                  .replace("Technique name", name))
            f.write_text(t, encoding="utf-8")

    meta = dest / "meta.yml"
    data = yaml.safe_load(meta.read_text(encoding="utf-8"))
    data.update({"id": tid, "name": name, "tactic": tactic or data.get("tactic"), "status": "wip"})
    meta.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    readme = dest / "README.md"
    readme.write_text(readme.read_text().replace("**Tactic:** ·", f"**Tactic:** {tactic} ·"), encoding="utf-8")

    print(f"created {dest.relative_to(ROOT)}/  — now run scripts/build_tracker.py when you update status")


if __name__ == "__main__":
    main()
