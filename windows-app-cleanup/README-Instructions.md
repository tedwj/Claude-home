# Application Cleanup Scripts - Usage Guide

## 📋 What's Included

You have **3 PowerShell scripts** to help clean up your Windows applications:

1. **Preview-Removals.ps1** - Safe preview (RECOMMENDED TO RUN FIRST)
2. **Remove-PriorityApps.ps1** - Remove only safe priority items
3. **Remove-Applications-Complete.ps1** - Full cleanup with multiple options

---

## 🚀 Quick Start - Recommended Order

### Step 1: Preview What Will Be Removed (SAFE - Nothing gets deleted)

```powershell
# 1. Right-click PowerShell and select "Run as Administrator"
# 2. Navigate to where you saved the scripts:
cd "C:\Users\YourName\Downloads"

# 3. Allow script execution (temporary):
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 4. Run the preview:
.\Preview-Removals.ps1
```

This will show you:
- What applications were found on your system
- How much space they take up
- Whether they can be auto-removed or need manual removal

### Step 2: Create System Restore Point (CRITICAL!)

**Before removing anything:**
1. Press Windows key
2. Type "Create a restore point"
3. Click the "Create" button
4. Name it "Before App Cleanup"
5. Wait for it to complete

### Step 3: Choose Your Cleanup Script

#### Option A: Priority Only (Safest)
Removes only confirmed bloatware and duplicate versions:
```powershell
.\Remove-PriorityApps.ps1
```

#### Option B: Complete Cleanup (More Options)
Interactive menu with 5 cleanup levels:
```powershell
.\Remove-Applications-Complete.ps1
```

Choose from:
1. Priority Only (safest)
2. Priority + Outdated Software  
3. Priority + AMD/GIGABYTE Bloat
4. Full Cleanup
5. Custom Selection

---

## ⚠️ IMPORTANT SAFETY NOTES

### BEFORE Running Any Removal Script:

✅ **Must Do:**
- Create System Restore Point
- Close all running applications
- Run PowerShell as Administrator
- Review what will be removed

❌ **Don't:**
- Skip the System Restore Point
- Run while applications are open
- Run without reviewing the preview first
- Panic if something needs manual removal

### What Gets Removed by Each Script:

**Remove-PriorityApps.ps1:**
- Disk Analyzer Pro (bloatware)
- Qualys BrowserCheck (unnecessary)
- PuTTY 0.78 (you have 0.81)
- Python 3.9.5 (you have 3.14.2)

**Remove-Applications-Complete.ps1 (Full):**
- Everything above, plus:
- Node.js 14 (very outdated)
- AlienVault Agent
- runZero Explorer  
- Cheat Engine
- AMD Privacy View, DVR64, WVR64, Product Verification Tool
- GIGABYTE: @BIOS, EasyTune, SIV, RGB Fusion, Smart Backup, GService

---

## 🔧 Troubleshooting

### "Execution Policy" Error
Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### "Access Denied" Error
You need to run PowerShell as Administrator:
1. Right-click PowerShell icon
2. Select "Run as Administrator"

### Script Shows "Not Found"
The application may already be removed or uses a different name. This is fine - skip it.

### "Manual Removal Required"
Some apps don't have silent uninstallers. Remove them via:
1. Settings → Apps → Installed apps
2. Find the app and click Uninstall

### Python 3.9.5 Has Multiple Entries
This is normal - Python installs many components. The script will attempt to remove all of them, but you may need to manually verify in Settings → Apps.

---

## 📊 After Running the Scripts

### Verify Removals:
1. Open Settings → Apps → Installed apps
2. Search for the removed application names
3. Check if they're gone

### Clean Up Leftovers:
1. Run Disk Cleanup:
   - Press Windows key + R
   - Type: `cleanmgr.exe`
   - Select drive C:
   - Check all boxes and click OK

2. Optional: Use CCleaner or similar tool for registry cleanup

### Restart Your Computer
Some uninstallers require a restart to complete removal.

---

## 🆘 If Something Goes Wrong

### Restore Your System:
1. Press Windows key
2. Type "Create a restore point"
3. Click "System Restore"
4. Select "Before App Cleanup" restore point
5. Follow the wizard

This will undo all changes made by the scripts.

---

## 📝 What Each File Does

| File | Purpose | Safety Level |
|------|---------|--------------|
| Preview-Removals.ps1 | Shows what would be removed (nothing actually removed) | 100% Safe |
| Remove-PriorityApps.ps1 | Removes only confirmed bloatware/duplicates | Very Safe |
| Remove-Applications-Complete.ps1 | Interactive menu with multiple cleanup options | User's Choice |
| app_analysis.md | Full analysis report of all your applications | Info Only |

---

## 💡 Tips

- **Start with the preview script** - See what's on your system first
- **Use Priority Only first** - Test that everything works
- **Wait a day** - Make sure nothing broke before doing more cleanup
- **Keep your restore point** - Don't delete it for at least a week
- **Check Settings > Apps** - Some apps need manual removal

---

## 🎯 Expected Results

**Space Savings:**
- Priority removals: 500MB - 2GB
- With outdated software: 1GB - 3GB  
- With AMD/GIGABYTE bloat: 2GB - 5GB
- Plus any games you remove separately: 50GB - 500GB+

**Performance:**
- Fewer background processes
- Faster system startup
- Less clutter in menus

---

## ❓ FAQ

**Q: Will this break my system?**
A: No, if you create a restore point first. The priority removals are very safe.

**Q: What if I remove something I need?**
A: Use the System Restore Point to undo changes.

**Q: Can I reinstall removed applications?**
A: Yes, you can download and reinstall anything you removed.

**Q: Should I remove AMD/GIGABYTE utilities?**
A: Only if you don't use them. Keep AMD Software (main driver) and APP Center (if you use it).

**Q: What about the games?**
A: Games are not included in these scripts - remove them manually via Steam/Epic/etc.

**Q: Why isn't Python 3.9.5 being removed?**
A: Python installs in components. You may need to manually remove remaining pieces from Settings > Apps.

---

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Use System Restore to go back
3. Post the error message for more help

**Remember:** When in doubt, use the Preview script first and start with Priority Only!
