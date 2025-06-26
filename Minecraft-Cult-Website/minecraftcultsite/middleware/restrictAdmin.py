from django.http import HttpResponseRedirect
from django.urls import reverse


class AdminAccessRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print("running middleware")
        if request.path.startswith(reverse('admin:index').rstrip('/')):
            remote_ip = request.META.get("REMOTE_ADDR", "")
            if not remote_ip.startswith("192.168.254"):
                return self.get_response(request)
        return HttpResponseRedirect(reverse('home'))