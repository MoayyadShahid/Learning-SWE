import asyncio
import sys
import websockets

async def connect_to_server():
    # Notice we hit port 8000 and pass a name dynamic parameter in the URL path
    uri = "ws://127.0.0.1:8000/ws/Moayyad"
    print(f"Connecting to FastAPI server at {uri}...")
    
    async with websockets.connect(uri) as websocket:
        print("Connected to FastAPI room!")
        
        while True:
            user_message = await asyncio.to_thread(input, "> ")
            
            if user_message.strip().lower() == "exit":
                print("Disconnecting...")
                break
                
            if not user_message.strip():
                continue

            await websocket.send(user_message)
            
            # Print the incoming responses or broadcast items from the loop
            response = await websocket.recv()
            print(response)

if __name__ == "__main__":
    try:
        asyncio.run(connect_to_server())
    except KeyboardInterrupt:
        print("\nSession ended.")
