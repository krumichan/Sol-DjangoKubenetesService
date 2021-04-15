$(function () {
    initPlugin();
    initMountOption();
    initNodeAffinity();
});


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// form submit 관련

<!-- form submit 관련. -->
/**
 * Persistent Volume을 Add하는 form의 submit 함수.
 */
function save() {
    const persistentVolumeForm = document.getElementById("add-persistent-volume-form");
    const dataInput = document.getElementById("persistent-volume-data");

    const pl = payload();
    if (pl === null) {
        return null;
    }

    persistentVolumeForm.method = "POST";
    persistentVolumeForm.action = "/c/persistent-volumes/api/add";

    dataInput.value = pl;
    persistentVolumeForm.submit();
}

/**
 * Persistent Volume List Page로 이동하는 함수.
 */
function cancel() {
    const persistentVolumeForm = document.getElementById("add-persistent-volume-form");

    persistentVolumeForm.method = "POST";
    persistentVolumeForm.action = "/c/persistent-volumes/"

    persistentVolumeForm.submit();
}

/**
 * submit을 수행할 시, back-end 단으로 보낼 json 형식의 data를 생성한다.
 */
function payload() {
    // map 형식의 object.
    const result = Object();

    // Persistent Volume Name을 습득.
    result["name"] = document.getElementById("name").value;
    if (result["name"].trim() === "") {
        alert("name empty.");
        return null;
    }

    // Persistent Volume Description을 습득.
    const description = document.getElementById("description").value;
    // discription의 내용이 존재할 경우만 result object에 삽입한다.
    if (description.trim() !== "") {
        result["descrption"] = description.trim();
    }

    // Persistent Volume capacity를 습득.
    const storage = document.getElementById("capacity").value;
    if (result["capacity"] === "") {
        alert("capacity empty.");
        return null;
    }
    result["capacity"] = {storage: storage.toString() + "Gi"};

    // Persistent Volume Volume Plugin의 field 명을 습득.
    const volumePluginTag = document.getElementById("volume-plugin-select");
    const currentSelectedOption = volumePluginTag.options[volumePluginTag.selectedIndex];
    const volumePlugin = currentSelectedOption.value;
    if(volumePlugin === "default") {
        alert("choose a volume plugin.");
        return null;
    }

    // Persistent Volume Plugin Configuration울 습득.
    const volumePluginTtitle = currentSelectedOption.text;
    result[volumePlugin] = pluginConfigurationPayload(volumePluginTtitle);
    if(result[volumePlugin] === null) {
        return null;
    }

    // Persistent Volume의 access mode를 습득.
    const accessModeField = "accessModes";
    const accessModeList = accessModesPayload(accessModeField);
    if (accessModeList === null) {
        alert("check access modes at least once.");
        return null;
    }
    result[accessModeField] = accessModeList;

    // Persistent Volume의 mount option을 습득.
    const mountOptionField = "mountOptions";
    const mountOptionList = mountOptionsPayload(mountOptionField);
    if (mountOptionList !== null) {
        result[mountOptionField] = mountOptionList;
    }

    // Persistent Volume의 Storage Class를 습득.
    const storageClass = document.getElementById("storageClassId").value;
    if (storageClass !== "default") {
        result["storageClassId"] = storageClass;
    }

    // Persistent Volume의 Node Affinity를 습득.
    const nodeAffinityField = "nodeAffinity";
    const nodeSelectorTermsField = "nodeSelectorTerms";
    const nodeSelectorTermList = nodeSelectorTermsPayload(nodeSelectorTermsField);
    if (nodeSelectorTermList !== null) {
        const nodeSelectorTerm = { nodeSelectorTerms: nodeSelectorTermList };
        result[nodeAffinityField] = { required: nodeSelectorTerm };
    }

    // map 형식의 object를 json 형식의 string으로 변환하여 반환한다.
    return JSON.stringify(result);
}

/**
 * 임의의 volumePlugin에 대한 현재 plugin configuration에 정의되어 있는 값들을 map 형식의 object로 반환.
 * @param volumePluginTitle 현재 선택되어 있는 volumePlugin의 title.
 */
function pluginConfigurationPayload(volumePluginTitle) {
    // back-end로부터 넘어온 plugin configurtaion mapping으로부터 인수로 받은 volumePlugin에 맞는 configuration 추출.
    const pluginConfigurationString = document.getElementById("plugin-configuration-template-hidden").value;
    const pluginConfigurationMapping = JSON.parse(pluginConfigurationString);
    const currentVolumePlugin = pluginConfigurationMapping[volumePluginTitle];
    const currentPluginConfiguration = currentVolumePlugin["configuration"];

    // configuration에 정의되어 있는 모든 field에 대해, [field: value] 구조로 값 습득.
    let configurationPayload = {};
    for (const [name, value] of Object.entries(currentPluginConfiguration)) {
        const val = configurationToValue(name, value);
        if (val === null) {
            alert(name + " empty.");
            return null;
        } else if (val === "") {
            // do nothing...
        } else {
            configurationPayload[name] = val;
        }
    }

    return configurationPayload;
}

/**
 * plugin configuration의 field명과 configurtaion mapping 중, field의 type을 기반으로 값을 추출.
 * @param name plugin configurtaion의 field명.
 * @param value 해당 field에 대한 plugin configurtaion.
 * @returns {|null|*} field와 plugin configuration을 기반으로 page에서 추출한 값.
 */
function configurationToValue(name, value) {
    switch(value["type"]) {
        case "label/string": return labelStringToValue(name, value);
        case "label/int": return labelIntToValue(name, value);
        case "label/fix": return labelFixToValue(name, value);
        case "radio": return radioToValue(name, value);
        case "select": return selectToValue(name, value);
        case "map/addable": return mapAddableToValue(name, value);
        default: return null;
    }
}

/**
 * plugin configuration의 type이 'label/string'인 경우의 추출.
 * @param name field명( tag의 id값으로도 사용됨. ).
 * @param value plugin configurtaion.
 * @returns {*} field명을 id로 가진 tag로부터 추출한 value.
 */
function labelStringToValue(name, value) {
    const tag = document.getElementById(name.toString());
    const val = tag.value.trim();
    const req = value["required"];

    if (val === "") {
        return req === true ? null : "";
    }

    return val;
}

/**
 * plugin configuration의 type이 'label/int'인 경우의 추출.
 * @param name field명( tag의 id값으로도 사용됨. ).
 * @param value plugin configurtaion.
 * @returns {*} field명을 id로 가진 tag로부터 추출한 value.
 */
function labelIntToValue(name, value) {
    const tag = document.getElementById(name.toString());
    const val = tag.value.trim();
    const req = value["required"];

    if (val === "") {
        return req === true ? null : "";
    }

    return val;
}

/**
 * plugin configuration의 type이 'label/fix'인 경우의 추출.
 * @param name field명( tag의 id값으로도 사용됨. ).
 * @param value plugin configurtaion.
 * @returns {*} field명을 id로 가진 tag로부터 추출한 value.
 */
function labelFixToValue(name, value) {
    const tag = document.getElementById(name.toString());
    const val = tag.value.trim();
    const req = value["required"];

    if (val === "") {
        return req === true ? null : "";
    }

    return val;
}

/**
 * plugin configuration의 type이 'radio'인 경우의 추출.
 * @param name field명( tag의 name값으로도 사용됨. ).
 * @param value plugin configurtaion.
 * @returns {*} field명을 name로 가진 tag들 중, checked인 tag로부터 추출한 value.
 */
function radioToValue(name, value) {
    return document.querySelector('input[name="' + name + '"]:checked').value;
}

/**
 * plugin configuration의 type이 'select'인 경우의 추출.
 * @param name field명( tag의 id값으로도 사용됨. ).
 * @param value plugin configurtaion.
 * @returns {*} field명을 id로 가진 tag에서, selected인 tag로부터 추출한 value.
 */
function selectToValue(name, value) {
    const selectTag = document.getElementById(name.toString());
    const currentOption = selectTag.options[selectTag.selectedIndex];
    return currentOption.value;
}

/**
 * plugin configuration의 type이 'map'인 경우의 추출.
 * @param name field명( tag의 name값으로도 사용됨. ).
 * @param value plugin configurtaion.
 * @returns {*} field명을 name로 가진 tag들로부터, [key, value] 형식으로 값을 추출한 json 형식의 object.
 */
function mapAddableToValue(name, value) {
    const result = {};
    const required = value["required"];

    // table로부터 tbody 안에 있는 모든 row를 습득.
    const table = document.getElementById(name.toString());
    const tbody = table.getElementsByTagName("tbody")[0];
    const trows = tbody.getElementsByTagName("tr");
    if (trows.length === 0) {
        return required === true ? null : "";
    }

    // row들을 순회.
    for (const row of trows) {
        const key = row.cells[0].getElementsByTagName("input")[0].value.trim();
        const val = row.cells[1].getElementsByTagName("input")[0].value.trim();

        // key, value의 두 값이 모두 있는 경우만 삽입.
        if (key !== "" && val !== "") {
            result[key] = val;
        }
    }

    return result.length !== 0 ? result :
        required !== true ? null : "";
}

/**
 * access mode의 field명을 기반으로 access mode들의 tag를 얻어오고 값을 list로 반환한다.
 * @param accessModeField access mode의 field명.
 * @returns {null|[]} checked인 access mode들의 값 list. ( null 인 경우, checked인 access mode가 없음을 의미. )
 */
function accessModesPayload(accessModeField) {
    // checked인 access mode의 tag들만을 습득.
    const accessModeTags = document.querySelectorAll('input[name="' + accessModeField + '"]:checked');
    // 없을 경우, null을 반환.
    if (accessModeTags.length === 0) {
        return null;
    }

    // checked 되어있는 access mode들을 순환하며 값을 추출하여 list에 추가.
    const accessModeList = [];
    accessModeTags.forEach((element) => { accessModeList.push(element.value); });

    return accessModeList;
}

/**
 * mount option의 field명을 가진 모든 tag들의 값을 list에 담아서 반환한다.
 * @param mountOptionField mount option의 field명.
 * @returns {null|[]} mount option list. ( tag가 없을 경우, null을 반환한다. )
 */
function mountOptionsPayload(mountOptionField) {
    // mount option의 field명을 가진 모든 tag들을 추출.
    const mountOptionTags = document.getElementsByName(mountOptionField);
    // 없을시 null을 반환.
    if (mountOptionTags.length === 0) {
        return null;
    }

    // 추출한 mount option들을 순회하면서 값을 list에 추가.
    const mountOptionList = [];
    mountOptionTags.forEach((element) => {
        if (element.value.trim() !== "") {
            mountOptionList.push(element.value.trim());
        }
    });

    return mountOptionList;
}

/**
 * Node Affinity에서 생성된 Node Selector들의 data를 json 형식의 Object로 반환한다.
 * @param nodeSelectorTermsField node selector 묶음을 지지는 field명.
 * @returns {null|[]} json 형식의 Object. ( 유효한 node selector가 하나도 없는 경우 null을 반환한다. )
 */
function nodeSelectorTermsPayload(nodeSelectorTermsField) {

    // 인수로 받은 field 명에 대응하는 모든 node selector를 습득.
    const nodeSelectorTermsTags = document.getElementsByClassName(nodeSelectorTermsField);
    if (nodeSelectorTermsTags.length === 0) {
        return null;
    }

    // node selector들을 순회.
    const nodeSelectorTermsList = [];
    for (const element of nodeSelectorTermsTags) {

        // node selector로부터 rule들을 습득.
        const matchExpressions = matchExpressionsPayload(element);

        // rule 들이 있는 경우에만 node selector terms list에 삽입.
        if (matchExpressions !== null) {
            nodeSelectorTermsList.push({ "matchExpressions": matchExpressions });
        }
    }

    // 유효한 node selector term이 하나도 없는 경우, null을 반환.
    if (nodeSelectorTermsList.length === 0) {
        return null;
    }

    return nodeSelectorTermsList;
}

/**
 * 하나의 Node Selector로부터 정의되어 있는 모든 rule을 json 형식의 Object를 반환한다.
 * @param div 하나의 Node Selector.
 * @returns {null|[]} json 형식의 Object. ( 유요한 rule이 하나도 없는 경우, null을 반환. )
 */
function matchExpressionsPayload(div) {

    // Node Selector 내의 table로부터 모든 rule row를 습득.
    const table = div.getElementsByTagName("table")[0];
    const tbody = table.getElementsByTagName("tbody")[0];
    const trows = tbody.getElementsByTagName("tr");
    if (trows.length === 0) {
        return null;
    }

    // rule row들을 순회.
    const matchExpressionList = [];
    for (const row of trows) {

        // 하나의 rule row로부터 json 형식의 object를 습득.
        const matchExpression = matchExpressionPayload(row);

        // rule row 내에 유효한 값이 있는 경우에만 삽입.
        if (matchExpression !== null) {
            matchExpressionList.push(matchExpression);
        }
    }

    return matchExpressionList.length === 0 ? null : matchExpressionList;
}

/**
 * 임의의 Node Selector에 있는 하나의 rule을 json 형식의 Object로 반환한다.
 * @param row 하나의 rule을 가지고 있는 row.
 * @returns {null|any} json 형식의 하나의 rule Object.
 */
function matchExpressionPayload(row) {
    const matchExpression = Object();

    // 하나의 row로부터 값을 추출함.
    const key = row.cells[0].getElementsByTagName("input")[0].value.trim();
    const operator = row.cells[1].getElementsByTagName("select")[0].value;
    const valuesTag = row.cells[2].getElementsByTagName("input")[0];
    const isHidden = valuesTag.style.visibility === "hidden";

    // 만약 hidden일 경우, 해당 row는 value를 가지지 않으므로 무시.
    const values = [];
    if (!isHidden) {
        // values string을 얻음.
        const valuesString = valuesTag.value.trim();
        if (valuesString !== "") {

            // values string을 ','를 기준으로 잘라냄.
            const temper = valuesString.split(',');

            // 잘라낸 값들을 순회하면서 삽입.
            for (const one of temper) {
                values.push(one.trim());
            }
        }
    }

    // key가 없을 경우, null을 반환하여 해당 expression 생성을 무시.
    if (key === "") {
        return null;
    }

    // key는 있지만, value값이 없는 경우, null을 반환하여 해당 expression의 생성을 무시.
    if (!isHidden && values.length === 0) {
        return null;
    }

    // key, operator 값을 json 형식으로 삽입.
    matchExpression["key"] = key;
    matchExpression["operator"] = operator;

    // hidden이 아닌 경우, 즉, value가 있는 경우, value를 json 형식으로 삽입.
    if (!isHidden) {
        matchExpression["values"] = values;
    }

    return matchExpression;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// plugin 관련

let plugin;
let pluginTemplate;

let pluginParentDiv;

// 초기화 함수를 page onload 시 실행.
window.addEventListener("load", initialization);

/**
 * 초기화 함수.
 * plugin 관련 정보를 내부 변수로 습득한다.
 */
function initPlugin() {
    plugin = document.getElementById("plugin-configuration-template-hidden");
    pluginTemplate = plugin.value;
    pluginParentDiv = document.getElementById("plugin-configuration-parent-div");
}

/**
 * Volume Plugin이 선택되었을시의 Event를 수행한다.
 * @param select 선택시에 사용된 select tag.
 */
function onVolumePluginSelected(select) {
    const selectedOption = select.options[select.selectedIndex];
    const field = selectedOption.value;
    const title = selectedOption.text;

    // 해당 volume source의 기재 내용을 출력할 div를 모두 비워둔다.
    $("#" + pluginParentDiv.id).empty();
    // default의 경우, text만을 출력한다.
    if (field === "default") {
        pluginParentDiv.innerHTML = "Choose a Volume Source above...";

    // default가 아닌경우, 해당 volume source에 대한 configuration div를 삽입한다.
    } else {
        pluginParentDiv.appendChild(loadPluginConfigurationDiv(title));
    }
}

/**
 * 임의의 volume source에 대한 configuration을 생성하여 div에 삽입 및 호출하는 함수.
 * @param title 임의의 volume source의 title.
 * @returns {HTMLDivElement} configuration이 삽입된 div.
 */
function loadPluginConfigurationDiv(title) {
    const div = document.createElement("div");

    // back-end 로부터 얻은 data를 json 형식의 object로 변환한다.
    const volumeSources = JSON.parse(pluginTemplate);

    // 입력으로 들어온 volume source에 대한 configuration 정보 mapping을 습득한다.
    const volumeSource = volumeSources[title];
    const configuration = volumeSource["configuration"];

    // configuration mapping을 기반으로 각종 component를 제작하여 div에 삽입한다.
    for (const [name, value] of Object.entries(configuration)) {
        // configuration의 name label.
        div.appendChild(Object.assign(document.createElement("label"), { innerText: value["label"], style: "font-weight: bold" }));
        // 줄바꿈.
        div.appendChild(document.createElement("br"));
        // configuration에 따른 tag 생성 및 삽입.
        div.appendChild(generate(name, value));

        // 줄바꿈.
        div.appendChild(document.createElement("br"));
        div.appendChild(document.createElement("br"));
    }

    return div;
}

/**
 * 임의의 Volume Source Configuration에 해당하는 tag를 생성하여 반환한다.
 * @param name configuration의 name.
 * @param value configuration의 value mapper.
 * @returns {(HTMLInputElement & {id: string, placeholder: *, type: string, value: *, required: *})|(HTMLSelectElement & {id: string})|HTMLDivElement|(HTMLLabelElement & {innerText: *, id: string, value: *})} 생성된 tag.
 */
function generate(name, value) {
    // tag의 type에 맞게 tag를 생성한다.
    // tag의 type은 back-end에서 결정되어 view로 넘어오게 된다.
    switch(value["type"]) {
        case "label/string": return childLabelString(name, value);
        case "label/int": return childLabelInt(name, value);
        case "label/fix": return childLabelFix(name, value);
        case "radio": return childRadio(name, value);
        case "select": return childSelect(name, value);
        case "map/addable": return childMapAddable(name, value);
    }
}

/**
 * tag의 type이 문자열인 경우.\n
 * input tag에 type 속성은 text인 tag를 생성한다.
 * @param name 해당 tag로 생성될 field의 이름.
 * @param value 해당 field가 가지고 있는 설정값.
 * @returns {HTMLInputElement & {id: string, placeholder: *, type: string, value: *, required: *}} 완성된 tag.
 */
function childLabelString(name, value) {
    return Object.assign(
        document.createElement("input")
        , {
            type: "text"
            , id: name.toString()
            , placeholder: value["placeholder"]
            , value: value["default"]
            , required: value["required"]
        });
}

/**
 * tag의 type이 정수 문자열인 경우.\n
 * input tag에 type 속성은 number인 tag를 생성한다.
 * @param name 해당 tag로 생성될 field의 이름.
 * @param value 해당 field가 가지고 있는 설정값.
 * @returns {HTMLInputElement & {id: string, placeholder: *, type: string, value: *, required: *}} 완성된 tag.
 */
function childLabelInt(name, value) {
    return Object.assign(
        document.createElement("input")
        , {
            type: "number"
            , id: name.toString()
            , placeholder: value["placeholder"]
            , value: value["default"]
            , required: value["required"]
        });
}

/**
 * tag의 type이 수정불가의 고정인 문자열인 경우.\n
 * label tag를 생성한다.
 * @param name 해당 tag로 생성될 field의 이름.
 * @param value 해당 field가 가지고 있는 설정값.
 * @returns {HTMLLabelElement & {innerText: *, id: string, value: *}} 완성된 tag.
 */
function childLabelFix(name, value) {
    return Object.assign(
        document.createElement("label")
        , {
            id: name.toString()
            , value: value["default"]
            , innerText: value["default"]
        });
}

/**
 * tag의 type이 택일선택인 radio인 경우.\n
 * radio tag와 radio tag를 grouping할 div를 생성한다.
 * @param name 해당 tag로 생성될 field 이름.
 * @param value 해당 field가 가지고 있는 설정값.
 * @returns {HTMLDivElement} 완성된 radio group tag.
 */
function childRadio(name, value) {
    // radio들을 grouping할 div tag를 생성.
    const result = Object.assign(
        document.createElement("div")
        , {
            style: "display: inline;"
        }
    );

    const items = value["items"];

    let counter = 0;
    const limit = items.length;

    // field가 가지고 있는 목록들을 순희.
    value["items"].forEach((item) => {
        const label = Object.assign(
           document.createElement("label")
           , {
               for: name.toString()
               , innerText: item["label"]
           });

        // 각 목록을 하나의 radio button으로 생성.
        const input = Object.assign(
            document.createElement("input")
            , {
                type: "radio"
                , name: name.toString()
                , value: item["value"]
                , checked: (item["value"] === value["default"])
            });

        // 생성 완료된 radio button을 label에 삽입.
        label.insertBefore(input, label.firstChild);

        // 줄바꿈 문자 추가.
        if (counter !== limit) {
            label.appendChild(document.createElement("br"));
        }

        // label-radio 묶음을 radio grouping div에 삽입.
        result.appendChild(label);
    });

    return result;
}

/**
 * tag의 type이 택일 dropbox인 select인 경우.\n
 * select tag를 생성한다.
 * @param name 해당 tag로 생성될 field 이름.
 * @param value 해당 field가 가지고 있는 설정값.
 * @returns {HTMLSelectElement & {id: string}} 완성된 tag.
 */
function childSelect(name, value) {
    // option들을 담을 select tag를 생성한다.
    const result = Object.assign(
        document.createElement("select")
        , {
            id: name.toString()
        });

    // 해당 field가 가지고 있는 목록들을 순회.
    value["items"].forEach((item) => {
        // 각 목록을 하나의 option으로 만든다.
        const option = Object.assign(
            document.createElement("option")
            , {
                value: item["value"]
                , innerText: item["label"]
                , selected: (item["value"] === value["default"])
            }
        );

        // 만든 option을 select tag에 삽입한다.
        result.appendChild(option);
    });

    return result;
}

/**
 * tag의 type이 key-value를 받고, row add 및 row remove가 포함되어 있는 경우.\n
 * table tag와 add/remove button 및 각종 요소들을 생성한다.
 * @param name 해당 tag로 생성될 field의 이름.
 * @param value 해당 field가 가지고 있는 설정값.
 * @returns {HTMLDivElement} 완성된 key-value 및 add/remove button package.
 */
function childMapAddable(name, value) {
    // 모든 요소들을 담을 하나의 div tag를 생성한다.
    const result = document.createElement("div");

    // div tag에 table을 삽입한다.
    result.innerHTML =
        '<table id="' + name + '">' +
        '   <thead>' +
        '       <th>Key</th>' +
        '       <th>Value</th>' +
        '       <th></th>' +
        '   </thead>' +
        '   <tbody>' +
        '       ' +
        '   </tbody>' +
        '</table>';

    // div tag에 add button을 삽입한다.
    result.innerHTML += '<button type="button" id="' + name + '-add">Add</button>';

    // div tag로부터 table과 tbody를 추출한다.
    // 여기서 tbody는 key-value 및 remove button 구조의 row를 담는다.
    const table = result.firstChild;
    const tbody = table.getElementsByTagName("tbody")[0];

    // 각 remove button의 고유id 생성을 위해 suffix로 사용한다.
    // ( 이것이 없으면, 모든 remove button은 동일 id를 가지게 되어서,
    //   어떤 remove button을 눌러도 모든 row가 삭제되어버린다. )
    let autoIncrement = 0;

    // row를 생성하는 함수.
    const createRow = function(body, name, key, value) {
        const row = body.insertRow();
        const number = autoIncrement++;

        // 하나의 row를 생성한다.
        row.innerHTML =
            '<tr>' +
            '   <td><input type="text" value="' + key + '"/></td>' +
            '   <td><input type="text" value="' + value + '"</td>' +
            '   <td><button type="button" id="' + name + number.toString() + '">remove</button></td>' +
            '</tr>';

        // row에 있는 remove button에 event를 추가한다.
        $(document).on(
            'click'
            ,'#' + name + number.toString()
            , function() {
                row.remove();
            }
        )
    }

    // div tag에 있는 add button에 event를 추가한다.
    $(document).on(
        'click'
        , '#' + name + '-add'
        , function() {
            createRow(tbody, name, "", "");
        });

    // field의 value가 가지고 있는 기본값으로,
    // 위의 요소들을 생성한 후, 기본으로 들어가 있는 row들을 생성한다.
    $.each(value["default"], function(key, value) {
        createRow(tbody, name, key, value);
    });

    return result;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Mount Option 관련

let parentTable;
let autoIncrement = 0;

window.addEventListener("load", initialization);

function initMountOption() {
    parentTable = document.getElementById("mount-option-table");
}

/**
 * mount option의 add button을 누를경우 발생하는 event callback 함수.
 */
function onAddMountOption() {
    const tbody = parentTable.getElementsByTagName("tbody")[0];
    const row = tbody.insertRow();

    // remove button의 고유id를 생성하기 위한 suffix.
    // ( 이것이 없으면, 모든 remove button은 동일 id를 가지게 되어서,
    //   어떤 remove button을 눌러도 모든 row가 삭제되어버린다. )
    const number = autoIncrement++;

    // mount option의 하나의 값을 설정하는 row를 추가한다.
    row.innerHTML =
        '<tr>' +
        '   <td><input type="text" name="mountOptions" placeholder="Value"/></td>' +
        '   <td><button type="button" id="mount-options-remove' + number.toString() + '">remove</button></td>' +
        '<tr/>';

    // remove button에 event를 추가한다.
    $(document).on(
        'click'
        ,'#mount-options-remove' + number.toString()
        , function() {
            row.remove();
        }
    );
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Node Affinity 관련 관련

let nodeAffinityParentTable;

let autoIncrementSelector = 0;
let autoIncrementRule = 0;

window.addEventListener("load", initialization);

function initNodeAffinity() {
    nodeAffinityParentTable = document.getElementById("node-affinity-table");
}

function onAddNodeAffinity() {
    const tbody = nodeAffinityParentTable.getElementsByTagName("tbody")[0];
    const row = tbody.insertRow();
    const selectorNumber = autoIncrementSelector++;

    generateNodeSelector(row, selectorNumber);
}

function generateNodeSelector(row, selectorNumber) {
    row.innerHTML =
        '<tr>' +
        '   <td>' +
        '       <div class="nodeSelectorTerms" style="border: 1px solid black;">' +
        '           <label style="font-style: inherit; font-size: 1.5em">Node Selector</label>' +
        '           <label id="node-selector-remove' + selectorNumber.toString() + '" ' +
        '                  style="cursor: pointer; text-decoration: underline; color: dodgerblue;">Remove this Node Selector</label><br/><br/>' +
        '           <label>Rules</label>' +
        '           <button type="button" id="add-rule' + selectorNumber.toString() + '">Add Rule</button>' +
        '           <table>' +
        '               <thead>' +
        '                   <th>Key</th>' +
        '                   <th>Operator</th>' +
        '                   <th>Values</th>' +
        '                   <th></th>' +
        '               </thead>' +
        '               <tbody>' +
        '               </tbody>' +
        '           </table>' +
        '       </div>' +
        '   </td>' +
        '<tr/>';

    $(document).on(
        "click"
        , "#node-selector-remove" + selectorNumber.toString()
        , function() {
            row.remove();
        }
    );

    $(document).on(
        "click"
        , "#add-rule" + selectorNumber.toString()
        , function() {
            const ruleTable = row.getElementsByTagName("table")[0];
            const ruleTbody = ruleTable.getElementsByTagName("tbody")[0];
            const ruleRow = ruleTbody.insertRow();
            const ruleNumber = autoIncrementRule++;

            generateRule(ruleRow, selectorNumber, ruleNumber);
        }
    );
}

function generateRule(row, selectNumber, ruleNumber) {
    const selectorOperatorString = document.getElementById("node-affinity-hidden").value;
    const selectorOperator = JSON.parse(selectorOperatorString);
    const unique =  + selectNumber.toString() + ruleNumber.toString();

    row.innerHTML =
        '<tr>' +
        '   <td><input type="text" placeholder="e.g. kubernetes.io/hostname"/></td>' +
        '   <td><select id="selector-operator-select' + unique + '"></select></td>' +
        '   <td><input type="text" id="selector-operator-values' + unique + '" placeholder="Comma-separated, e.g. node1,dode2"/></td>' +
        '   <td><button type="button" id="rule-remove' + unique + '">remove</button></td>' +
        '<tr/>';

    const selector = "#selector-operator-select" + unique;
    selectorOperator.forEach((entity) => {
        const option = $('<option value="' + entity['value'] + '">' + entity['label'] + '</option>')
        option.attr("selected", entity['value'] === "In");
        $(selector).append(option);
    });

    $(document).on(
        "change"
        , selector
        , function() {
            const selectorValue = $(selector).val();
            const flag = selectorValue === "Exists" || selectorValue === "DoesNotExist";
            const values = $("#selector-operator-values" + unique);
            values.val("");
            values.css({ visibility: flag ? "hidden" : "" });
        }
    )

    $(document).on(
        "click"
        , "#rule-remove" + unique
        , function() {
            row.remove();
        }
    )
}