# Telegraf Deployment Guide

## Deploy Relay Server to Render.com

### Step-by-Step Instructions

1. **Create Render Account**
   - Go to https://render.com
   - Sign up (free tier available)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Choose "Build and deploy from a Git repository"

3. **Connect Repository**
   - Option A: Push `/relay` folder to GitHub
   - Option B: Use Render's manual deploy

4. **Configure Service**
   - Name: `telegraf-relay`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py`
   - Instance Type: Free

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)

6. **Get Your URL**
   - Copy the URL: `https://telegraf-relay.onrender.com`
   - Convert to WebSocket: `wss://telegraf-relay.onrender.com`

7. **Update Client Config**
   - Edit `config/config.json`
   - Set `relay_server` to your URL
   - Rebuild client if needed

### Alternative: Railway.app

1. Go to https://railway.app
2. New Project → "Deploy from GitHub"
3. Select repository with `/relay` folder
4. Railway auto-detects Python and deploys
5. Get URL from dashboard
6. Update client config

### Alternative: Fly.io

```bash
cd relay
fly auth login
fly launch --name telegraf-relay
fly deploy
```

Get URL: `wss://telegraf-relay.fly.dev`

## Testing Deployment

Test your relay server:

```bash
# Install wscat
npm install -g wscat

# Connect to your server
wscat -c wss://your-relay-server.onrender.com

# Send test message
{"type":"ping"}

# Should receive
{"type":"pong"}
```

## Troubleshooting

### Server not responding
- Check Render/Railway logs
- Verify PORT environment variable is set
- Check if service is sleeping (free tier)

### Connection refused
- Ensure using `wss://` (not `ws://`)
- Check firewall settings
- Verify URL is correct

### Messages not delivered
- Check both clients are connected
- Verify encryption keys exchanged
- Check server logs for errors

## Free Tier Limitations

### Render.com
- Sleeps after 15 min inactivity
- 750 hours/month free
- Wakes up on first request (cold start)

### Railway.app
- $5 free credit/month
- No sleep
- Better for active use

### Fly.io
- 3 VMs free
- Always on
- Best performance

## Production Recommendations

For production use:
1. Use paid tier (no sleep)
2. Add SSL certificate (auto on Render/Railway)
3. Set up monitoring
4. Add rate limiting
5. Implement user authentication
6. Add database for message history

## Security Notes

- Always use WSS (secure WebSocket)
- Don't expose relay server URL publicly
- Implement rate limiting
- Add authentication if needed
- Monitor for abuse

## Support

If deployment fails:
- Check Render/Railway logs
- Verify Python version (3.11)
- Ensure requirements.txt is correct
- Test locally first

## Success!

Once deployed, your relay server URL should work globally.

Share `Telegraf.exe` with friends and start chatting! 🚀
