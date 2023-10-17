# -*- coding: utf-8 -*-


class Verb(dict):
    map = {
        "subject": "subjects",
        "modality": "modalities",
        "tense": "tenses"
    }

    def add_sub_dicts(self):
        pass

    @classmethod
    def query(cls, args, key):
        if (
            (isinstance(args[key], list) or isinstance(args[key], tuple))
            and
            (data := list(filter(lambda i: i in getattr(cls, cls.map[key]), args[key])))
        ):
            return data
        elif isinstance(args[key], str) and args[key] in getattr(cls, cls.map[key]):
            return [args[key]]

    @classmethod
    def isinstance(cls, instance: 'Verb'):
        def inner(self, other):
            if len(other) != len(self):
                return False
            for k1, k2 in zip(self, other):
                if k1 != k2:
                    return False
                if isinstance(self[k1], dict):
                    if isinstance(other[k2], dict):
                        return inner(self[k1], other[k1])
                    else:
                        return False
            return True
        return inner(cls.__call__(verb=""), instance)
