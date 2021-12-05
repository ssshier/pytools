import importlib


class ClassLoad:

    def __init__(self):
        self._classes = []

    def load(self, path: str):
        module = importlib.import_module(path)
        for name in dir(module):
            attr = getattr(importlib.import_module(path), name)
            if type(attr).__name__ == "type":
                self._classes.append(attr)
        return self._classes
