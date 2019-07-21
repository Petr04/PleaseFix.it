from django.contrib import admin


# Register your models here.

from .models import Problem, UserProfile

admin.site.register(Problem)
admin.site.register(UserProfile)
