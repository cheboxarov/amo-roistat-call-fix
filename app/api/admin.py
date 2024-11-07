from django.contrib import admin
from .models import AmoProject, AmoWidget


admin.site.register(AmoWidget)
admin.site.register(AmoProject)