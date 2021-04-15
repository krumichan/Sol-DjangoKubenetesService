# Catalog Key 관련 Constant
SCOPE = 'scope'
CAN_CLONE_STRING = 'canClone'

# Catalog Value 관련 Constant
CATALOG_SCOPE = 'Global'

# default catalog 에 대한 name 과 url 의 상수 정의
LIBRARY_NAME = 'library'
LIBRARY_URL = 'https://git.rancher.io/charts'

SYSTEM_LIBRARY_NAME = 'system-library'
SYSTEM_LIBRARY_URL = 'https://git.rancher.io/system-charts'

HELM_NAME = 'helm'
HELM_URL = 'https://kubernetes-charts.storage.googleapis.com/'

HELM_INCUBATOR_NAME = 'helm-incubator'
HELM_INCUBATOR_URL = 'https://kubernetes-charts-incubator.storage.googleapis.com/'

HELM_3_LIBRARY_NAME = 'helm3-library'
HELM_3_LIBRARY_URL = 'https://git.rancher.io/helm3-charts'

ALIBABA_APP_HUB_NAME = 'alibaba-app-hub'
ALIBABA_APP_HUB_URL = 'https://apphub.aliyuncs.com'

# default catalog 에 대한 branch, type, kind, state 상수 정의
# 'state'의 경우, catalog 가 아직 추가되지 않았을 경우에 입력할 default value 가 된다.
DEFAULT_BRANCH = 'master'
DEFAULT_TYPE = 'catalog'
DEFAULT_KIND = 'helm'
DEFAULT_STATE = 'Disabled'

# default catalog 를 자동으로 추가하기 위한 정보.
# name string 의 경우, catalog 습득 API 를 호출하였을 때, 실제 catalog name 이 정의되어 있는 부분의 key 값과 같아야한다.
# ⇒ name string 을 기반으로 현재 활성화된 catalog 들에 default catalog 가 포함되어 있는지를 판단하기 때문이다.
#   포함되어 있지 않을 경우만 default catalog iterator 를 통해서 row 를 추가한다.
TYPE_STRING = 'type'
NAME_STRING = 'name'
URL_STRING = 'url'
BRANCH_STRING = 'branch'
KIND_STRING = 'kind'
STATE_STRING = 'state'
AUTO_DEFAULT_CATALOG_ITERATOR = [
    {
        TYPE_STRING: DEFAULT_TYPE
        , SCOPE: CATALOG_SCOPE
        , NAME_STRING: LIBRARY_NAME
        , URL_STRING: LIBRARY_URL
        , BRANCH_STRING: DEFAULT_BRANCH
        , KIND_STRING: DEFAULT_KIND
        , STATE_STRING: DEFAULT_STATE
    }
    , {
        TYPE_STRING: DEFAULT_TYPE
        , SCOPE: CATALOG_SCOPE
        , NAME_STRING: SYSTEM_LIBRARY_NAME
        , URL_STRING: SYSTEM_LIBRARY_URL
        , BRANCH_STRING: DEFAULT_BRANCH
        , KIND_STRING: DEFAULT_KIND
        , STATE_STRING: DEFAULT_STATE
    }
    , {
        TYPE_STRING: DEFAULT_TYPE
        , SCOPE: CATALOG_SCOPE
        , NAME_STRING: HELM_NAME
        , URL_STRING: HELM_URL
        , BRANCH_STRING: DEFAULT_BRANCH
        , KIND_STRING: DEFAULT_KIND
        , STATE_STRING: DEFAULT_STATE
    }
    , {
        TYPE_STRING: DEFAULT_TYPE
        , SCOPE: CATALOG_SCOPE
        , NAME_STRING: HELM_INCUBATOR_NAME
        , URL_STRING: HELM_INCUBATOR_URL
        , BRANCH_STRING: DEFAULT_BRANCH
        , KIND_STRING: DEFAULT_KIND
        , STATE_STRING: DEFAULT_STATE
    }
    , {
        TYPE_STRING: DEFAULT_TYPE
        , SCOPE: CATALOG_SCOPE
        , NAME_STRING: HELM_3_LIBRARY_NAME
        , URL_STRING: HELM_3_LIBRARY_URL
        , BRANCH_STRING: DEFAULT_BRANCH
        , KIND_STRING: DEFAULT_KIND
        , STATE_STRING: DEFAULT_STATE
    }
    , {
        TYPE_STRING: DEFAULT_TYPE
        , SCOPE: CATALOG_SCOPE
        , NAME_STRING: ALIBABA_APP_HUB_NAME
        , URL_STRING: ALIBABA_APP_HUB_URL
        , BRANCH_STRING: DEFAULT_BRANCH
        , KIND_STRING: DEFAULT_KIND
        , STATE_STRING: DEFAULT_STATE
    }
    ,
]


def isDefaultCatalog(name):
    """
    인수의 name 에 해당하는 Catalog가 Default Catalog인지 확인한다.\n
    :param name: Default Catalog 인지를 확인할 Catalog의 name
    :return: Default Catalog 인지의 여부
    """

    for default_catalog in AUTO_DEFAULT_CATALOG_ITERATOR:
        if default_catalog[NAME_STRING] == name:
            return True

    return False
