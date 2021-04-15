$(function () {
    groupDeleteButton = document.getElementById("group-delete-button");
    deletables = document.getElementsByName("deletable");
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// 이동 관련

function onGoToAddPersistentVolume(clusterId) {
    const addPersistentVolumeForm = document.getElementById("add_persistent_volume_form");

    document.getElementById("add_persistent_volume_id").value = "";

    addPersistentVolumeForm.method = "POST";
    addPersistentVolumeForm.action = "/c/" + clusterId + "/persistent-volumes/add-form";

    addPersistentVolumeForm.submit();
}

function onGoToPersistentVolumeDetail(label, clusterId) {
    const persistentVolumeDetailForm = document.getElementById("persistent-volume-detail-form");

    const persistentVolumeName = label.innerHTML;
    document.getElementById("persistent-volume-detail-id").value = persistentVolumeName;

    persistentVolumeDetailForm.method = "POST";
    persistentVolumeDetailForm.action = "/c/" + clusterId + "/persistent-volumes/" + persistentVolumeName + "/detail/";

    persistentVolumeDetailForm.submit();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// 삭제 관련

let groupDeleteButton = null;
let deletables = null;

function onAnyPersistentVolumeCheckBoxChecked() {
    const deletableValueList = [];
    for (const deletable of deletables) {
        deletableValueList.push(deletable.value);
    }

    if (deletableValueList.length === 0) {
        groupDeleteButton.disabled = true;
        return;
    }

    const checkers = document.querySelectorAll("input[name=checker]:checked");
    if (checkers.length === 0) {
        groupDeleteButton.disabled = true;
        return;
    }

    for (const checker of checkers) {
        if (!deletableValueList.includes(checker.value)) {
            groupDeleteButton.disabled = true;
            return;
        }
    }

    groupDeleteButton.disabled = false;
}

function onDelete(button) {

}

function onGroupDelete(button) {

}
