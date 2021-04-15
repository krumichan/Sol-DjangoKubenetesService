from common import constants as CC
from common.error.dummy import DummyError
from core.example.rancher_caller_example import RancherCallerExample

from .catalogs.delete_catalogs_executor import DeleteCatalogsExecutor
from .catalogs.create_executor import CreateExecutor
from .catalogs.default_executor import DefaultExecutor
from .catalogs.enabled_executor import EnabledExecutor
from .catalogs.edit_executor import EditExecutor
from .catalogs.clone_executor import CloneExecutor
from .catalogs.delete_executor import DeleteExecutor
from .catalogs.refresh_executor import RefreshExecutor
from .catalogs.list_executor import ListExecutor


class CatalogsService:
    """
    Catalog Page에 관련한 모든 API Call에 대한 Service를 제공하는 클래스.
    """

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(CatalogsService, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            cls._me.__caller = RancherCallerExample.call()
            cls._me.__deleters = DeleteCatalogsExecutor()
            cls._me.__creater = CreateExecutor()
            cls._me.__defaulter = DefaultExecutor()
            cls._me.__enableder = EnabledExecutor()
            cls._me.__editor = EditExecutor()
            cls._me.__cloner = CloneExecutor()
            cls._me.__deleter = DeleteExecutor()
            cls._me.__refresher = RefreshExecutor()
            cls._me.__lister = ListExecutor()

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

    def _list_catalogs(self, options):
        """
        views 에서의 실제 Catalog list 호출에 대한 Business Logic 을 이곳에서 처리한다.\n
        :param options: 탐색시의 option 내용
        :return: Catalog list
        """

        # Rancher API를 통하여 Catalog List 습득
        catalog_dictionary = self._me.__caller.list_catalogs(options)

        # Rancher API로부터 얻은 Catalog List를 View에 맞게 가공한다.
        model = self._me.__lister.list_catalogs(catalog_dictionary)

        # Rancher API로부터 얻어온 Catalog 들 중에서,
        # 아직 생성되지 않은 Default Catalog 를 얻어온다.
        default_catalog_dictionary = self._me.__list_default_catalogs(model)

        # View 에 반환할 catalogs 에 filtering 한 default catalog 를 추가한다.
        model.extend(default_catalog_dictionary)

        return model

    def _delete_catalogs(self, options):
        """
        names 정보에 해당하는 Catalogs를 삭제한다.
        :param options: Client로부터 받은 option data
        :return: 삭제 결과
        """

        names = options[CC.OPTIONS_STRING]

        delete_result = []

        for name in names:
            opts = {"name": name}
            # Rancher API를 통하여 Catalog Delete 후의 결과를 습득
            delete_result.append(self._me.__caller.delete_catalog(opts).copy())

        # Catalog Delete 결과에 추가로 작업을 수정 후 습득
        model = self._me.__deleters.delete_catalogs(delete_result)

        return model

    def _create_catalog(self, options):
        """
        Options 정보에 의거하여 Catalog 를 생성한다.\n
        :param options: Catalog 생성시 필요한 Data
        :return: 생성 결과의 Catalog
        """

        # Rancher API를 통하여 Catalog Create 후의 결과를 습득
        create_result = self._me.__caller.create_catalog(options)

        # Catalog Create 결과에 추가로 작업을 수정 후 습득
        model = self._me.__creater.create_catalog(create_result)

        return model

    def _edit_catalog(self, options):
        """
        Options 정보에 의거하여 Catalog 를 갱신한다.\n
        :param options: Catalog 갱신시 필요한 Data
        :return: 갱신 결과의 Catalog
        """

        # Rancher API를 통하여 Catalog Edit 후의 결과를 습득
        edit_result = self._me.__caller.update_catalog(options)

        # Catalog Edit 결과에 추가로 작업을 수정 후 습득
        model = self._me.__editor.edit_catalog(edit_result)

        return model

    def _clone_catalog(self, options):
        """
        Options 정보에 의거하여 Catalog 를 복제한다.\n
        :param options: Catalog 생성시 필요한 Data
        :return: 생성 결과의 Catalog
        """

        # Rancher API를 통하여 Catalog Clone 후의 결과를 습득
        # Clone과 Create는 사실상 같은 동작을 수행하기 때문에 create API를 사용
        clone_result = self._me.__caller.create_catalog(options)

        # Catalog Clone 결과에 추가로 작업을 수정 후 습득
        model = self._me.__cloner.clone_catalog(clone_result)

        return model

    def _delete_catalog(self, options):
        """
        Options 정보에 해당하는 Catalog를 삭제한다.
        :param options: Catalog 삭제시 필요한 Data
        :return: 삭제 결과
        """

        # Rancher API를 통하여 Catalog Delete 후의 결과를 습득
        delete_result = self._me.__caller.delete_catalog(options)

        # Catalog Delete 결과에 추가로 작업을 수정 후 습득
        model = self._me.__deleter.delete_catalog(delete_result)

        return model

    def _enabled_catalog(self, options):
        """
        default Catalog 중에서 임의의 Catalog를 default data를 기반으로 생성한다.\n
        :param options: 임의의 Catalog를 지칭하는 data 및 create API 호출시의 options.
        :return: default Catalog 생성 결과.
        """

        name = options["name"]

        default_catalog_options = self._me.__enableder.get_default_catalog_options_by_name(name)

        enabled_result = self._me.__caller.create_catalog(default_catalog_options)

        model = self._me.__enableder.enabled_catalog(enabled_result)

        return model

    def _refresh_catalog(self, options):
        """
        Options 정보에 해당하는 Catalog를 Refresh한다.
        :param options: Catalog Refresh시 필요한 Data
        :return: Refresh 결과
        """

        # Rancher API를 통하여 Catalog Refresh 후의 결과를 습득
        refresh_result = self._me.__caller.refresh_catalog(options)

        # Catalog Refresh 결과에 추가로 작업을 수정 후 습득
        model = self._me.__refresher.refresh_catalog(refresh_result)

        return model

    def __list_default_catalogs(self, catalogs):
        """
        아직 생성되지 않은, 기본적으로 제공되어질 Catalog에 대한 list를 습득힌다.\n
        :param catalogs: 현재 생성되어진 catalog list
        :return: 생성되지 않은 Default Catalog List
        """

        uncreated_default_catalogs = self._me.__defaulter.list_default_catalogs(
            catalogs
        )

        return uncreated_default_catalogs
