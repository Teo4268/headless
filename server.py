import asyncio
import base64
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
import uvicorn

app = FastAPI()
latest_frame = None
clients = set()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Stream Viewer</title>
    <style>
        body { margin: 0; background: black; }
        img { width: 100vw; height: 100vh; object-fit: contain; display: block; }
    </style>
</head>
<body>
    <img id="screen" />
    <script>
        const img = document.getElementById("screen");
        const ws = new WebSocket("wss://" + location.host + "/view");
        ws.onmessage = e => {
            img.src = "data:image/jpeg;base64," + e.data;
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def ws_client(websocket: WebSocket):
    await websocket.accept()
    global latest_frame
    try:
        while True:
            data = await websocket.receive_text()
            latest_frame = data
            # Gửi ngay cho tất cả client đang xem
            disconnected = []
            for client in clients:
                try:
                    await client.send_text(data)
                except WebSocketDisconnect:
                    disconnected.append(client)
            for dc in disconnected:
                clients.discard(dc)
    except WebSocketDisconnect:
        pass

@app.websocket("/view")
async def ws_view(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(10)  # duy trì kết nối
    except WebSocketDisconnect:
        clients.discard(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
