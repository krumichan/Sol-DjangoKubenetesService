import copy
import json

from common.error.dummy import DummyError
from common.utility.format import FormatUtility

from . import constants as PersistentVolumesConstant


class RowExecutor:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 intstance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, "_me"):
            # instance 생성.
            cls._me = super(RowExecutor, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    def row_persistent_volume(self, persistent_volume):
        """
        persistent volume을 view에 맞게 재가공한다.\n
        :param persistent_volume: 대상 persistent volume.
        :return: 재가공이 완료된 persistent volume.
        """

        refactoring_results = {
            "origin": json.dumps(persistent_volume)
            ,
        }

        can_write_persistent_volume = persistent_volume.copy()

        # 날짜의 형식을 변경.
        can_write_persistent_volume[PersistentVolumesConstant.CREATED] \
            = self.__formatting(persistent_volume)

        # accessModes의 값을 기반으로 accessModes를 확장.
        can_write_persistent_volume[PersistentVolumesConstant.ACCESS_MODES] \
            = self.__refactoring_access_modes(persistent_volume)

        # nodeAffinity의 값을 기반으로 nodeAffinity를 refactoring.
        can_write_persistent_volume[PersistentVolumesConstant.NODE_AFFINITY] \
            = self.__refactoring_node_affinity(persistent_volume)

        # Plugin Configuration의 field명을 습득.
        field_name = self.__pull_out_field(persistent_volume)
        can_write_persistent_volume[PersistentVolumesConstant.FIELD] \
            = field_name

        can_write_persistent_volume[field_name] \
            = self.__refactoring_field(persistent_volume, field_name)

        # configuration을 습득.
        can_write_persistent_volume[PersistentVolumesConstant.CONFIGURATION] \
            = self.__pull_out_configuration(persistent_volume)

        # 결과 dictionary와 결합.
        refactoring_results.update(can_write_persistent_volume)

        return refactoring_results

    def __formatting(self, persistent_volume):
        """
        persistent volume내의 created( 생성시간 )을 "%Y-%m-%d %H:%M:%S" 형식으로 변환하여 반환한다.\n
        :param persistent_volume: 대상 persistent volume.
        :return: 형식을 변환한 date string.
        """

        # static 경고 방지용.
        dummy = self._me

        return FormatUtility.call().string_date_format_change(
            persistent_volume[PersistentVolumesConstant.CREATED]
            , "%Y-%m-%dT%H:%M:%SZ"
            , "%Y-%m-%d %H:%M:%S")

    def __refactoring_access_modes(self, persistent_volume):
        """
        persistent volume 내의 accessModes의 값을 기반으로 {label, id, value} 형식으로 확장한다.\n
        label, id는 Persistent Volume의 Constants로부터 추출한다.\n
        :param persistent_volume: 확장 대상의 persistent volume.
        :return: 확장한 access mode list.
        """

        # static 경고 방지용.
        dummy = self._me

        refactoring_modes = []

        # mode template에서 'mode'의 value를 습득.
        access_modes_template = copy.copy(PersistentVolumesConstant.FORM_ACCESS_MODES)
        mode_template = access_modes_template["mode"]

        # persistent volume에서 accessModes를 습득.
        access_mode_in_pv = persistent_volume[PersistentVolumesConstant.ACCESS_MODES]

        # mode template에 있는 모든 mode를 순회.
        for mode in mode_template:
            # mode의 value를 습득.
            value = mode[PersistentVolumesConstant.VALUE]

            # template의 mode에서 얻은 value가 persistent의 accessModes에 포함되어 있다면,
            # mode를 mode의 모든 정보를 result에 담음.
            if value in access_mode_in_pv:
                refactoring_modes.append(mode)

        # 담은 result를 갱신하고 반환.
        access_modes_template["mode"] = refactoring_modes

        return access_modes_template

    def __refactoring_node_affinity(self, persistent_volume):
        """
        persistent volume 내의 nodeAffinity의 값을 기반으로 matchExpressions의 값을 재구축한다.\n
        구체적으로는 matchExpressions의 내의 values 배열을 ','로 이어지는 하나의 string으로 변환시키기 위함이다.\n
        :param persistent_volume: 재구축 대상의 persistent volume.
        :return: 재구축 결과.
        """

        dummy = self._me

        # node affinity가 있는지 확인.
        try:
            node_affinity = persistent_volume[PersistentVolumesConstant.NODE_AFFINITY]

        # 만약 없을 경우, None을 반환.
        except KeyError:
            return None

        refactoring_terms = []

        # nodeSelectorTerms list를 추출.
        node_selector_terms = node_affinity[PersistentVolumesConstant.REQUIRED][PersistentVolumesConstant.NODE_SELECTOR_TERMS]

        # 추출한 nodeSelectorTerms를 순회.
        for node_selector_term in node_selector_terms:
            match_expressions = []

            # matchExpressions list를 추출.
            for row in node_selector_term[PersistentVolumesConstant.MATCH_EXPRESSIONS]:
                match_expression = {}

                # matchExpressions내의 요소를 key,value로 분류하여 순회.
                for expr_key, expr_value in row.items():
                    # 만약 현재의 key가 values라면 ','로 이어서 하나의 string으로 결합.
                    match_expression[expr_key] \
                        = ",".join(expr_value) if expr_key == PersistentVolumesConstant.VALUES else expr_value

                match_expressions.append(match_expression)

            refactoring_terms.append({PersistentVolumesConstant.MATCH_EXPRESSIONS: match_expressions})

        return refactoring_terms

    def __pull_out_field(self, persistent_volume):
        """
        임의의 Persistent Volume의 정보를 기반으로 source를 추출하고, 해당 source의 field name을 반환한다.\n
        :param persistent_volume: 임의의 persistent volume.
        :return: 해당 persistent volume에 맞는 configurtaion template.
        """

        # static 경고 제거용.
        dummy = self._me

        VOLUME_SOURCES = PersistentVolumesConstant.VOLUME_SOURCE_DICTIONARY[PersistentVolumesConstant.VOLUME_SOURCE]
        for value in VOLUME_SOURCES.values():
            # field 명을 습득한다.
            field_name = value[PersistentVolumesConstant.FIELD]

            # 해당 field가 존재하므로 field name을 반환.
            if field_name in persistent_volume and value[PersistentVolumesConstant.SUPPORTED]:
                return field_name

        # 어느 field에도 해당하는 내용이 없는 경우, DummyException을 발생시킴.
        raise DummyError("invalid data -- source does not exists." + "\n" + "data:" +
                         json.dumps(persistent_volume))

    def __refactoring_field(self, persistent_volume, field_name):

        # static 경고 제거용.
        dummy = self._me

        can_write_plugin = persistent_volume[field_name]

        if field_name == "hostPath":
            deeper = PersistentVolumesConstant.VOLUME_SOURCE_DICTIONARY[PersistentVolumesConstant.VOLUME_SOURCE]
            deeper = deeper[PersistentVolumesConstant.TITLE_HOST_PATH]
            deeper = deeper[PersistentVolumesConstant.CONFIGURATION]
            deeper = deeper["kind"]
            deeper = deeper["items"]
            for item in deeper:

                if item["value"] == can_write_plugin["kind"]:
                    deeper = item["label"]
                    break

                deeper = None

            # TODO: error 내용 제대로 쓸 필요 있음.
            if deeper is None:
                raise DummyError("error..")

            can_write_plugin["kind"] = deeper

        return can_write_plugin

    def __pull_out_configuration(self, persistent_volume):
        """
        임의의 Persistent Volume의 정보를 기반으로 source를 추출하고, 해당 source의 configuration을 반환한다.\n
        :param persistent_volume: 임의의 persistent volume.
        :return: 해당 persistent volume에 맞는 configurtaion template.
        """

        # static 경고 제거용.
        dummy = self._me

        VOLUME_SOURCES = PersistentVolumesConstant.VOLUME_SOURCE_DICTIONARY[PersistentVolumesConstant.VOLUME_SOURCE]
        for value in VOLUME_SOURCES.values():
            # field 명을 습득한다.
            field_name = value[PersistentVolumesConstant.FIELD]

            # 해당 field가 존재하므로 configuration을 반환.
            if field_name in persistent_volume and value[PersistentVolumesConstant.SUPPORTED]:
                return value[PersistentVolumesConstant.CONFIGURATION]

        # 어느 field에도 해당하는 내용이 없는 경우, DummyException을 발생시킴.
        raise DummyError("invalid data -- source does not exists." + "\n" + "data:" +
                         json.dumps(persistent_volume))
