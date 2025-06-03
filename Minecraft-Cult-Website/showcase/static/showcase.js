// Submit the search form if the clear content
document.addEventListener("DOMContentLoaded", function () {
    const sidebarSearchInput = document.getElementById("sidebar-search");
    const sidebarForm = document.getElementById("sidebar-form");

    if (sidebarSearchInput && sidebarForm) {
        sidebarSearchInput.addEventListener("input", function () {
            if (this.value === "") {
                sidebarForm.submit();
            }
        });
    }

    const mobileSearchInput = document.getElementById("mobile-search");
    const mobileForm = document.getElementById("mobile-form");

    if (mobileSearchInput && mobileForm) {
        mobileSearchInput.addEventListener("input", function () {
            if (this.value === "") {
                mobileForm.submit();
            }
        });
    }
    // Tagify for the create build model
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




