from common.error.dummy import DummyError


class StringUtility:

    def __new__(cls):
        """
         새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
         없을시, 새로 생성하여 반환한다.
         """

        if not hasattr(cls, '_me'):
            # instance를 생성.
            cls._me = super(StringUtility, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    @staticmethod
    def call():
        """
        해당 class 의 unique instance를 호출한다.
        :return: unique instance
        """

        return StringUtility()

    def to_string(self, value):
        """
        임의의 값을 문자열료 변환한다.\n
        :param value: 임의의 값
        :return: 변환 완료한 문자열
        """

        # static 경고 방지용.
        dummy = self._me

        return str(value)

    def replace_range(self, value, old, new, start, end):
        """
        임의의 문자열로부터 일정 범위 내에서 특정 문자열을 replace 하는 함수이다.\n
        :param value: 대상 문자열
        :param old: replace 할 대상의 단어
        :param new: replace 할 단어
        :param start: 임의의 문자열의 시작 범위
        :param end: 임의의 문자열의 종료 범위
        :return: 대체 완료한 문자열
        """

        # static 경고 방지용.
        dummy = self._me

        # start 또는 end 가 정수가 아닌 경우.
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError("start or end value are not digit.")

        # start 가 end 보다 큰 경우.
        if start > end:
            raise DummyError("end value is greater than start value.")

        # start 또는 end 가 음수인 경우.
        if start < 0 or end < 0:
            raise DummyError("start or end value is less than 0")

        # start 또는 end 가 대상 문자열의 길이보다 큰 경우.
        VALUE_LENGTH = len(value)
        if start >= VALUE_LENGTH or end >= VALUE_LENGTH:
            raise DummyError("start or end value is greater than target value length.")

        # [start:end] 범위 외의 문자열을 따로 저장.
        prefix = value[:start]
        suffix = value[end:]

        # [start:end] 범위 내의 문자열 습득.
        range_string = value[start:end]
        result_string = ''

        OLD_LENGTH = len(old)

        while True:
            # old 문자열이 있는 시작 index 습득.
            start_index = range_string.find(old)

            # old 문자열이 더 이상 발견되지 않을 경우 종료.
            if start_index == -1:
                break

            # old 문자열의 시작점 이전 부분을 입력.
            result_string += range_string[:start_index]

            # old 문자열의 시작 위치에 new 문자열을 입력.
            result_string += new

            # 대상 문자열에서 old 문자열 이후의 문자열들을 저장.
            start_index += OLD_LENGTH
            range_string = range_string[start_index:]

        result_string = prefix + result_string + suffix
        return result_string

    def last_index(self, value, sub):
        dummy = self
        return str(value).index(str(sub)) + len(str(sub))
