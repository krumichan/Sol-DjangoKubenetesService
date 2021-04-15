import os
import inspect


class PathUtility:

    def __new__(cls):
        if not hasattr(cls, "_me"):
            # instance를 생성.
            cls._me = super(PathUtility, cls).__new__(cls)
            # 해당 instance의 필수 요구 member를 생성.
            # 해당 instance의 필수 요구 변수 생성.
            cls.sep = os.path.sep

        return cls._me

    def absolute(self, file):
        dummy = self

        return os.path.dirname(os.path.realpath(file))

    def wkdir(self, file):

        absolute = self.absolute(file)

        sep = os.path.sep
        if sep in absolute:
            return absolute[
                   str(absolute).rindex(sep) + 1
                   :]

        else:
            return absolute
