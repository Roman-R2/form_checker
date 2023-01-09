from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class GetFormView(View):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args, **kwargs):
        print(*args, **kwargs)
        print(request.POST)
        return JsonResponse({"status": "error"})
