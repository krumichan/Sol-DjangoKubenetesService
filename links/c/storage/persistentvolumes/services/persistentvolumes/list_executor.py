import json

from common.error.dummy import DummyError
from common.utility.json import JsonUtility

from . import constants as PersistentVolumesConstant


class ListExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(ListExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    def list_persistent_volumes(self, persistent_volumes):
        """
        API로부터 얻은 모든 Persistent Volumes를 View에 맞추어서 가공하여 반환한다.\n
        :param persistent_volumes: API로부터 얻은 모든 Persistent Volumes.
        :return: 가공 결과.
        """

        result_persistent_volumes = []

        # RestObject 를 dictionary 객체로 변환
        try:
            dict_persistent_volumes = JsonUtility.call().to_dictionary(persistent_volumes)
        except DummyError as de:
            raise de

        # dictionary로부터 data를 추출
        try:
            persistent_volumes_mapping = dict_persistent_volumes['data']
        except KeyError:
            raise DummyError("persistent_volumes['data'] row is not eixsts. please check your data.")

        for persistent_volume in persistent_volumes_mapping:
            can_write_persistent_volume = persistent_volume.copy()

            # 해당 persistent volume의 삭제 가능 여부 flag setting.
            can_write_persistent_volume[PersistentVolumesConstant.CAN_REMOVE] = self.__can_remove(persistent_volume)

            try:
                # Persistent Volume의 Source 를 얻음.
                can_write_persistent_volume[PersistentVolumesConstant.SOURCE] = self.__getSource(persistent_volume)

            # source가 존재하지 않을 경우 무시.
            except Exception as e:
                raise e

            result_persistent_volumes.append(can_write_persistent_volume.copy())

        return result_persistent_volumes

    def __can_remove(self, persistent_volume):
        """
        임의의 Persistent volume의 삭제 가능 여부를 반환한다.\n
        :param persistent_volume: 임의의 Persistent Volume.
        :return: 삭제 가능 여부.
        """

        return self.__remove_exists(persistent_volume) and not self.__state_bound(persistent_volume)

    def __remove_exists(self, persistent_volume):
        """
        임의의 Persistent Volume으로부터 remove link가 있는지의 여부를 반환한다.\n
        :param persistent_volume: 임의의 Persistent Volume.
        :return: remove link의 존재 여부.
        """

        # static 경고 제거용.
        dummy = self._me

        # remove link가 있는지 확인.
        try:
            return persistent_volume[PersistentVolumesConstant.LINKS][PersistentVolumesConstant.REMOVE] is not None

        # links 또는 remove가 없는 경우.
        except KeyError:
            return False

    def __state_bound(self, persistent_volume):
        """
        임의의 Persistent volume의 status가 bound인지의 여부를 반환한다.\n
        :param persistent_volume: 임의의 Persistent Volume.
        :return: status의 bound 여부.
        """

        # static 경고 제거용.
        dummy = self._me

        return persistent_volume[PersistentVolumesConstant.STATE] == PersistentVolumesConstant.STATE_BOUND

    def __getSource(self, persistent_volume):
        """
        임의의 Persistent volume의 정보를 기반으로 source를 파악하여 source field를 생성 및 값을 입력한다.\n
        :param persistent_volume: 임의의 Persistent Volume.
        :return 해당 persistent volume에 맞는 title.
        """

        # static 경고 제거용.
        dummy = self._me

        VOLUME_SOURCES = PersistentVolumesConstant.VOLUME_SOURCE_DICTIONARY[PersistentVolumesConstant.VOLUME_SOURCE]
        for value in VOLUME_SOURCES.values():
            # field 명을 습득한다.
            field_name = value[PersistentVolumesConstant.FIELD]

            # 해당 field가 존재하므로 field의 title을 반환.
            if field_name in persistent_volume and value[PersistentVolumesConstant.SUPPORTED]:
                return value[PersistentVolumesConstant.TITLE]

        # 어느 field에도 해당하는 내용이 없을 경우, DummyException을 발생시킴.
        raise DummyError("invalid data --- source does not exists." + "\n" + "data:"
                         + json.dumps(persistent_volume))
