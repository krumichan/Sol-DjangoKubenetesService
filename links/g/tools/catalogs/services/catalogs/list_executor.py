import copy

from common.error.dummy import DummyError
from common.utility.json import JsonUtility

from links.g.tools.catalogs.services.catalogs import constants as CatalogConstant


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

    def list_catalogs(self, catalogs):
        """
        모든 catalog 를 불러온다.\n
        :param catalogs: API 로부터 얻은 모든 catalog
        :return: 가공 처리가 완료된 catalog list
        """

        # static 경고 방지용.
        dummy = self._me

        result_catalogs = []

        # RestObject 를 dictionary 객체로 변환
        try:
            dict_catalogs = JsonUtility.call().to_dictionary(catalogs)
        except DummyError as de:
            raise de

        # dictionary 로부터 'data' dictionary 를 추출.
        try:
            catalogs_mapping = dict_catalogs['data']
        except KeyError:
            raise DummyError("catalogs['data'] row is not eixsts. please check your data.")

        try:
            for cata in catalogs_mapping:
                # catalog 를 복제한다.
                can_write_catalog = copy.copy(cata)

                # 해당 catalog 는 Clone 이 가능한지 여부를 넣는다.
                catalog_name = can_write_catalog[CatalogConstant.NAME_STRING]
                can_write_catalog[CatalogConstant.CAN_CLONE_STRING] \
                    = not CatalogConstant.isDefaultCatalog(catalog_name)

                # catalog 에 scope 를 추가한다.
                can_write_catalog[CatalogConstant.SCOPE] = CatalogConstant.CATALOG_SCOPE

                # refactoring 이 완료된 catalog 를 결과 list 에 추가한다.
                result_catalogs.append(can_write_catalog.copy())
        except Exception as e:
            raise Exception("unknown exception...\n" + e)

        return result_catalogs
