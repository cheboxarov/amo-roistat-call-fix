from django.contrib import admin
from .models import AmoProject, AmoWidget, LeadProcessed


admin.site.register(AmoWidget)
admin.site.register(AmoProject)
admin.site.register(LeadProcessed)