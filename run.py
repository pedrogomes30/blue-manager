from flask import Flask
from app.routes import register_routes, set_bt_controller
from app.bluetooth_controller import BluetoothController
import asyncio

app = Flask(__name__)
register_routes(app)

bt_controller = BluetoothController()
set_bt_controller(bt_controller)

async def main():
    """Executa o servidor Flask de forma assíncrona."""
    app.run(debug=True, port=5000, use_reloader=False)

if __name__ == "__main__":
    asyncio.run(main())
