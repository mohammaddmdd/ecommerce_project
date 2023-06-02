from rest_framework.serializers import HyperlinkedModelSerializer

from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        lookup_field = 'phone_number'
        fields = (
            'url',
            'phone_number',
            'email',
            'first_name',
            'last_name',
        )

        extra_kwargs = {
            'url': {"lookup_field": 'phone_number'},
        }
