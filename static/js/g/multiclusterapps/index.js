$(function () {

});


function onGoToManagerCatalogs() {
    const manage_catalogs_form = document.getElementById("manage_catalogs_form");

    document.getElementById("manage_catalogs_id").value = "";

    manage_catalogs_form.method = "POST";
    manage_catalogs_form.action = "/g/tools/catalogs/";

    manage_catalogs_form.submit();
}

function onGoToLaunch() {
    const launch_form = document.getElementById("launch_form");

    document.getElementById("launch_id").value = "";

    launch_form.method = "POST";
    launch_form.action = "/g/multi-cluster-apps/templates";

    launch_form.submit();
}

function deleteApplication(btn) {
    const application_delete_form = document.getElementById("application_delete_form");

    document.getElementById("application_delete_id").value = btn.value;

    application_delete_form.method = "POST";
    // TODO: URL 수정 필요.
    application_delete_form.action = "/g/multi-cluster-apps/api/delete";

    application_delete_form.submit();
}
