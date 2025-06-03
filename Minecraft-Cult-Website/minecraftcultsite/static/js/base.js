const url = "https://api.mcstatus.io/v2/status/java/mc.theminecraftcult.com"

getStatus();
setInterval(getStatus, 30000); 

function getStatus() {
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network Error');
        }
        return response.json();
    })
    .then(data => {
        changeStatus(data);
    })
    .catch(error => {
        console.error('Error: ', error);
    });
}

function changeStatus(data) {
    console.log(data)
    statusIcons = document.querySelectorAll('.StatusIcon');
    statusTexts = document.querySelectorAll('.StatusText');
    // console.log(statusIcons)
    // console.log(statusTexts)
    if (data.online) {
        for (icon of statusIcons) {
            icon.classList.remove('bi-x-circle-fill');
            icon.style.color = 'green';
            icon.classList.add('bi-check-circle-fill');
        }
        for (text of statusTexts) {
            text.innerText = `${data.players.online}/${data.players.max} Players`
        }
    } else {
        for (icon of statusIcons) {
            icon.classList.remove('bi-check-circle-fill')
            icon.style.color = 'darkred';
            icon.classList.add('bi-x-circle-fill');
        }
        for (text of statusTexts) {
            text.innerText = "Offline"
        }
    }
}
