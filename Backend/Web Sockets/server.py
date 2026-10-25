import asyncio
import websockets


async def echo_handler(websocket):
    print("A client has connected!")
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echoing back: {message}")

async def main():
    # start server of port 8765
    async with websockets.serve(echo_handler, "localhost", 8765):
        print("Websocket server is running on ws://localhost:8765")
        await asyncio.Future() # keep server running indefinitely

if __name__ == "__main__":
    asyncio.run(main())