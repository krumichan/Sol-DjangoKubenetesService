class CreateExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(CreateExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    def create_cluster(self, create_cluster_result, create_cluster_registration_token_result):

        # static 경고 제거용.
        dummy = self._me

        return create_cluster_result
