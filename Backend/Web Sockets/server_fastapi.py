import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Industry Best Practice: Enable Cross-Origin Resource Sharing (CORS) 
# This prevents unauthorized websites from connecting to your sockets
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your exact domain (e.g., ["https://myapp.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory registry to track our connected client sessions
class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        # 1. Accept the HTTP 101 Upgrade handshake explicitly
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"New client connected! Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        # 2. Clean up memory references when a client leaves
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast(self, message: str, sender: WebSocket):
        # 3. Send the payload to everyone EXCEPT the person who sent it
        for connection in self.active_connections:
            if connection != sender:
                await connection.send_text(message)

manager = ConnectionManager()

# FastAPI handles routing beautifully. We can even read parameters from the URL path!
@app.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await manager.connect(websocket)
    
    # Send a custom welcome message to the connecting client
    await websocket.send_text(f"System: Welcome to the server, {client_name}!")
    await manager.broadcast(f"System: {client_name} has joined the chat room.", sender=websocket)
    
    try:
        while True:
            # Continuously listen for incoming text data frames
            data = await websocket.receive_text()
            print(f"[{client_name}]: {data}")
            
            # Broadcast the message to all other users
            await manager.broadcast(f"[{client_name}]: {data}", sender=websocket)
            
            # Echo a confirmation directly back to the sender
            await websocket.send_text(f"You sent: {data}")
            
    except WebSocketDisconnect:
        # FastAPI catches the connection tear-down automatically
        manager.disconnect(websocket)
        await manager.broadcast(f"System: {client_name} has left the room.", sender=websocket)

if __name__ == "__main__":
    import uvicorn
    # Start the Uvicorn engine on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
