from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from form_checker.services import ProcessTypeValidationChain


@method_decorator(csrf_exempt, name='dispatch')
class GetFormView(View):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args, **kwargs):
        sending_form = {}
        for key, value in request.POST.items():
            validation_result = ProcessTypeValidationChain(value).get_data_dto()
            sending_form.update({key: validation_result.data_type.value})
        print(sending_form)
        return JsonResponse(sending_form)
