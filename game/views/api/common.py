from djangorestframework.mixins import AuthMixin
from djangorestframework.views import View, ModelView
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.authentication import BasicAuthentication


class AuthRequiredView(View, AuthMixin):
    authentication = (BasicAuthentication,)
    permissions = (IsAuthenticated,)
