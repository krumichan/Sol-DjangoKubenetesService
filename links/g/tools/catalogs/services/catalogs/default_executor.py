from links.g.tools.catalogs.services.catalogs import constants as CatalogConstant


class DefaultExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(DefaultExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    def list_default_catalogs(self, catalogs):
        """
        default catalog 를 불러오기 위한 함수.\n
        default catalog 가 이미 활성화 ( active ) 되어있는 경우,\n
        해당하는 catalog 의 load 는 생략한다.\n
        ( 기본적으로 load 되는 catalog 는 disabled 상태로 load 된다. )\n
        ⇒ disabled 상태는 실제 api 에 등록되지 않은 상태를 의미. ) \n
        :param catalogs: API 호출로부터 얻어온 catalog 목록
        :return: default catalog mapping list
        """

        default_catalogs = []

        for default_catalog in CatalogConstant.AUTO_DEFAULT_CATALOG_ITERATOR:
            catalog_name = default_catalog[CatalogConstant.NAME_STRING]

            # 이미 추가되어 있는 경우 ( active 상태 ) 생략.
            if self.__contains_by_name(catalogs, catalog_name):
                continue

            default_catalogs.append(default_catalog.copy())

        return default_catalogs

    def __contains_by_name(self, catalogs, name):
        """
        catalog 목록에 해당하는 name 의 값이 이미 포함되어 있는지를 확인하다.\n
        :param catalogs: catalog 목록
        :param name: 포함되어 있음을 판단하기 위한 name 값
        :return: 포함 여부
        """

        # static 경고 제거용.
        dummy = self._me

        for cata in catalogs:
            cata_name = cata[CatalogConstant.NAME_STRING]
            if cata_name == name:
                return True

        return False
