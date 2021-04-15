from links.g.tools.catalogs.services.catalogs import constants as CatalogConstant


class EnabledExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(EnabledExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    def get_default_catalog_options_by_name(self, name):
        # static 경고 제거용.
        dummy = self._me

        for default_catalog in CatalogConstant.AUTO_DEFAULT_CATALOG_ITERATOR:
            if name == default_catalog[CatalogConstant.NAME_STRING]:
                default_catalog.pop(CatalogConstant.STATE_STRING, default_catalog)
                return default_catalog

        return None

    def enabled_catalog(self, enabled_result):
        # static 경고 제거용.
        dummy = self._me

        return enabled_result
