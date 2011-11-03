from django.conf import settings


class temporary_settings:
    def __init__(self, dic):
        self.dic = dic

    def __enter__(self):
        self.old_values = dict()
        for key, value in self.dic.items():
            self.old_values[key] = getattr(settings, key)
            setattr(settings, key, value)

    def __exit__(self, type, value, traceback):
        for key, value in self.old_values.items():
            setattr(settings, key, value)
