from django.contrib import admin
from django.apps import apps

models = apps.get_models()

for model in models:
  try:
    admin.site.register(model)
  except admin.sites.AlreadyRegistered:
    pass

from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
  user = User.objects.create_user('admin', 'admin@admin.com', 'admin', is_staff=True)
