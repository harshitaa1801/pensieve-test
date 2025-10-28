from django.urls import path
from . import views

app_name = "dive"

urlpatterns = [
    path("test/raise-500/", views.raise_500, name="raise_500"),
    path("test/delay/", views.delay_random, name="delay_random"),
    path("test/instant/", views.instant, name="instant"),
    path("test/status/", views.status_json, name="status_json"),
    path("test/cpu/", views.cpu_work, name="cpu_work"),
    path("test/raise-nested/", views.nested_error, name="raise_nested"),
    path("test/raise-chain/", views.chained_error, name="raise_chained"),
    path("test/raise-key/", views.key_error_in_helper, name="raise_key"),
    path("test/bad-request/", views.bad_request, name="bad_request"),
    path("test/not-found/", views.not_found, name="not_found"),
]
