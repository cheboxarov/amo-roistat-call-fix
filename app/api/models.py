from django.db import models


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
    