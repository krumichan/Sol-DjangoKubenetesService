class RestoreSnapshotExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(RestoreSnapshotExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    def restore_snapshot_cluster(self, restore_snapshot_result):
        # static 경고 제거용.
        dummy = self

        return restore_snapshot_result
