from django.urls import path
from .views import AmoWebhookView, AmoInstallWidgetWebhookView



urlpatterns = [
    path("amo-wh/", AmoWebhookView.as_view()),
    path("install/", AmoInstallWidgetWebhookView.as_view())
]
