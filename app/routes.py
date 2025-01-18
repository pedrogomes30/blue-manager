
from flask import Blueprint, jsonify, request, render_template
from app.bluetooth_controller import bluetooth_controller

bp = Blueprint("api", __name__)

# Crie uma instância do bluetooth_controller
bt_controller = bluetooth_controller()

# Função para registrar as rotas
def register_routes(app):
    app.register_blueprint(bp)

# Rotas da API
@bp.route("/")
def index():
    return render_template("index.html")

# app/routes.py

@bp.route("/devices", methods=["GET"])
async def devices():
    devices = await bt_controller.list_devices()
    # Exibe o nome e o endereço do dispositivo
    return jsonify([{"name": device["name"], "address": device["address"]} for device in devices])


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
    address = data.get("address")
    command = data.get("command")
    if not address or not command:
        return jsonify({"error": "Address and command are required"}), 400
    result = await bt_controller.send_command(address, command)
    if result["status"] == "success":
        return jsonify({"message": "Command sent successfully", "device": result["device"], "command": result["command"]})
    return jsonify({"error": result.get("message", "Failed to send command")}), 500
