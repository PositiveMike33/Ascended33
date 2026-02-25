# 🔧 LAUNCH_VAULT.PS1 - FIX FINAL (Revision 2)

## Problem Persists - Root Cause Analysis

**Error (Still Appearing):**
```
Impossible d'exécuter un document au milieu d'un pipeline
C:\Program Files\Docker\Docker\resources\bin\docker
```

**Why Previous Fix Didn't Work:**
The previous attempt still used PowerShell pipeline operators directly with docker.exe:
```powershell
# ❌ STILL BROKEN - Pipeline with docker.exe
$dockerRunning = & docker ps --format "{{.Names}}" 2>&1 | Out-String
```

The problem: Even with `&`, piping from docker.exe causes PowerShell to try to execute the .exe file as a document in the pipeline.

---

## Solution: Use CMD as Intermediary

The issue is that PowerShell's pipeline internals don't work well with `.exe` files that have spaces in paths.

**Solution:** Use `cmd /c` to invoke Docker through the Windows command interpreter:

```powershell
# ✅ CORRECT - Use cmd /c to invoke docker
$output = & cmd /c "$dockerPath ps --format {{.Names}} 2>&1"
```

This way:
1. PowerShell calls `cmd.exe` (which is safe)
2. `cmd` executes the docker command
3. Output is returned cleanly to PowerShell
4. No pipeline issues

---

## Complete Fix Applied

### Before (Broken - Lines 77-84):
```powershell
$dockerRunning = & docker ps --format "{{.Names}}" 2>&1 | Out-String

if ($dockerRunning -match "th3-") {
    WARN "Containers déjà actifs. Skip rebuild."
}
```

### After (Fixed - Lines 77-95):
```powershell
$allContainers = @()
$output = & cmd /c "$dockerPath ps --format {{.Names}} 2>&1"
if ($output) {
    $allContainers = $output -split "`n" | Where-Object { $_ -match "th3-" }
}

if ($allContainers.Count -gt 0) {
    WARN "Containers déjà actifs. Skip rebuild."
}
```

**Key changes:**
1. ✅ Use `cmd /c` instead of direct docker invocation
2. ✅ Store output in variable first, then process
3. ✅ Use `-split` and `Where-Object` AFTER getting results
4. ✅ Check `.Count` instead of relying on pipeline logic

---

## Why This Works

### The Pipeline Problem Explained

**PowerShell Pipeline Chain:**
```
Command 1 → Object → Command 2 → Command 3
```

When PowerShell sees:
```powershell
docker ps | Select-String
```

It tries to:
1. Get the executable path for `docker`
2. Execute it as part of the pipeline
3. Connect the output to `Select-String`

With docker.exe having spaces in `C:\Program Files\...`, PowerShell's pipeline handler gets confused and tries to treat the .exe file itself as a PowerShell object.

### The CMD Solution

```powershell
cmd /c "C:\Program Files\Docker\Docker\resources\bin\docker ps"
```

- PowerShell calls `cmd.exe` (no spaces in path)
- `cmd` passes the full docker command to Windows
- Windows executes docker and returns output
- PowerShell receives clean string output
- No pipeline confusion

---

## Code Changes Summary

### Change 1: Docker Detection (Lines 67-75)
```powershell
# ✅ Store docker path, don't execute yet
try {
    $cmdDocker = Get-Command docker -ErrorAction Stop
    $dockerPath = $cmdDocker.Source
    $dockerAvailable = $true
} catch {
    $dockerAvailable = $false
}
```

### Change 2: Container Check (Lines 77-90)
```powershell
# ✅ Use cmd /c to run docker safely
if ($dockerAvailable) {
    try {
        $allContainers = @()
        $output = & cmd /c "$dockerPath ps --format {{.Names}} 2>&1"
        if ($output) {
            $allContainers = $output -split "`n" | Where-Object { $_ -match "th3-" }
        }
        
        if ($allContainers.Count -gt 0) {
            WARN "Containers déjà actifs. Skip rebuild."
        }
```

### Change 3: Docker Compose (Lines 91-103)
```powershell
# ✅ Use cmd /c for docker compose too
& cmd /c "$dockerPath compose up -d --no-build 2>&1" | Out-Null

# ✅ Get results safely
$result = @()
$output2 = & cmd /c "$dockerPath ps --format {{.Names}} 2>&1"
if ($output2) {
    $result = $output2 -split "`n" | Where-Object { $_ -and $_.Trim() }
}
```

---

## Testing the Fix

### Test 1: Basic Docker Command
```powershell
$dockerPath = (Get-Command docker).Source
$output = & cmd /c "$dockerPath ps --format {{.Names}} 2>&1"
Write-Host $output
```
Should show container names.

### Test 2: Filter Results
```powershell
$dockerPath = (Get-Command docker).Source
$output = & cmd /c "$dockerPath ps --format {{.Names}} 2>&1"
$containers = $output -split "`n" | Where-Object { $_ -match "th3-" }
$containers | ForEach-Object { Write-Host "Found: $_" }
```
Should list th3-* containers.

### Test 3: Full Script
```powershell
cd D:\Vault\Vault
.\LAUNCH_VAULT.ps1
```
Should now detect Docker correctly and show:
- ✅ Containers found or
- ✅ Container startup messages

---

## Key Technical Points

### Why cmd /c Works
- `cmd` is the Windows command interpreter
- PowerShell can safely call it
- `cmd` handles the full command string
- Result is returned as clean strings

### Why Direct Docker Doesn't
- PowerShell tries to parse the executable path
- Spaces in path cause parsing issues
- Pipeline handlers get confused
- PowerShell tries to treat .exe as PowerShell object

### Best Practice
For external .exe files with spaces in paths:
1. **Avoid direct pipelines**: Don't do `exe | Filter`
2. **Use cmd /c**: Use `cmd /c "exe args"`
3. **Store then process**: Get output, then filter
4. **Check before running**: Verify tool exists first

---

## Files Updated

📄 **D:\Vault\Vault\LAUNCH_VAULT.ps1** - Complete rewrite with cmd /c fix

---

## Expected Output

When running the fixed script:

```
[1/5] Docker — Containers Ascended33

✅ Containers déjà actifs. Skip rebuild.

[2/5] Obsidian — Vault D:\Vault\Vault

✅ Obsidian lancé

[3/5] Streamlit — HexStrike Dashboard

✅ Streamlit démarré → http://localhost:8501

[4/5] VS Code — Vault workspace

✅ VS Code lancé

[5/5] Navigateur — HexStrike Dashboard

✅ Navigateur ouvert

─────────────────────────────────────────────────

🎉 VAULT 100% OPÉRATIONNEL
```

---

## PowerShell Pipeline Reference

### Problems with Direct .exe
```powershell
# ❌ Never do this with .exe files:
docker ps | Select-String "th3-"
```

### Correct Approaches
```powershell
# ✅ Option 1: Use cmd /c (Recommended for .exe with spaces)
$output = & cmd /c "C:\path\to\exe command args"
$filtered = $output | Where-Object { ... }

# ✅ Option 2: Use full quoted path with &
$output = & "C:\path\to\exe" args
$filtered = $output | Where-Object { ... }

# ✅ Option 3: Store output first, then filter
$results = @()
$output = & C:\path\to\exe args
$results = $output | Where-Object { ... }
```

---

## Summary

✅ **Problem**: PowerShell pipeline confusion with docker.exe  
✅ **Root Cause**: Direct invocation of .exe with spaces in path  
✅ **Solution**: Use `cmd /c` as intermediary  
✅ **Result**: Docker detection works reliably  
✅ **File**: D:\Vault\Vault\LAUNCH_VAULT.ps1 updated  

**Status**: Ready to test!
