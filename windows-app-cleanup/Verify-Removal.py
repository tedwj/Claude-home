#!/usr/bin/env python3
"""
Application Removal Verification Script
Captures system state before and after removal, then generates comparison report
"""

import subprocess
import json
import os
import sys
from datetime import datetime
import winreg

# Target applications to track
TARGET_APPS = [
    "EA Desktop",
    "EA app", 
    "Epic Games Launcher",
    "Wargaming.net Game Center",
    "Wargaming Game Center",
    "Docker Desktop"
]

TARGET_PROCESSES = [
    "EADesktop.exe",
    "EABackgroundService.exe", 
    "EALauncher.exe",
    "EpicGamesLauncher.exe",
    "EpicWebHelper.exe",
    "wgc.exe",
    "wgc_api.exe",
    "Docker Desktop.exe",
    "com.docker.backend.exe",
    "com.docker.proxy.exe",
    "dockerd.exe"
]

TARGET_PORTS = [2179]  # Docker's main port

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")

def get_installed_apps():
    """Get all installed applications from registry"""
    apps = []
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
                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                        except:
                            version = "Unknown"
                        try:
                            publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                        except:
                            publisher = "Unknown"
                        
                        apps.append({
                            "name": display_name,
                            "version": version,
                            "publisher": publisher
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

def get_running_processes():
    """Get list of running processes"""
    try:
        result = subprocess.run(
            ["powershell", "-Command", 
             "Get-Process | Select-Object ProcessName, Id, @{Name='MemoryMB';Expression={[math]::Round($_.WorkingSet/1MB,2)}} | ConvertTo-Json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return []

def get_startup_programs():
    """Get startup programs"""
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-CimInstance Win32_StartupCommand | Select-Object Name, Command | ConvertTo-Json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return []

def get_listening_ports():
    """Get listening ports"""
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-NetTCPConnection -State Listen | Select-Object LocalPort, @{Name='ProcessName';Expression={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}} | ConvertTo-Json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # Handle single item (not a list)
            if isinstance(data, dict):
                return [data]
            return data
    except:
        pass
    return []

def filter_target_apps(apps):
    """Filter for target applications only"""
    filtered = []
    for app in apps:
        for target in TARGET_APPS:
            if target.lower() in app["name"].lower():
                filtered.append(app)
                break
    return filtered

def filter_target_processes(processes):
    """Filter for target processes only"""
    filtered = []
    if isinstance(processes, list):
        for proc in processes:
            if isinstance(proc, dict) and "ProcessName" in proc:
                for target in TARGET_PROCESSES:
                    if target.lower() == proc["ProcessName"].lower():
                        filtered.append(proc)
                        break
    return filtered

def filter_target_ports(ports):
    """Filter for target ports only"""
    filtered = []
    if isinstance(ports, list):
        for port in ports:
            if isinstance(port, dict) and "LocalPort" in port:
                if port["LocalPort"] in TARGET_PORTS:
                    filtered.append(port)
    return filtered

def filter_target_startup(startup_items):
    """Filter for target startup programs"""
    filtered = []
    if isinstance(startup_items, list):
        for item in startup_items:
            if isinstance(item, dict) and "Command" in item:
                for target in ["EA", "Epic", "Wargaming", "wgc", "Docker"]:
                    if target.lower() in item["Command"].lower():
                        filtered.append(item)
                        break
    return filtered

def capture_state():
    """Capture current system state"""
    print("Capturing system state...")
    
    state = {
        "timestamp": datetime.now().isoformat(),
        "installed_apps": [],
        "running_processes": [],
        "startup_programs": [],
        "listening_ports": []
    }
    
    print("  [1/4] Scanning installed applications...")
    all_apps = get_installed_apps()
    state["installed_apps"] = filter_target_apps(all_apps)
    print(f"        Found {len(state['installed_apps'])} target apps")
    
    print("  [2/4] Checking running processes...")
    all_processes = get_running_processes()
    state["running_processes"] = filter_target_processes(all_processes)
    print(f"        Found {len(state['running_processes'])} target processes")
    
    print("  [3/4] Checking startup programs...")
    all_startup = get_startup_programs()
    state["startup_programs"] = filter_target_startup(all_startup)
    print(f"        Found {len(state['startup_programs'])} target startup items")
    
    print("  [4/4] Checking listening ports...")
    all_ports = get_listening_ports()
    state["listening_ports"] = filter_target_ports(all_ports)
    print(f"        Found {len(state['listening_ports'])} target ports")
    
    return state

def save_state(state, filename):
    """Save state to JSON file"""
    with open(filename, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"\n✓ State saved to: {filename}")

def load_state(filename):
    """Load state from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def compare_states(before, after):
    """Compare before and after states"""
    comparison = {
        "apps_removed": [],
        "apps_remaining": [],
        "processes_stopped": [],
        "processes_remaining": [],
        "startup_removed": [],
        "startup_remaining": [],
        "ports_closed": [],
        "ports_remaining": []
    }
    
    # Compare apps
    before_app_names = {app["name"] for app in before["installed_apps"]}
    after_app_names = {app["name"] for app in after["installed_apps"]}
    
    comparison["apps_removed"] = list(before_app_names - after_app_names)
    comparison["apps_remaining"] = list(after_app_names)
    
    # Compare processes
    before_proc_names = {proc["ProcessName"] for proc in before["running_processes"]}
    after_proc_names = {proc["ProcessName"] for proc in after["running_processes"]}
    
    comparison["processes_stopped"] = list(before_proc_names - after_proc_names)
    comparison["processes_remaining"] = list(after_proc_names)
    
    # Compare startup
    before_startup_names = {item["Name"] for item in before["startup_programs"]}
    after_startup_names = {item["Name"] for item in after["startup_programs"]}
    
    comparison["startup_removed"] = list(before_startup_names - after_startup_names)
    comparison["startup_remaining"] = list(after_startup_names)
    
    # Compare ports
    before_ports = {port["LocalPort"] for port in before["listening_ports"]}
    after_ports = {port["LocalPort"] for port in after["listening_ports"]}
    
    comparison["ports_closed"] = list(before_ports - after_ports)
    comparison["ports_remaining"] = list(after_ports)
    
    return comparison

def generate_report(before, after, comparison, output_file):
    """Generate detailed comparison report"""
    report = []
    
    report.append("=" * 80)
    report.append("APPLICATION REMOVAL VERIFICATION REPORT".center(80))
    report.append("=" * 80)
    report.append("")
    report.append(f"Before Snapshot: {before['timestamp']}")
    report.append(f"After Snapshot:  {after['timestamp']}")
    report.append("")
    
    # Apps section
    report.append("=" * 80)
    report.append("INSTALLED APPLICATIONS")
    report.append("=" * 80)
    report.append("")
    
    if comparison["apps_removed"]:
        report.append("✓ SUCCESSFULLY REMOVED:")
        for app in comparison["apps_removed"]:
            report.append(f"  • {app}")
        report.append("")
    else:
        report.append("! NO APPLICATIONS WERE REMOVED")
        report.append("")
    
    if comparison["apps_remaining"]:
        report.append("✗ STILL INSTALLED:")
        for app in comparison["apps_remaining"]:
            report.append(f"  • {app}")
        report.append("")
    else:
        report.append("✓ All target applications removed!")
        report.append("")
    
    # Processes section
    report.append("=" * 80)
    report.append("RUNNING PROCESSES")
    report.append("=" * 80)
    report.append("")
    
    if comparison["processes_stopped"]:
        report.append("✓ PROCESSES STOPPED:")
        for proc in comparison["processes_stopped"]:
            report.append(f"  • {proc}")
        report.append("")
    
    if comparison["processes_remaining"]:
        report.append("✗ PROCESSES STILL RUNNING:")
        for proc in comparison["processes_remaining"]:
            report.append(f"  • {proc}")
        report.append("")
    else:
        report.append("✓ All target processes stopped!")
        report.append("")
    
    # Startup section
    report.append("=" * 80)
    report.append("STARTUP PROGRAMS")
    report.append("=" * 80)
    report.append("")
    
    if comparison["startup_removed"]:
        report.append("✓ REMOVED FROM STARTUP:")
        for item in comparison["startup_removed"]:
            report.append(f"  • {item}")
        report.append("")
    
    if comparison["startup_remaining"]:
        report.append("✗ STILL IN STARTUP:")
        for item in comparison["startup_remaining"]:
            report.append(f"  • {item}")
        report.append("")
    else:
        report.append("✓ All target startup items removed!")
        report.append("")
    
    # Ports section
    report.append("=" * 80)
    report.append("LISTENING PORTS")
    report.append("=" * 80)
    report.append("")
    
    if comparison["ports_closed"]:
        report.append("✓ PORTS CLOSED:")
        for port in comparison["ports_closed"]:
            report.append(f"  • Port {port}")
        report.append("")
    
    if comparison["ports_remaining"]:
        report.append("✗ PORTS STILL LISTENING:")
        for port in comparison["ports_remaining"]:
            report.append(f"  • Port {port}")
        report.append("")
    else:
        report.append("✓ All target ports closed!")
        report.append("")
    
    # Summary
    report.append("=" * 80)
    report.append("SUMMARY")
    report.append("=" * 80)
    report.append("")
    
    total_removed = len(comparison["apps_removed"])
    total_remaining = len(comparison["apps_remaining"])
    success_rate = (total_removed / (total_removed + total_remaining) * 100) if (total_removed + total_remaining) > 0 else 0
    
    report.append(f"Applications Removed: {total_removed}")
    report.append(f"Applications Remaining: {total_remaining}")
    report.append(f"Success Rate: {success_rate:.1f}%")
    report.append("")
    
    if total_remaining == 0:
        report.append("✓ ALL TARGET APPLICATIONS SUCCESSFULLY REMOVED!")
    elif total_removed > 0:
        report.append("! PARTIAL SUCCESS - Some applications still remain")
        report.append("  Manual removal may be required via Settings > Apps")
    else:
        report.append("✗ NO APPLICATIONS WERE REMOVED")
        report.append("  Check if the removal script ran correctly")
    
    report.append("")
    report.append("=" * 80)
    
    # Write to file
    report_text = "\n".join(report)
    with open(output_file, 'w') as f:
        f.write(report_text)
    
    return report_text

def main():
    """Main execution"""
    print_header("Application Removal Verification Tool")
    
    print("This tool captures system state before and after app removal")
    print("to verify that applications were successfully removed.")
    print()
    print("Usage:")
    print("  1. Run this BEFORE removal: python Verify-Removal.py before")
    print("  2. Run removal script: python Remove-Game-Launchers.py")
    print("  3. Run this AFTER removal: python Verify-Removal.py after")
    print()
    
    if len(sys.argv) < 2:
        print("ERROR: Please specify 'before' or 'after'")
        print("\nExamples:")
        print("  python Verify-Removal.py before")
        print("  python Verify-Removal.py after")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    before_file = os.path.join(desktop, "system_state_before.json")
    after_file = os.path.join(desktop, "system_state_after.json")
    report_file = os.path.join(desktop, "removal_verification_report.txt")
    
    if mode == "before":
        print_header("CAPTURING 'BEFORE' STATE")
        state = capture_state()
        save_state(state, before_file)
        
        print("\n✓ Before state captured!")
        print("\nNext steps:")
        print("  1. Run: python Remove-Game-Launchers.py")
        print("  2. After removal, run: python Verify-Removal.py after")
        
    elif mode == "after":
        print_header("CAPTURING 'AFTER' STATE")
        
        # Load before state
        before_state = load_state(before_file)
        if not before_state:
            print("ERROR: Before state not found!")
            print(f"Please run 'python Verify-Removal.py before' first")
            sys.exit(1)
        
        print(f"✓ Loaded before state from: {before_file}\n")
        
        # Capture after state
        after_state = capture_state()
        save_state(after_state, after_file)
        
        # Compare
        print("\nComparing states...")
        comparison = compare_states(before_state, after_state)
        
        # Generate report
        print("Generating report...")
        report_text = generate_report(before_state, after_state, comparison, report_file)
        
        print(f"\n✓ Report saved to: {report_file}")
        print("\n" + "=" * 80)
        print("REPORT PREVIEW")
        print("=" * 80)
        print(report_text)
        
    else:
        print(f"ERROR: Invalid mode '{mode}'")
        print("Use 'before' or 'after'")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
