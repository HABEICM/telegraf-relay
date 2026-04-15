"""
Telegraf Relay Server
WebSocket relay server for connecting users globally
Deploy on Render.com, Railway.app, or Fly.io
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime
from collections import defaultdict
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connected clients: {user_id: websocket}
clients = {}
# User data: {user_id: {username, status, public_key}}
users = {}
# Message queue for offline users
message_queue = defaultdict(list)

async def register_user(websocket, data):
    """Register new user"""
    user_id = data.get('user_id')
    username = data.get('username')
    public_key = data.get('public_key')

    users[user_id] = {
        'username': username,
        'status': 'online',
        'public_key': public_key,
        'last_seen': datetime.now().isoformat()
    }
    clients[user_id] = websocket

    logger.info(f"User registered: {username} ({user_id})")

    # Send pending messages
    if user_id in message_queue:
        for msg in message_queue[user_id]:
            await websocket.send(json.dumps(msg))
        message_queue[user_id].clear()

    # Notify all users about new user
    await broadcast({
        'type': 'user_online',
        'user_id': user_id,
        'username': username
    }, exclude=user_id)

    # Send user list to new user
    user_list = [
        {'user_id': uid, **udata}
        for uid, udata in users.items()
        if uid != user_id
    ]

    await websocket.send(json.dumps({
        'type': 'user_list',
        'users': user_list
    }))

async def handle_message(websocket, data):
    """Route message to recipient"""
    recipient_id = data.get('to')
    sender_id = data.get('from')

    message = {
        'type': 'message',
        'from': sender_id,
        'from_username': users.get(sender_id, {}).get('username', 'Unknown'),
        'to': recipient_id,
        'content': data.get('content'),
        'encrypted': data.get('encrypted', False),
        'timestamp': datetime.now().isoformat(),
        'message_type': data.get('message_type', 'text')
    }

    # Try to send to online user
    if recipient_id in clients:
        try:
            await clients[recipient_id].send(json.dumps(message))
            logger.info(f"Message delivered: {sender_id} -> {recipient_id}")
        except:
            # User disconnected, queue message
            message_queue[recipient_id].append(message)
            logger.info(f"Message queued for offline user: {recipient_id}")
    else:
        # Queue for offline user
        message_queue[recipient_id].append(message)
        logger.info(f"Message queued for offline user: {recipient_id}")

    # Send delivery confirmation
    await websocket.send(json.dumps({
        'type': 'message_sent',
        'status': 'delivered' if recipient_id in clients else 'queued'
    }))

async def handle_typing(websocket, data):
    """Notify recipient that user is typing"""
    recipient_id = data.get('to')
    sender_id = data.get('from')

    if recipient_id in clients:
        await clients[recipient_id].send(json.dumps({
            'type': 'typing',
            'from': sender_id,
            'from_username': users.get(sender_id, {}).get('username', 'Unknown')
        }))

async def get_public_key(websocket, data):
    """Send user's public key for encryption"""
    user_id = data.get('user_id')

    if user_id in users:
        await websocket.send(json.dumps({
            'type': 'public_key',
            'user_id': user_id,
            'public_key': users[user_id].get('public_key')
        }))

async def broadcast(message, exclude=None):
    """Broadcast message to all connected clients"""
    disconnected = []

    for user_id, ws in clients.items():
        if user_id != exclude:
            try:
                await ws.send(json.dumps(message))
            except:
                disconnected.append(user_id)

    # Clean up disconnected clients
    for user_id in disconnected:
        await handle_disconnect(user_id)

async def handle_disconnect(user_id):
    """Handle user disconnection"""
    if user_id in clients:
        del clients[user_id]

    if user_id in users:
        users[user_id]['status'] = 'offline'
        users[user_id]['last_seen'] = datetime.now().isoformat()

        logger.info(f"User disconnected: {user_id}")

        # Notify others
        await broadcast({
            'type': 'user_offline',
            'user_id': user_id
        })

async def handler(websocket, path):
    """Main WebSocket handler"""
    user_id = None

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type')

                if msg_type == 'register':
                    user_id = data.get('user_id')
                    await register_user(websocket, data)

                elif msg_type == 'message':
                    await handle_message(websocket, data)

                elif msg_type == 'typing':
                    await handle_typing(websocket, data)

                elif msg_type == 'get_public_key':
                    await get_public_key(websocket, data)

                elif msg_type == 'ping':
                    await websocket.send(json.dumps({'type': 'pong'}))

            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
            except Exception as e:
                logger.error(f"Error handling message: {e}")

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if user_id:
            await handle_disconnect(user_id)

async def main():
    """Start relay server"""
    port = int(os.environ.get('PORT', 8765))

    logger.info(f"Starting Telegraf Relay Server on port {port}")

    # Updated for websockets 16.0+ - handler is now a connection handler
    async with websockets.serve(
        lambda ws: handler(ws, ws.request.path if hasattr(ws, 'request') else '/'),
        "0.0.0.0",
        port
    ):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
