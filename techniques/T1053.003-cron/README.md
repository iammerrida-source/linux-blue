# T1053.003 — Scheduled Task/Job: Cron

**Tactic:** Persistence (also Execution, Privilege Escalation) · **MITRE:** https://attack.mitre.org/techniques/T1053/003/

## What the attacker does
Drops a line into a crontab (system-wide `/etc/crontab`, a file in `/etc/cron.d/`, a script in
`/etc/cron.{hourly,daily,weekly,monthly}/`, or a user crontab under `/var/spool/cron/`) so their
command keeps running on a schedule — and survives reboots.

## What it looks like in telemetry
| Source | Signal | Why it matters |
|---|---|---|
| auditd (`-k lb_cron`) | write / attribute change on cron paths | the persistence write itself |
| auditd (`-k lb_cron_exec`) | execution of `/usr/bin/crontab` | user-crontab edits go through this binary |
| Auditbeat | `file.path`, `process.executable`, `user.name` on those events | who wrote what, with which tool |
| syslog | `CRON[...]: (root) CMD (...)` | the job actually running later |

## Evidence
Put sanitized Kibana / Splunk exports in `evidence/`.

## Files
- [Simulation](simulate.md)
- [Playbook](playbook.md)
- Rules: [auditd](rules/auditd.rules) · [Sigma](rules/sigma.yml) · [Elastic](rules/elastic.esql) · [Splunk](rules/splunk.spl)

## Lessons / gotchas
- Package installs (`dpkg`, `apt`) legitimately drop files in `/etc/cron.d/` — exclude by process, not by path.
- `crontab -e` writes via a temp file then renames it into `/var/spool/cron/crontabs/` — watch the directory, not just the file.
