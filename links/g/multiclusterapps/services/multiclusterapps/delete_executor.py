
class DeleteExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(DeleteExecutor, cls).__new__(cls)

        return cls._me

    def delete_application(self, delete_result):
        """
        Multi-Cluster Application의 삭제 후의 결과를 가공하여 반환한다.\n
        :return: 가공 결과
        """

        # static 경고 제거용.
        dummy = self._me

        return delete_result
