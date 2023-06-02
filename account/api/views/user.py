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
from basket.api.serializers import (
    CartSerializer,
    PackCartSerializer
)

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

    @action(detail=True, methods=['GET', 'POST'])
    def carts(self, request, phone_number=None, *args, **kwargs):
        user = self.get_object()
        user_cart = user.get_cart()
        payload = request.data

        if request.method == 'GET':
            serializer = CartSerializer(user_cart, many=False)
            status_code = status.HTTP_200_OK
        elif request.method == 'POST':
            pack_serializer = PackCartSerializer(data=payload, many=True)
            pack_serializer.is_valid(raise_exception=True)
            pack_serializer.save()
            serializer = CartSerializer(user_cart, many=False)
            status_code = status.HTTP_201_CREATED
        else:
            raise exceptions.MethodNotAllowed()
        return Response(
            serializer.data,
            status=status_code
        )
