from django.http import HttpResponseRedirect

class TrailingSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.endswith('/'):
            return HttpResponseRedirect(request.path + '/')
        return self.get_response(request)
