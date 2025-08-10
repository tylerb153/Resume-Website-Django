window.addEventListener('ServerInfoLoaded', (e) => {
    const data = e.detail;
    setInfoPanelDetails(data);
});

function setInfoPanelDetails(data) {
    console.log(data);

    // data comes in as an array of [launchData, eventData] due to coming from two separate API calls
    const launchData = data[0]
    const eventData = data[1]


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


    // Setting the Event details
    const eventNameElement = document.getElementById('eventName');
    const eventDescriptionElement = document.getElementById('eventDescription');
    const eventTimeElement = document.getElementById('eventTime');

    eventNameElement.innerText = `${eventData.name}`;
    eventDescriptionElement.innerText = `${eventData.description}`;
    eventTimeElement.innerText = `${eventData.date}`;

}