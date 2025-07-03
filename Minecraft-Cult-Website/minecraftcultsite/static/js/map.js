document.addEventListener('DOMContentLoaded', () => {
    const buttonGroup = document.querySelector(".btn-group")
    if (buttonGroup) {
        const bluemapIframe = document.querySelector("#bluemap");
        const dynmapIframe = document.querySelector("#dynmap");

        const dynmapButton = document.querySelector("#DynmapButton")
        const bluemapButton = document.querySelector("#BluemapButton")

        const updateMapVisibility = () => {
            if (dynmapButton && dynmapButton.checked) {
                if (dynmapIframe) dynmapIframe.classList.remove('d-none');
                if (bluemapIframe) bluemapIframe.classList.add('d-none');
            } else if (bluemapButton && bluemapButton.checked) {
                if (bluemapIframe) bluemapIframe.classList.remove('d-none');
                if (dynmapIframe) dynmapIframe.classList.add('d-none');
            }
        };

        // Initialise on page load
        updateMapVisibility();

        // React to user changes
        dynmapButton?.addEventListener('change', updateMapVisibility);
        bluemapButton?.addEventListener('change', updateMapVisibility);
    }
});