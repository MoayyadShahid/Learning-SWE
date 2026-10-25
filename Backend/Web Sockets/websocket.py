import asyncio
from websockets.asyncio.server import serve
from datetime import datetime

# for each new client the server calls handler once 
async def handler(websocket):
    
    while True:
        current_time = datetime.now().isoformat()
        await websocket.send(f"The time is: {current_time}")
        # this waits 1 second without blocking other clients, else if we did time.sleep(1) it freezes the whole server, so all other clients stop too
        await asyncio.sleep(1)

async def main():
    print("The server has started...")
    # this opens the server and stores it in 'server'
    async with serve(handler, "localhost", 8765) as server:
        # this keeps the server alive
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())