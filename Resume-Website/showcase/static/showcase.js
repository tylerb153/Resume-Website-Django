document.addEventListener("DOMContentLoaded", function () {
    // Submit the search form if the clear content
    const sidebarSearchInput = document.getElementById("sidebar-search");
    const sidebarForm = document.getElementById("sidebar-form");

    if (sidebarSearchInput && sidebarForm) {
        let previousSidebarValue = sidebarSearchInput.value;
        let sidebarWasClearedByMouse = false;

        sidebarSearchInput.addEventListener("mousedown", function () {
            sidebarWasClearedByMouse = true;
        });

        sidebarSearchInput.addEventListener("input", function () {
            if (previousSidebarValue !== "" && this.value === "" && sidebarWasClearedByMouse) {
                sidebarForm.submit();
            }
            previousSidebarValue = this.value;
            sidebarWasClearedByMouse = false;
        });
    }

    const mobileSearchInput = document.getElementById("mobile-search");
    const mobileForm = document.getElementById("mobile-form");

    if (mobileSearchInput && mobileForm) {
        let previousMobileValue = mobileSearchInput.value;
        let mobileWasClearedByMouse = false;

        mobileSearchInput.addEventListener("mousedown", function () {
            mobileWasClearedByMouse = true;
        });

        mobileSearchInput.addEventListener("input", function () {
            if (previousMobileValue !== "" && this.value === "" && mobileWasClearedByMouse) {
                mobileForm.submit();
            }
            previousMobileValue = this.value;
            mobileWasClearedByMouse = false;
        });
    }
    // Tagify for the create project model
    const input = document.querySelector('input[name="tagsInput"]');
    if (input) {
        const tags = JSON.parse(document.getElementById('tags').textContent);
        tagify = new Tagify(input, {
            whitelist: tags,
            maxTags: 10,
            dropdown: {
                maxItems: 20,
                classname: 'tags-look',
                enabled: 0,
                closeOnSelect: false
            }
        });
    }


});
