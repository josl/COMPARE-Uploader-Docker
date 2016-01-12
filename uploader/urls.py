"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin

from api.views import (
    ChunkedUploadDemo, MyChunkedUploadCompleteView,
    SaveView, ChunkedUploadedSize
)

from meta.views import SendData, SendFile, SaveMeta
from token_auth.views import Refresh

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',
        ChunkedUploadDemo.as_view(), name='chunked_upload'),

    url(r'^admin/', admin.site.urls),

    url(r'^login/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^token/refresh/', Refresh.as_view(), name='refres_token'),
    url(r'^api/save/?$',
        MyChunkedUploadCompleteView.as_view(),
        name='api_chunked_upload_complete'),
    url(r'^api/chunks/?$', SaveView.as_view(),
        name='api_chunked_upload_save'),
    url(r'^api/size/?$', ChunkedUploadedSize.as_view(),
        name='api_chunked_upload_size'),

    url(r'^api/data/?$', SendData.as_view(),
        name='api_chunked_upload_data'),
    url(r'^api/meta/save/?$', SaveMeta.as_view(),
        name='api_chunked_upload_data'),
    url(r'^api/file/?$', SendFile.as_view(),
        name='api_chunked_upload_data'),

    url(r'^static/(.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': False}),
)
