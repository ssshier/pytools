from .class_format import ClassFormat
from .class_load import ClassLoad


def cformat(path: str):
    classes = ClassLoad().load(path)
    print(classes)
    for cls in classes:
        result = ClassFormat().format(cls)
        print(result)
