from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import exceptions
from rest_framework.renderers import (
    BrowsableAPIRenderer,
)
from rest_framework.permissions import (
    IsAuthenticated,
    DjangoModelPermissions
)
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.mixins import RetrieveModelMixin

from painless.api.exceptions import BadRequest
from painless.api.renderers import DataStatusMessage_Renderer
from account.api.serializers import UserSerializer


User = get_user_model()

class UserViewSet(
    RetrieveModelMixin,
    GenericViewSet
    ):

    lookup_field = 'phone_number'
    lookup_url_kwarg = 'phone_number'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions
    )
    renderer_classes = [
        BrowsableAPIRenderer,
        DataStatusMessage_Renderer
    ]
    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(),    
            phone_number=self.kwargs["phone_number"]
        )
        if self.request.user.phone_number == obj.phone_number:
            self.check_object_permissions(self.request, obj)
        else:
            if settings.DEBUG:
                status_code = HTTP_403_FORBIDDEN
                raise exceptions.PermissionDenied()
            else:
                status_code = HTTP_404_NOT_FOUND
                raise exceptions.NotFound()
        return obj

