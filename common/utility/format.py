import os
from datetime import datetime as DateTime

from common.error.dummy import DummyError


class FormatUtility:

    def __new__(cls):
        """
         새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
         없을시, 새로 생성하여 반환한다.
         """

        if not hasattr(cls, '_me'):
            # instance를 생성.
            cls._me = super(FormatUtility, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.

        return cls._me

    @staticmethod
    def call():
        """
        해당 class 의 unique instance를 호출한다.
        :return: unique instance
        """

        return FormatUtility()

    def string_to_datetime(self, string, formatting):
        """
        시간 문자열을 <datetime> 형식으로 변환.\n
        :param string: 시간 문자열.
        :param formatting: 변환 규칙.
        :return: <datetime> 형식의 시간.
        """
        # static 경고 방지용.
        dummy = self._me

        try:
            return DateTime.strptime(string, formatting)

        except Exception as e:
            DummyError("fail to convert from string to date." + "\n" +
                       "reason: " + str(e) + "\n" +
                       "date string: " + string + "\n" +
                       "format: " + formatting)

    def datetime_to_string(self, date, formatting):
        """
        <datetime> 형식의 시간을 문자열로 변환.\n
        :param date: <datetime> 형식의 시간.
        :param formatting: 변환 규칙.
        :return: 시간 문자열.
        """
        # static 경고 방지용.
        dummy = self._me

        try:
            return date.strftime(formatting)

        except Exception as e:
            DummyError("fail to convert from date to string." + "\n" +
                       "reason: " + str(e) + "\n" +
                       "date: " + str(date) + "\n" +
                       "format: " + formatting)

    def string_date_format_change(self, string, before, after):
        """
        시간 문자열을 다른 시간 규칙으로 변환\n
        :param string: 시간 문자열.
        :param before: 변환 전 규칙.
        :param after: 변환 후 규칙.
        :return: 변환 완료한 시간 문자열.
        """
        date = self.string_to_datetime(string, before)

        return self.datetime_to_string(date, after)

    def name_to_class(self, path, class_name):
        """
        class name을 <classobj> 형식으로 변환.\n
        :param path: 해당 class를 가진 파일이 있는 디렉토리.
        :param class_name: 가져올 class 이름.
        :return: <classobj> 형식의 객체.
        """
        dummy = self
        extension = ".py"
        pkg_join_sep = "."

        for file in [file[:-len(extension)] for file in os.listdir(path) if file.endswith(extension)]:
            module = __import__(pkg_join_sep.join([path.replace(os.sep, pkg_join_sep), file]), fromlist=[file])

            if hasattr(module, class_name):
                return getattr(module, class_name)

        raise Exception("Modules in '" + path + "' do not have '" + class_name + "' attribute.")
