from bleak import BleakScanner, BleakClient

class bluetooth_controller:
    def __init__(self):
        self.synced_devices = {}  # Dispositivos sincronizados {address: name}

    async def list_devices(self):
        """Escaneia dispositivos Bluetooth disponíveis."""
        devices = await BleakScanner.discover()
        # Adiciona o nome do dispositivo junto com o endereço
        print(devices)
        return [{"name": d.name if d.name else d.address, "address": d.address} for d in devices]

    async def sync_device(self, address, name):
        """Sincroniza um dispositivo específico."""
        if address not in self.synced_devices:
            self.synced_devices[address] = name
            return {"status": "success", "device": {"name": name, "address": address}}
        else:
            return {"status": "already_synced", "device": {"name": name, "address": address}}

    async def send_command(self, address, command):
        """Envia um comando a um dispositivo específico."""
        if address not in self.synced_devices:
            return {"status": "error", "message": "Device not synced."}

        try:
            async with BleakClient(address) as client:
                # Enviar um comando via Bluetooth Low Energy (exemplo)
                if client.is_connected:
                    # O comando pode ser um write characteristic ou qualquer outra operação BLE
                    # Aqui simulamos enviando um texto para um serviço de exemplo:
                    SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"  # Exemplo de UUID
                    await client.write_gatt_char(SERVICE_UUID, command.encode())
                    return {"status": "success", "device": address, "command": command}
                else:
                    return {"status": "error", "message": "Device not connected."}
        except Exception as e:
            return {"status": "error", "message": str(e)}