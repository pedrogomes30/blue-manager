async function listDevices() {
    try {
        const response = await fetch("/devices");
        const devices = await response.json();

        const deviceList = document.getElementById("device-list");
        const syncedDeviceList = document.getElementById("synced-devices");

        if (deviceList) deviceList.innerHTML = "";
        if (syncedDeviceList) syncedDeviceList.innerHTML = "";

        devices.forEach(device => {
            const li = document.createElement("li");
            li.textContent = `${device.name} (${device.address})`;
            // Ao clicar, tenta sincronizar (estabelecer conexão persistente)
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
    } catch (error) {
        console.error("Erro ao listar dispositivos:", error);
    }
}

// Loop de atualização a cada 5 segundos
// async function startDevicePolling() {
//     while (true) {
//         await listDevices();
//         await new Promise(resolve => setTimeout(resolve, 500));
//     }
// }

async function syncDevice(address) {
    try {
        const response = await fetch("/sync", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ address })
        });
        const result = await response.json();
        if (response.ok) {
            alert(result.message);
        } else {
            alert(result.error || "Failed to sync device.");
        }
        // Atualiza a lista após a sincronização
        await listDevices();
    } catch (error) {
        console.error("Error syncing device:", error);
        alert("An error occurred while syncing the device.");
    }
}

async function sendVolumeDownCommand() {
    try {
        const syncedDeviceList = document.getElementById("synced-devices");
        const syncedDevices = [];

        if (syncedDeviceList) {
            const deviceItems = syncedDeviceList.getElementsByTagName("li");
            for (let item of deviceItems) {
                if (item.textContent) {
                    const [name, address] = item.textContent.split(" (");
                    syncedDevices.push({ name, address: address.slice(0, -1) });
                }
            }
        }

        const responseCommand = await fetch("/command", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: "volume_down", devices: syncedDevices })
        });

        const result = await responseCommand.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error("Error sending command:", error);
        alert("An error occurred while sending the command.");
    }
}

// Inicia o polling ao carregar a página
window.onload = startDevicePolling;
