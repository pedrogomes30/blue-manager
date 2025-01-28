import aiosqlite
from bleak import BleakScanner, BleakClient

class BluetoothController:
    def __init__(self, db_path="synced_devices.db"):
        self.db_path = db_path

    async def init_db(self):
        """Inicializa o banco de dados."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS synced_devices (
                    address TEXT PRIMARY KEY,
                    name TEXT
                )
            """)
            await db.commit()

    async def get_synced_devices(self):
        """Obtém a lista de dispositivos Bluetooth que já estão sincronizados."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT address, name FROM synced_devices") as cursor:
                rows = await cursor.fetchall()
                return [{"address": row[0], "name": row[1]} for row in rows]

    async def sync_device(self, address, name):
        """Sincroniza um dispositivo específico."""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("INSERT INTO synced_devices (address, name) VALUES (?, ?)", (address, name))
                await db.commit()
                return {"status": "success", "device": {"name": name, "address": address}}
            except aiosqlite.IntegrityError:
                return {"status": "already_synced", "device": {"name": name, "address": address}}

    async def list_devices(self):
        """Escaneia dispositivos Bluetooth disponíveis."""
        devices = await BleakScanner.discover()
        synced_devices = await self.get_synced_devices()
        synced_addresses = {device['address'] for device in synced_devices}

        # Adiciona o nome do dispositivo junto com o endereço e status de sincronização
        return [{"name": d.name if d.name else d.address, "address": d.address, "synced": d.address in synced_addresses, "uuid": d.metadata.get("uuids", [""])[0] if d.metadata.get("uuids") else ""} for d in devices]

    async def send_command(self, command, devices):
        """Envia um comando a todos os dispositivos sincronizados e ao alcance."""
        results = []

        for device in devices:
            address = device['address']
            uuid = device['uuid']
            try:
                async with BleakClient(address) as client:
                    await client.connect()
                    if client.is_connected:
                        await client.write_gatt_char(uuid, command.encode())
                        results.append({"status": "success", "device": address, "command": command})
                    else:
                        results.append({"status": "error", "device": address, "message": "Device not connected."})
            except Exception as e:
                results.append({"status": "error", "device": address, "message": str(e)})

        return results