from common import constants as CC
from common.error.dummy import DummyError
from core.example.rancher_caller_example import RancherCallerExample

from .multiclusterapps.delete_executor import DeleteExecutor
from .multiclusterapps.list_executor import ListExecutor


class MultiClusterAppsService:
    """
    Multi-Cluster Application Page에 관련한 모든 API Call에 대한 Service를 제공하는 클래스.
    """

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(MultiClusterAppsService, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            cls._me.__caller = RancherCallerExample.call()
            cls._me.__lister = ListExecutor()
            cls._me.__deleter = DeleteExecutor()

        return cls._me

    def request_mapping(self, func_name, payload):

        # 받은 function 이름을 protected 이름으로 변경.
        prot_name = "_" + func_name
        if not hasattr(self._me, prot_name):
            raise Exception(self._me.__class__.__name__ + " object has no attribute '" + func_name + "'")

        # protected 처리된 function을 호출.
        reflect_func = getattr(self._me, prot_name)

        # 인수로 받은 option 값이 없는 경우.
        if payload is None:
            raise Exception("[payload] does not exist.")

        # 현재 Rancher API의 Schema가 cluster에 맞추어져 있는지 확인.
        self._me.__caller.evaluate_schema_if_invalid_do_update("global", "")

        # option 습득.
        options = {"me": "true"} \
            if CC.OPTIONS_STRING not in payload \
            else payload[CC.OPTIONS_STRING]

        return reflect_func(options)

    def _list_multi_cluster_applications(self, options):
        """
        views 에서의 실제 Multi-Cluster Application list 호출에 대한 Business Logic 을 이곳에서 처리한다.\n
        TODO: 찾기 기능 추가시, AppService의 인수로, 찾기에 들어온 문자를 option으로 넣어주서야 한다.\n
        :param options: 탐색시의 option 내용
        :return: Multi-Cluster Application list
        """

        model = self._me.__lister.list_applications(
            self._me.__caller.list_multi_cluster_applications(options)
            , self._me.__caller.list_projects()
            , self._me.__caller.list_clusters()
            , self._me.__caller.list_multi_cluster_application_templates()
        )

        return model

    def _delete_multi_cluster_appliction(self, options):
        """
        Options 정보에 해당하는 Multi-Cluster Application을 삭제한다.\n
        :param options: Multi-Cluster Application 삭제시 필요한 Data
        :return: 삭제 결과
        """

        delete_result = self._me.__caller.delete_multi_cluster_application(options)

        model = self._me.__deleter.delete_application(delete_result)

        return model
