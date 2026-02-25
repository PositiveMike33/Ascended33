# Automation Activation Guide
**Date**: 2026-02-22  
**Status**: Ready to Deploy  
**Target**: Daily Automated Organization of Report Files

---

## 🎯 Objective

Enable automatic daily execution of the `organize-daily-reports` skill to:
- Monitor `D:/Vault/Vault/THIRTY3/daily` for new files
- Automatically move files matching `(YYYY-MM-DD)` pattern
- Create appropriate folder structure in destination
- Handle duplicates with `_1.md` naming
- Generate execution logs for tracking

---

## 📋 Prerequisites

✅ **All components are ready:**
- ✓ organize-reports.ps1 (main script - tested successfully)
- ✓ check-obsidian-links.py (link verification - optional)
- ✓ HOOK-CONFIG.md (configuration guide)
- ✓ register-hook.ps1 (registration script)
- ✓ automation-log.txt (log file initialized)
- ✓ Test results from 2026-02-22 (2 files successfully moved)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Run the Hook Registration Script

Open PowerShell and execute:

```powershell
cd "D:\Vault\Vault\SKILLS\organize-daily-reports\scripts"
.\register-hook.ps1
```

**Expected Output:**
```
✓ Skill path verified
✓ Created hooks directory
✓ Hook registered successfully
```

### Step 2: Verify Hook in Claude Code

1. Open Claude Code
2. Navigate to **Settings** → **Hooks**
3. Look for `organize-daily-reports-automated`
4. Confirm status shows: **Enabled** ✓
5. Confirm schedule shows: **0 9 * * * (UTC)**

### Step 3: Test the Hook

1. In Claude Code Hooks settings
2. Find `organize-daily-reports-automated`
3. Click **"Test Hook"** or **"Run Now"**
4. Wait 5-10 seconds for execution
5. Check results:

```
Log File: D:\Vault\Vault\SKILLS\organize-daily-reports\reports\automation-log.txt
Expected Lines:
  [timestamp] - ⊙ EXECUTING - Hook execution started
  [timestamp] - ✓ SUCCESS - Files processed: X
  [timestamp] - ✓ COMPLETED - Hook execution completed
```

---

## 📊 Verification Checklist

After activation, verify:

- [ ] Hook appears in Claude Code Hooks settings
- [ ] Hook status is **Enabled**
- [ ] Schedule is **0 9 * * *** (daily at 09:00 UTC)
- [ ] Manual test executed successfully
- [ ] Automation log file has new entries
- [ ] No errors in automation log

---

## 🔍 Monitoring

### Daily Check (Manual)

Each morning, verify automation worked:

```powershell
# Check automation log for last execution
$logPath = "D:\Vault\Vault\SKILLS\organize-daily-reports\reports\automation-log.txt"
Get-Content $logPath -Tail 5
```

### Weekly Review (Recommended)

Every Friday, run comprehensive check:

```powershell
# Check for any errors in the past week
$logPath = "D:\Vault\Vault\SKILLS\organize-daily-reports\reports\automation-log.txt"
Select-String -Path $logPath -Pattern "ERROR|WARNING" -Context 0,2
```

### Monthly Metrics

Track automation performance:

- **Files Processed**: Count in automation log
- **Success Rate**: (Successful Runs / Total Runs) × 100
- **Average Files/Day**: Total Files / Days Active
- **Duplicate Occurrences**: Count of `_1.md` files created

---

## ⚙️ Configuration Options

### Option A: Keep Default (Recommended)

**Schedule**: Daily at 09:00 UTC  
**Days**: All days (including weekends)  
**Best for**: Continuous organization

### Option B: Weekdays Only

Edit Hook schedule to: `0 9 * * 1-5`  
**Best for**: Business hours only

### Option C: Multiple Daily Runs

Create multiple Hooks:
- 09:00 UTC (morning)
- 13:00 UTC (midday)
- 17:00 UTC (evening)

**Best for**: High-volume daily reports

### Option D: Custom Time

Change `0 9 * * *` to your preferred time:
- `0 8 * * *` = 08:00 UTC
- `0 10 * * *` = 10:00 UTC
- `30 14 * * *` = 14:30 UTC

---

## 🐛 Troubleshooting

### Issue: Hook doesn't appear in Claude Code

**Solution:**
1. Restart Claude Code completely
2. Re-run `register-hook.ps1`
3. Check file was created: `$env:USERPROFILE\.claude\hooks\organize-daily-reports-hook.json`

### Issue: Hook fails to execute

**Check:**
1. Is Claude Code running?
2. Do source files exist in `D:/Vault/Vault/THIRTY3/daily`?
3. Check error in automation-log.txt
4. Verify PowerShell execution policy: `Get-ExecutionPolicy`

**Fix:**
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Files not being moved

**Verify:**
1. Files have correct pattern: `(YYYY-MM-DD) filename.md`
2. Source folder exists: `D:/Vault/Vault/THIRTY3/daily`
3. Destination folder accessible: `D:/Vault/Vault/REPORT/...`
4. File permissions allow read/write

**Debug:**
```powershell
# Test the script manually
cd "D:\Vault\Vault\SKILLS\organize-daily-reports\scripts"
.\organize-reports.ps1 -SourcePath "D:\Vault\Vault\THIRTY3\daily" -DryRun
```

### Issue: Duplicate files created

**This is normal behavior** - duplicates are created when:
- File with same name already exists in destination
- Naming convention: `filename_1.md`

**Action:**
1. Review the duplicate in automation log
2. Manually decide which version to keep
3. Delete the `_1.md` version or merge content
4. Hook will continue operating normally

---

## 📝 Manual Execution (Backup)

If automation fails, manually run anytime:

```powershell
# Navigate to skill directory
cd "D:\Vault\Vault\SKILLS\organize-daily-reports\scripts"

# Run the script
.\organize-reports.ps1 `
  -SourcePath "D:\Vault\Vault\THIRTY3\daily" `
  -DestinationBasePath "D:\Vault\Vault\REPORT\declassified report\02 Rapport Février" `
  -Verbose
```

---

## 📚 Documentation References

- **HOOK-CONFIG.md** - Detailed Hook configuration
- **README.md** - Skill overview
- **usage-guide.md** - Usage instructions
- **COMPLETION-SUMMARY.md** - Project status

---

## ✅ Success Indicators

**Hook is working correctly if:**

1. ✓ New files with `(YYYY-MM-DD)` pattern are moved daily
2. ✓ Destination folder structure is created automatically
3. ✓ Automation log shows `✓ COMPLETED` entries
4. ✓ No error entries in automation log
5. ✓ Files appear in correct week folders (e.g., `22-02-2026`)
6. ✓ Source directory becomes empty after processing
7. ✓ Obsidian links continue working in destination

---

## 🎓 Learning Resources

### PowerShell Script Concepts Used
- Scheduled task execution
- File pattern matching with regex
- Folder creation and path handling
- Error handling and logging
- Duplicate file detection

### Claude Code Hook Concepts
- Time-based scheduling (cron syntax)
- Skill integration
- Automated notifications
- Log monitoring

---

## 📞 Support & Next Steps

### Immediate Next Steps
1. ✓ Execute `register-hook.ps1`
2. ✓ Verify Hook in Claude Code
3. ✓ Test Hook manually
4. ✓ Monitor first 24 hours

### Long-term Monitoring
- Check automation log weekly
- Review duplicate handling
- Verify Obsidian link integrity
- Adjust schedule if needed

### Advanced Configuration (Optional)
- Add email notifications
- Create backup copies before moving
- Implement weekly digest reports
- Add metrics tracking dashboard

---

**Status**: ✅ Ready for Deployment  
**Last Updated**: 2026-02-22  
**Next Execution**: 2026-02-23 09:00 UTC
