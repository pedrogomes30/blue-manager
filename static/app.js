async function listDevices() {
    const response = await fetch("/devices");
    const devices = await response.json();

    const deviceList = document.getElementById("device-list");
    if (deviceList) {
        deviceList.innerHTML = "";
    }
    devices.forEach(device => {
        const li = document.createElement("li");
        li.textContent = `${device.name} (${device.address})`;
        li.onclick = () => syncDevice(device.address);  // Ao clicar, tenta sincronizar o dispositivo
        if (deviceList) {
            deviceList.appendChild(li);
        }
    });
}


async function syncDevice(address) {
    // Exibe uma mensagem enquanto aguarda a resposta da API
    const syncButton = document.getElementById(`sync-button-${address}`);
    if (syncButton) {
        syncButton.textContent = "Sincronizando..."; // Atualiza o texto do botão para 'Sincronizando'
    }

    // Envia a requisição para a API
    const response = await fetch("/sync", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address })
    });

    const result = await response.json();
    alert(result.message || result.error);

    // Atualiza o botão e a lista de dispositivos
    if (syncButton) {
        syncButton.textContent = "Sincronizar"; // Restaura o texto do botão
    }

    // Após a sincronização, atualize a lista de dispositivos
    listDevices(); // Atualiza a lista de dispositivos (agora com os sincronizados)
}

async function sendCommand() {
    const address = prompt("Endereço do dispositivo:");
    const commandInput = document.getElementById("command-input");
    const command = commandInput ? commandInput.value : "";

    const response = await fetch("/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address, command })
    });

    const result = await response.json();
    alert(result.message || result.error);
}
