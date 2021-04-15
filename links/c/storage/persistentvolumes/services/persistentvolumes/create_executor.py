import json

from common.error.dummy import DummyError

from . import constants as PersistentVolumesConstant


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

    def generate_payload(self, options, current_schema):

        # View로부터 얻은 payload로부터 Volume Source를 추출.
        current_volume_source_field_name = self.__pull_out_field_name(options)

        # schema로부터 위에서 추출한 volume source의 field에 해당하는 type을 추출.
        volume_source_type = self.__pull_out_type_from_schema(current_schema, current_volume_source_field_name)

        # options에서 volume source의 type을 추가해줌.
        options[current_volume_source_field_name].update({"type": volume_source_type})

        # options에서 해당 persistent volume의 type을 추가해줌.
        options["type"] = PersistentVolumesConstant.PERSISTENT_VOLUME

        return options

    def create_persistent_volume(self, create_result):
        """
        API 로부터 Persistent Volume을 생성하고 남은 결과를 View에 맞게 가공한다.\n
        :param create_result: Persistent Volume 생성 후의 결과.
        :return: View에 맞게 가공한 Data.
        """

        # static 경고 무시용.
        dummy = self._me

        return create_result

    def __pull_out_field_name(self, options):
        """
        View로부터 받은 payload로부터 Volume Source의 Field Name을 추출한다.\n
        :param options: View로부터 받은 payload
        :return: 추출한 Field Name.
        """

        # static 경고 무시용.
        dummy = self._me

        # volume source mapping을 습득.
        volume_sources = PersistentVolumesConstant.VOLUME_SOURCE_DICTIONARY[PersistentVolumesConstant.VOLUME_SOURCE]

        # volume source mapping을 순회하면서 field를 추출하여 반환.
        for volume_source_value in volume_sources.values():
            try:
                # 현재의 field명을 습득.
                current_field = volume_source_value[PersistentVolumesConstant.FIELD]
                # 현재 field명에 해당하는 정보가 options에 있는지 확인.
                # 만약 없을 경우, KeyError Exception이 발생하여 건너뛰게 됨.
                checker = options[current_field]
                # 있을 경우, 현재의 field를 반환.
                return current_field

            # 해당 field명에 부합하는 Data가 없을 경우, Key Error가 발생. 이 경우 무시.
            except KeyError:
                pass

        # 어느 Field에도 해당하지 않을 경우, Error를 반환함.
        # 보통은 부정적인 접근이나 또는 Coding Error로 인해 발생. ( Coding Error로 인한 발생이 거의 대부분일듯. )
        raise DummyError("volume source field doesn't exist. please check your data." + "\n" + json.dumps(options))

    def __pull_out_type_from_schema(self, schema, field):

        # static 경고 무시용.
        dummy = self._me

        schema_to_string = str(schema)
        schema_to_dict = json.loads(schema_to_string)

        data_list = schema_to_dict["data"]

        for row in data_list:
            try:
                # 하나의 schema data로부터 id를 추출.
                row_id = row["id"]

                # id가 persistentVolume인지를 확인.
                if row_id == PersistentVolumesConstant.PERSISTENT_VOLUME:
                    # resourceFields를 추출.
                    resource_fields = row["resourceFields"]
                    # resourceFields로부터 field에 해당하는 Data를 추출.
                    field_values = resource_fields[field]

                    # field에 해당하는 data로부터 type을 추출.
                    return field_values["type"]

            except Exception as ex:
                DummyError("Invalid schema." + "\n" + schema, ex)

        raise DummyError("field type doesn't exist in schema." + "\nfield:" + field + "\n" + schema)


