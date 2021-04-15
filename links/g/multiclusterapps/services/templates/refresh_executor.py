class RefreshExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(RefreshExecutor, cls).__new__(cls)

        return cls._me

    def refresh_multi_cluster_applications(self, result_projectcatalogs, result_clustercatalogs, result_catalogs):
        """
        모든 Catalog의 Refreshing 후의 결과를 가공하여 반환한다.\n
        :param result_projectcatalogs: 모든 project의 모든 Catalog의 refresh 결과.
        :param result_clustercatalogs: 모든 cluster의 모든 Catalog의 refresh 결과.
        :param result_catalogs: global의 모든 Catalog의 refersh 결과.
        :return: 모든 refresh 결과를 가공한 후의 결과.
        """
        # static 경고 제거용.
        dummy = self._me

        refactoring_results = None
        return refactoring_results
