from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "books"

    def ready(self):
        # Python 3.14 + Django 5.1 admin template context bug fix
        _patch_django_context_copy()


def _patch_django_context_copy():
    """Fix: AttributeError 'super' object has no attribute 'dicts' (Python 3.14)."""
    try:
        from django.template import context as ctx
    except Exception:
        return

    def _base_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        # BaseContext uses .dicts; keep any other instance attrs if present
        for k, v in getattr(self, "__dict__", {}).items():
            if k != "dicts":
                setattr(duplicate, k, v)
        duplicate.dicts = list(self.dicts)
        return duplicate

    def _request_copy(self):
        duplicate = _base_copy(self)
        # RequestContext extras
        if hasattr(self, "request"):
            duplicate.request = self.request
        if hasattr(self, "_processors"):
            duplicate._processors = self._processors
        if hasattr(self, "_processors_index"):
            duplicate._processors_index = self._processors_index
        return duplicate

    ctx.BaseContext.__copy__ = _base_copy
    if hasattr(ctx, "RequestContext"):
        ctx.RequestContext.__copy__ = _request_copy
    if hasattr(ctx, "Context"):
        ctx.Context.__copy__ = _base_copy
