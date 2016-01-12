from django.contrib import admin

# Register your models here.
from .models import Metadata


class MetadataAdmin(admin.ModelAdmin):
    class Meta:
        model = Metadata

admin.site.register(Metadata, MetadataAdmin)
