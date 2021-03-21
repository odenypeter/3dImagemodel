from django.contrib import admin
from .models import *

"""
Register models to admin console
To see the admin console
run: python manage.py createsuperuser
then follow the prompts and login at http://localhost:8000/admin
"""


@admin.register(GeneratedFile)
class GeneratedFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file',)


@admin.register(Image)
class GeneratedFileAdmin(admin.ModelAdmin):
    list_display = ('generated_file', 'image',)
    list_filter = ('generated_file',)
