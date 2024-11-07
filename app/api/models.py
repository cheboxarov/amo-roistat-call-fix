from django.db import models
from .amo_api import get_tokens_by_refresh
from py_amo.services import AmoSession


class AmoWidget(models.Model):

    client_id = models.TextField()
    client_secret = models.TextField()


class AmoProject(models.Model):
    subdomain = models.CharField(max_length=255)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    widget = models.ForeignKey(to=AmoWidget, on_delete=models.CASCADE)


    def __str__(self):
        return self.subdomain
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["subdomain", "widget"], name="subdomain_widget_unique")
        ]
    
    def update_tokens(self):
        widget = self.widget
        response = get_tokens_by_refresh(widget.client_id, widget.client_secret, self.refresh_token, self.subdomain)
        self.access_token = response.get("access_token")
        self.save()

    def get_api(self) -> AmoSession:
        return AmoSession(self.access_token, self.subdomain)