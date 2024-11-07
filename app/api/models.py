from django.db import models


class AmoProject(models.Model):
    subdomain = models.CharField(max_length=255)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.subdomain
    

class AmoWidget(models.Model):

    client_id = models.TextField()
    client_secret = models.TextField()