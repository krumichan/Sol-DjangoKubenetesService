import json

from links.c.storage.storageclasses.services.storageclasses import constants as StorageClassesConstant


class CreateFormExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, "_me"):
            # instance 생성.
            cls._me = super(CreateFormExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    def add_form_storage_class(self):

        # static 경고 방지용.
        dummy = self._me

        # 원본 data의 변동을 막기 위해 임시로 storage classes dictionary를 복사한다.
        storage_classes_template_dict = StorageClassesConstant.STORAGE_CLASS_DICTIONARY[
            StorageClassesConstant.STORAGE_CLASS].copy()

        result_add_form = {
            "cruStorageClass": StorageClassesConstant.CRU_STORAGE_CLASS
            , StorageClassesConstant.STORAGE_CLASS: self._me.__remove_unsupported(storage_classes_template_dict)
            , StorageClassesConstant.STORAGE_CLASS_STRING: json.dumps(
                self._me.__remove_unsupported(storage_classes_template_dict))
        }

        return result_add_form

    def __remove_unsupported(self, storage_classes_template_dict):
        """
        모든 Storage Class 중에 지원되지 않는 Storage Class를 dictionary로부터 지운다.\n
        :param storage_classes_template_dict storage classes template.
        :return: 지원되지 않는 Storage Class 를 지운 dictionary
        """

        # static 경고 제거용.
        dummy = self._me

        # foreach 작동중, 동시성 수정( Concurrent Modification )을 방지하기 위해 결과 dictionary를 복사 생성.
        result_dict = storage_classes_template_dict.copy()

        # Storage Class Template 순회.
        for key, value in storage_classes_template_dict.items():

            # supported field가 없거나, supported가 false인 storage class는 result dictionary로부터 제거한다.
            if StorageClassesConstant.SUPPORTED not in value or not value[StorageClassesConstant.SUPPORTED]:
                del result_dict[key]

        return result_dict
