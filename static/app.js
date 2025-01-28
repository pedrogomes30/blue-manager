async function listDevices() {
    const response = await fetch("/devices");
    const devices = await response.json();

    const deviceList = document.getElementById("device-list");
    const syncedDeviceList = document.getElementById("synced-devices");

    if (deviceList) {
        deviceList.innerHTML = "";
    }
    if (syncedDeviceList) {
        syncedDeviceList.innerHTML = "";
    }

    devices.forEach(device => {
        const li = document.createElement("li");
        li.textContent = `${device.name} (${device.address})`;
        li.onclick = () => syncDevice(device.address);

        if (device.synced) {
            if (syncedDeviceList) {
                syncedDeviceList.appendChild(li);
            }
        } else {
            if (deviceList) {
                deviceList.appendChild(li);
            }
        }
    });
}

// Função para iniciar o loop de pesquisa a cada 5 segundos
function startDevicePolling() {
    listDevices();
    setInterval(listDevices, 5000);
}

// Iniciar o polling quando a página carregar
window.onload = startDevicePolling;

async function syncDevice(address) {
    const response = await fetch("/sync", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address })
    });

    const result = await response.json();
    alert(result.message || result.error);

    // Após a sincronização, atualize a lista de dispositivos
    listDevices();
}

async function sendVolumeDownCommand() {
    const response = await fetch("/devices");
    const devices = await response.json();

    const syncedDevices = devices.filter(device => device.synced);

    const responseCommand = await fetch("/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: "volume_down", devices: syncedDevices })
    });

    const result = await responseCommand.json();
    alert(result.message || result.error);
}