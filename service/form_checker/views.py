from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from form_checker.services import (FindSuitableFormInDB,
                                   ProcessTypeValidationChain)


@method_decorator(csrf_exempt, name='dispatch')
class GetFormView(View):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args, **kwargs):
        sending_form = {}
        # Validate form field types
        for key, value in request.POST.items():
            validation_result = ProcessTypeValidationChain(value).get_data_dto()
            sending_form.update({key: validation_result.data_type.value})
        # Looking for a suitable form in the database
        form_from_db = FindSuitableFormInDB(form_canvas=sending_form).conclusion()

        return JsonResponse(sending_form) if form_from_db is None else JsonResponse({'name': form_from_db['name']})
