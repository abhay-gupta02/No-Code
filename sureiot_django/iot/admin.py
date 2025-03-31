from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Project, Activity, Report, UserGroup

admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Activity)
admin.site.register(Report)
admin.site.register(UserGroup)

#random text