from django.contrib.auth.mixins import AccessMixin

from event.models import Event
from django.core.exceptions import PermissionDenied


# class EventStartedMixin(AccessMixin):
class ProductExistsRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if Event.objects.filter(pk=1, activate=True):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
