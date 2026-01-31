# ============================================================================
# Windows Application Cleanup Script - DRY RUN (Safe Preview)
# ============================================================================
# 
# This script shows what WOULD be removed without actually removing anything
# Run this FIRST to see what the cleanup script will do
#
# To run this script:
# 1. Right-click PowerShell and select "Run as Administrator"
# 2. Navigate to the script location: cd "C:\Path\To\Script"
# 3. Enable script execution: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# 4. Run: .\Preview-Removals.ps1
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "    Application Removal Preview - DRY RUN (Nothing will be removed)" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Define applications to check
$appsToCheck = @{
    "Priority Removals (Safe)" = @(
        "Disk Analyzer Pro",
        "Qualys BrowserCheck",
        "PuTTY release 0.78",
        "Python 3.9.5"
    )
    "Optional - Outdated Software" = @(
        "Node.js 14",
        "AlienVault Agent",
        "runZero Explorer",
        "Cheat Engine"
    )
    "Optional - AMD Bloat" = @(
        "AMD Privacy View",
        "AMD Product Verification Tool",
        "AMD User Experience Program",
        "AMD DVR64",
        "AMD WVR64"
    )
    "Optional - GIGABYTE Bloat" = @(
        "@BIOS",
        "EasyTune",
        "SIV",
        "GigabyteFirmwareUpdateUtility",
        "RGB Fusion",
        "Smart Backup",
        "GService"
    )
}

function Find-InstalledApps {
    param (
        [string]$AppName
    )
    
    $apps = @()
    $apps += Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | 
             Where-Object { $_.DisplayName -like "*$AppName*" }
    $apps += Get-ItemProperty "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | 
             Where-Object { $_.DisplayName -like "*$AppName*" }
    
    return $apps
}

$totalFound = 0
$totalSize = 0

foreach ($category in $appsToCheck.Keys) {
    Write-Host "--- $category ---" -ForegroundColor Yellow
    Write-Host ""
    
    $categoryFound = 0
    
    foreach ($appName in $appsToCheck[$category]) {
        $found = Find-InstalledApps -AppName $appName
        
        if ($found.Count -gt 0) {
            foreach ($app in $found) {
                $categoryFound++
                $totalFound++
                
                $size = "Unknown"
                if ($app.EstimatedSize) {
                    $sizeMB = [math]::Round($app.EstimatedSize / 1024, 2)
                    $size = "$sizeMB MB"
                    $totalSize += $app.EstimatedSize
                }
                
                Write-Host "  ✓ FOUND: $($app.DisplayName)" -ForegroundColor Green
                Write-Host "    Version: $($app.DisplayVersion)" -ForegroundColor Gray
                Write-Host "    Publisher: $($app.Publisher)" -ForegroundColor Gray
                Write-Host "    Size: $size" -ForegroundColor Gray
                
                if ($app.UninstallString) {
                    Write-Host "    Can be auto-removed: YES" -ForegroundColor Green
                } else {
                    Write-Host "    Can be auto-removed: NO (manual removal required)" -ForegroundColor Red
                }
                Write-Host ""
            }
        } else {
            Write-Host "  ✗ Not found: $appName" -ForegroundColor DarkGray
        }
    }
    
    if ($categoryFound -eq 0) {
        Write-Host "  No applications from this category are installed." -ForegroundColor DarkGray
    }
    
    Write-Host ""
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total applications found: $totalFound" -ForegroundColor Yellow

if ($totalSize -gt 0) {
    $totalSizeMB = [math]::Round($totalSize / 1024, 2)
    $totalSizeGB = [math]::Round($totalSize / 1024 / 1024, 2)
    Write-Host "Estimated total size: $totalSizeMB MB ($totalSizeGB GB)" -ForegroundColor Yellow
    Write-Host "Note: This doesn't include game sizes which can be much larger" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Review the applications listed above" -ForegroundColor White
Write-Host "2. If you want to proceed, run Remove-PriorityApps.ps1" -ForegroundColor White
Write-Host "3. Create a System Restore Point before removing anything" -ForegroundColor White
Write-Host ""

pause
