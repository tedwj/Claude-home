#!/usr/bin/env python3
"""
Application Removal Script
Stops running processes and uninstalls specified applications
Must be run as Administrator
"""

import subprocess
import sys
import time
import winreg
import os

# Applications to remove
APPS_TO_REMOVE = [
    {
        "name": "EA Desktop",
        "processes": ["EADesktop.exe", "EABackgroundService.exe", "EALauncher.exe"],
        "search_terms": ["EA Desktop", "EA app"]
    },
    {
        "name": "Epic Games Launcher",
        "processes": ["EpicGamesLauncher.exe", "EpicWebHelper.exe"],
        "search_terms": ["Epic Games Launcher"]
    },
    {
        "name": "Wargaming.net Game Center",
        "processes": ["wgc.exe", "wgc_api.exe"],
        "search_terms": ["Wargaming.net Game Center", "Wargaming Game Center"]
    },
    {
        "name": "Docker Desktop",
        "processes": ["Docker Desktop.exe", "com.docker.backend.exe", "com.docker.proxy.exe", 
                     "vpnkit.exe", "dockerd.exe"],
        "search_terms": ["Docker Desktop"]
    }
]

def is_admin():
    """Check if script is running with administrator privileges"""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def print_header():
    """Print script header"""
    print("=" * 70)
    print("Application Removal Script".center(70))
    print("=" * 70)
    print()

def kill_process(process_name):
    """Kill a process by name"""
    try:
        # Use taskkill to force close the process
        result = subprocess.run(
            ["taskkill", "/F", "/IM", process_name, "/T"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  ✓ Killed process: {process_name}")
            return True
        elif "not found" in result.stderr.lower():
            print(f"  - Process not running: {process_name}")
            return True
        else:
            print(f"  ! Could not kill {process_name}: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"  ✗ Error killing {process_name}: {e}")
        return False

def get_installed_apps():
    """Get list of installed applications from registry"""
    apps = []
    
    # Registry paths to check
    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    
    for hkey, path in registry_paths:
        try:
            key = winreg.OpenKey(hkey, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    try:
                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        try:
                            uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]
                        except:
                            uninstall_string = None
                        
                        apps.append({
                            "name": display_name,
                            "uninstall": uninstall_string,
                            "key_path": f"{path}\\{subkey_name}"
                        })
                    except:
                        pass
                    
                    winreg.CloseKey(subkey)
                except:
                    continue
            
            winreg.CloseKey(key)
        except:
            continue
    
    return apps

def find_app_uninstaller(app_name, search_terms):
    """Find uninstaller for an application"""
    print(f"\n[*] Searching for: {app_name}")
    installed_apps = get_installed_apps()
    
    for app in installed_apps:
        for term in search_terms:
            if term.lower() in app["name"].lower():
                print(f"  ✓ Found: {app['name']}")
                if app["uninstall"]:
                    print(f"    Uninstaller: {app['uninstall']}")
                    return app
                else:
                    print(f"    ! No uninstaller found in registry")
                    return None
    
    print(f"  ! Not found in registry")
    return None

def uninstall_app(uninstall_string):
    """Execute uninstaller"""
    if not uninstall_string:
        return False
    
    try:
        # Handle MsiExec uninstallers
        if "msiexec" in uninstall_string.lower():
            # Extract product code
            import re
            match = re.search(r'\{[A-F0-9\-]+\}', uninstall_string)
            if match:
                product_code = match.group(0)
                cmd = ["msiexec.exe", "/x", product_code, "/qn", "/norestart"]
                print(f"    Running: msiexec /x {product_code} /qn /norestart")
        else:
            # Handle regular uninstallers
            # Add silent flags
            if "/S" not in uninstall_string and "/SILENT" not in uninstall_string.upper():
                uninstall_string += " /S"
            
            # Split command and arguments
            if uninstall_string.startswith('"'):
                # Command is quoted
                end_quote = uninstall_string.find('"', 1)
                exe = uninstall_string[1:end_quote]
                args = uninstall_string[end_quote+1:].strip().split()
            else:
                parts = uninstall_string.split()
                exe = parts[0]
                args = parts[1:] if len(parts) > 1 else []
            
            cmd = [exe] + args
            print(f"    Running: {' '.join(cmd)}")
        
        # Execute uninstaller
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"  ✓ Uninstalled successfully")
            return True
        else:
            print(f"  ! Uninstaller returned code {result.returncode}")
            if result.stderr:
                print(f"    Error: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ! Uninstaller timed out (5 minutes)")
        return False
    except Exception as e:
        print(f"  ✗ Error running uninstaller: {e}")
        return False

def main():
    """Main execution"""
    print_header()
    
    # Check for admin privileges
    if not is_admin():
        print("ERROR: This script must be run as Administrator!")
        print("\nTo run as Administrator:")
        print("1. Right-click PowerShell")
        print("2. Select 'Run as Administrator'")
        print("3. Run: python Remove-Game-Launchers.py")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("This script will:")
    print("• Stop running processes")
    print("• Uninstall the following applications:")
    for app in APPS_TO_REMOVE:
        print(f"  - {app['name']}")
    print()
    
    # Confirm
    response = input("Do you want to continue? (yes/no): ").strip().lower()
    if response != "yes":
        print("\nCancelled by user.")
        sys.exit(0)
    
    print("\n" + "=" * 70)
    print("PHASE 1: Stopping Running Processes".center(70))
    print("=" * 70)
    
    # Stop all processes first
    for app in APPS_TO_REMOVE:
        print(f"\n[*] Stopping {app['name']} processes...")
        for process in app['processes']:
            kill_process(process)
    
    print("\n" + "=" * 70)
    print("PHASE 2: Uninstalling Applications".center(70))
    print("=" * 70)
    
    results = []
    
    # Uninstall each application
    for app in APPS_TO_REMOVE:
        found_app = find_app_uninstaller(app['name'], app['search_terms'])
        
        if found_app and found_app['uninstall']:
            print(f"  [*] Attempting to uninstall...")
            success = uninstall_app(found_app['uninstall'])
            results.append({
                "name": app['name'],
                "status": "Success" if success else "Failed",
                "found": True
            })
        else:
            results.append({
                "name": app['name'],
                "status": "Not Found",
                "found": False
            })
        
        time.sleep(2)  # Wait between uninstalls
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY".center(70))
    print("=" * 70)
    print()
    
    for result in results:
        status_symbol = "✓" if result['status'] == "Success" else "✗" if result['status'] == "Failed" else "!"
        print(f"{status_symbol} {result['name']}: {result['status']}")
    
    print("\n" + "=" * 70)
    print()
    print("NOTES:")
    print("• Some applications may require manual removal via Settings > Apps")
    print("• Docker Desktop may require a system restart to fully remove")
    print("• Check Settings > Apps > Installed apps to verify removals")
    print()
    print("NEXT STEPS:")
    print("1. Verify apps are removed in Settings > Apps")
    print("2. Restart your computer")
    print("3. Check Task Manager > Startup to ensure they're gone")
    print()
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
