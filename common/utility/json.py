import ast
import json

from common.error.dummy import DummyError


class JsonUtility:

    def __new__(cls):
        """
         새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
         없을시, 새로 생성하여 반환한다.
         """

        if not hasattr(cls, '_me'):
            # instance를 생성.
            cls._me = super(JsonUtility, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    @staticmethod
    def call():
        """
        해당 class 의 unique instance를 호출한다.
        :return: unique instance
        """
        return JsonUtility()

    def to_dictionary(self, source):
        """
        임의의 data 를 dictionary 형식의로 변환한다.\n
        임의의 data 는 dictionary 형태로 변환할 수 있는 모형이여야 하며, 그렇지 않으면 예외를 발생시킨다.\n
        :param source: 변환 대싱인 임의의 data
        :exception: 변환 실패, DummyException 발생
        :return: 변환이 완료된 dictionary 객체
        """

        try:
            try:
                return self.__literal_evaluation(source)
            # 만일 ast library 를 이용한 변환을 실패하였을 경우.
            except Exception as e:
                return self.__json_dumps_then_loads(source)
        # 만일 json library 를 사용한 변환에도 실패했을 경우.
        except (TypeError or json.JSONDecodeError) as e:
            # 변환 실패 exception 을 발생시킨다.
            raise DummyError(
                "this source can't convert to dinctionary. please check your source." + "\n" + source
                , e
            )

    def __literal_evaluation(self, source):
        """
        ast library 를 사용하여 임의의 data를 바로 dictionary 로 변환한다.
        :param source: json 변환 대상의 source
        :return: json string을 변환시킨 dictionary
        """

        # static 경고 방지용.
        dummy = self._me

        return ast.literal_eval(str(source))

    def __json_dumps_then_loads(self, source):
        """
        json library 를 사용하여 임의의 data를 바로 dictionary 로 변환한다.
        :param source: json 변환 대상의 source
        :return: json string을 변환시킨 dictionary
        """
        # static 경고 방지용.
        dummy = self._me

        json.loads(
            str(source)
            , indent=4
            , sort_keys=True
            , default=str
        )
