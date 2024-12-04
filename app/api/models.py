from django.db import models
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

    def get_api(self) -> AmoSession:
        return AmoSession(self.access_token, self.subdomain)
    

class LeadProcessed(models.Model):

    lead_id = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.lead_id}"