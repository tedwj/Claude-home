# ============================================================================
# Windows Application Cleanup Script - COMPLETE VERSION
# ============================================================================
# 
# This script offers multiple cleanup levels:
# 1. Priority Only (safest - bloatware and duplicates)
# 2. Priority + Outdated Software
# 3. Priority + AMD/GIGABYTE Bloat
# 4. Full Cleanup (everything recommended)
#
# CRITICAL: Create a System Restore Point BEFORE running!
#
# To run this script:
# 1. Right-click PowerShell and select "Run as Administrator"
# 2. Navigate to the script location
# 3. Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# 4. Run: .\Remove-Applications-Complete.ps1
# ============================================================================

# Require Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "This script requires Administrator privileges!"
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'"
    pause
    exit
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "    Windows Application Cleanup - Complete Version" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Define application groups
$appGroups = @{
    "Priority" = @(
        "Disk Analyzer Pro",
        "Qualys BrowserCheck",
        "PuTTY release 0.78"
    )
    "Outdated" = @(
        "Node.js 14",
        "Python 3.9.5",
        "AlienVault Agent",
        "runZero Explorer",
        "Cheat Engine"
    )
    "AMD_Bloat" = @(
        "AMD Privacy View",
        "AMD Product Verification Tool",
        "AMD User Experience Program",
        "AMD DVR64",
        "AMD WVR64"
    )
    "GIGABYTE_Bloat" = @(
        "@BIOS",
        "EasyTune",
        "EasyTuneEngineService",
        "SIV",
        "GigabyteFirmwareUpdateUtility",
        "RGB Fusion",
        "Smart Backup",
        "GService"
    )
}

# Display menu
Write-Host "Select cleanup level:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Priority Only (Safest - bloatware and old versions)" -ForegroundColor Green
Write-Host "   - Disk Analyzer Pro, Qualys, old PuTTY" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Priority + Outdated Software" -ForegroundColor Yellow
Write-Host "   - Above + old Node.js, Python 3.9, AlienVault, runZero, Cheat Engine" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Priority + AMD/GIGABYTE Bloat" -ForegroundColor Yellow
Write-Host "   - Above + unnecessary AMD and GIGABYTE utilities" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Full Cleanup (All recommended removals)" -ForegroundColor Red
Write-Host "   - Everything listed above" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Custom Selection" -ForegroundColor Cyan
Write-Host "   - Choose which groups to remove" -ForegroundColor Gray
Write-Host ""
Write-Host "0. Exit" -ForegroundColor DarkGray
Write-Host ""

$choice = Read-Host "Enter your choice (0-5)"

# Determine which apps to remove based on choice
$appsToRemove = @()

switch ($choice) {
    "1" { 
        $appsToRemove = $appGroups["Priority"]
        Write-Host "`nSelected: Priority Only" -ForegroundColor Green
    }
    "2" { 
        $appsToRemove = $appGroups["Priority"] + $appGroups["Outdated"]
        Write-Host "`nSelected: Priority + Outdated Software" -ForegroundColor Yellow
    }
    "3" { 
        $appsToRemove = $appGroups["Priority"] + $appGroups["AMD_Bloat"] + $appGroups["GIGABYTE_Bloat"]
        Write-Host "`nSelected: Priority + AMD/GIGABYTE Bloat" -ForegroundColor Yellow
    }
    "4" { 
        $appsToRemove = $appGroups["Priority"] + $appGroups["Outdated"] + $appGroups["AMD_Bloat"] + $appGroups["GIGABYTE_Bloat"]
        Write-Host "`nSelected: Full Cleanup" -ForegroundColor Red
    }
    "5" {
        Write-Host "`nCustom Selection:" -ForegroundColor Cyan
        Write-Host "Include Priority removals? (yes/no): " -NoNewline
        if ((Read-Host) -eq "yes") { $appsToRemove += $appGroups["Priority"] }
        Write-Host "Include Outdated software? (yes/no): " -NoNewline
        if ((Read-Host) -eq "yes") { $appsToRemove += $appGroups["Outdated"] }
        Write-Host "Include AMD bloat? (yes/no): " -NoNewline
        if ((Read-Host) -eq "yes") { $appsToRemove += $appGroups["AMD_Bloat"] }
        Write-Host "Include GIGABYTE bloat? (yes/no): " -NoNewline
        if ((Read-Host) -eq "yes") { $appsToRemove += $appGroups["GIGABYTE_Bloat"] }
    }
    "0" {
        Write-Host "Exiting..." -ForegroundColor Gray
        exit
    }
    default {
        Write-Host "Invalid choice. Exiting..." -ForegroundColor Red
        pause
        exit
    }
}

if ($appsToRemove.Count -eq 0) {
    Write-Host "No applications selected. Exiting..." -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "The following applications will be targeted for removal:" -ForegroundColor Yellow
Write-Host ""
foreach ($app in $appsToRemove) {
    Write-Host "  - $app" -ForegroundColor White
}
Write-Host ""

# Safety confirmations
Write-Host "============================================================================" -ForegroundColor Red
Write-Host "  CRITICAL SAFETY CHECKS" -ForegroundColor Red
Write-Host "============================================================================" -ForegroundColor Red
Write-Host ""

$restorePoint = Read-Host "Have you created a System Restore Point? (yes/no)"
if ($restorePoint -ne 'yes') {
    Write-Host ""
    Write-Host "STOP! Create a System Restore Point first:" -ForegroundColor Red
    Write-Host "1. Press Windows key and type 'Create a restore point'" -ForegroundColor Yellow
    Write-Host "2. Click 'Create' button at the bottom" -ForegroundColor Yellow
    Write-Host "3. Name it 'Before App Cleanup' and wait for completion" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host ""
$finalConfirm = Read-Host "Type 'REMOVE' to proceed with uninstallation"
if ($finalConfirm -ne 'REMOVE') {
    Write-Host "Cancelled. Nothing was removed." -ForegroundColor Yellow
    pause
    exit
}

# Uninstall function
function Uninstall-Application {
    param ([string]$AppName)
    
    Write-Host "`n--- Processing: $AppName ---" -ForegroundColor Cyan
    
    $apps = @()
    $apps += Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like "*$AppName*" }
    $apps += Get-ItemProperty "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like "*$AppName*" }
    
    if ($apps.Count -eq 0) {
        Write-Host "Not found (may already be removed)" -ForegroundColor DarkGray
        return
    }
    
    foreach ($app in $apps) {
        $displayName = $app.DisplayName
        $uninstallString = $app.UninstallString
        
        Write-Host "Found: $displayName" -ForegroundColor White
        
        if ([string]::IsNullOrWhiteSpace($uninstallString)) {
            Write-Host "  ⚠ No uninstaller found - manual removal required" -ForegroundColor Yellow
            continue
        }
        
        Write-Host "  Uninstalling..." -ForegroundColor Green
        
        try {
            if ($uninstallString -match "msiexec") {
                $productCode = $uninstallString -replace ".*({[A-F0-9\-]+}).*", '$1'
                Start-Process "msiexec.exe" -ArgumentList "/x $productCode /qn /norestart" -Wait -NoNewWindow
                Write-Host "  ✓ Uninstalled successfully" -ForegroundColor Green
            }
            elseif ($uninstallString -match '(.+\.exe)(.*)') {
                $exePath = $matches[1].Trim('"')
                $arguments = $matches[2].Trim()
                if ($arguments -notmatch '/S|/silent|/quiet|/q') { $arguments += " /S" }
                
                if (Test-Path $exePath) {
                    Start-Process -FilePath $exePath -ArgumentList $arguments -Wait -NoNewWindow -ErrorAction Stop
                    Write-Host "  ✓ Uninstalled successfully" -ForegroundColor Green
                } else {
                    Write-Host "  ⚠ Uninstaller not found - manual removal required" -ForegroundColor Yellow
                }
            }
            else {
                Write-Host "  ⚠ Unsupported uninstaller - manual removal required" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "  ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "  Manual removal via Settings > Apps may be needed" -ForegroundColor Yellow
        }
        
        Start-Sleep -Milliseconds 500
    }
}

# Execute uninstallation
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Starting Uninstallation Process..." -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

$startTime = Get-Date

foreach ($app in $appsToRemove) {
    Uninstall-Application -AppName $app
    Start-Sleep -Seconds 1
}

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Uninstallation Complete!" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Time taken: $($duration.Minutes) minutes $($duration.Seconds) seconds" -ForegroundColor Gray
Write-Host ""
Write-Host "Important Notes:" -ForegroundColor Yellow
Write-Host "  • Some applications may require manual removal via Settings > Apps" -ForegroundColor White
Write-Host "  • Python 3.9.5 has multiple components - check for all of them" -ForegroundColor White
Write-Host "  • Restart may be needed for changes to take full effect" -ForegroundColor White
Write-Host ""
Write-Host "Recommended Next Steps:" -ForegroundColor Green
Write-Host "  1. Verify removals in Settings > Apps > Installed apps" -ForegroundColor White
Write-Host "  2. Restart your computer" -ForegroundColor White
Write-Host "  3. Run Disk Cleanup (cleanmgr.exe) to remove leftover files" -ForegroundColor White
Write-Host "  4. Consider running CCleaner or similar tool for registry cleanup" -ForegroundColor White
Write-Host ""

$restart = Read-Host "Would you like to restart now? (yes/no)"
if ($restart -eq 'yes') {
    Write-Host "Restarting in 10 seconds... (Close this window to cancel)" -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    Restart-Computer -Force
}

pause
