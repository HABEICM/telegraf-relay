# Telegraf Relay Server

Deploy this relay server to connect users globally without port forwarding.

## Quick Deploy Options

### Option 1: Render.com (Recommended)
1. Go to https://render.com
2. Create new Web Service
3. Connect this GitHub repo or upload files
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python server.py`
6. Deploy!

Your server URL will be: `https://your-app.onrender.com`

### Option 2: Railway.app
1. Go to https://railway.app
2. New Project -> Deploy from GitHub
3. Select this folder
4. Railway auto-detects and deploys
5. Get your URL from dashboard

### Option 3: Fly.io
```bash
fly launch
fly deploy
```

## Configuration

After deployment, copy your server URL (e.g., `wss://your-app.onrender.com`) and update:
`C:\Users\habeicm\Desktop\telegraf\config\config.json`

Set `relay_server` to your deployed URL.

## Environment Variables

- `PORT` - automatically set by hosting platform

## Testing

Test your relay server:
```bash
python server.py
```

Connect via WebSocket client to verify it works.
