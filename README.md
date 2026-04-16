# 🚀 Telegraf Premium - Modern Desktop Messenger

**Version 2.1 - Registration Edition**

Premium desktop messenger with beautiful glassmorphism UI, mandatory registration system, end-to-end encryption, and zero-friction launch.

---

## ✨ What's New in v2.1

### 🔐 Mandatory Registration System
- **User registration required** - No anonymous access
- **Secure login** - Username and password authentication
- **Local database** - SQLite storage with password hashing (SHA-256)
- **User validation** - Minimum 3 chars username, 4 chars password
- **Toggle mode** - Easy switch between login and registration

### 🎨 Application Icon
- **Custom icon** - Modern gradient design with rocket emoji
- **Multi-size** - Optimized for Windows (16x16 to 256x256)
- **Auto-generation** - Created automatically during build
- **Professional look** - Used in .exe and installer

### 📦 Improved Installer
- **Choose directory** - User can select installation location
- **Easy uninstall** - Option to keep or delete chat history
- **Russian support** - Full Russian language in installer
- **Shortcuts** - Desktop, Start Menu, Quick Launch options

---

## ✨ Features

### 🎨 Premium UI
- **Glassmorphism design** - Frosted glass effects with blur
- **Smooth animations** - Fade-in messages, hover effects
- **Modern gradients** - Beautiful color transitions
- **Custom window** - Frameless design with draggable title bar
- **Dark theme** - Easy on the eyes

### 🔐 Security
- **Mandatory registration** - Users must register before access
- **Password authentication** - SHA-256 hashed passwords
- **User database** - Secure SQLite storage
- **End-to-end encryption** - AES-256 + RSA-2048
- **Secure key exchange** - Automatic public key distribution
- **Private messages** - Relay server cannot read content

### 🌐 Zero-Friction Launch
- **Auto-connect** - Connects to server automatically
- **No configuration** - Works out of the box
- **Fallback servers** - Multiple server options
- **Instant start** - Beautiful splash screen

### 💬 Messaging
- **Real-time chat** - WebSocket communication
- **Message history** - All messages saved
- **Typing indicators** - See when someone is typing
- **Online status** - Real-time presence
- **Multi-user** - Chat with multiple people

---

## 🚀 Quick Start

### For End Users (4 Steps):

1. **Run** `START.bat`
2. **Wait** 2-5 minutes (first time only)
3. **Register** with username and password
4. **Start chatting!**

### First Time Registration:
- Click "Регистрация" (Registration)
- Enter username (min 3 characters)
- Enter password (min 4 characters)
- Click "Зарегистрироваться" (Register)

### Login:
- Enter your username
- Enter your password
- Click "Войти" (Login)

### For Developers:

```bash
# Local testing
START_RELAY.bat  # Terminal 1: Start relay server
RUN.bat          # Terminal 2: Start client

# Build executable
BUILD.bat

# Quick run (after setup)
RUN.bat
```

---

## 📦 What Gets Installed

When you run `START.bat`:

✅ Python 3.11 (if not installed)
✅ Virtual environment
✅ All dependencies (PyQt6, websockets, cryptography)
✅ Project structure
✅ Telegraf.exe build

**Zero manual setup required!**

---

## 🎨 UI Components

### Premium Components:
- **GlassButton** - Animated buttons with hover effects
- **GlassInput** - Input fields with glow on focus
- **GlassPanel** - Frosted glass containers
- **MessageBubble** - Animated message bubbles
- **UserListItem** - Interactive user cards
- **SearchBar** - Live search with glass effect
- **TypingIndicator** - Animated typing dots
- **ConnectionStatus** - Real-time connection indicator
- **SplashScreen** - Beautiful startup animation

---

## 🌐 Global Connectivity

### Deploy Relay Server (5 minutes):

#### Option 1: Render.com (Recommended)
1. Go to https://render.com
2. Create new Web Service
3. Upload `/relay` folder
4. Deploy (auto-detected)
5. Copy URL: `wss://your-app.onrender.com`

#### Option 2: Railway.app
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select `/relay` folder
4. Get URL from dashboard

#### Option 3: Fly.io
```bash
cd relay
fly launch
fly deploy
```

### Configure Client:

Edit `config/config.json`:
```json
{
    "relay_server": "wss://your-app.onrender.com",
    "fallback_servers": [
        "wss://backup-server.com"
    ]
}
```

### Rebuild:
```bash
BUILD.bat
```

Now share `dist/Telegraf.exe` with friends worldwide!

---

## 📁 Project Structure

```
telegraf/
├── START.bat              ← Run this first!
├── RUN.bat               ← Quick launch
├── BUILD.bat             ← Build .exe
├── START_RELAY.bat       ← Local server
│
├── client/               ← Client application
│   ├── main.py          (Premium UI + Registration)
│   ├── database.py      (User database)
│   ├── components.py    (Reusable components)
│   ├── styles.py        (Style system)
│   └── encryption.py    (E2E encryption)
│
├── relay/               ← Relay server
│   ├── server.py        (WebSocket relay)
│   ├── requirements.txt
│   ├── Procfile         (For cloud deploy)
│   └── README.md
│
├── assets/              ← Application assets
│   ├── telegraf.ico     (App icon)
│   └── telegraf.png     (Icon preview)
│
├── config/
│   └── config.json      ← Configuration
│
├── data/
│   └── users.db         ← User database (auto-created)
│
├── scripts/
│   ├── build.py         (Build script)
│   ├── create_icon.py   (Icon generator)
│   └── test.py          (Test script)
│
├── dist/
│   └── Telegraf.exe     ← Built executable
│
├── installer/
│   ├── telegraf.iss         ← Inno Setup script
│   └── Telegraf_Setup.exe   ← Windows installer
│
└── Documentation:
    ├── README.md            (This file)
    ├── КАК_ЗАПУСТИТЬ.md     (Russian setup guide)
    ├── SETUP_GUIDE.md       (English setup guide)
    ├── QUICKSTART.md        (Quick start guide)
    ├── DEPLOYMENT.md        (Deployment guide)
    ├── INSTALLER.md         (Installer guide)
    ├── UPGRADE.md           (v2.0 changes)
    └── STATUS.md            (Project status)
```

---

## 🎯 Usage

### First Time:
```bash
START.bat
```
- Installs everything automatically
- Builds executable
- Launches client

### After Setup:
```bash
RUN.bat
```
- Instant launch
- No installation needed

### Build Only:
```bash
BUILD.bat
```
- Creates `dist/Telegraf.exe`
- Ready to share

### Build Installer:
```bash
BUILD_INSTALLER.bat
```
- Creates `installer/Telegraf_Setup.exe`
- Professional Windows installer
- See `INSTALLER.md` for details

---

## 🔧 Configuration

### config.json Options:

```json
{
    "relay_server": "ws://localhost:8765",
    "fallback_servers": [],
    "auto_connect": true,
    "show_splash": true,
    
    "ui": {
        "theme": "glassmorphism",
        "animations": true,
        "blur_radius": 20,
        "opacity": 0.7
    },
    
    "network": {
        "timeout": 30,
        "reconnect_interval": 5,
        "max_reconnect_attempts": 10
    },
    
    "window": {
        "width": 1400,
        "height": 900,
        "frameless": true,
        "transparent": true
    }
}
```

---

## 🎨 Customization

### Change Colors:

Edit `client/styles.py`:
```python
COLORS = {
    'primary': 'rgba(100, 150, 255, 200)',
    'secondary': 'rgba(150, 100, 255, 200)',
    'success': 'rgba(100, 200, 100, 200)',
    # ... customize
}
```

### Adjust Animations:
```python
ANIMATION_DURATION = {
    'fast': 150,
    'normal': 300,
    'slow': 500,
}
```

### Modify Gradients:
```python
GRADIENTS = {
    'primary': """
        qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(100, 150, 255, 200),
            stop:1 rgba(150, 100, 255, 200))
    """,
}
```

---

## 🧪 Testing

### Local Test (Same Computer):

1. **Terminal 1**: `START_RELAY.bat`
2. **Terminal 2**: `RUN.bat` (User 1)
3. **Terminal 3**: `RUN.bat` (User 2)
4. Register different users and chat!

### Global Test (Different Cities):

1. Deploy relay to Render.com
2. Update `config.json` with URL
3. Build: `BUILD.bat`
4. Share `Telegraf.exe` with friend
5. Both run and chat!

---

## 🛠️ Technology Stack

- **Client**: PyQt6 (GUI framework)
- **Network**: WebSockets (real-time)
- **Encryption**: cryptography (AES + RSA)
- **Build**: PyInstaller (standalone .exe)
- **Server**: Python asyncio + websockets

---

## 📋 Requirements

- Windows 10/11
- Python 3.11+ (auto-installed)
- Internet connection

**No manual setup required!**

---

## 🐛 Troubleshooting

### "Cannot connect to server"
→ Check `config.json` relay URL
→ Verify relay server is running
→ Check internet connection

### "Python not found"
→ Restart computer after START.bat
→ Or install Python 3.11 manually

### "Build failed"
→ Run `pip install -r requirements.txt`
→ Check Python version: `python --version`

### Window not draggable
→ Click and drag the title bar (top area)

---

## 🎯 What's New in v2.1

| Feature | v2.0 | v2.1 |
|---------|------|------|
| Registration | Optional | **Mandatory** |
| User Database | None | **SQLite** |
| Password Auth | Basic | **SHA-256 hashed** |
| Application Icon | None | **Custom icon** |
| Installer | Basic | **Choose directory** |
| Uninstall | Delete all | **Keep/delete data** |
| Language | English | **Russian support** |

See `SETUP_GUIDE.md` for full changelog.

---

## 💡 Tips

- **Drag window**: Click title bar and drag
- **Minimize**: Click − button
- **Close**: Click × button
- **Search users**: Type in search bar at top
- **Send message**: Press Enter or click 📤
- **Voice messages**: Coming soon!

---

## 🎉 Success!

You now have a **premium, production-ready messenger** with:

✅ Beautiful glassmorphism UI
✅ Zero-friction launch
✅ Smooth animations everywhere
✅ End-to-end encryption
✅ Global connectivity
✅ Professional polish

**Just run START.bat and start chatting!** 🚀✨💬

---

## 📄 License

MIT License - Free to use and modify

---

## 🤝 Contributing

This is a complete MVP. Feel free to extend it!

Possible improvements:
- Voice messages
- File sharing
- Group chats
- Stickers
- Mobile app
- Video calls
- Profile pictures
- Message editing/deletion

---

## 📞 Support

- Full docs: `README.md` (this file)
- Russian guide: `КАК_ЗАПУСТИТЬ.md` ⭐ **Detailed setup instructions**
- Setup guide: `SETUP_GUIDE.md`
- Quick start: `QUICKSTART.md`
- Deployment: `DEPLOYMENT.md`
- Changelog: `UPGRADE.md`
- Status: `STATUS.md`

---

**Telegraf Premium - Modern messaging with mandatory registration, beautifully designed.** 💎🔐
