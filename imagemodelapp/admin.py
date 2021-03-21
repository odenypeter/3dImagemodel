from django.contrib import admin
from .models import *


@admin.register(GeneratedFile)
class GeneratedFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file',)


@admin.register(Image)
class GeneratedFileAdmin(admin.ModelAdmin):
    list_display = ('generated_file', 'image',)
    list_filter = ('generated_file',)
