window.addEventListener('ServerInfoLoaded', (e) => {
    const data = e.detail;
    setInfoPanelDetails(data);
});

function setInfoPanelDetails(data) {
    // console.log(data)
    const statusElement = document.getElementById('serverStatus');
    const versionElement = document.getElementById('version-label');
    const playersListElement = document.getElementById('serverPlayersList');
    const playersLabel = document.getElementById('serverPlayersLabel');

    if (data.online) {
        statusElement.classList.remove('text-danger');
        statusElement.classList.add('text-success');
        statusElement.innerText = "Online";
        versionElement.innerText = `Version: ${data.version.name_clean}`;
        playersLabel.innerText = `${data.players.online}/${data.players.max} Players`

        var playersListHTML = "";
        for (player of data.players.list) {
            playersListHTML += `<li><i class="bi bi-person-fill me-1"></i>${player.name_clean}</li>`;
        }
        playersListElement.innerHTML = playersListHTML;

    } else if (!data.online) {
        statusElement.classList.remove('text-success');
        statusElement.classList.add('text-danger');
        statusElement.innerText = "Offline";
        versionElement.innerText = "";
        playersListElement.innerHTML = "";
        playersLabel.innerText = "";
    }
}