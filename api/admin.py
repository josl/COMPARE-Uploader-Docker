from django.contrib import admin

# Register your models here.
from .models import MyChunkedUpload


class MyChunkedUploadAdmin(admin.ModelAdmin):
    class Meta:
        model = MyChunkedUpload

admin.site.register(MyChunkedUpload, MyChunkedUploadAdmin)
