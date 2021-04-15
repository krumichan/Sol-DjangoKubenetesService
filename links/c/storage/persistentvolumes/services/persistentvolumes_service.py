from common import constants as CC
from common.error.dummy import DummyError
from core.example.rancher_caller_example import RancherCallerExample

from .persistentvolumes.create_executor import CreateExecutor
from .persistentvolumes.create_form_executor import CreateFormExecutor
from .persistentvolumes.list_executor import ListExecutor
from .persistentvolumes.row_executor import RowExecutor


class PersistentVolumesService:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(PersistentVolumesService, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            cls._me.__caller = RancherCallerExample()
            cls._me.__creator = CreateExecutor()
            cls._me.__create_former = CreateFormExecutor()
            cls._me.__lister = ListExecutor()
            cls._me.__rower = RowExecutor()

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

    def _list_persistent_volumes(self, options):
        """
        모든 Peirsistent Volume을 API로부터 습득하여, View 에 맞게 가공 및 반환한다.\n
        :param options: API 호출시의 options.
        :return: 가공 결과.
        """

        persistent_volumes = self._me.__caller.list_persistent_volumes(options)

        model = self._me.__lister.list_persistent_volumes(persistent_volumes)

        return model

    def _add_form_persistent_volume(self, options):

        storage_classes = self._me.__caller.list_storage_classes(options)

        model = self._me.__create_former.add_form_persistent_volume(storage_classes)

        return model

    def _add_persistent_volume(self, options):

        # 현재 schema를 추출.
        current_schema = self._me.__caller.current_schema()

        # options를 persistent volume 생성 API에 맞게 수정.
        payload = self._me.__creator.generate_payload(options, current_schema)

        create_result = self._me.__caller.create_persistent_volume(payload)

        model = self._me.__creator.create_persistent_volume(create_result)

        return model

    def _detail_persistent_volume(self, options):

        # API로부터 특정 persistent volume만을 추출.
        persistent_volume = self._me.__caller.list_persistent_volumes(options)

        # 특정 persistent volume을 가공 처리.
        # 실제 결과는 1개이지만, list 형식으로 불려오게 됨.
        models = self._me.__lister.list_persistent_volumes(persistent_volume)
        if len(models) > 1:
            DummyError("Results are too many.")

        # list로부터 결과를 추출.
        model = self._me.__rower.row_persistent_volume(models[0])

        return model
