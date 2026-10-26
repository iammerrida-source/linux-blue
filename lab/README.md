# 🧪 Lab

```
┌──────────────────────┐     Auditbeat (ECS)     ┌──────────────────────────┐
│  Ubuntu victim VM    │ ──────────────────────▶ │  Elasticsearch + Kibana  │
│  auditd + ART (pwsh) │                         │  (ES|QL / detection rules)│
│                      │     Universal Forwarder  ├──────────────────────────┤
│                      │ ──────────────────────▶ │  Splunk + linux_audit    │
└──────────────────────┘                         └──────────────────────────┘
```

## Components
| Piece | Role |
|---|---|
| Ubuntu VM | target; runs auditd + Atomic Red Team (Invoke-AtomicRedTeam on PowerShell 7) |
| Auditbeat | ships auditd + FIM events in ECS to Elastic |
| Elasticsearch / Kibana | ES\|QL hunting + detection rules, CSV export for evidence |
| Splunk + UF | `linux_audit` sourcetype, SPL versions of the rules |

## Baseline collection
Each technique's `rules/auditd.rules` is a drop-in file:

```bash
sudo cp techniques/*/rules/auditd.rules /etc/audit/rules.d/   # or pick individual ones
sudo augenrules --load
sudo auditctl -l | grep lb_
```

Rule keys are prefixed `lb_` so they're easy to filter (`tags` in Auditbeat, `key` in Splunk).

## Gotchas collected so far
- In Auditbeat, `process.title` is a **text** field, not keyword — use `RLIKE`/`LIKE` carefully or prefer `process.executable` / `process.args`.
- Keep host IPs and real usernames out of committed evidence.
