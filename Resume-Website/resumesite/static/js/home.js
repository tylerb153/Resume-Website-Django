window.addEventListener('ServerInfoLoaded', (e) => {
    const data = e.detail;
    setInfoPanelDetails(data);
});

function setInfoPanelDetails(launchData) {

    // Setting the Launch details
    const launchNameElement = document.getElementById('launchName');
    const launchRocketElement = document.getElementById('launchRocket');
    const launchDestinationElement = document.getElementById('launchDestination');
    const launchLaunchpadElement = document.getElementById('launchLaunchpad');
    const launchTimeElement = document.getElementById('launchTime');

    launchNameElement.innerText = `${launchData.name}`;
    launchRocketElement.innerText = `${launchData.rocket.configuration.name}`;
    launchDestinationElement.innerText = `${launchData.mission.orbit.name}`;
    launchLaunchpadElement.innerText = `${launchData.pad.name} at ${launchData.pad.location.name}`;
    launchTimeElement.innerText =  `${launchData.window_start}`;
}