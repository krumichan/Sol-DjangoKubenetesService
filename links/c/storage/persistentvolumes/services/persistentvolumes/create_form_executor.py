import json

from common.error.dummy import DummyError
from common.utility.json import JsonUtility

from . import constants as PersistentVolumeConstant


class CreateFormExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(CreateFormExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    def add_form_persistent_volume(self, storage_classes):

        # 원본 data의 변동을 막기 위해 임시로 storage class dictionary를 복사한다.
        storage_classes_template_dict = PersistentVolumeConstant.VOLUME_SOURCE_DICTIONARY[
            PersistentVolumeConstant.VOLUME_SOURCE].copy()

        result_view_write = {
            PersistentVolumeConstant.TITLE: "Add Persistent Volume"
            , PersistentVolumeConstant.VOLUME_SOURCES: self._me.__remove_unsupported(storage_classes_template_dict)
            , PersistentVolumeConstant.VOLUME_SOURCES_STRING: json.dumps(
                self._me.__remove_unsupported(storage_classes_template_dict))
            , PersistentVolumeConstant.SELECTOR_OPERATOR: json.dumps(self._me.__get_volume_node_selector_operator())
            , PersistentVolumeConstant.ACCESS_MODES: PersistentVolumeConstant.FORM_ACCESS_MODES
        }

        # RestObject 를 dictionary 객체로 변환
        try:
            dict_storage_classes = JsonUtility.call().to_dictionary(storage_classes)
        except DummyError as de:
            raise de

        # dictionary 로부터 'data' dictionary를 추출.
        try:
            storage_classes_mapping = dict_storage_classes['data']
        except KeyError:
            raise DummyError("storageClass['data'] row is not eixsts. please check your data.")

        result_view_write[PersistentVolumeConstant.STORAGE_CLASSES] = \
            self._me.__get_all_storage_class_id(storage_classes_mapping)

        return result_view_write

    def __remove_unsupported(self, storage_classes_template_dict):
        """
        모든 Storage Class 중에 지원되지 않는 Storage Class를 dictionary로부터 지운다.\n
        :param storage_classes_template_dict storage classes template.
        :return: 지원되지 않는 Storage Class 를 지운 dictionary
        """

        # static 경고 제거용.
        dummy = self._me

        # foreach 동작중, 동시성 수정( Concurrent Modification )을 방지하기 위해 결과 dictionary를 새로 생성.
        result_dict = storage_classes_template_dict.copy()

        # Storage Class 순회.
        for key, value in storage_classes_template_dict.items():

            # supperted element가 없거나, supported가 false인 경우, 제외시킨다.
            if PersistentVolumeConstant.SUPPORTED not in value or not value[PersistentVolumeConstant.SUPPORTED]:
                del result_dict[key]

        return result_dict

    def __get_volume_node_selector_operator(self):
        # static 경고 제거용.
        dummy = self._me

        return PersistentVolumeConstant.VOLUME_NODE_SELECTOR_OPERATOR

    def __get_all_storage_class_id(self, storage_classes):
        # static 경고 제거용.
        dummy = self._me

        storage_classes_list = storage_classes.copy()

        # for storage_class in storage_classes:
        #     try:
        #         storage_classes_list.append(storage_class.copy())
        #     except KeyError:
        #         pass

        return storage_classes_list
