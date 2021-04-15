from common import constants as CC
from common.share import Share
from common.utility.format import FormatUtility

mapper_path = CC.APPLICATION_ROOTDIR + CC.path.sep + Share().generator_path(__file__, CC.APPLICATION_MAPPERDIR)


def validate(request, callback, mapper, name=None, names=None, search=None):
    """
    Client로부터 받은 요청에 대한 검증을 수행한 후, 기능을 수행.\n
    :param request: Client의 요청 객체.
    :param callback: Client의 요청을 수행할 함수의 이름.
    :param mapper: callback 함수를 가지고 있는 클래스 이름.
    :param name: specific value on url.
    :param names: specific value on url.
    :param search: specific value on url.
    :return: Client의 요청 처리 결과.
    """

    # session 확인.
    check_session()

    # callback 확인.
    check_callback(callback)

    # mapper 생성.
    mapper = FormatUtility().name_to_class(path=mapper_path, class_name=mapper)()

    # mapping 함수에 넘겨줄 요소 생성.
    arguments = {
        CC.NAME_STRING: name
        , CC.NAMES_STRING: names
        , CC.SEARCH_STRING: search
        ,
    }

    return mapper.api_mapping(request=request
                              , api_name=callback
                              , filepath=__file__
                              , arguments=arguments)


def check_session():
    """
    Client의 요청의 Session이 유효한 Session인지 검사.\n
    :return: 검사 결과.
    """

    # TODO: Login Session 검증.
    return True


def check_callback(callback):
    """
    Client 요청을 수행할 함수의 이름이 유효한지를 검사.\n
    :param callback: Client 요청을 수행할 함수.
    :return: 검사 결과.
    """
    if not callback:
        raise Exception("Callback function does not exist.")

    return True
