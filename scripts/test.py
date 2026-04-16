"""
Test script for Telegraf
"""

import asyncio
import websockets
import json

async def test_relay_server(url):
    """Test connection to relay server"""
    print(f"Testing connection to {url}...")

    try:
        async with websockets.connect(url) as websocket:
            print("✅ Connected successfully!")

            # Send ping
            await websocket.send(json.dumps({"type": "ping"}))
            print("📤 Sent ping")

            # Receive pong
            response = await websocket.recv()
            data = json.loads(response)

            if data.get("type") == "pong":
                print("✅ Received pong - server is working!")
                return True
            else:
                print(f"❌ Unexpected response: {data}")
                return False

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test local server
    print("Testing local relay server...")
    result = asyncio.run(test_relay_server("ws://localhost:8765"))

    if result:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Tests failed. Check if relay server is running.")
