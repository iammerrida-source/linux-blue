# 🐧🛡️ linux-blue

**Linux purple-team detection lab.** One MITRE ATT&CK technique at a time:
simulate it → catch it in real telemetry → write the detection → write the playbook.

Every technique gets the same five things:

| | |
|---|---|
| 🎯 **Simulation** | the exact commands used to emulate it (Atomic Red Team + manual variants) |
| 📒 **Playbook** | how an analyst triages, contains and cleans it up |
| 🔭 **auditd** | the collection rule that makes the behaviour visible |
| 🧩 **Sigma** | vendor-neutral detection |
| ⚡ **Elastic** | ES\|QL query against Auditbeat (ECS) |
| 🔎 **Splunk** | SPL query against `linux_audit` |

> ⚠️ Simulations are meant for an isolated lab only. Don't run them on systems you don't own.

---

## 📊 Tracker

<!-- TRACKER:START -->
**Progress:** `░░░░░░░░░░░░░░░░░░░░` 0/16 done · ✅ 0 · 🧪 1 · 🔄 3 · 📥 2 · ⬜ 10

| Technique | Status | Tactic | Simulation | Playbook | auditd | Sigma | Elastic | Splunk |
|---|---|---|---|---|---|---|---|---|
| [T1003.008](https://attack.mitre.org/techniques/T1003/008/) OS Credential Dumping: /etc/passwd and /etc/shadow | ⬜ planned | Credential Access | — | — | — | — | — | — |
| [T1018](https://attack.mitre.org/techniques/T1018/) Remote System Discovery | 🔄 in progress | Discovery | — | — | — | — | — | — |
| [T1053.003](https://attack.mitre.org/techniques/T1053/003/) [Scheduled Task/Job: Cron](techniques/T1053.003-cron/) | 🧪 review | Persistence | [✅](techniques/T1053.003-cron/simulate.md) | [✅](techniques/T1053.003-cron/playbook.md) | [✅](techniques/T1053.003-cron/rules/auditd.rules) | [✅](techniques/T1053.003-cron/rules/sigma.yml) | [✅](techniques/T1053.003-cron/rules/elastic.esql) | [✅](techniques/T1053.003-cron/rules/splunk.spl) |
| [T1059.004](https://attack.mitre.org/techniques/T1059/004/) Command and Scripting Interpreter: Unix Shell | ⬜ planned | Execution | — | — | — | — | — | — |
| [T1070.003](https://attack.mitre.org/techniques/T1070/003/) Indicator Removal: Clear Command History | ⬜ planned | Defense Evasion | — | — | — | — | — | — |
| [T1071.001](https://attack.mitre.org/techniques/T1071/001/) Application Layer Protocol: Web Protocols | 📥 import | Command and Control | — | — | — | — | — | — |
| [T1098.004](https://attack.mitre.org/techniques/T1098/004/) Account Manipulation: SSH Authorized Keys | ⬜ planned | Persistence | — | — | — | — | — | — |
| [T1105](https://attack.mitre.org/techniques/T1105/) Ingress Tool Transfer | ⬜ planned | Command and Control | — | — | — | — | — | — |
| [T1136.001](https://attack.mitre.org/techniques/T1136/001/) Create Account: Local Account | ⬜ planned | Persistence | — | — | — | — | — | — |
| [T1485](https://attack.mitre.org/techniques/T1485/) Data Destruction | 📥 import | Impact | — | — | — | — | — | — |
| [T1486](https://attack.mitre.org/techniques/T1486/) [Data Encrypted for Impact](techniques/T1486-data-encrypted-for-impact/) | 🔄 in progress | Impact | [📝](techniques/T1486-data-encrypted-for-impact/simulate.md) | [📝](techniques/T1486-data-encrypted-for-impact/playbook.md) | [✅](techniques/T1486-data-encrypted-for-impact/rules/auditd.rules) | [✅](techniques/T1486-data-encrypted-for-impact/rules/sigma.yml) | [✅](techniques/T1486-data-encrypted-for-impact/rules/elastic.esql) | [✅](techniques/T1486-data-encrypted-for-impact/rules/splunk.spl) |
| [T1543.002](https://attack.mitre.org/techniques/T1543/002/) Create or Modify System Process: Systemd Service | ⬜ planned | Persistence | — | — | — | — | — | — |
| [T1546.004](https://attack.mitre.org/techniques/T1546/004/) Event Triggered Execution: Unix Shell Configuration Modification | ⬜ planned | Persistence | — | — | — | — | — | — |
| [T1548.001](https://attack.mitre.org/techniques/T1548/001/) Abuse Elevation Control Mechanism: Setuid and Setgid | ⬜ planned | Privilege Escalation | — | — | — | — | — | — |
| [T1548.003](https://attack.mitre.org/techniques/T1548/003/) [Abuse Elevation Control Mechanism: Sudo and Sudo Caching](techniques/T1548.003-sudo-caching/) | 🔄 in progress | Privilege Escalation | [📝](techniques/T1548.003-sudo-caching/simulate.md) | [📝](techniques/T1548.003-sudo-caching/playbook.md) | [📝](techniques/T1548.003-sudo-caching/rules/auditd.rules) | [📝](techniques/T1548.003-sudo-caching/rules/sigma.yml) | [✅](techniques/T1548.003-sudo-caching/rules/elastic.esql) | [📝](techniques/T1548.003-sudo-caching/rules/splunk.spl) |
| [T1574.006](https://attack.mitre.org/techniques/T1574/006/) Hijack Execution Flow: Dynamic Linker Hijacking | ⬜ planned | Persistence | — | — | — | — | — | — |
<!-- TRACKER:END -->

**Legend:** ✅ done · 🧪 review (drafted, needs lab validation) · 🔄 in progress · 📥 done in lab, not imported yet · ⬜ planned
**Cells:** ✅ written · 📝 template only (still has `TODO`) · — missing

---

## 🔁 Workflow

```bash
# 1. start a technique (copies the template, pre-fills name/tactic from roadmap.yml)
python3 scripts/new_technique.py T1543.002

# 2. simulate → collect telemetry → write rules + playbook
#    (edit the files in techniques/T1543.002-*/)

# 3. set `status:` in meta.yml, then refresh the table above
python3 scripts/build_tracker.py
```

## 🗂️ Layout

```
linux-blue/
├── README.md                 ← you are here (tracker is auto-generated)
├── roadmap.yml               ← every technique planned, with tactic + status
├── lab/                      ← lab architecture + baseline collection config
├── scripts/
│   ├── build_tracker.py      ← renders the tracker table
│   └── new_technique.py      ← scaffolds a technique folder
└── techniques/
    ├── _template/
    └── T1053.003-cron/
        ├── README.md         ← technique card: telemetry, evidence, notes
        ├── meta.yml          ← id, name, tactic, status
        ├── simulate.md
        ├── playbook.md
        └── rules/
            ├── auditd.rules
            ├── sigma.yml
            ├── elastic.esql
            └── splunk.spl
```

## 🧪 Lab

See [`lab/`](lab/README.md) — Ubuntu VM shipping auditd telemetry via Auditbeat (ECS) to Elasticsearch/Kibana, plus a Splunk + Universal Forwarder pipeline for the SPL side.
