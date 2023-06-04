from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin


User = get_user_model()


class GetIPMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if request.user.is_authenticated:
            request.user.ip_address = ip
        else:
            request.user.ip_address_anon = ip
        response = self.get_response(request)
        return response


def get_request_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
