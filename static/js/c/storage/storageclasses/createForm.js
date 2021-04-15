$(function () {
    initMountOption();
    initParameters();
    initRadioGroupOfCustomize();
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Mount Option 관련
let parentTable;
let autoCounter = 0;

let placeholder;
let field;

/**
 * Page Load 후 호출되는 초기화 callback 함수.
 */
function initMountOption() {
    parentTable = document.getElementById("mount-options-table");
}

/**
 * Add Mount button을 눌렀을 때 호출되는 trigger 함수.
 * @param button Add Mount Button.
 */
function onAddMountOption(button) {
    const tbody = parentTable.getElementsByTagName("tbody")[0];
    const row = tbody.insertRow();

    // placeholder 또는 field 값이 없을 경우, 이를 가지고 온다.
    if (!!!placeholder || !!!field) {
        const val = button.value;
        const jsonVal = JSON.parse(val);
        placeholder = jsonVal["placeholder"];
        field = jsonVal["field"];
    }

    // remove button의 고유id를 생성하기 위한 suffix.
    // ( 이것이 없으면, 모든 remove button은 동일 id를 가지게 되어서,
    //   어떤 remove button을 눌러도 모든 row가 삭제되어버린다. )
    const counter = autoCounter++;

    // mount option의 하나의 값을 설정하는 row를 추가한다.
    row.innerHTML =
        '<tr>' +
        '   <td><input type="text" name="' + field + '" placeholder="' + placeholder + '"/></td>' +
        '   <td><button type="button" id="mount-options-remove' + counter.toString() + '">remove</button></td>' +
        '<tr/>';

    // remove button에 event를 추가한다.
    $(document).on(
        "click"
        , "#mount-options-remove" + counter
        , function () {
            row.remove();
        }
    );
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Parameters 관련
let before;

let parameters;
let parametersTemplateString;
let parametersTemplate;

const parentDivSuffix = "-parent-div";
const rootDivName = "root-div";

let customDefaultValue;

const provisionerMapping = Object();

let parentDiv;

/**
 * Page Load 후 호출되는 초기화 callback 함수.
 */
function initParameters() {
    // provisioner input tag 습득.
    const provisionerInput = document.getElementById("provisioner-input");

    // provisioner input tag로부터 값 습득.
    before = provisionerInput.value;

    // provisioner input으로부터 datalist 추출 및 options 값을 mapping.
    for (const option of provisionerInput.list.options) {
        const dataValue = option.getAttribute("data-value");
        if (!isNullOrEmpty(dataValue)) {
            provisionerMapping[option.getAttribute("value")] = dataValue;
        } else {
            customDefaultValue = option.getAttribute("value");
        }
    }

    parameters = document.getElementById("parameters-template-hidden");
    parametersTemplateString = parameters.value;
    parametersTemplate = JSON.parse(parametersTemplateString);

    parentDiv = document.getElementById("parameters-parent-div");

    // 첫 시작 default value에 대한 parameters load.
    componentGenerateExample(parentDiv, provisionerMapping[before]);
}

/**
 * Provisioner Input Field가 Focusing 되었을 때 호출되는 trigger 함수.
 * @param input Provisioner Input Field.
 */
function onFocusedProvisioner(input) {
    input.value = "";
}

/**
 * Provisioner Input Field의 값이 Changing 되었을 때 호출되는 trigger 함수.
 * @param input Provisioner Input Field.
 */
function onChangedProvisioner(input) {
    before = input.value;
    input.blur();

    if (before in provisionerMapping) {
        // 선택된 값에 대한 parameters load.
        componentGenerateExample(parentDiv, provisionerMapping[before]);
    } else {
        // input의 value 뒤에 custom suffix를 붙임.
        let fixValue = input.value + customDefaultValue;

        // custom suffix의 앞까지 모두 잘라버림.
        fixValue = fixValue.substring(0, fixValue.indexOf(customDefaultValue));

        // 자른 값에 custom suffix를 붙여서 다시 input의 value에 삽입.
        // 이를 통해서 custom suffix의 중복 삽입을 방지할 수 있다.
        input.value = fixValue + customDefaultValue;

        // 중복을 제거한 값을 다시 삽입.
        before = input.value;

        loadCustomParameterDiv(parentDiv, fixValue);
    }
}

/**
 * Provisioner Input Field가 UnFocusing 되었을 때 호출되는 trigger 함수.
 * @param input Provisioner Input Field.
 */
function onBlurProvisioner(input) {
    if (input.value !== before) {
        input.value = before;
    }
}

/**
 * parameters가 cutomizing일 경우, custom용 div를 생성 및 삽입하는 함수.
 * @param div 생성한 div를 삽입할 parent div.
 */
function loadCustomParameterDiv(div, name) {
    const saveBeforeInnerHTML = div.innerHTML;

    try {
        // parent div를 일단 비워둠.
        div.innerHTML = '';

        // 새로운 div 생성.
        const newDiv = Object.assign(
            document.createElement("div")
            , {
                id: "custom" + parentDivSuffix
                , style: "display: inline;"
                , name: rootDivName
            }
        );

        // 이후, 새로 생성한 div를 id를 통해 document로부터 호출하기 위해 parent div에 선삽입.
        div.appendChild(newDiv);

        // configuration에 따른 tag 생성.
        const generatedElement = generate(name, {"type": "map/addable"});
        if (generatedElement === null) {
            alert("failed to create [" + name + "] tag.");
            throw "";
        }

        // 이후의 과정에서 document로부터 tag를 검색하기 위해 삽입.
        newDiv.appendChild(generatedElement);

    } catch (error) {
        div.innerHTML = saveBeforeInnerHTML;
        throw error;
    }
}

function componentGenerateExample(parentTag, componentName) {
    // 인수로 들어온 component name 값을 이용하여 configuration 정보를 습득한다.
    const volumeSource = parametersTemplate[componentName];
    const configuration = volumeSource["configuration"];

    loadExample(parentTag, configuration);
}

/**
 * 임의의 Storage Class에 대한 configuration을 습득하고, 그 내용을 바탕으로 div를 생성 및 삽입하는 함수.
 * @param parentTag 생성한 div를 삽입할 parent div.
 * @param configuration 생성할 component에 대한 정보를 가진 설정값.
 */
function loadExample(parentTag, configuration) {
    const saveBeforeInnerHTML = parentTag.innerHTML;

    try {
        // parent div를 일단 비워둠.
        parentTag.innerHTML = '';

        // configuration mapping을 기반으로 각종 tag를 제작하여 div에 삽입한다.
        for (const [field, information] of Object.entries(configuration)) {
            // 새로운 div 생성.
            const newDiv = Object.assign(
                document.createElement("div")
                , {
                    id: field.toString() + parentDivSuffix
                    , style: "display: inline;"
                    , name: rootDivName
                }
            );
            // 새로운 div를 parent div에 삽입.
            parentTag.appendChild(newDiv);

            if (information["label"] !== "") {
                // 줄바꿈.
                newDiv.appendChild(document.createElement("br"));

                // configuration의 name label.
                newDiv.appendChild(Object.assign(
                    document.createElement("label")
                    , {
                        innerText: information["label"]
                        , style: "font-weight: bold"
                    }
                ));
                // 줄바꿈.
                newDiv.appendChild(document.createElement("br"));
            }

            // configuration에 따른 tag 생성.
            const generatedElement = generate(field, information);
            if (generatedElement === null) {
                alert("failed to create [" + field + "] tag.");
                continue;
            }

            // 이후의 과정에서 document로부터 tag를 검색하기 위해 삽입.
            newDiv.appendChild(generatedElement);

            // condition 추가.
            setConditionExample(generatedElement, information["condition"], configuration);

            // related 추가.
            setRelatedExample(generatedElement, field, information["related"]);

            // 줄바꿈.
            newDiv.appendChild(document.createElement("br"));
        }
    } catch (error) {
        parentTag.innerHTML = saveBeforeInnerHTML;
        throw error;
    }
}

/**
 * 임의의 Storage Class Configuration에 해당하는 tag를 생성하여 반환한다.
 * @param field configuration의 name.
 * @param information configuration의 value mapper.
 * @returns {(HTMLInputElement & {id: string, placeholder: *, type: string, value: *, required: *})|(HTMLSelectElement & {id: string})|HTMLDivElement|(HTMLLabelElement & {innerText: *, id: string, value: *})} 생성된 tag.
 */
function generate(field, information) {
    switch (information["type"]) {
        case "label/string":
            return childLabelString(field, information);
        case "label/int":
            return childLabelInteger(field, information);
        case "label/fix":
            return childLabelFix(field, information);
        case "radio":
            return childRadio(field, information);
        case "select":
            return childSelect(field, information);
        case "map/addable":
            return childMapAddable(field, information);
    }

    return null;
}

/**
 * tag의 type이 문자열인 경우.\n
 * input tag에 type 속성은 text인 tag를 생성한다.
 * @param field 해당 tag로 생성될 field의 이름.
 * @param information 해당 field가 가지고 있는 설정값.
 * @returns {HTMLInputElement & {id: string, placeholder: *, type: string, value: *, required: *}} 완성된 tag.
 */
function childLabelString(field, information) {
    return Object.assign(
        document.createElement("input")
        , {
            type: "text"
            , id: field.toString()
            , "placeholder": information["placeholder"]
            , value: information["default"]
            , required: information["required"]
        }
    );
}

/**
 * tag의 type이 정수 문자열인 경우.\n
 * input tag에 type 속성은 number인 tag를 생성한다.
 * @param field 해당 tag로 생성될 field의 이름.
 * @param information 해당 field가 가지고 있는 설정값.
 * @returns {HTMLInputElement & {id: string, placeholder: *, type: string, value: *, required: *}} 완성된 tag.
 */
function childLabelInteger(field, information) {
    return Object.assign(
        document.createElement("input")
        , {
            type: "number"
            , id: field.toString()
            , placeholder: information["placeholder"]
            , value: information["default"]
            , required: information["required"]
        }
    );
}

/**
 * tag의 type이 수정불가의 고정인 문자열인 경우.\n
 * label tag를 생성한다.
 * @param field 해당 tag로 생성될 field의 이름.
 * @param information 해당 field가 가지고 있는 설정값.
 * @returns {HTMLLabelElement & {innerText: *, id: string, value: *}} 완성된 tag.
 */
function childLabelFix(field, information) {
    return Object.assign(
        document.createElement("label")
        , {
            id: field.toString()
            , value: information["default"]
            , innerText: information["default"]
        }
    );
}

/**
 * tag의 type이 택일선택인 radio인 경우.\n
 * radio tag와 radio tag를 grouping할 div를 생성한다.
 * @param field 해당 tag로 생성될 field 이름.
 * @param information 해당 field가 가지고 있는 설정값.
 * @returns {HTMLDivElement} 완성된 radio group tag.
 */
function childRadio(field, information) {
    // radio들을 grouping할 div tag를 생성.
    const element = Object.assign(
        document.createElement("div")
        , {
            style: "display: inline;"
        }
    );

    const items = information["items"];

    let counter = 0;
    const limit = items.length;

    // field가 가지고 있는 목록들을 순희.
    items.forEach((item) => {
        counter++;

        const label = Object.assign(
            document.createElement("label")
            , {
                for: field.toString()
                , innerText: item["label"]
            });

        // 각 목록을 하나의 radio button으로 생성.
        const input = Object.assign(
            document.createElement("input")
            , {
                type: "radio"
                , name: field.toString()
                , value: item["value"]
                , checked: item["value"] === information["default"]
            });

        // 생성 완료된 radio button을 label에 삽입.
        label.insertBefore(input, label.firstChild);

        // 줄바꿈 문자 추가.
        if (counter !== limit) {
            label.appendChild(document.createElement("br"));
        }

        // label-radio 묶음을 radio grouping div에 삽입.
        element.appendChild(label);
    });

    return element;
}

/**
 * tag의 type이 택일 dropbox인 select인 경우.\n
 * select tag를 생성한다.
 * @param field 해당 tag로 생성될 field 이름.
 * @param information 해당 field가 가지고 있는 설정값.
 * @returns {HTMLSelectElement & {id: string}} 완성된 tag.
 */
function childSelect(field, information) {
    // option들을 담을 select tag를 생성한다.
    const result = Object.assign(
        document.createElement("select")
        , {
            id: field.toString()
        });

    // 해당 field가 가지고 있는 목록들을 순회.
    information["items"].forEach((item) => {
        // 각 목록을 하나의 option으로 만든다.
        const option = Object.assign(
            document.createElement("option")
            , {
                value: item["value"]
                , innerText: item["label"]
                , selected: (item["value"] === information["default"])
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
 * @param field 해당 tag로 생성될 field의 이름.
 * @param information 해당 field가 가지고 있는 설정값.
 * @returns {HTMLDivElement} 완성된 key-value 및 add/remove button package.
 */
function childMapAddable(field, information) {
    // 모든 요소들을 담을 하나의 div tag를 생성한다.
    const result = document.createElement("div");

    // div tag에 table을 삽입한다.
    result.innerHTML =
        '<table id="' + field + '">' +
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
    result.innerHTML += '<button type="button" id="' + field + '-add">Add</button>';

    // div tag로부터 table과 tbody를 추출한다.
    // 여기서 tbody는 key-value 및 remove button 구조의 row를 담는다.
    const table = result.firstChild;
    const tbody = table.getElementsByTagName("tbody")[0];

    // 각 remove button의 고유id 생성을 위해 suffix로 사용한다.
    // ( 이것이 없으면, 모든 remove button은 동일 id를 가지게 되어서,
    //   어떤 remove button을 눌러도 모든 row가 삭제되어버린다. )
    let autoIncrement = 0;

    // row를 생성하는 함수.
    const createRow = function (body, name, key, value) {
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
            , '#' + name + number.toString()
            , function () {
                row.remove();
            }
        )
    }

    // div tag에 있는 add button에 event를 추가한다.
    $(document).on(
        'click'
        , '#' + field + '-add'
        , function () {
            createRow(tbody, field, "", "");
        });

    // field의 value가 가지고 있는 기본값으로,
    // 위의 요소들을 생성한 후, 기본으로 들어가 있는 row들을 생성한다.
    if ("default" in information) {
        $.each(information["default"], function (key, value) {
            createRow(tbody, field, key, value);
        });
    }

    return result;
}

/**
 * 임의의 element의 초기 condition( 조건 )을 구축한다.\n
 * 해당 element의 event의 trigger가 될 다른 element가 condition에 정의되어 있다.\n
 * 예를 들면, A element의 값을 수정하면 해당 element의 visibility가 visible이 된다. 등.
 * @param element 임의의 element.
 * @param conditionList 해당 element에 정의할 condition( 조건 ) List.
 * @param configuration 임의의 Storage Class에 대한 configuration.
 */
function setConditionExample(element, conditionList, configuration) {

    // condition list의 값이 존재하는지 확인.
    if (!isNullOrEmpty(conditionList)) {

        // 임의의 element의 root가 되는 parent div를 탐색.
        let parentDiv = getRootByName(element, rootDivName);
        if (isNullOrEmpty(parentDiv)) {
            return;
        }

        // parent div 내에 있는 모든 node를 습득.
        const allNodes = parentDiv.childNodes;

        // 모든 condition을 순회.
        for (const condition of conditionList) {

            // condition에 정의되어 있는 해당 element의 trigger가 될 다른 element의 type을 습득.
            // condition["id"]는 다른 element의 id값이다.
            const type = configuration[condition["id"]]["type"];
            // 얻은 type을 이용하여 다른 element의 값을 추출.
            const value = getValueTemplate(type, condition["id"]);

            // trigger 발생시 해당 element의 변경할 속성 정보.
            const action = condition["action"];

            // 변경할 속성이 style인지 확인.
            const isStyle = action.startsWith("style.");
            // style인 경우, style의 field 명을 추출.
            const styleName = (isStyle) ? action.substr(action.indexOf("style.") + "style.".length) : null;

            // 변경할 속성에 어떠한 변경값을 넣을지 actionParameter mapping으로부터 추출.
            const actionParameter = condition["actionParameter"][
                (value === condition["value"].toString()) ? "OK" : "NG"];

            // 해당 element를 품은 parent div 내에 있는 모든 node를 순회.
            for (const node of allNodes) {
                // style일 경우, style을 설정.
                if (isStyle) {
                    node.style[styleName] = actionParameter;

                    // style이 아닌 경우, attribute를 설정.
                } else {
                    node.setAttribute(action, actionParameter);
                }
            }
        }
    }
}

/**
 * 임의의 element의 trigger 발동시 수행을 할 다른 element의 관계를 구축한다.\n
 * 해당 element의 event trigger 발동시, 수행을 할 다른 element의 정보가 related에 정의되어 있다.\n
 * 예를 들면 해당 element의 값이 수정될 시, B/C element의 visibility가 visible이 된다. 등.
 * @param element 임의의 element.
 * @param field 임의의 element의 field 값.
 * @param relatedList 해당 element가 가지고 있는 수행원 element List.
 */
function setRelatedExample(element, field, relatedList) {

    // related List의 값이 존재하는지 확인.
    if (!isNullOrEmpty(relatedList)) {

        // 해당 element의 field 값을 통해, field 값에 해당하는 모든 element를 가지고 옴.
        // 해당 element가 하나일수도, 여러개일수도 있기 때문에, field 값을 통해 모두 가져온다.
        const selfNodes = getAllNodeUsingIdAndName(field.toString());

        // 모든 해당하는 element를 순회.
        for (const node of selfNodes) {

            // 수행원 element의 정보를 가지고 있는 related list를 순회.
            for (const related of relatedList) {

                // related로부터 수행원 element의 변경할 속성 정보를 습득.
                const action = related["action"];

                // 변경할 속성 정보가 style인지 확인.
                const isStyle = action.startsWith("style.");
                // style인 경우, style의 field 명을 추출.
                const styleName = (isStyle) ? action.substr(action.indexOf("style.") + "style.".length) : null;

                // 변경할 속성에 어떠한 변경값을 넣을지 actionParamter mapping으로부터 추출.
                const actionParameter = related["actionParameter"][
                    (node.getAttribute(related["attribute"]) === related["value"].toString()) ? "OK" : "NG"];

                // 수행원 element의 id( 또는 name )값을 추출.
                const targetId = related["targetId"];

                // 해당하는 element에 event를 추가.
                node.addEventListener(
                    related["trigger"]
                    , function () {
                        // 수행원 element의 id( 또는 name ) 값을 이용하여 모든 수행원 element를 추출.
                        // 수행원 element가 하나일수도, 여러개일수도 있기 때문에, field값을 통해 모두 가져온다.
                        const targetNodes = getAllNodeUsingIdAndName(targetId);

                        // id, name으로 탐색한 node들은 반드시 유일한 parent div를 가지고 있다고 가정한다.
                        // 즉, 수행원 element가 여러개여도, 하나의 유일한 parent div에 전부 들어가있다고 가정.
                        // 하나의 유일한 parent div를 습득한다.
                        let targetParentDiv = getRootByName(targetNodes[0], rootDivName);
                        if (isNullOrEmpty(targetParentDiv)) {
                            return;
                        }

                        // parent div 내에 있는 모든 node를 습득한다.
                        const allTargetNodes = targetParentDiv.childNodes;

                        // parent div 내에 있는 모든 node를 순회.
                        for (const targetNode of allTargetNodes) {
                            // style인 경우, style을 설정.
                            if (isStyle) {
                                targetNode.style[styleName] = actionParameter;

                                // style이 아닌 경우, attribute를 설정.
                            } else {
                                targetNode.setAttribute(action, actionParameter);
                            }
                        }
                    }
                )
            }
        }
    }
}

/**
 * type을 통해 어떠한 종류의 tag로부터 값을 추출할지 결정하고, id값을 통해 해당 tag로부터 값을 추출한다.
 * @param type 추출할 tag의 종류.
 * @param id 추출할 tag의 id( 또는 name )
 * @returns {string|null|*} 추출한 값.
 */
function getValueTemplate(type, id) {
    switch (type) {
        case "label/string":
            return document.getElementById(id).value;
        case "label/int":
            return document.getElementById(id).value;
        case "label/fix":
            return document.getElementById(id).innerText;
        case "radio":
            return document.querySelector('input[name="' + id + '"]:checked').value;
        case "select":
            return document.getElementById(id).options[document.getElementById(id).selectedIndex].value;
        case "map/addable":
            return null;
        default:
            return null;
    }
}

/**
 * id( 또는 name ) 값을 통해 모든 element를 습득한다.
 * @param id 탐색시 사용할 id( 또는 name ) 값.
 * @returns {*[]} 습득한 모든 element.
 */
function getAllNodeUsingIdAndName(id) {
    return Array.prototype.slice.call(
        // tag의 id attribute가 입력ID와 같은 모든 element를 습득.
        document.querySelectorAll('[id="' + id + '"]')
    ).concat(
        Array.prototype.slice.call(
            // tag의 name attribute가 입력ID와 같은 모든 element를 습득.
            document.querySelectorAll('[name="' + id + '"]')
        )
    );
}

/**
 * 임의의 object가 null 또는 길이가 0인 List, Map 등인지를 확인한다.
 * @param target 임의의 object.
 * @returns {boolean} null 또는 길이가 0인지의 여부.
 */
function isNullOrEmpty(target) {
    return target === null || target === undefined || target.length === 0;
}

/**
 * 임의의 element로부터 거슬러 올라가서 name인 element를 습득한다.
 * @param firstElement 임의의 element.
 * @param name 습득할 대상의 name attribute 값.
 * @returns {(() => (Node | null))|ActiveX.IXMLDOMNode|(Node & ParentNode)|null} 습득한 값.
 */
function getRootByName(firstElement, name) {
    // 최상위 element는 입력받은 임의의 element라고 가정한다.
    let root = firstElement;

    while (true) {

        // 최상위 element가 null이면 발견하지 못했다고 가정하고 null을 반환.
        if (root === null) {
            alert("Parent div doesn't exists.");
            return null;
        }

        // 최상위 element의 name attribute가 입력받은 name 값과 같다면 탐색 종료.
        if (root.name === name) {
            break;
        }

        // 이번 순서의 element가 최상위 element가 아니기 때문에, 이번 순서의 element의 parent node를 대입.
        root = root.parentNode;
    }

    return root;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Customize의 Radio Group 관련

// page load 후, 초기화 함수를 호출할 수 있도록 callback을 등록.
window.addEventListener("load", initialization);

/**
 * Page Load 후 호출되는 초기화 callback 함수.
 */
function initRadioGroupOfCustomize() {

    // Customize의 Reclaim Policy Radio Group의 값을 초기화.
    document.getElementsByName(
        document.getElementById("reclame-policy-name-hidden").value
    )[0].checked = true;

    // Customize의 Volume Binding Mode Radio Group의 값을 초기화.
    document.getElementsByName(
        document.getElementById("volume-binding-mode-name-hidden").value
    )[0].checked = true;
}