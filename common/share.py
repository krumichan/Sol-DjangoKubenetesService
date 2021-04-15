from .utility.path import PathUtility
from .utility.string import StringUtility
from . import constants


class Share:

    def __new__(cls):
        if not hasattr(cls, "_me"):
            # instance 생성.
            cls._me = super(Share, cls).__new__(cls)
            # 해당 instance의 필수 요구 member 생성.
            cls.__path = PathUtility()
            cls.__string = StringUtility()

        return cls._me

    def generator_path(self, filepath, file):
        absolute = self.__path.absolute(filepath)
        prefix = absolute[
                 self.__string.last_index(absolute, constants.APPLICATION_ROOT)
                 :]

        return prefix + self.__path.sep + file
