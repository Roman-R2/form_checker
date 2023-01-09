from django.urls import path

from form_checker.views import GetFormView

app_name = 'form_checker'

urlpatterns = [
    path('get_form/', GetFormView.as_view(), name='get_form'),
]
