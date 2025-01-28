from flask import Blueprint, jsonify, request, render_template
from app.bluetooth_controller import BluetoothController

bp = Blueprint("api", __name__)

# Crie uma instância do BluetoothController
bt_controller = BluetoothController()

# Função para registrar as rotas
def register_routes(app):
    app.register_blueprint(bp)

# Rotas da API
@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/devices", methods=["GET"])
async def devices():
    devices = await bt_controller.list_devices()
    return jsonify(devices)

@bp.route("/sync", methods=["POST"])
async def sync():
    data = request.json
    address = data.get("address")
    name = data.get("name", "Unknown Device")
    if not address:
        return jsonify({"error": "Device address is required"}), 400
    result = await bt_controller.sync_device(address, name)
    if result["status"] == "success":
        return jsonify({"message": "Device synchronized successfully", "device": result["device"]})
    elif result["status"] == "already_synced":
        return jsonify({"message": "Device already synchronized", "device": result["device"]})
    return jsonify({"error": "Failed to synchronize device"}), 500

@bp.route("/command", methods=["POST"])
async def command():
    data = request.json
    command = data.get("command")
    devices = data.get("devices")
    if not command or not devices:
        return jsonify({"error": "Command and devices are required"}), 400
    results = await bt_controller.send_command(command, devices)
    return jsonify(results)