# -*- coding: UTF-8 -*-


class CustomBaseException(Exception):
    def __init__(self, prefix: str, arg: str, code: int, addition=""):
        self._prefix = prefix
        self._arg = arg
        self._code = code
        self._addition = addition

    def __str__(self):
        if not self._prefix == "":
            string = "{0}: "
        else:
            string = ""

        string += "{1} 。CODE: {2}"
        string = string.format(self._prefix, self._arg, str(self._code))

        if not self._addition == "":
            string += "\nADDITION:\n{0}".format(self._addition)
        return string


class NoArgumentException(CustomBaseException):
    def __init__(self, arg: str):
        self._prefix = "不完整的命令行参数"
        self._arg = arg
        self._code = 10
        self._addition = ""


class UnknownArgumentException(CustomBaseException):
    def __init__(self, arg: str):
        self._prefix = "未知的命令行参数"
        self._arg = arg
        self._code = 11
        self._addition = ""


class AnotherException(CustomBaseException):
    def __init__(self, addition: str):
        self._prefix = ""
        self._arg = "其它类型的错误."
        self._code = 5
        self._addition = addition


class InvalidCompoundException(CustomBaseException):
    def __init__(self, arg: str):
        self._prefix = "无效的参数组合"
        self._arg = arg
        self._code = 12
        self._addition = ""


class InvalidPathException(CustomBaseException):
    def __init__(self, target: str, arg: str):
        self._prefix = "无效的{0}目录".format(target)
        self._arg = arg
        self._code = 13
        self._addition = ""


class CannotCreatePathException(CustomBaseException):
    def __init__(self, target: str, addition: str):
        self._prefix = "无法创建的目录或文件"
        self._arg = target
        self._code = 14
        self._addition = addition


class LoginFailedException(CustomBaseException):
    def __init__(self, arg: str):
        self._prefix = "登陆失败"
        self._arg = arg
        self._code = 21
        self._addition = ""


class NoValidFileWarning(CustomBaseException):
    def __init__(self, url=""):
        self._prefix = ""
        self._arg = "未找到有效文件"
        if url:
            self._arg += "。请自行前往论坛查看"
        else:
            self._arg += "。请检查是否有缓存/下载目录的读写权限或目录是否存在"
        self._code = 101
        self._addition = url


class WatchdogTimeoutWarning(CustomBaseException):
    def __init__(self):
        self._prefix = ""
        self._arg = "文件监听等待超时"
        self._code = 102
        self._addition = ""
