from common import constants as CC
from common.error.dummy import DummyError
from core.example.rancher_caller_example import RancherCallerExample

from .storageclasses.create_form_executor import CreateFormExecutor
from .storageclasses.list_executor import ListExecutor


class StorageClassesService:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\b
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(StorageClassesService, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            cls._me.__caller = RancherCallerExample()
            cls._me.__create_former = CreateFormExecutor()
            cls._me.__lister = ListExecutor()

        return cls._me

    def request_mapping(self, func_name, cluster_id, payload):

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
        self._me.__caller.evaluate_schema_if_invalid_do_update("cluster", cluster_id)

        # option 습득.
        options = {"me": "true"} \
            if CC.OPTIONS_STRING not in payload \
            else payload[CC.OPTIONS_STRING]

        return reflect_func(options)

    def _list_storage_classes(self, options):
        """
        모든 Storage Classes를 API로부터 습득하여, View에 맞게 가공 및 반환한다.\n
        :param options: API 호출시의 options.
        :return: 가공 결과.
        """

        storage_classes = self._me.__caller.list_storage_classes(options)

        model = self._me.__lister.list_storage_classes(storage_classes)

        return model

    def _add_form_storage_class(self):

        # static 경고 방지용.
        dummy = self._me

        model = self._me.__create_former.add_form_storage_class()

        return model

    def _add_storage_class(self, opts):

        # static 경고 방지용.
        dummy = self._me

        model = None

        return model

    def _detail_storage_class(self, opts):

        # static 경고 방지용.
        dummy = self._me

        model = None

        return model
