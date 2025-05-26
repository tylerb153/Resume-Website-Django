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
});