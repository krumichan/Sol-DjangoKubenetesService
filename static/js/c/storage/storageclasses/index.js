$(function () {

});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// 이동 관련

function onGoToAddStorageClass(clusterId) {
    const addStorageClassForm = document.getElementById("add_storage_class_form");

    document.getElementById("add_storage_class_id").value = "";

    addStorageClassForm.method = "POST";
    addStorageClassForm.action = "/c/" + clusterId + "/storage-classes/add-form";

    addStorageClassForm.submit();
}

function onGoToStorageClassDetail(label, clusterId) {
    const storageClassDetailForm = document.getElementById("storage-class-detail-form");

    const storageClassName = label.innerHTML;
    document.getElementById("storage-class-detail-id").value = storageClassName;

    storageClassDetailForm.method = "POST";
    storageClassDetailForm.action = "/c/" + clusterId + "/storage-classes/" + storageClassName + "/detail/";

    storageClassDetailForm.submit();
}
