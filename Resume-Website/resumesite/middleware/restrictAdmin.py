from django.http import HttpResponseRedirect
from django.urls import reverse


class AdminAccessRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print("running middleware")
        if request.path.startswith(reverse('admin:index').rstrip('/')):
            remote_ip = request.META.get("REMOTE_ADDR", "")
            if remote_ip.startswith("192.168.254") or remote_ip.startswith("127.0.0.1"):
                return self.get_response(request)
            return HttpResponseRedirect(reverse('home'))
        return self.get_response(request)