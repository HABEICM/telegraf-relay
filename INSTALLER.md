# 📦 TELEGRAF - WINDOWS INSTALLER GUIDE

## ✅ Professional Installation Package

**Version:** 2.0.0
**Installer Type:** Inno Setup
**Output:** Telegraf_Setup.exe

---

## 🚀 Quick Build

### Step 1: Build the Application
```bash
cd C:\Users\habeicm\Desktop\telegraf
BUILD.bat
```
**Result:** Creates `dist\Telegraf.exe`

### Step 2: Build the Installer
```bash
BUILD_INSTALLER.bat
```
**Result:** Creates `installer\Telegraf_Setup.exe`

### Step 3: Distribute
Share `installer\Telegraf_Setup.exe` with users!

---

## 📋 Prerequisites

### Required Software:
1. **Inno Setup 6** (Free)
   - Download: https://jrsoftware.org/isdl.php
   - Install to default location: `C:\Program Files (x86)\Inno Setup 6\`

2. **Built Application**
   - Run `BUILD.bat` first to create `dist\Telegraf.exe`

### Required Files:
```
telegraf/
├── dist/
│   └── Telegraf.exe          ✅ From BUILD.bat
├── config/
│   └── config.json           ✅ Present
├── assets/
│   ├── telegraf.ico          ⚠️ Optional (app icon)
│   ├── wizard-image.bmp      ⚠️ Optional (installer image)
│   └── wizard-small.bmp      ⚠️ Optional (installer logo)
├── README.md                 ✅ Present
├── QUICKSTART.md             ✅ Present
├── INSTRUCTIONS.md           ✅ Present
└── installer/
    └── telegraf.iss          ✅ Present
```

---

## 🎯 What the Installer Does

### Installation Features:
✅ **Installation Wizard**
- Welcome screen
- Choose installation directory
- Select components
- Progress bar
- Completion screen

✅ **Shortcuts Created**
- Desktop icon (optional)
- Start Menu folder with:
  - Telegraf launcher
  - README
  - Uninstall shortcut

✅ **File Installation**
- Main executable: `Telegraf.exe`
- Configuration: `config.json`
- Documentation: README, QUICKSTART, INSTRUCTIONS
- Assets folder (if present)

✅ **Directory Setup**
- Creates `logs` folder
- Creates `data` folder
- Sets proper permissions

✅ **Uninstall Support**
- Appears in Windows "Programs and Features"
- Option to keep or delete user data
- Complete cleanup

---

## 🛠️ Customization

### Change App Version:
Edit `installer\telegraf.iss`:
```inno
#define MyAppVersion "2.0.0"  ← Change this
```

### Change Install Location:
```inno
DefaultDirName={autopf}\{#MyAppName}  ← Default: C:\Program Files\Telegraf
```

### Add/Remove Files:
```inno
[Files]
Source: "dist\Telegraf.exe"; DestDir: "{app}"
Source: "config\config.json"; DestDir: "{app}\config"
; Add more files here
```

### Customize Icons:
```inno
[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Add more shortcuts here
```

---

## 🧪 Testing the Installer

### Test Installation:
1. Run `installer\Telegraf_Setup.exe`
2. Follow wizard steps
3. Choose installation directory
4. Select desktop icon option
5. Complete installation
6. Launch from Start Menu or Desktop

### Test Uninstallation:
1. Open Windows Settings → Apps
2. Find "Telegraf"
3. Click Uninstall
4. Choose to keep or delete data
5. Verify complete removal

---

## 📊 Installer Details

### Technical Specs:
- **Compression:** LZMA2/Max (best compression)
- **Architecture:** x64 only
- **Min Windows:** Windows 10
- **Privileges:** User-level (no admin required)
- **Style:** Modern wizard UI

### File Sizes (Approximate):
- Telegraf.exe: ~50-80 MB
- Installer: ~30-50 MB (compressed)
- Installed: ~100-150 MB

---

## 🎨 Adding Custom Icons

### App Icon (telegraf.ico):
1. Create 256x256 PNG icon
2. Convert to .ico format (use online converter)
3. Save as `assets\telegraf.ico`
4. Rebuild installer

### Wizard Images:
- **wizard-image.bmp**: 164x314 pixels (left side)
- **wizard-small.bmp**: 55x58 pixels (top right)

---

## 🚨 Troubleshooting

### Error: "Inno Setup not found"
**Solution:**
1. Download from https://jrsoftware.org/isdl.php
2. Install to default location
3. Restart command prompt
4. Run `BUILD_INSTALLER.bat` again

### Error: "Telegraf.exe not found"
**Solution:**
```bash
BUILD.bat  # Build app first
BUILD_INSTALLER.bat  # Then build installer
```

### Error: "Installer script not found"
**Solution:**
Verify `installer\telegraf.iss` exists

### Installer Won't Run:
**Solution:**
- Right-click → Properties → Unblock
- Run as Administrator (if needed)
- Check Windows Defender/Antivirus

---

## 📦 Distribution

### For Friends/Local Network:
1. Share `installer\Telegraf_Setup.exe`
2. Users run it → Next → Install → Done
3. No Python or dependencies needed!

### For Website/Download:
1. Upload `Telegraf_Setup.exe` to hosting
2. Provide download link
3. Users download and install

### For Enterprise:
1. Test installer thoroughly
2. Create deployment script
3. Use Group Policy or SCCM
4. Silent install: `Telegraf_Setup.exe /SILENT`

---

## 🎯 Silent Installation

### Command Line Options:
```bash
# Silent install (no UI)
Telegraf_Setup.exe /SILENT

# Very silent (no progress)
Telegraf_Setup.exe /VERYSILENT

# Custom directory
Telegraf_Setup.exe /DIR="C:\MyApps\Telegraf"

# No desktop icon
Telegraf_Setup.exe /TASKS="!desktopicon"

# Silent uninstall
unins000.exe /SILENT
```

---

## ✅ Final Checklist

### Before Building:
- ✅ `BUILD.bat` completed successfully
- ✅ `dist\Telegraf.exe` exists and works
- ✅ Inno Setup 6 installed
- ✅ All documentation files present
- ✅ Config files ready

### After Building:
- ✅ `installer\Telegraf_Setup.exe` created
- ✅ Installer runs without errors
- ✅ App installs correctly
- ✅ Shortcuts work
- ✅ App launches from Start Menu
- ✅ Uninstall works properly

---

## 🎉 Success!

**You now have a professional Windows installer!**

### Distribution Ready:
✅ One-click installation
✅ No dependencies required
✅ Professional wizard UI
✅ Start Menu integration
✅ Clean uninstall
✅ Production quality

### Share with confidence:
```
installer\Telegraf_Setup.exe
```

**Users just run it and enjoy!** 🚀💬✨
