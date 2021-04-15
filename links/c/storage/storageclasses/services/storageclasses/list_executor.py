import json

from common.utility.json import JsonUtility
from common.error.dummy import DummyError

from links.c.storage.storageclasses.services.storageclasses import constants as StorageClassesConstant


class ListExecutor:

    def __new__(cls):

        if not hasattr(cls, '_me'):
            # instance 생성
            cls._me = super(ListExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            
        return cls._me
    
    def list_storage_classes(self, storage_classes):
        """
        API로부터 얻은 Storage Classes를 View에 맞게 가공하여 반환한다.\n
        :param storage_classes: API로부터 얻은 Storage Classes.
        :return: 가공된 Storage Classes List.
        """
        
        result_storage_classes = []
        
        # RestObject를 dictionary 객체로 변환
        try:
            dict_storage_classes = JsonUtility.call().to_dictionary(storage_classes)
        except DummyError as de:
            raise de

        try:
            storage_classes_mapping = dict_storage_classes['data']
        except KeyError:
            raise DummyError("persistent_volumes['data'] row is not eixsts. please check your data.")

        for storage_class in storage_classes_mapping:
            can_write_storage_class = storage_class.copy()

            # storage class의 상태를 active로 설정. (default)
            # TODO: 추후 화면 출력 Table을 Template화 하면, 상태를 넣을 필요가 있기 때문에 넣어준다. ( 사실 상태가 존재하지 않음. )
            can_write_storage_class[StorageClassesConstant.STATE_STRING] = StorageClassesConstant.DEFAULT_STATE

            # 화면에 출력할 title을 습득.
            can_write_storage_class[StorageClassesConstant.PROVISIONER] = self.__get_provisioner(storage_class)

            result_storage_classes.append(can_write_storage_class.copy())

        return result_storage_classes

    def __get_provisioner(self, storage_class):
        """
        API로부터 얻은 data 중, provisioner에 해당하는 title을 습득한다.\n
        :param storage_class: provisioner를 추출할 API로부터 얻은 data.
        :return: 습득한 title.
        """

        # static 경고 제거용.
        dummy = self._me

        provisioner = storage_class[StorageClassesConstant.PROVISIONER]

        STORAGE_CLASSES = StorageClassesConstant.STORAGE_CLASS_DICTIONARY[StorageClassesConstant.STORAGE_CLASS]
        for one_class in STORAGE_CLASSES.values():

            # provisioner 값을 기반으로 title 을 반환한다.
            if one_class[StorageClassesConstant.PROVISIONER] == provisioner:
                return one_class[StorageClassesConstant.TITLE]

        # 어느 field에도 해당하는 내용이 없을 경우, DummyEvolume)xception을 발생시킴.
        raise DummyError("invalid data --- provisioner does not exists." + "\n" + "data:"
                         + json.dumps(storage_class))
