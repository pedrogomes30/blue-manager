from flask import Blueprint, jsonify, request, render_template

bp = Blueprint("api", __name__)
bt_controller = None  # Será atribuído no momento da inicialização

def register_routes(app):
    app.register_blueprint(bp)
    
def set_bt_controller(controller):
    """Define a instância do BluetoothController para ser usada nas rotas."""
    global bt_controller
    bt_controller = controller

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/devices", methods=["GET"])
def devices():
    if not bt_controller:
        return jsonify({"error": "Bluetooth controller not initialized"}), 500
    result = bt_controller.get_devices()
    return jsonify(result)

@bp.route("/sync", methods=["POST"])
def sync_device():
    if not bt_controller:
        return jsonify({"error": "Bluetooth controller not initialized"}), 500

    data = request.json
    address = data.get("address")
    if not address:
        return jsonify({"error": "Device ID (address) is required"}), 400

    try:
        bt_controller.sync_device(address)
        return jsonify({"message": f"Device {address} synchronized successfully"})
    except Exception as e:
        return jsonify({"error": f"Failed to synchronize device: {str(e)}"}), 500

@bp.route("/command", methods=["POST"])
def send_command():
    if not bt_controller:
        return jsonify({"error": "Bluetooth controller not initialized"}), 500

    data = request.json
    command = data.get("command")
    devices = data.get("devices", [])
    if not command or not devices:
        return jsonify({"error": "Command and devices are required"}), 400

    results = []
    for device in devices:
        address = device.get("address")
        if address:
            results.append(bt_controller.send_command(address, command))
    return jsonify(results)
