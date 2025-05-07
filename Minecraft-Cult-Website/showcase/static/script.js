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
    statusIcon = document.querySelector('#StatusIcon');
    statusText = document.querySelector('#StatusText');
    if (data.online) {
        statusIcon.classList.remove('bi-x-circle-fill');
        statusIcon.style.color = 'green';
        statusIcon.classList.add('bi-check-circle-fill');
        statusText.innerText = `${data.players.online}/${data.players.max} Players`
    } else {
        statusIcon.classList.remove('bi-check-circle-fill')
        statusIcon.style.color = 'darkred';
        statusIcon.classList.add('bi-x-circle-fill');
        statusText.innerText = "Offline"
    }
}
