import asyncio
import websockets
import json


location = {
        "latitude":" 28.974033",
        "longitude":"77.640352",
        "address":"Delhi Roorkee Bypass Road, Meerut Rural, Meerut 250005, Uttar Pradesh Meerut Rural Meerut Uttar Pradesh India"
}

async def receive_location():
    uri = "ws://localhost:8000/ws/location"
    async with websockets.connect(uri) as websocket:
        message = await websocket.recv()
        data = json.loads(message)
        print(data)
        return data 
    

async def location_stream():
    uri = "ws://localhost:8000/ws/location"
    async with websockets.connect(uri) as websocket:
        print("[WebSocket] Connected to location stream...")
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                location.update(data)
            except Exception as e:
                print(f"[ERROR] WebSocket receive failed: {e}")
                
def start_location_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(location_stream())
if __name__ == "__main__": 
    asyncio.run(receive_location())