#!/usr/bin/env python
import os
import sys


def _patch_python314_django_context():
    """Python 3.14 da Django admin template xatosini tuzatadi."""
    if sys.version_info < (3, 14):
        return
    try:
        from django.template import context as ctx
    except Exception:
        return

    def _base_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        for k, v in getattr(self, "__dict__", {}).items():
            if k != "dicts":
                setattr(duplicate, k, v)
        duplicate.dicts = list(self.dicts)
        return duplicate

    def _request_copy(self):
        duplicate = _base_copy(self)
        if hasattr(self, "request"):
            duplicate.request = self.request
        if hasattr(self, "_processors"):
            duplicate._processors = self._processors
        if hasattr(self, "_processors_index"):
            duplicate._processors_index = self._processors_index
        return duplicate

    ctx.BaseContext.__copy__ = _base_copy
    if hasattr(ctx, "Context"):
        ctx.Context.__copy__ = _base_copy
    if hasattr(ctx, "RequestContext"):
        ctx.RequestContext.__copy__ = _request_copy


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django topilmadi. Virtual muhitni faollashtirib, "
            "requirements.txt ni o'rnatganingizga ishonch hosil qiling."
        ) from exc
    # Django import qilingandan keyin patch
    _patch_python314_django_context()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
