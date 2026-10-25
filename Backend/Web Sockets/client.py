import asyncio
import websockets
import sys


async def connect_to_server():
    uri = "ws://localhost:8765"
    print(f"Connecting to server at {uri} ...")

    async with websockets.connect(uri) as websocket:
        print("Connected! Type your message below (or type 'exit' to quit):")

        while True:

            user_message = await asyncio.to_thread(input, "> ")

            if user_message.strip().lower() == "exit":
                print("Closing connection...")
                break

            if not user_message.strip():
                continue


            await websocket.send(user_message)
            response = await websocket.recv()
            print(f"Server response: {response}")


if __name__ == "__main__":
    try:
        asyncio.run(connect_to_server())
    except:
        print("\nDisconnected by user.")