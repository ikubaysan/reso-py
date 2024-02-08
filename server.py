import asyncio
import websockets
import contextlib
import io

class CodeExecutorServer:
    def __init__(self, port=5734):
        self.port = port

    async def execute_code(self, code, websocket):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            try:
                # Running code without restricting built-ins
                exec(code)
            except Exception as e:
                await websocket.send(str(e))
                return
        output = stdout.getvalue()
        await websocket.send(output if output else "No output")

    async def handler(self, websocket, path):
        async for message in websocket:
            await self.execute_code(message, websocket)

    def start(self):
        start_server = websockets.serve(self.handler, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = CodeExecutorServer()
    server.start()
