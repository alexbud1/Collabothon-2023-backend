from django.contrib import admin

from .models import *

for model in [User, Participant, Parent, Child, ChatFile, Survey]:
    admin.site.register(model)
