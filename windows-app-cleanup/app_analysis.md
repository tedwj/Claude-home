# Windows Application Audit & Cleanup Recommendations

**Total Applications:** 223  
**Analysis Date:** January 31, 2026

---

## 🎯 PRIORITY REMOVALS - Likely Unnecessary

### Bloatware & Trial Software
- **Disk Analyzer Pro** (Systweak Software) - Potentially unwanted software, often bundled
- **Qualys BrowserCheck** - Browser security check tool, usually not needed
- **AlienVault Agent** - Enterprise security monitoring (unless required for work)
- **runZero Explorer** - Network discovery tool (unless actively used)

### Duplicate/Old Utilities
- **PuTTY 0.78** - You have newer version 0.81 installed, remove the old one
- **Python 3.9.5** - You have Python 3.14.2, unless you specifically need 3.9 for compatibility

### Old/Unused Gaming Modding Tools
- **Cheat Engine 7.5** - Game memory editor (2023 install, may be outdated)

---

## 🟡 REVIEW CAREFULLY - May Not Be Needed

### AMD System Utilities (Consider Removing Some)
You have **extensive AMD software** installed. Most users only need AMD Software/Drivers:

**KEEP:**
- AMD Software (main control panel)
- AMD Chipset Software
- AMD Ryzen Master (if you overclock)

**CONSIDER REMOVING:**
- AMD Privacy View
- AMD Product Verification Tool
- AMD User Experience Program Installer
- AMD DVR64, WVR64 (video recording - only if unused)
- AMD GPIO2 Driver, PCI Driver, PSP Driver (usually auto-installed but may not be needed)

### GIGABYTE Motherboard Utilities
You have many GIGABYTE apps. Most are redundant:

**KEEP ONE:**
- APP Center (main utility hub)

**CONSIDER REMOVING:**
- @BIOS (firmware updates - only use when needed)
- EasyTune, EasyTuneEngineService (overclocking - if not used)
- SIV (system info - redundant with CPU-Z)
- GigabyteFirmwareUpdateUtility
- RGB Fusion (unless you control RGB lighting)
- Smart Backup
- GService

### RGB/Peripheral Software (Keep Only What You Use)
- Corsair iCUE5 (Corsair peripherals)
- Logitech G HUB (Logitech peripherals)
- NGENUITY (HyperX peripherals)
- Patriot Viper M2 SSD RGB
- Verbatim_SureFireGaming_Product
- Multiple ENE RGB HAL drivers

**Recommendation:** Only keep the ones for hardware you actually own and want to control

### Streaming/Virtual Camera Software
- **FaceRig** + virtual drivers - Avatar streaming (if unused, remove)
- **Animaze** - Newer version of FaceRig (pick one if you use this)
- **Voicemod** - Voice changer (if unused)

### Development Tools
- **Node.js 14.17.3** - Very outdated (current is 22.x), update or remove
- **Docker Desktop** - Large program, remove if not developing

---

## ✅ KEEP - Essential or Actively Used

### System Essentials
- All **Microsoft .NET** runtimes (required by many programs)
- All **Visual C++ Redistributables** (required by many programs)
- Microsoft Edge, Edge WebView2
- Windows Subsystem for Linux (if you use it)

### Security
- **Bitdefender Agent** - Antivirus (essential)
- **Cisco Secure Client** - VPN (likely required for work)
- **NextDNS** - DNS security

### Productivity
- Microsoft 365
- Adobe Acrobat
- Bitwarden (password manager)
- Notepad++
- PowerToys

### Utilities (Keep)
- 7-Zip
- Google Chrome, Firefox
- Google Drive
- VLC media player
- Wireshark (if you use it for network analysis)
- PuTTY 0.81
- HashTab
- CrystalDiskInfo (disk health monitoring)

### Gaming Platforms
- Steam
- Epic Games Launcher
- EA app
- Ubisoft Connect
- GOG GALAXY
- REDlauncher (CD Projekt RED)

### Monitoring Tools
- CPU-Z, HWMonitor (hardware monitoring)
- K-Lite Codec Pack (media playback)

---

## 🎮 GAMES - Evaluate Your Play Time

You have many games installed. Consider removing games you haven't played in 6+ months:

**Large AAA Games (Consider Removing if Not Playing):**
- Cyberpunk 2077
- Mass Effect Legendary Edition
- Ghost Recon Breakpoint/Wildlands
- The Elder Scrolls Online
- Path of Exile 2
- PGA TOUR 2K23
- Way of the Hunter
- Warframe

**Smaller/Idle Games:**
- AdVenture Capitalist
- Cell to Singularity
- Forts
- RISK: Global Domination
- Rogue Tower
- SpaceBourne 2
- Starvester Playtest
- Upload Labs
- Magic Archery

**Keep games you actively play** - you can always reinstall later

---

## 🔧 SPECIALTY TOOLS - Remove if Not Using

### IT/Security Professional Tools
- Splunk Enterprise (enterprise log management)
- STIG Viewer (security compliance)
- VanDyke SecureCRT (terminal emulator)
- Tftpd32 (TFTP server)
- Vector (data pipeline)
- Synergy (keyboard/mouse sharing)
- Npcap, USBPcap, Wireshark (packet capture)

**If you're not an IT professional or don't actively use these for work, remove them**

### System/Hardware Tools
- APC Back-UPS HS (UPS software - keep if you have APC UPS)
- WD P40 Game Drive (keep if you have this drive)
- Anker Upgrade (peripheral firmware)
- Easy Setting Box (Samsung monitor utility)
- Horizon HTML5 Multimedia Redirection Client (VMware Horizon)
- Omnissa Workspace ONE (device management)

### Miscellaneous
- BOINC (distributed computing - uses CPU/GPU for science projects when idle)
- DAX Studio (Power BI/Excel add-in)
- Measure Killer (data analysis tool)
- XML To CSV Converter
- TechSmith Screen Capture Codec
- Futuremark SystemInfo
- Equalizer APO (audio equalizer)
- qBittorrent (torrent client - keep if you use it)
- Google Earth Pro
- Google Play Games (Android game emulator)
- WiFiman Desktop (network analyzer)

---

## 📊 ESTIMATED SPACE SAVINGS

**High Priority Removals:** ~2-5 GB
**AMD/GIGABYTE Bloat:** ~1-3 GB  
**Unused Games:** Can vary from 50-500+ GB depending on which games
**Old Software/Duplicates:** ~1-2 GB

**Potential Total:** 54-510+ GB depending on game removals

---

## ⚠️ BEFORE YOU START

1. **Create a System Restore Point** - In case something goes wrong
2. **Backup important data** - Always good practice
3. **Check with IT if work computer** - Some software may be required by your employer
4. **Uninstall carefully** - Use "Revo Uninstaller" (you have it!) for stubborn programs

---

## 🚀 UNINSTALL PRIORITY ORDER

### Phase 1 - Safe Removals (Start Here)
1. Disk Analyzer Pro
2. Old PuTTY version (0.78)
3. Unused games (based on your play history)
4. Old Python 3.9.5 (if not needed)
5. Qualys BrowserCheck
6. Node.js 14.17.3 (update first, then remove old)

### Phase 2 - RGB/Peripheral Cleanup
1. Remove RGB software for hardware you don't own
2. Consolidate to one GIGABYTE utility (APP Center)

### Phase 3 - Specialty Tools
1. Remove IT tools if not needed for work
2. Remove Cheat Engine if not using
3. Remove FaceRig/Animaze if not streaming

### Phase 4 - Optional Deep Clean
1. AMD driver cleanup (keep essentials only)
2. GIGABYTE utilities purge
3. Game launcher consolidation

---

## 📝 NOTES

- Your system appears to be a **gaming/enthusiast PC** with AMD Ryzen + AMD GPU
- You have **GIGABYTE motherboard** with extensive utilities
- Multiple **RGB peripheral** brands suggest hardware customization
- **IT/Security tools** suggest professional use or hobbyist interest
- Consider updating **Node.js** - version 14.17.3 is very outdated

**Questions to Ask Yourself:**
- Do I stream or create content? (Affects FaceRig/Voicemod decision)
- Do I do IT work? (Affects Wireshark/Splunk/SecureCRT)
- Do I overclock? (Affects AMD Ryzen Master/EasyTune)
- Do I care about RGB lighting? (Affects iCUE/G HUB/RGB Fusion)
- Which games have I played in the last 3 months?

