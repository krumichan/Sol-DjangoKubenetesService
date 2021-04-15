from common.error.dummy import DummyError
from common.utility.json import JsonUtility
from links.g.tools.catalogs.services.catalogs import constants as CatalogConstant

from . import constants as Constant


class FilterExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """
        if not hasattr(cls, '_me'):
            # instance 생성.
            cls._me = super(FilterExecutor, cls).__new__(cls)

        return cls._me

    def filter_multi_cluster_application_templates(self, apps_templates, opts):
        """
        모든 Multi-Cluster Applications의 Templates를 임의의 Catalog 명으로 Filtering한다.\n
        :param apps_templates: 모든 Multi-Cluster Application의 Templates.
        :param opts: Filtering 및 모든 Multi-Cluster Applications의 Templates의 API 호출시의 options.
        :return: Filtering이 완료된 Multi-Cluster Applications의 Templates List.
        """
        # category name을 추출한다.
        category_name = opts['category']

        result_templates = {
            Constant.CATEGORY_COUNT_DICTIONARY: {
                "All": 0,
            }
            , Constant.CATEGORY_FOCUS: category_name
            , Constant.DATA: {

            }
            ,
        }

        # RestObject 를 dictionary 로 변환
        try:
            dict_templates = JsonUtility.call().to_dictionary(apps_templates)
        except DummyError as de:
            raise de

        # dictionary 로부터 'data' dictionary 를 추출.
        try:
            templates_mapping = dict_templates['data']
        except:
            raise DummyError("[data] row is not eixsts. please check your data.\n")

        for templ in templates_mapping:
            # apps_templates 를 복제한다.
            can_write_template = templ.copy()

            # 각 Category 에 따른 갯수 추가.
            self.__calculate_category_count(templ, result_templates)

            # Category 를 result mapping 에 분류하여 삽입.
            self.__classify_category(
                can_write_template, result_templates[Constant.DATA], category_name)

        return result_templates

    def __calculate_category_count(self, templ, result_mapping):
        """
        임의의 Multi-Cluster Application의 template을 Category 별로 counting 한다.
        :param templ: 임의의 Multi-Cluster Application의 Template.
        :param result_mapping: 결과를 담을 mapper.
        """
        # 먄약 현재의 templ 이 system library templ이라면 무시한다.
        if self.__is_system_library(templ):
            return None

        # All Categories 갯수 추가.
        result_mapping[Constant.CATEGORY_COUNT_DICTIONARY]["All"] += 1

        # category list를 가지고 있는 경우.
        try:
            # category list 추출
            categories = templ['categories']

            # 각 Category 에 따른 갯수 추가.
            for category in categories:
                # result mapping에 category 갯수를 추가시킨다.
                self.__insert_category_count(category, result_mapping)

        # category list를 가지고 있지 않은 경우 무시한다.
        except KeyError:
            pass

    def __is_system_library(self, templ):
        """
        임의의 Multi-Cluster Application의 Template가 System Library Catalog의 Template인가를 확인한다.\n
        :param templ: 임의의 Multi-Cluster Application의 Template.
        :return: 확인 결과.
        """
        # static 경고 제거용.
        dummy = self._me

        # catalog id 추출
        catalog_id = templ['catalogId']

        # 만약 catalog id가 system library의 이름과 같다면 무시한다.
        if catalog_id == CatalogConstant.SYSTEM_LIBRARY_NAME:
            return True

        return False

    def __insert_category_count(self, category, result_mapping):
        """
        결과 Mppaer의 임의의 Catalog에 해당하는 Counter를 증가시킨다.\n
        :param category: 증가시킬 대상의 Catalog 이름.
        :param result_mapping: 결과 Mapper.
        """
        # static 경고 제거용.
        dummy = self._me

        try:
            # 특정 Category의 갯수를 1 추가시킨다.
            # 만약 특정 Category에 대한 value(갯수)가 존재하지 않은 경우 KeyError 발생.
            result_mapping[Constant.CATEGORY_COUNT_DICTIONARY][category] += 1

        # 특정 Category에 대한 value가 존재하지 않는 경우.
        except KeyError:
            result_mapping[Constant.CATEGORY_COUNT_DICTIONARY][category] = 1

    def __classify_category(self, can_write_templ, data_dictionary, category_name):
        """
        임의의 Multi-Cluster Application의 Template를 Catalog 명으로 분류시켜 결과 Mapper에 삽입한다.\n
        여기서 사용되는 Catalog 명은, Filtering의 대상을 선정할 시 기준이 되는 Catalog 명이다.\n
        :param can_write_templ: 임의의 Multi-Cluster Application의 Template.
        :param data_dictionary: 결과 Mppaer.
        """
        # catalog id 추출
        catalog_id = can_write_templ['catalogId']

        # 만약 catalog id 가 system library에 해당한다면 무시한다.
        if catalog_id == CatalogConstant.SYSTEM_LIBRARY_NAME:
            return

        # 만약 template의 categories의 안에 category_name이 포함되지 않는 경우라면 무시한다.
        if category_name != 'All' and not self.__is_contained(can_write_templ, category_name):
            return

        # 선별한 category를 result templates 에 추가한다.
        self.__insert_category_into_result_mapping(catalog_id, can_write_templ, data_dictionary)

    def __insert_category_into_result_mapping(self, catalog_id, can_write_templ, data_dictionary):
        """
        임의의 Multi-Cluster Application의 Template를 Catalog명으로 분류시켜 결과 Mapper에 삽입한다.\n
        :param catalog_id: 분류의 기준이 될 Catalog 명.
        :param can_write_templ: 임의의 Multi-Cluster Application의 Template.
        :param data_dictionary: 결과 Mppaer.
        """
        # static 경고 제거용.
        dummy = self._me

        try:
            # 특정 catalog id에 값을 추가.
            data_dictionary[catalog_id].append(can_write_templ.copy())

        # 특정 catalog id에 대한 value가 존재하지 않는 경우.
        except KeyError:
            # 특정 catalog id에 해당 system library를 list에 삽입한 형태로 추가한다.
            data_dictionary[catalog_id] = [can_write_templ.copy()]

    def __is_contained(self, templ, category_name):
        """
        임의의 Multi-Cluster Application의 Template가 임의의 Catalog명을 포함하고 있는지를 확인.\n
        :param templ: 임의의 Multi-Cluster Application의 Tepmlate.
        :param category_name: Filtering 기준이 될 임의의 Catalog 명.
        :return: 포함하고 있는지의 여부.
        """
        # static 경고 제거용.
        dummy = self._me

        try:
            # category list 를 추출
            categories = templ['categories']

            # category list에 인수로 받은 category가 포함되는지 확인.
            if category_name in categories:
                return True

            return False

        # category list가 존재하지 않을 경우.
        except:
            return False
