# 🚀 TELEGRAF - QUICK START GUIDE

## For End Users (5 Steps)

### Option 1: Use Pre-built Executable (Easiest)

1. **Download** `Telegraf.exe` from `dist/` folder
2. **Run** `Telegraf.exe`
3. **Register** with username and password
4. **Wait** for connection to relay server
5. **Start chatting!**

### Option 2: Build from Source

1. **Run** `START.bat` (double-click)
   - Everything installs automatically
   - Takes 2-5 minutes first time
2. **Register** when app opens
3. **Start chatting!**

## For Developers

### Local Testing (2 Users on Same Network)

1. **Terminal 1**: Start relay server
   ```bash
   cd relay
   python server.py
   ```

2. **Terminal 2**: Start client 1
   ```bash
   python client/main.py
   ```

3. **Terminal 3**: Start client 2
   ```bash
   python client/main.py
   ```

4. Register different users and test messaging!

### Global Deployment (Users in Different Cities)

#### Step 1: Deploy Relay Server (5 minutes)

**Render.com (Recommended)**:
1. Go to https://render.com
2. New Web Service → Connect GitHub
3. Upload `/relay` folder
4. Deploy (auto-detected)
5. Copy URL: `https://your-app.onrender.com`

**Railway.app**:
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select `/relay` folder
4. Get URL from dashboard

#### Step 2: Configure Client

Edit `config/config.json`:
```json
{
    "relay_server": "wss://your-app.onrender.com"
}
```

#### Step 3: Rebuild (if needed)

```bash
BUILD.bat
```

#### Step 4: Distribute

Share `dist/Telegraf.exe` with friends anywhere in the world!

## What Gets Installed Automatically

When you run `START.bat`:

✅ Python 3.11 (if not installed)
✅ Virtual environment
✅ All dependencies (PyQt6, websockets, cryptography)
✅ Project structure
✅ Telegraf.exe build

**Zero manual setup required!**

## Features

- 💬 Real-time messaging
- 🔐 End-to-end encryption (AES-256 + RSA-2048)
- 👥 Multi-user support
- 🌐 Global connectivity (no port forwarding)
- 🎨 Modern Telegram-like UI
- 📦 Standalone .exe

## Troubleshooting

### "Cannot connect to server"
- Check `config/config.json` has correct relay URL
- Verify relay server is running
- Check internet connection

### "Python not found" (after START.bat)
- Restart computer after Python installation
- Or manually install Python 3.11 from python.org

### "Build failed"
- Run `pip install -r requirements.txt` manually
- Check Python version: `python --version`

## File Structure

```
telegraf/
├── START.bat          ← Run this first!
├── RUN.bat           ← Quick launch after setup
├── BUILD.bat         ← Rebuild .exe
├── README.md         ← Full documentation
├── DEPLOYMENT.md     ← Deployment guide
│
├── client/           ← Client application
├── relay/            ← Relay server (deploy to cloud)
├── config/           ← Configuration
├── scripts/          ← Build scripts
└── dist/             ← Built executables
    └── Telegraf.exe  ← Share this!
```

## Security

- All messages encrypted end-to-end
- Keys never leave your device
- Relay server cannot read messages
- Passwords hashed with SHA-256

## Support

- Full docs: `README.md`
- Deployment: `DEPLOYMENT.md`
- Issues: Check logs in `/logs`

## That's It!

**Just run START.bat and you're ready to chat!** 🎉

No configuration, no manual setup, no technical knowledge required.
