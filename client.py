import asyncio
import websockets

class CodeExecutorClient:
    def __init__(self, uri="ws://localhost:5734"):
        self.uri = uri

    async def send_code(self):
        async with websockets.connect(self.uri) as websocket:
            while True:
                code = input("Enter Python code to execute: ")
                await websocket.send(code)
                response = await websocket.recv()
                print(f"Response: {response}")

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.send_code())

if __name__ == "__main__":
    client = CodeExecutorClient()
    client.start()
