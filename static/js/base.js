$(document).ready(function() {

    // LEFT CSS 설정
    const nowLocation = window.location.href.split("/");
});

/**
 * 모든 ajax 요청을 수행하기 전에, ajax 요청에 대한 default 설정을 수행한다.
 */
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", generateToken("CSRF"));
        }
    }
})

/**
 * CSFR Token을 요구하는지 확인하는 함수.
 * @param method 검증할 HTTP Method.
 * @returns {boolean} 요구여부.
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/**
 * cookie로부터 원하는 key에 대응하는 값을 추출한다.
 * @param tokenKey 원하는 값에 대한 key.
 * @returns {string|null} 습득 결과. ( 없거나, 부정의 값인 경우 null을 반환. )
 */
function generateToken(tokenKey) {
    let result = null;

    // parameter를 제대로 넣어줬는지 확인.
    if (!!!tokenKey || tokenKey === "") {
        alert("Invalid parameters.");
        return result;
    }

    // cookie가 제대로 있는지 확인.
    const cookie = document.cookie;
    if (!!!cookie || cookie !== "") {
        alert("Cookie doesn't exists.");
        return result;
    }

    // cookie 값들을 token 단위로 분리.
    const cookieTokens = document.cookie.split(";");

    // cookie token 들을 순회.
    for (const token of cookieTokens) {

        // 하나의 token을 key-value로 분리.
        const keyValue = token.trim().split("=");

        // key-value 구조가 아니라면 부정한 값으로 판단.
        if (keyValue.length !== 2) {
            alert("Invalid Cookie..." + "\n" + "cookie:" + cookie);
            return result;
        }

        // key가 호출자가 원하는 값이라면, 해당 key에 대응하는 value를 반환.
        if (keyValue[0] === tokenKey) {
            result = decodeURIComponent(keyValue[1]);
            break;
        }
    }

    if (!!!result) {
        // 호출자가 원하는 값과 일치하는 값이 cookie에 없는 경우.
        alert("[" + tokenKey + "] doesn't exists...");
        return result;
    }

    return result;
}

/**
 * post 전송.
 * @param functionName post 대상 함수명.
 * @param divName 결과를 출력할 div의 id.
 * @param payload post 전송시 같이 전송할 data.
 * @param canGetResult post 후의 결과를 습득할지 결정.
 * @returns {null} 결과 습득시, 결과를 반환.
 */
function post(functionName, divName, payload={}, canGetResult=false) {
    let response = null;

    $.ajax({
        type: "POST"
        , url: "{% url '" + functionName +"' %}"
        , async: !canGetResult
        , headers: {
            'X-CSRFToken': generateToken("CSRF")
        }
        , data: JSON.stringify(payload)
        , success: function(data) {
            response = data;
            $("#" + divName).html(response);
        }, complete: function(data) {
            // do nothings...
        }, error: function(request, error) {
            const message = "code: " + request.status + "\n"
                + "message: " + request.responseText + "\n"
                + "error: " + error;
            alert(message);
        }
    });

    return response;
}