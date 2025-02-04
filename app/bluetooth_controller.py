import bluetooth

class BluetoothController:
    def __init__(self):
        self.devices = []               # Lista de dispositivos descobertos
        self.synced_devices = set()     # Conjunto com os endereços sincronizados
        self.connections = {}           # Mapeia address -> socket (conexão persistente)

    def start_discovery(self):
        """Realiza uma descoberta dos dispositivos Bluetooth disponíveis e atualiza a lista."""
        discovered = bluetooth.discover_devices(
            duration=8, 
            lookup_names=True, 
            flush_cache=True, 
            lookup_class=False
        )
        new_devices = []
        # Adiciona os dispositivos encontrados
        for addr, name in discovered:
            new_devices.append({
                "name": name,
                "address": addr,
                "synced": addr in self.synced_devices
            })
        # Se houver dispositivos já sincronizados, mas que não foram encontrados agora,
        # podemos adicioná-los (com o nome "Unknown" se não tivermos informação)
        for addr in self.synced_devices:
            if addr not in [device["address"] for device in new_devices]:
                new_devices.append({
                    "name": "Unknown",
                    "address": addr,
                    "synced": True
                })
        self.devices = new_devices

    def get_devices(self):
        """Retorna a lista atual de dispositivos (atualiza a descoberta antes)."""
        # Atualiza a lista de dispositivos sempre que solicitada
        self.start_discovery()
        return self.devices

    def sync_device(self, address):
        """
        Tenta estabelecer uma conexão persistente com o dispositivo e o marca como sincronizado.
        Se a conexão já estiver estabelecida, não faz nada.
        """
        # Verifica se o dispositivo foi descoberto na última pesquisa
        if address not in [device["address"] for device in self.devices]:
            raise ValueError("Device not found during discovery.")

        # Se já estiver sincronizado e com conexão ativa, retorne
        if address in self.synced_devices and address in self.connections:
            return

        try:
            # Cria e estabelece uma conexão Bluetooth no canal HID (0x11)
            sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
            sock.connect((address, 0x11))
            self.connections[address] = sock
            self.synced_devices.add(address)
            # Atualiza o status do dispositivo na lista
            for device in self.devices:
                if device["address"] == address:
                    device["synced"] = True
                    break
        except Exception as e:
            raise ValueError(f"Failed to establish connection: {str(e)}")

    def send_command(self, address, command):
        """
        Envia um comando via conexão persistente. Utiliza a conexão previamente
        estabelecida em sync_device. Se não houver conexão, retorna erro.
        """
        if address not in self.synced_devices or address not in self.connections:
            return {"error": "Device is not synced or connection not established."}

        sock = self.connections[address]
        try:
            if command == "volume_down":
                hid_report = b'\xa1\x02\x00\x00\x00\xe9\x00\x00'
                sock.send(hid_report)
            return {"message": f"Comando '{command}' enviado para {address}"}
        except Exception as e:
            return {"error": f"Erro ao enviar comando: {str(e)}"}
