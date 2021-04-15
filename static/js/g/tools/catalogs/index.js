$(function () {
    initDelete();
    Modal.initalization();
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// 삭제 관련

let checkCount = 0;
let catalogCheckboxGroup = null;
let catalogDeleteButton = null;

const checkedCatalogList = [];

/**
 * [Catalog List]의 [Delete] 관련 초기화 작업을 수행한다.
 */
function initDelete() {
    catalogCheckboxGroup = document.getElementsByClassName("catalog_checkbox");
    catalogDeleteButton = document.getElementById("btn_catalog_delete");

    for (const cb of catalogCheckboxGroup) {
        cb.checked = false;
    }

    checkCount = 0;

    setBntCatalogDeleteDisabled();
}

/**
 * 임의의 Catalog Checkbox 중 checking 관련 event가 일어났을 경우,
 * delete button 의 활성화 여부를 결정한다.
 * @param selfChkBox checking 관련 event가 일어난 Checkbox
 */
function onAnyCatalogCheckboxChanged(selfChkBox) {
    calculateCheckboxCount(selfChkBox.checked, selfChkBox.value);
    setBntCatalogDeleteDisabled();
}

/**
 * Checkbox 의 check event 의 발생에 따라, 현재 checkbox 의 check 수를 계산한다.
 * @param flag checking flag.
 * @param value checking이 일어났을 때의 checkbox가 가진 value.
 */
function calculateCheckboxCount(flag, value) {
    if (flag) {
        checkCount++;
        checkedCatalogList.push(value);
    } else {
        checkCount--;
        const index = checkedCatalogList.indexOf(value);
        checkedCatalogList.splice(index, 1);
    }

}

/**
 * checkbox의 checking 되어 있는 수를 기반으로, catalog delete button을 활성화 할 지 여부를 결정한다.
 */
function setBntCatalogDeleteDisabled() {
    catalogDeleteButton.disabled = checkCount <= 0;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Modal Event 관련

/**
 * Modal 창을 관리하기 위한 클래스.
 */
class Modal {
    static elements = {
        "modal_div": null
        , "modal_title": null
        , "modal_name": null
        , "modal_url": null
        , "modal_private_check_box": null
        , "modal_private_div": null
        , "modal_private_input_id": null
        , "modal_private_input_pw": null
        , "modal_branch": null
        , "modal_global": null
        , "modal_helm_version": null
        , "modal_hidden_current_state": null
        , "modal_form": null
    }

    /**
     * Modal 내의 모든 요소들을 초기화한다.
     * @constructor
     */
    static initalization() {
        Modal.elementInitialization();
        Modal.refresh();
    }

    /**
     * Modal 내의 모든 요소들을 Modal Class Member 변수에 Mapping 한다.
     */
    static elementInitialization() {
        Object.keys(Modal.elements).forEach((key) => {
            if (Modal.elements[key] == null) {
               Modal.elements[key] = document.getElementById(key);
           }
        });
    }

    /**
     * Modal Window 의 Visible 을 설정한다.
     * @param flag Modal Window 를 보이게 할지 여부.
     */
    static visible(flag) {
        const first = Object.keys(Modal.elements)[0];
        const firstObject = Modal.elements[first];

        if (flag) {
            firstObject.style.display = "";
        } else {
            firstObject.style.display = "none";
        }

        Modal.refresh();
    }

    /**
     * Modal 내의 모든 요소들을 초기화한다.
     */
    static refresh() {
        Object.keys(Modal.elements).forEach((key) => {
            Modal.elements[key].value = "";
            Modal.elements[key].disabled = false;
            Modal.elements[key].checked = false;
        });

        Modal.elements["modal_private_div"].style.display = "none";
        Modal.elements["modal_private_input_id"].required = false;
        Modal.elements["modal_private_input_pw"].required = false;
    }

    /**
     * Modal 내의 모든 요소의 Data 를 JSON string 형식으로 변형하여 반환한다.
     * @return JSON string 형식의 Data
     */
    static sendDataFactoring() {
        let sendData = {
            name: Modal.elements["modal_name"].value
            , url: Modal.elements["modal_url"].value
            , branch: Modal.elements["modal_branch"].value
            , scope: Modal.elements["modal_global"].value
            , helmVersion: Modal.elements["modal_helm_version"].value
        }

        if (Modal.elements["modal_private_check_box"].checked) {
            sendData["username"] = Modal.elements["modal_private_input_id"];
            sendData["password"] = Modal.elements["modal_private_input_pw"];
        }

        return JSON.stringify(sendData);
    }
}

window.addEventListener("load", function() {
    Modal.initalization()
});

/**
 * Modal Window 를 끈다.
 */
function modalOff() {
    Modal.refresh();
    Modal.visible(false);
}

/**
 * Modal Window 를 켠다.
 * TODO: btn 으로붙어 얻은 ROW를 Python을 통해 다시 얻고 있음.. 불필요 API 호출이 일어나기 때문에 수정要
 * @param btn 해당 Event의 발생원
 */
function modalOn(btn) {
    Modal.refresh();
    Modal.visible(true);

    // default 설정
    Modal.elements["modal_hidden_current_state"].value = "create";
    Modal.elements["modal_title"].innerHTML = "Create Catalog"

    // event 발생원으로부터 data를 받았을 경우.
    if (btn.value != null) {
        // data 를 JSON 형식으로 변환
        const valueMapping = JSON.parse(btn.value);

        // 변환한 JSON 형식의 값으로부터 value를 습득.
        const name = valueMapping['name'];
        const token = valueMapping['csrfmiddlewaretoken'];
        const type = valueMapping['type'];

        // python 으로부터 해당 name 에 관련한 data 를 얻어옴.
        const specificRow = getSpecificCatalogDataByName(name, token);

        // Edit 의 경우와 Clone 의 경우를 나누어서 수행
        if (type === 'create') {

        } else if (type === 'edit') {
            modalForEdit(specificRow);
        } else if (type === 'clone') {
            modalForClone(specificRow);
        }
    }
}

function modalSubmit() {
    const modalForm = Modal.elements["modal_form"];
    const modalState = Modal.elements["modal_hidden_current_state"].value;

    const required_elements = modalForm.querySelectorAll("[required]");
    for (let i = 0; i < required_elements.length; ++i) {
        if (required_elements[i].value === "") {
            alert("some field in modal is empty.");
            return;
        }
    }

    modalForm.method = "POST";
    Modal.elements["modal_hidden_current_state"].value = Modal.sendDataFactoring();

    switch (modalState) {
        case "create": modalForm.action = "/g/tools/catalogs/api/create"; break;
        case "edit": modalForm.action = "/g/tools/catalogs/api/edit"; break;
        case "clone": modalForm.action = "/g/tools/catalogs/api/clone"; break;
    }

    modalForm.submit();
}

function checkedDeleteCatalog() {
    const checkedDeleteCatalogsForm = document.getElementById("checked_delete_catalogs_form");

    document.getElementById("checked_delete_catalogs_id").value = JSON.stringify(checkedCatalogList);

    checkedDeleteCatalogsForm.method = "POST";
    // TODO: URL 수정 필요.
    checkedDeleteCatalogsForm.action = "/g/tools/catalogs/delete";

    checkedDeleteCatalogsForm.submit();
}

function deleteCatalog(btn) {
    const catalogListDeleteForm = document.getElementById("catalog_list_delete_form");

    document.getElementById("catalog_delete_id").value = btn.value;

    catalogListDeleteForm.method = "POST";
    // TODO: URL 수정 필요.
    catalogListDeleteForm.action = "/g/tools/catalogs/delete";

    catalogListDeleteForm.submit();
}

function enabledCatalog(btn) {
    const catalogListEnabledForm = document.getElementById("catalog_list_enabled_form");

    document.getElementById("catalog_enabled_id").value = btn.value;

    catalogListEnabledForm.method = "POST";
    // TODO: URL 수정 필요.
    catalogListEnabledForm.action = "/g/tools/catalogs/enabled";

    catalogListEnabledForm.submit();
}

function refreshCatalog(btn) {
    const catalogRefreshForm = document.getElementById("catalog_refresh_form");

    document.getElementById("catalog_refresh_id").value = btn.value;

    catalogRefreshForm.method = "POST"
    // TODO: URL 수정 필요.
    catalogRefreshForm.action = "/g/tools/catalogs/refresh";

    catalogRefreshForm.submit();
}

/**
 * 임의의 Catalog name에 대한 data 를 얻어온다.
 * TODO: 해당 page 로부터 얻은 ROW 의 값을 JSON 형식으로 변환하지 못하여 API 로부터 재호출 하고 있음. 해당 함수의 제거가 최종 목표.
 * @param name Catalog name
 * @param token csrf token
 */
function getSpecificCatalogDataByName(name, token) {
    let specificRow = null;

    $.ajax({
        type: "POST"
        , async: false   // 비동기화 Off
        , url: "{% url 'getSpecificRowByName' %}"
        , contentType: "application/json"
        , dataType: "text"
        , headers: {
            'X-CSRFToken': token
        }
        , data: JSON.stringify({
            name: name
        })
        , success: function(data) {
            specificRow = data;
        }, complete: function(data) {
            // do nothings...
        }, error: function(request, error) {
            const message = "code: " + request.status + "\n"
                + "message: " + request.responseText + "\n"
                + "error: " + error;
            alert(message);
        }
    });

    return JSON.parse(specificRow)["data"];
}

/**
 * Catalog row data를 기반으로 edit 형태에 맞게 Modal 요소의 내용을 수정.
 * @param row Catalog row data
 */
function modalForEdit(row) {
    Modal.elements["modal_name"].value = row["name"];
    Modal.elements["modal_name"].disabled = true;
    Modal.elements["modal_url"].value = row["url"];
    Modal.elements["modal_private_check_box"].checked = (row["username"] != null);
    if (Modal.elements["modal_private_check_box"].checked) {
        Modal.elements["modal_private_div"].style.display = "";
        Modal.elements["modal_private_input_id"].value = row["username"];
    }
    Modal.elements["modal_branch"].value = row["branch"];
    Modal.elements["modal_global"].value = row["scope"];
    Modal.elements["modal_global"].disabled = true;
    Modal.elements["modal_helm_version"].value = row["helmVersion"];
    Modal.elements["modal_helm_version"].disabled = true;
    Modal.elements["modal_title"].innerHTML = "Edit Catalog"
    Modal.elements["modal_hidden_current_state"].value = "edit";
}

/**
 * Catalog row data를 기반으로 clone 형태에 맞게 Modal 요소의 내용을 수정.
 * @param row Catalog row data
 */
function modalForClone(row) {
    Modal.elements["modal_name"].value = "";
    Modal.elements["modal_name"].disabled = false;
    Modal.elements["modal_url"].value = row["url"];
    Modal.elements["modal_private_check_box"].checked = (row["username"] != null);
    if (Modal.elements["modal_private_check_box"].checked) {
        Modal.elements["modal_private_div"].style.display = "";
        Modal.elements["modal_private_input_id"].value = row["username"];
    }
    Modal.elements["modal_branch"].value = row["branch"];
    Modal.elements["modal_global"].value = row["scope"];
    Modal.elements["modal_global"].disabled = false;
    Modal.elements["modal_helm_version"].value = row["helmVersion"];
    Modal.elements["modal_helm_version"].disabled = false;
    Modal.elements["modal_title"].innerHTML = "Clone Catalog"
    Modal.elements["modal_hidden_current_state"].value = "clone";
}

/**
 * private 관련 정보를 사용할지를 정한다.
 * ( private 관련에는 id, pw 정보가 들어가 있다. )
 */
function usePrivate() {

    // private 관련 정보 사용
    if (privateCheckBoxIsChecked()) {

        // private 공간을 보이게 한다.
        Modal.elements["modal_private_div"].style.display = "";

        // private 관련 tag 들을 필수 요구 tag 로 설정한다.
        privateInputFieldRequired(true);

    // private 관련 정보 미사용
    } else {

        // private 공간을 보이지 않게 한다.
        Modal.elements["modal_private_div"].style.display = "none";

        // private 관련 tag 들을 필수 요구하지 않도록 설정한다.
        privateInputFieldRequired(false);
    }
}

/**
 * private checkbox 의 check 여부를 반환한다.
 * @returns {boolean|boolean|*} private checkbox 의 체크여부.
 */
function privateCheckBoxIsChecked() {
    return Modal.elements["modal_private_check_box"].checked;
}

/**
 * private field 의 각종 Component 들을 필수 요구로 설정할지를 결정한다.
 * @param flag 필수 요구로 설정할지 여부 ( boolean 값이 요구된다. )
 */
function privateInputFieldRequired(flag) {
    Modal.elements["modal_private_input_id"].required = flag;
    Modal.elements["modal_private_input_id"].required = flag;
}

function modalTitle(title) {
    Modal.elements["modal_name"].value = title;
}
