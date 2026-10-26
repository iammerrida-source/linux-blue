# Playbook — T1053.003 Cron

## 1. Triage
Look at the entry the alert points to and who wrote it:

```bash
sudo ls -la --time-style=full-iso /etc/crontab /etc/cron.d/ /etc/cron.*/ /var/spool/cron/crontabs/
sudo cat /etc/cron.d/<file>
sudo ausearch -k lb_cron -i --start recent
```

**Benign if:** written by `dpkg`/`apt`, matches a known package, owned by an expected admin change.
**Suspicious if:** written by a shell/interpreter (`bash`, `python`, `curl`…), runs from `/tmp`, `/dev/shm` or a hidden path, downloads something, or uses base64/obfuscation.

## 2. Scope
- Same command/hash on other hosts? Same user writing cron files elsewhere?
- Check syslog for the job having already run: `grep CRON /var/log/syslog`
- Pivot on the parent process / login session (`auid`, `ses` in auditd).

## 3. Contain
- Isolate the host if the payload reaches out to the network.
- Disable the entry (move the file to a quarantine folder rather than deleting — keep it as evidence).

## 4. Eradicate
- Remove the cron entry and whatever it executes.
- Kill running child processes started by the job.
- Hunt for sibling persistence (systemd units, shell rc files, `authorized_keys`).

## 5. Recover & harden
- Restrict cron with `/etc/cron.allow`.
- Keep the `lb_cron` auditd watches permanently enabled.

## False positives seen
- Package installs/updates dropping files into `/etc/cron.d/`.
