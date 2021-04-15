from common import constants as CC
from common.error.dummy import DummyError
from common.utility.json import JsonUtility
from core.example.rancher_caller_example import RancherCallerExample

from .clusters.restore_snapshot_executor import RestoreSnapshotExecutor


class ClustersService:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(ClustersService, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            cls._me.__caller = RancherCallerExample()
            cls._me.__restorer = RestoreSnapshotExecutor()

        return cls._me

    def request_mapping(self, func_name, payload):

        # 받은 function 이름을 protected 이름으로 변경.
        prot_name = "_" + func_name
        if not hasattr(self._me, prot_name):
            raise Exception(self._me.__class__.__name__ + " object has no attribute '" + func_name + "'")

        # protected 처리된 function을 호출.
        reflect_func = getattr(self._me, prot_name)

        # 인수로 받은 option 값이 없는 경우.
        if payload is None:
            raise Exception("[payload] does not exist.")

        # 현재 Rancher API의 Schema가 cluster에 맞추어져 있는지 확인.
        self._me.__caller.evaluate_schema_if_invalid_do_update("global", "")

        # option 습득.
        options = {"me": "true"} \
            if CC.OPTIONS_STRING not in payload \
            else payload[CC.OPTIONS_STRING]

        return reflect_func(options)

    def _delete_clusters(self, options):
        if CC.NAMES_STRING not in options or not options[CC.NAMES_STRING]:
            raise Exception("Delete API require names attributes." + "\n" + "options:" + str(options))

        model = []
        names = options[CC.NAMES_STRING]

        for name in names.split(CC.URL_WILDCARD):
            name = name.strip()

            # cluster name을 통해 cluster id를 습득.
            target_cluster = self._me.__caller.list_clusters({CC.RANCHER_KEY_NAME: name})

            # RestObject를 dictionary type으로 변환.
            target_cluster_dict = JsonUtility().to_dictionary(target_cluster)

            # cluster id 추출( 실제 위에서 얻은 결과는 row가 하나인 list로 이루어져 있음 ).
            target_cluster_id = target_cluster_dict[CC.RANCHER_KEY_DATA][0][CC.RANCHER_KEY_ID]

            # cluster 삭제.
            model.append(
                self._me.__caller.delete_cluster({CC.RANCHER_KEY_ID: target_cluster_id})
            )

        return model

    def _restore_snapshot_cluster(self, options):

        # cluster id를 추출.
        backup_id = options[CC.RANCHER_KEY_ETCD_BACK_ID]
        target_cluster_id = backup_id[:backup_id.find(":")]

        restore_snapshot_result = self._me.__caller.restore_snapshot_cluster(target_cluster_id, options)

        model = self._me.__restorer.restore_snapshot_cluster(restore_snapshot_result)

        return model

    def _snapshot_now_clusters(self, options):
        if CC.NAMES_STRING not in options or not options[CC.NAMES_STRING]:
            raise Exception("Snapshot now API require names attributes." + "\n" + "options:" + str(options))

        model = []
        names = options[CC.NAMES_STRING]

        for name in names.split(CC.URL_WILDCARD):
            name = name.strip()

            # cluster name을 통해 cluster id를 습득.
            target_cluster = self._me.__caller.list_clusters({CC.RANCHER_KEY_NAME: name})

            # RestObject를 dictionary type으로 변환.
            target_cluster_dict = JsonUtility().to_dictionary(target_cluster)

            # cluster id 추출( 실제 위에서 얻은 결과는 row가 하나인 list로 이루어져 있음 ).
            target_cluster_id = target_cluster_dict[CC.RANCHER_KEY_DATA][0][CC.RANCHER_KEY_ID]

            # cluster 삭제.
            model.append(
                self._me.__caller.snapshot_cluster({CC.RANCHER_KEY_ID: target_cluster_id})
            )

        return model

    def _rotate_certificates_cluster(self, options):
        if CC.NAME_STRING not in options:
            raise Exception("Rotate certifications API require cluster 'name' attribute.")

        name = options[CC.NAME_STRING]
        del options[CC.NAME_STRING]

        # cluster name을 통해 cluster id를 습득.
        target_cluster = self._me.__caller.list_clusters({CC.RANCHER_KEY_NAME: name})

        # RestObject를 dictionary type으로 변환.
        target_cluster_dict = JsonUtility().to_dictionary(target_cluster)

        # cluster row 추출 ( 실제 위에서 얻은 결과는 row가 하나인 list로 이루어져 있음 ).
        target = target_cluster_dict[CC.RANCHER_KEY_DATA][0]

        # cluster id 추출.
        target_cluster_id = target[CC.RANCHER_KEY_ID]

        model = self._me.__caller.rotate_certificates_cluster(target_cluster_id, options)

        return model

    def _save_as_rke_templates_cluster(self, options):

        # cluster name 추출.
        name = options[CC.NAME_STRING]
        del options[CC.NAME_STRING]

        # revision 값이 없을시 값을 default 값으로 설정.
        if CC.RANCHER_KEY_CLUSTER_TEMPLATE_REVISION_NAME not in options:
            options[CC.RANCHER_KEY_CLUSTER_TEMPLATE_REVISION_NAME] = CC.RANCHER_CLUSTER_TEMPLATE_REVISION_DEFAULT

        # cluster name을 통해 cluster id 습득.
        target_cluster = self._me.__caller.list_clusters({CC.RANCHER_KEY_NAME: name})

        # RestObject를 dictionary type으로 변환.
        target_cluster_dict = JsonUtility().to_dictionary(target_cluster)

        # cluster row 추출 ( 실제 위에서 얻은 결과는 row가 하나인 list로 이루어져 있음 ).
        target = target_cluster_dict[CC.RANCHER_KEY_DATA][0]

        # 해당 cluster가 이미 cluster rke template을 가지고 있는지 확인.
        if target[CC.RANCHER_KEY_CLUSTER_TEMPLATE_ID]:
            raise Exception("[" + name + "] Cluster already has RKE Template.")

        # 현재 cluster가 active 또는 updaing 상태인지 확인.
        if target[CC.RANCHER_KEY_STATE] not in [CC.RANCHER_STATE_ACTIVE, CC.RANCHER_STATE_UPDATING]:
            raise Exception("Rotate certification can not execute to this state." + "\n"
                            + "state: " + str(target[CC.RANCHER_KEY_STATE]))

        # cluster id 추출.
        target_cluster_id = target[CC.RANCHER_KEY_ID]

        model = self._me.__caller.save_as_rke_templates_cluster(target_cluster_id, options)

        return model

    def _run_cis_scan_cluster(self, options):
        if CC.NAME_STRING not in options:
            raise Exception("Run CIS Scan API require cluster 'name' attribute.")

        name = options[CC.NAME_STRING]
        del options[CC.NAME_STRING]

        # options에 failuresOnly가 있는지 확인.
        if CC.RANCHER_KEY_FAILURES_ONLY not in options:
            options[CC.RANCHER_KEY_FAILURES_ONLY] = False

        # options에 skil이 있는지 확인.
        if CC.RANCHER_KEY_SKIP not in options:
            options[CC.RANCHER_KEY_SKIP] = None

        # cluster name을 통해 cluster id 습득.
        target_cluster = self._me.__caller.list_clusters({CC.RANCHER_KEY_NAME: name})

        # RestObject를 dictionary type으로 변환.
        target_cluster_dict = JsonUtility().to_dictionary(target_cluster)

        # cluster row 추출 ( 실제 위에서 얻은 결과는 row가 하나인 list로 이루어져 있음 ).
        target = target_cluster_dict[CC.RANCHER_KEY_DATA][0]

        # 현재 cluster가 active 상태인지 확인.
        if target[CC.RANCHER_KEY_STATE] not in [CC.RANCHER_STATE_ACTIVE]:
            raise Exception("Rotate certification can not execute to this state." + "\n"
                            + "state: " + str(target[CC.RANCHER_KEY_STATE]))

        # 현재 다른 CIS Scan이 실행되고 있는지 확인.
        if CC.RANCHER_KEY_CURRENT_CIS_RUN_NAME in target:
            raise Exception("CIS Scan is already running.")

        # cluster id 추출.
        target_cluster_id = target[CC.RANCHER_KEY_ID]

        model = self._me.__caller.run_cis_scan_cluster(target_cluster_id, options)

        return model
