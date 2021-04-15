import copy

from common.error.dummy import DummyError
from common.utility.json import JsonUtility

from . import constants as Constant


class ListExecutor:
    """
    API로부터 호출된 후의 Multi-Cluster Applications 결과의 가공을 담당하는 Class.
    """

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(ListExecutor, cls).__new__(cls)

        return cls._me

    def list_applications(self, multi_cluster_apps, projects, clusters, template_apps):
        """
        모든 multi-cluster application 을 불러온다.\n
        projects 와 clusters 가 필요한 이유는 multi-cluster application 의 대상이 되고있는 project 와 cluster 명을 얻기 위해서이다.\n
        :param template_apps: API 로부터 얻은 모든 multi-cluster application teamplates
        :param multi_cluster_apps: API 로부터 얻은 모든 multi-cluster application
        :param projects: API 로부터 얻은 projects
        :param clusters: API 로부터 얻은 clusters
        :return: 가공 처리가 완료된 multi-cluster application list
        """
        result_multi_cluster_applications = []

        # RestObject 를 dictionary 객체로 변환
        try:
            dict_multi_cluster_apps = JsonUtility.call().to_dictionary(multi_cluster_apps)
            dict_projects = JsonUtility.call().to_dictionary(projects)
            dict_clusters = JsonUtility.call().to_dictionary(clusters)
            dict_template_apps = JsonUtility.call().to_dictionary(template_apps)
        except DummyError as de:
            raise de

        # 각 dictionary 로부터 'data' dictionary 를 추출.
        try:
            multi_cluster_apps_mapping = dict_multi_cluster_apps['data']
            projects_mapping = dict_projects['data']
            clusters_mapping = dict_clusters['data']
            template_apps_mapping = dict_template_apps['data']

        except:
            raise DummyError("[data] row is not eixsts. please check your data.")

        try:
            for application in multi_cluster_apps_mapping:
                # application 을 복제한다.
                can_write_application = copy.copy(application)

                # application id 를 추출한다.
                application_id = self._me.__to_application_id(application)

                # application id 를 이용하여, template 로부터 row 를 추출한다.
                template_row = self._me.__find_by_key_then_get_row(template_apps_mapping, 'id', application_id)

                if template_row is not None:
                    # application 으로부터 apps_templates version 을 추출한다.
                    can_write_application[Constant.TEMPLATE_VERSION] \
                        = self._me.__to_template_version(application)

                    # icon link 를 추출한다.
                    can_write_application['iconLink'] = template_row['links']['icon']

                    # template의 latest(default) version 을 추출한다.
                    can_write_application[Constant.LATEST_VERSION] = template_row['defaultVersion']

                # application 을 이용하여 targets 를 refactoring 한다.
                refactoring = self._me.__targets_refactoring(application, clusters_mapping, projects_mapping)
                can_write_application['targets'] = refactoring.copy()

                # refactoring 이 완료된 application 을 결과 list 에 추가한다.
                result_multi_cluster_applications.append(can_write_application.copy())
        except DummyError as de:
            raise de
        except Exception as e:
            raise Exception("unknown exception...\n" + e)

        return result_multi_cluster_applications

    def __to_template_version(self, application):
        """
        대상 application 으로부터 apps_templates version 을 추출한다.\n
        :param application: 대상 application
        :return: 대상 application 의 apps_templates version
        """

        # static 경고 제거용.
        dummy = self._me

        template_version_id = application['templateVersionId']
        last_hyphen_index = template_version_id.rfind('-')

        if last_hyphen_index == -1:
            raise DummyError("application 의 templateVersionId 에 - 이 없습니다.")

        return template_version_id[last_hyphen_index + 1:]

    def __to_application_id(self, application):
        """
        대상 application 으로부터 application id 를 추출한다.\n
        :param application: 대상 application
        :return: 대상 application 의 id
        """

        # static 경고 제거용.
        dummy = self._me

        template_version_id = application['templateVersionId']
        last_hyphen_index = template_version_id.rfind('-')

        if last_hyphen_index == -1:
            raise DummyError("application 의 templateVersionId 에 - 이 없습니다.")

        return template_version_id[:last_hyphen_index]

    def __targets_refactoring(self, application, clusters_mapping, projects_mapping):
        """
        대상 application 의 targets 의 target 정보를 기반으로 cluster 와 project 명을 추출하고,
        추출한 cluster, project 명을 target 에 넣어준다.\n
        :param application: 대상 application
        :param clusters_mapping: cluster 명을 추출할 cluster mapping data
        :param projects_mapping: project 명을 추출할 project mapping data
        :return: refactoring 한 targets
        """

        refactoring_result = []
        targets = application['targets']

        for target in targets:
            # project id 추출
            project_id = target['projectId']

            #  cluster id 추출
            colon_index = project_id.find(':')
            if colon_index == -1:
                raise DummyError("[targets.clusterId] has not colon.\n" + project_id)

            cluster_id = project_id[:colon_index]

            # cluster id 를 기반으로 해당 cluster 의 row 습득.
            cluster_row = self._me.__find_by_key_then_get_row(clusters_mapping, 'id', cluster_id)
            if cluster_row is None:
                raise DummyError("[clusters] does not include this id.\nid:" + cluster_id)

            # project id 를 기반으로 해당 project 의 row 습득.
            project_row = self._me.__find_by_key_then_get_row(projects_mapping, 'id', project_id)
            if cluster_row is None:
                raise DummyError("[projects] does not include this id.\nid:" + project_id)

            # cluster row 로부터 name 을 추출.
            target[Constant.CLUSTER_NAME] = cluster_row['name']

            # project row 로부터 name 을 추출.
            target[Constant.PROJECT_NAME] = project_row['name']

            # refactoring 한 target 을 결과 list 에 추가.
            refactoring_result.append(target.copy())

        return refactoring_result

    def __find_by_key_then_get_row(self, rows, key, value):
        """
        data list 로부터 임의의 key 의 값이 value 인 row 를 추출.
        :param rows: data list
        :param key: 비교를 수행할 key 값
        :param value: key 로부터 얻은 값과 비교할 value
        :return: 추출한 row
        """

        result_row = None

        for row in rows:
            if self._me.__equals_value(row, key, value):
                result_row = row
                break

        return result_row

    def __equals_value(self, row, key, value):
        """
        data 로부터 임의의 key 의 값이 value 인지를 확인
        :param row: data
        :param key: 비교를 수행할 key 값
        :param value: key 로부터 얻은 값과 비교할 value
        :return: 동일 여부
        """

        # static 경고 제거용.
        dummy = self._me

        if row[key] == value:
            return True

        return False
