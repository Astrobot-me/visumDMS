# ws_server.py
import asyncio
import websockets
import json
import datetime

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print("[ESP32 → PY]", message)
    finally:
        connected_clients.remove(websocket)

async def broadcast_state(state, label):
    if not connected_clients:
        return

    payload = {
        "state": state,
        "label": label,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    message = json.dumps(payload)
    await asyncio.gather(
        *[client.send(message) for client in connected_clients]
    )

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("[WS] Server started on port 8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
