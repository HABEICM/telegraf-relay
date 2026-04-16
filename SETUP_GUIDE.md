# 🚀 Quick Setup Guide

## What's New

### ✅ Mandatory Registration System
- Users MUST register before using the app
- Login with username and password
- Secure database storage (SQLite)
- Password hashing (SHA-256)

### ✅ Application Icon
- Custom Telegraf icon created
- Used in .exe and installer
- Modern gradient design

### ✅ Improved Installer
- User can choose installation directory
- Option to keep/delete data on uninstall
- Russian language support
- Desktop and Start Menu shortcuts

---

## Quick Start

### 1. Build the Application

```bash
BUILD.bat
```

This will:
- Create the icon (if not exists)
- Build `dist/Telegraf.exe` with icon
- Include all dependencies

### 2. Create Installer (Optional)

```bash
BUILD_INSTALLER.bat
```

Requirements: Inno Setup 6

Output: `installer/Telegraf_Setup.exe`

### 3. First Run

1. Launch `Telegraf.exe` or run `RUN.bat`
2. Click "Регистрация" (Registration)
3. Enter username (min 3 chars)
4. Enter password (min 4 chars)
5. Click "Зарегистрироваться" (Register)

### 4. Login

1. Enter your username
2. Enter your password
3. Click "Войти" (Login)

---

## File Structure

```
telegraf/
├── assets/
│   ├── telegraf.ico          ← Application icon
│   └── telegraf.png          ← Icon preview
├── client/
│   ├── main.py               ← Updated with registration
│   ├── database.py           ← User database manager
│   └── ...
├── data/
│   └── users.db              ← User database (auto-created)
├── installer/
│   └── telegraf.iss          ← Updated installer script
├── scripts/
│   ├── build.py              ← Updated to use icon
│   └── create_icon.py        ← Icon generator
└── КАК_ЗАПУСТИТЬ.md          ← Detailed Russian guide
```

---

## Key Features

### Registration System
- **Database**: SQLite (`data/users.db`)
- **Password**: SHA-256 hashed
- **User ID**: Generated from username+password
- **Validation**: 
  - Username: min 3 chars, unique
  - Password: min 4 chars

### Login Dialog
- Toggle between Login/Register modes
- Real-time error messages
- Success notifications
- Enter key support

### Installer
- Choose installation directory
- Desktop shortcut option
- Start Menu shortcut option
- Uninstall keeps/deletes data option
- Russian language support

---

## Sharing with Friends

### Option 1: Share .exe
1. Build: `BUILD.bat`
2. Share: `dist/Telegraf.exe`
3. Friends run it directly

### Option 2: Share Installer
1. Build installer: `BUILD_INSTALLER.bat`
2. Share: `installer/Telegraf_Setup.exe`
3. Friends install with custom directory

### Option 3: Deploy Server
1. Deploy `relay/` to Render.com or Railway.app
2. Update `config/config.json` with server URL
3. Rebuild and share

See `КАК_ЗАПУСТИТЬ.md` for detailed deployment guide.

---

## Testing

### Local Network Test
1. Terminal 1: `START_RELAY.bat`
2. Terminal 2: `RUN.bat` (User 1 - register)
3. Terminal 3: `RUN.bat` (User 2 - register)
4. Chat between users

### Registration Test
1. Try to login without registration → Error
2. Register new user → Success
3. Try to register same username → Error
4. Login with correct credentials → Success
5. Login with wrong password → Error

---

## Troubleshooting

### "User already exists"
- Choose different username
- Or delete `data/users.db` to reset

### "Invalid username or password"
- Check spelling
- Make sure you registered first
- Delete `data/users.db` if forgot password

### Icon not showing
- Run `python scripts/create_icon.py`
- Rebuild with `BUILD.bat`

### Build fails
- Install Pillow: `pip install Pillow`
- Update requirements: `pip install -r requirements.txt`

---

## Changes Made

### 1. client/main.py
- Added `UserDatabase` import
- Updated `LoginDialog`:
  - Added database instance
  - Added toggle between login/register
  - Added error label with animations
  - Implemented proper login validation
  - Implemented proper registration validation
  - User ID now from database

### 2. client/database.py
- Already existed, no changes needed
- Handles user registration and login
- SQLite database in `data/users.db`

### 3. scripts/create_icon.py
- New file
- Generates `assets/telegraf.ico`
- Creates PNG preview
- Multiple sizes for Windows

### 4. scripts/build.py
- Auto-creates icon if missing
- Uses icon in PyInstaller build
- Fixed emoji encoding issues

### 5. installer/telegraf.iss
- Added `DisableDirPage=no` for directory selection
- Added Russian messages
- Updated uninstall to ask about data
- Added Start Menu task option
- Fixed icon references

### 6. requirements.txt
- Added `Pillow>=10.0.0` for icon generation

### 7. КАК_ЗАПУСТИТЬ.md
- Comprehensive Russian guide
- Step-by-step instructions
- Deployment options
- Troubleshooting section

---

## Summary

✅ **Registration system** - Users must register before login
✅ **Application icon** - Custom icon for .exe and installer  
✅ **Improved installer** - Choose directory, keep/delete data
✅ **Russian guide** - Detailed instructions in Russian
✅ **Better UX** - Error messages, success notifications

**Ready to share with friends!** 🎉
