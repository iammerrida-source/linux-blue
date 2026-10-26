# Simulation — T1053.003

## Atomic Red Team
Pick tests from the list for this technique, then run + clean up:

```powershell
Invoke-AtomicTest T1053.003 -ShowDetailsBrief
Invoke-AtomicTest T1053.003 -TestNumbers 1 -GetPrereqs
Invoke-AtomicTest T1053.003 -TestNumbers 1
Invoke-AtomicTest T1053.003 -TestNumbers 1 -Cleanup
```

## Manual variant (harmless payload)
System-wide entry:

```bash
echo '* * * * * root /bin/echo linux-blue-test > /tmp/lb_cron.txt' | sudo tee /etc/cron.d/lb-test
```

User crontab:

```bash
(crontab -l 2>/dev/null; echo '* * * * * /bin/echo linux-blue-user > /tmp/lb_cron_user.txt') | crontab -
```

Cleanup:

```bash
sudo rm -f /etc/cron.d/lb-test /tmp/lb_cron.txt /tmp/lb_cron_user.txt
crontab -l | grep -v linux-blue-user | crontab -
```

## Runs
| Date | Test | Detected? | Rule(s) that fired | Notes |
|---|---|---|---|---|
| | | | | |
