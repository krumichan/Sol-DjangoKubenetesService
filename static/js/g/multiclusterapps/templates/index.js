$(function () {

});


function onAppsTemplatesRefresh() {
    const appsTemplatesRefreshForm = document.getElementById("apps_templates_refresh_form");

    document.getElementById("apps_templates_refresh_id").value = "";

    appsTemplatesRefreshForm.method = "POST";
    appsTemplatesRefreshForm.action = "/g/multi-cluster-apps/templates/refresh";

    appsTemplatesRefreshForm.submit();
}

function onAppsTemplatesCategorySelected(select) {
    const appsTemplatesSelectedCategoryForm = document.getElementById("apps_templates_selected_category_form");

    const selectedOption = select.options[select.selectedIndex]
    document.getElementById("apps_templates_selected_category_id").value = "";

    appsTemplatesSelectedCategoryForm.method = "POST";
    appsTemplatesSelectedCategoryForm.action = "/g/multi-cluster-apps/templates/" + selectedOption.value + "/category-filter";

    appsTemplatesSelectedCategoryForm.submit();
}

function onAppsTemplatesLaunch(btn) {
    const appsTemplatesLaunchForm = document.getElementById("apps_templates_launch_form");

    document.getElementById("apps_templates_launch_id").value = btn.value;

    appsTemplatesLaunchForm.method = "POST";
    // TODO: app launch Address 수정 필요.
    appsTemplatesLaunchForm.action = "/apps_launch/createApplication"

    appsTemplatesLaunchForm.submit();
}
