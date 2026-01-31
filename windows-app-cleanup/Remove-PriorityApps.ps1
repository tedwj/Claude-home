# ============================================================================
# Windows Application Cleanup Script - Priority Removals
# ============================================================================
# 
# IMPORTANT: READ BEFORE RUNNING
# 1. Create a System Restore Point BEFORE running this script
# 2. Run PowerShell as Administrator
# 3. Review the list of applications that will be removed
# 4. Close all running applications before executing
#
# To run this script:
# 1. Right-click PowerShell and select "Run as Administrator"
# 2. Navigate to the script location: cd "C:\Path\To\Script"
# 3. Enable script execution: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# 4. Run: .\Remove-PriorityApps.ps1
# ============================================================================

# Require Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "This script requires Administrator privileges!"
    Write-Host "Please right-click PowerShell and select 'Run as Administrator', then run this script again."
    pause
    exit
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "    Windows Application Cleanup - Priority Removals" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Define applications to remove (using partial name matching)
$appsToRemove = @(
    "Disk Analyzer Pro",
    "Qualys BrowserCheck",
    "PuTTY release 0.78",
    "Python 3.9.5"
)

Write-Host "The following applications will be removed:" -ForegroundColor Yellow
Write-Host ""
foreach ($app in $appsToRemove) {
    Write-Host "  - $app" -ForegroundColor White
}
Write-Host ""

# Ask for confirmation
Write-Host "============================================================================" -ForegroundColor Red
Write-Host "  WARNING: This will uninstall the above applications!" -ForegroundColor Red
Write-Host "============================================================================" -ForegroundColor Red
Write-Host ""
$confirmation = Read-Host "Have you created a System Restore Point? (yes/no)"
if ($confirmation -ne 'yes') {
    Write-Host ""
    Write-Host "Please create a System Restore Point first:" -ForegroundColor Yellow
    Write-Host "1. Type 'Create a restore point' in Windows Search" -ForegroundColor White
    Write-Host "2. Click 'Create' button" -ForegroundColor White
    Write-Host "3. Name it 'Before App Cleanup' and click Create" -ForegroundColor White
    Write-Host ""
    Write-Host "Script cancelled. Run again after creating restore point." -ForegroundColor Red
    pause
    exit
}

Write-Host ""
$finalConfirm = Read-Host "Are you absolutely sure you want to proceed? (yes/no)"
if ($finalConfirm -ne 'yes') {
    Write-Host "Script cancelled by user." -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Starting uninstallation process..." -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Function to uninstall application
function Uninstall-Application {
    param (
        [string]$AppName
    )
    
    Write-Host "Searching for: $AppName" -ForegroundColor Yellow
    
    # Get all installed applications from both registry locations
    $apps = @()
    $apps += Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | 
             Where-Object { $_.DisplayName -like "*$AppName*" }
    $apps += Get-ItemProperty "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | 
             Where-Object { $_.DisplayName -like "*$AppName*" }
    
    if ($apps.Count -eq 0) {
        Write-Host "  Not found or already removed." -ForegroundColor Gray
        return
    }
    
    foreach ($app in $apps) {
        $displayName = $app.DisplayName
        $uninstallString = $app.UninstallString
        
        if ([string]::IsNullOrWhiteSpace($uninstallString)) {
            Write-Host "  Found: $displayName" -ForegroundColor White
            Write-Host "  WARNING: No uninstall string found. Manual removal required." -ForegroundColor Red
            continue
        }
        
        Write-Host "  Found: $displayName" -ForegroundColor White
        Write-Host "  Uninstalling..." -ForegroundColor Green
        
        try {
            # Handle MsiExec uninstallers
            if ($uninstallString -match "msiexec") {
                $productCode = $uninstallString -replace ".*({[A-F0-9\-]+}).*", '$1'
                $arguments = "/x $productCode /qn /norestart"
                Start-Process "msiexec.exe" -ArgumentList $arguments -Wait -NoNewWindow
                Write-Host "  Successfully uninstalled!" -ForegroundColor Green
            }
            # Handle standard uninstallers
            elseif ($uninstallString -match '(.+\.exe)(.*)') {
                $exePath = $matches[1].Trim('"')
                $arguments = $matches[2].Trim()
                
                # Add silent flags if not present
                if ($arguments -notmatch '/S|/silent|/quiet|/q') {
                    $arguments += " /S"
                }
                
                if (Test-Path $exePath) {
                    Start-Process -FilePath $exePath -ArgumentList $arguments -Wait -NoNewWindow
                    Write-Host "  Successfully uninstalled!" -ForegroundColor Green
                } else {
                    Write-Host "  WARNING: Uninstaller not found at: $exePath" -ForegroundColor Red
                    Write-Host "  You may need to uninstall manually via Settings > Apps" -ForegroundColor Yellow
                }
            }
            else {
                Write-Host "  WARNING: Unsupported uninstall method." -ForegroundColor Red
                Write-Host "  Uninstall manually via Settings > Apps > Installed apps" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "  You may need to uninstall manually via Settings > Apps" -ForegroundColor Yellow
        }
        
        Write-Host ""
    }
}

# Process each application
foreach ($app in $appsToRemove) {
    Uninstall-Application -AppName $app
    Start-Sleep -Seconds 2
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Uninstallation process complete!" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTES:" -ForegroundColor Yellow
Write-Host "- Some applications may require manual removal via Settings > Apps" -ForegroundColor White
Write-Host "- Python 3.9.5 has multiple components - remove all of them if found" -ForegroundColor White
Write-Host "- A system restart may be recommended for some uninstallers" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Check Settings > Apps > Installed apps to verify removals" -ForegroundColor White
Write-Host "2. Restart your computer if prompted" -ForegroundColor White
Write-Host "3. Run disk cleanup to remove leftover files" -ForegroundColor White
Write-Host ""

pause
