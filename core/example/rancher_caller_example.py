from .__rancher_runner_example import RancherRunnerExample


class RancherCallerExample(RancherRunnerExample):
    """
    Rancher API 호출을 제공하는 클래스
    """

    # Rancher Caller Example 의 unique instance 생성.
    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(RancherCallerExample, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            cls._me.__runner = RancherRunnerExample()

        return cls._me

    @staticmethod
    def call():
        """
        해당 class 의 unique instance를 호출한다.
        :return: unique instance
        """

        # Rancher Caller Example Class가 xxx라는 member를 소유하고 있는지 확인.
        if not hasattr(RancherCallerExample, 'me'):
            # unique instance가 존재하지 않을시, unique instance를 생성.
            RancherCallerExample.me = RancherCallerExample()

        return RancherCallerExample.me

    def evaluate_schema_if_invalid_do_update(self, url_type="global", type_id=""):
        """
        현재 Rancher Client의 Schema가 요청 API의 호출에 올바른 Schema인지 검증하고,
        올바른 Schema가 아니라면 Schema를 갱신한다.\n
        :param url_type Rancher Client의 Schema를 구성하기 위한 url type
        :param type_id: Schema 재구성시 사용되는 id
        """

        if not self._me.__runner.is_xxxxx(url_type, type_id):
            self._me.__runner.new_url_evaluate_then_reload_schema(url_type, type_id)

    def current_schema(self):
        """
        현재 구성되어 있는 Schema를 호출한다.\n
        본래의 schema의 얕은 복사 형태로 반환되며,
        수정, 추가, 삭제 등을 수행하여도 원본 Schema에는 영향이 없다.\n
        :return: 현재 구성되어 있는 Schema.
        """

        return self._me.__runner.load_client().load_schemas()

    def list_multi_cluster_applications(self, options={'me': 'true'}):
        """
        Option에 부합하는 모든 Multi-Cluster Applications 를 반환한다.\n
        :param options: API 호출시의 option
        :return: API 호출을 통해 얻은 모든 Multi-Cluster Applications
        """

        return self._me.__runner.load_client().list_multiClusterApp(**options)

    def delete_multi_cluster_application(self, options):
        """
        Options 정보에 해당하는 Multi-Cluster Application을 삭제한다.\n
        :param options: Multi-Cluster Application 삭제시 필요한 Data
        :return: 삭제 결과
        """

        application = self._me.__runner.load_client().by_id_multiClusterApp(options["id"])
        return self._me.__runner.load_client().delete(application)

    def list_multi_cluster_application_templates(self, options={'me': 'true'}):
        """
        Option에 부합하는 모든 Multi-Cluster Application의 Template 을 반환한다.\n
        :param options: API 호출시의 option
        :return: API 호출을 통해 얻은 모든 Multi-Cluster Application 의 Templates
        """

        return self._me.__runner.load_client().list_template(**options)

    def list_catalogs(self, options={'me': 'true'}):
        """
        Option에 부합하는 모든 Catalogs 를 반환한다.\n
        :param options: API 호출시의 option
        :return: API 호출을 통해 얻은 모든 Catalogs
        """

        return self._me.__runner.load_client().list_catalog(**options)

    def create_catalog(self, options):
        """
        Options 정보에 의거하여 Catalog 를 생성한다.\n
        :param options: Catalog 생성시 필요한 Data
        :return: 생성 결과의 Catalog
        """

        return self._me.__runner.load_client().create_catalog(options)

    def update_catalog(self, options):
        """
        Options 정보에 의거하여 Catalog 를 갱신한다.\n
        :param options: Catalog 갱신시 필요한 Data
        :return: 갱신 결과의 Catalog
        """

        catalog = self._me.__runner.load_client().by_id_catalog(options["name"])
        return self._me.__runner.load_client().update(catalog, options)

    def delete_catalog(self, options):
        """
        Options 정보에 해당하는 Catalog를 삭제한다.\n
        :param options: Catalog 삭제시 필요한 Data
        :return: 삭제 결과
        """

        catalog = self._me.__runner.load_client().by_id_catalog(options["name"])
        return self._me.__runner.load_client().delete(catalog)

    def refresh_catalog(self, options):
        """
        Options 정보에 해당하는 Catalog를 Refresh한다.\n
        :param options: Catalog Refresh시 필요한 Data
        :return: Refresh 결과
        """

        catalog = self._me.__runner.load_client().by_id_catalog(options["name"])
        return self._me.__runner.load_client().action(obj=catalog, action_name="refresh")

    def refresh_catalogs(self, options={'me': 'true'}):
        """
        모든 catalog를 refresh한다.\n
        :param options: API 호출시의 option
        :return: API 호출을 통해 얻은 결과
        """

        catalogs = self._me.__runner.load_client().by_id_catalog('')
        return self._me.__runner.load_client().action(obj=catalogs, action_name="refresh")

    def refresh_cluster_catalogs(self, options={'me': 'true'}):
        """
        모든 cluster catalog를 refresh한다.\n
        :param options: API 호출시의 option
        :return: API 호출을 통해 얻은 결과
        """

        cluster_catalogs = self._me.__runner.load_client().by_id_clusterCatalog('')
        return self._me.__runner.load_client().action(obj=cluster_catalogs, action_name="refresh")

    def refresh_project_catalogs(self, options={'me': 'true'}):
        """
        모든 project catalog를 refresh한다.\n
        :param options: API 호출시의 option
        :return: API 호출을 통해 얻은 결과
        """

        project_catalogs = self._me.__runner.load_client().by_id_projectCatalog('')
        return self._me.__runner.load_client().action(obj=project_catalogs, action_name="refresh")

    def list_persistent_volumes(self, options={'me': 'true'}):
        """
        임의의 id에 대한 모든 Persistent Volume을 호출한다.\n
        :param options: API 호출시 사용되는 options.
        :return: 임의의 id에 대한 모든 Persistent Volumes.
        """

        # TODO: c id를 외부에서 받아오는 방식으로 수정할 필요있음.
        return self._me.__runner.load_client().list_persistentVolume(**options)

    def create_persistent_volume(self, options):
        """
        임의의 id에 대한 cluster에 persistent volume을 추가한다.\n
        :param options: persistent volume을 추가하는 것에 사용되는 정보.
        :return: 추가 후의 결과.
        """

        # TODO: c id를 외부에서 받아오는 방식으로 수정할 필요있음.
        return self._me.__runner.load_client().create_persistentVolume(options)

    def list_storage_classes(self, options={'me': 'true'}):
        """
        임의의 id에 대한 모든 Storage Classes를 호출한다.\n
        :param options: Storage Classes를 호출하기 위해 필요한 options.
        :return: 임의의 id에 대한 모든 Storage Classes.
        """

        # TODO: c id를 외부에서 받아오는 방식으로 수정할 필요있음.
        return self._me.__runner.load_client().list_storageClass(**options)

    def list_projects(self, options={'me': 'true'}):
        """
        Option에 부합하는 모든 Projects 를 반환한다.\n
        :param options: API 호출시의 option
        :return: API 호출을 통해 얻은 모든 Projects
        """

        return self._me.__runner.load_client().list_project(**options)

    def list_clusters(self, options={'me': 'true'}):
        """
        Option에 부합하는 모든 Clusters 를 반환한다.\n
        :param options: API 호출시의 option
        :return: API 호출을 통해 얻은 모든 Clusters
        """

        return self._me.__runner.load_client().list_cluster(**options)

    def create_cluster(self, options):
        """
        Options 정보에 의거하여 Cluster를 생성한다.\n
        :param options: Cluster 생성시 필요한 Payload
        :return: 생성된 Cluster의 정보.
        """
        return self._me.__runner.load_client().create_cluster(options, {"_replace": "true"})

    def delete_cluster(self, options):
        """
        Options 정보로부터 삭제 대상의 cluster id를 습득하여 삭제한다.\n
        :param options: 삭제 대상의 cluster id를 가지고 있는 dictionary
        :return: 삭제 후 메세지.
        """
        cluster = self._me.__runner.load_client().by_id_cluster(options["id"])
        return self._me.__runner.load_client().delete(cluster)

    def snapshot_cluster(self, options):
        """
        Options 정보로부터 backup 대상의 cluster id를 습득하여 백업한다.\n
        :param options: backup 대상의 cluster id를 가지고 있는 dictionary
        :return: backup 저장 후 메세지.
        """
        cluster = self._me.__runner.load_client().by_id_cluster(options["id"])
        return self._me.__runner.load_client().action(obj=cluster, action_name="backupEtcd")

    def restore_snapshot_cluster(self, cluster_id, options):
        """
        cluster id에 해당하는 cluster를 Options 정보를 바탕으로 snapshot을 restore한다.\n
        :param cluster_id: 대상 cluster의 id.
        :param options: restore API 호출시에 사용되는 option dictionary.
        :return: restore 후 메세지.
        """
        cluster = self._me.__runner.load_client().by_id_cluster(cluster_id)
        return self._me.__runner.load_client().action(cluster, "restoreFromEtcdBackup", options)

    def rotate_certificates_cluster(self, cluster_id, options):
        """
        cluster id 해당하는 cluster를 Options 정보를 바탕으로 certificates를 rotate한다.\n
        :param cluster_id: 대상 cluster의 id.
        :param options: rotate API 호출시에 사용되는 option dictionary.
        :return: rotate 후 메세지.
        """
        cluster = self._me.__runner.load_client().by_id_cluster(cluster_id)
        return self._me.__runner.load_client().action(cluster, "rotateCertificates", options)

    def save_as_rke_templates_cluster(self, cluster_id, options):
        """
        Cluster id에 해당하는 cluster에 Options 정보를 바탕으로 RKE Template를 생성하여 저장한다.\n
        :param cluster_id: 대상 Cluster의 id.
        :param options: RKE Template의 생성 및 저장시 사용되는 Option Dictionary.
        :return: RKE Template 저장 후 메세지.
        """
        cluster = self._me.__runner.load_client().by_id_cluster(cluster_id)
        return self._me.__runner.load_client().action(cluster, "saveAsTemplate", options)

    def run_cis_scan_cluster(self, cluster_id, options):
        """
        Cluster id에 해당하는 cluster에 Options 정보를 바탕으로 CIS Scan을 실행한다.\n
        :param cluster_id: 대상 Cluster의 id.
        :param options: CIS Scan 실행시 사용되는 Otion Dictionary.
        :return: CIS Scan 실행 후 메세지.
        """
        cluster = self._me.__runner.load_client().by_id_cluster(cluster_id)
        return self._me.__runner.load_client().action(cluster, "runSecurityScan", options)

    def list_cluster_registration_token(self, options=None):
        """
        Options에 부합하는 모든 cluster regstration token을 반환한다.\n
        :param options: API 호출시에 사용되는 option dictionary.
        :return: 모든 Cluster Registration Token 리스트.
        """
        options = {"me": "true"} if not options else options
        return self._me.__runner.load_client().list_clusterRegistrationToken(**options)

    def create_cluster_registration_token(self, options):
        """
        Options 정보에 의거하여 Cluster Registration Token을 생성한다.\n
        :param options: Cluster Registration Token 생성시 필요한 Payload.
        :return: 삭제 후 메세지.
        """
        return self._me.__runner.load_client().create_clusterRegistrationToken(options)
