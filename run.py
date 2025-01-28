from flask import Flask
from app.routes import register_routes
from app.bluetooth_controller import BluetoothController
import asyncio

app = Flask(__name__)
register_routes(app)

# Inicializa o banco de dados
async def init_app():
    bt_controller = BluetoothController()
    await bt_controller.init_db()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_app())
    app.run(debug=True, port=5000)