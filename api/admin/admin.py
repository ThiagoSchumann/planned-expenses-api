from django.contrib import admin
from django.apps import apps

models = apps.get_models()

exclude_models = []

for model in models:
    try:
        if model not in exclude_models:
            admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
