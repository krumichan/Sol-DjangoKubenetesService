from common import constants as CC
from common.error.dummy import DummyError
from core.example.rancher_caller_example import RancherCallerExample

from .templates.filter_executor import FilterExecutor
from .templates.list_executor import ListExecutor
from .templates.refresh_executor import RefreshExecutor


class TemplatesService:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(TemplatesService, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            cls._me.__caller = RancherCallerExample.call()
            cls._me.__lister = ListExecutor()
            cls._me.__refresher = RefreshExecutor()
            cls._me.__filterer = FilterExecutor()

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

    def _list_multi_cluster_application_templates(self, options):
        """
        모든 Multi-Cluster Application의 Templates를 반환한다.\n
        :param options: Templates API 호출시의 options.
        :return: 모든 Multi-Cluster Applications의 Templates.
        """

        apps_templates_dictionary = self._me.__caller.list_multi_cluster_application_templates(options)

        model = self._me.__lister.multi_cluster_application_templates(apps_templates_dictionary)

        return model

    def _refresh_multi_cluster_application_templates(self, options):
        """
        모든 Catalog를 refresh한다.\n
        여기서의 모든에 해당하는 것은, Project Catalog, Cluster Catalog, Global Catalog가 있다.\n
        :param options: refresh API를 수행할 시의 option.
        :return: refresh 결과.
        """

        project_catalogs_refresh_result = self._me.__caller.refresh_project_catalogs(options)

        cluster_catalogs_refresh_result = self._me.__caller.refresh_cluster_catalogs(options)

        catalogs_refresh_result = self._me.__caller.refresh_catalogs(options)

        model = self._me.__refresher.refresh_multi_cluster_applications(
            project_catalogs_refresh_result
            , cluster_catalogs_refresh_result
            , catalogs_refresh_result
        )

        return model

    def _filter_by_category_multi_cluster_application_templates(self, options):
        """
        임의의 Catalog 명을 기반으로 Filtering을 수행한다.\n
        :param options: Filterling을 수행할 시의 options.
        :return: Filtering 결과.
        """

        apps_templates_dictionary = self._me.__caller.list_multi_cluster_application_templates()

        model = self._me.__filterer.filter_multi_cluster_application_templates(
            apps_templates_dictionary, options)

        return model

