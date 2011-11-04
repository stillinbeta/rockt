from djangorestframework.mixins import InstanceMixin, ReadModelMixin, AuthMixin
from djangorestframework.views import View, ModelView
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.authentication import BasicAuthentication


class ReadOnlyModelView(ModelView, InstanceMixin, ReadModelMixin):
    _suffix = 'Instance'


class AuthRequiredView(View, AuthMixin):
    authentication = (BasicAuthentication,)
    permissions = (IsAuthenticated,)
