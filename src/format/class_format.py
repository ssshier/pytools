import inspect
import re


class SampleFormat:

    def __init__(self, obj) -> None:
        self.obj = obj
        self.class_name = self.obj.__name__

        self.result = ""

        self._class = ""
        self._new = ""
        self._init = ""
        self._post_init = ""

        self._magic = {}
        self._property = {}
        self._staicmethod = {}
        self._classmethod = {}
        self._method = {}
        self._private = {}

    def cache_one(self, code):
        if f"class {self.class_name}" in code:
            self._class = code
        elif "def __new__" in code:
            self._new = code
        elif "def __init__" in code:
            self._init = code
        elif "def __post_init__" in code:
            self._post_init = code
        else:
            func_name = re.findall(r"def (.*)\(", code)[0]
            if self.check_sub(code, "    @property"):
                self._property[func_name] = code
            elif self.check_sub(code, "    @staticmethod"):
                self._staicmethod[func_name] = code
            elif self.check_sub(code, "    @classmethod"):
                self._classmethod[func_name] = code
            elif func_name.startswith("__") and func_name.endswith("__"):
                self._magic[func_name] = code
            elif func_name.startswith("_"):
                self._private[func_name] = code
            else:
                self._method[func_name] = code

    def check(self, line):
        lst = ["    @", "    def"]
        for item in lst:
            if line.startswith(item):
                return True
        return False

    def check_sub(self, code, flag):
        lines = code.splitlines()
        for line in lines:
            if line.startswith(flag):
                return True
        return False

    def combine(self):
        self.result += self._class
        self.result += self._new
        self.result += self._init
        self.result += self._post_init

        self.result += self.combine_dt(self._magic)
        self.result += self.combine_dt(self._property)
        self.result += self.combine_dt(self._staicmethod)
        self.result += self.combine_dt(self._classmethod)
        self.result += self.combine_dt(self._method)
        self.result += self.combine_dt(self._private)

    def combine_dt(self, dt):
        result = ""
        keys = sorted(dt.keys(), key=lambda x: x.lower())
        for key in keys:
            result += dt[key]
        return result

    def format(self):
        lines, start = inspect.getsourcelines(self.obj)
        lines.append("")
        lines.append("")

        cur_code = ""
        for index in range(len(lines) - 1):
            if self.check(lines[index + 1]) and not self.check(lines[index + 2]):
                self.cache_one(cur_code)
                cur_code = ""
            cur_code += lines[index]
        self.cache_one(cur_code)

        self.combine()

        return self.result
