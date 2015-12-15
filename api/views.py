from django.views.generic.base import TemplateView, View
from django.shortcuts import get_object_or_404
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView

from chunked_upload.response import Response
from chunked_upload.exceptions import ChunkedUploadError

import jwt
import json

from api.models import MyChunkedUpload
from meta.models import Metadata
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from uploader.settings import SECRET_KEY
import os


class ChunkedUploadDemo(TemplateView):
    template_name = 'index.html'


class ChunkedUploadView(ChunkedUploadView):

    model = MyChunkedUpload
    field_name = 'the_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class ChunkedUploadedSize(View):

    def get(self, request):
        # Check if file exists
        # print "GET: SIZE"
        response = HttpResponse()
        print request.GET['file']

        upload_id = request.GET.get('uid')
        token = request.GET.get('token')
        try:
            print jwt.decode(token, SECRET_KEY)
        except:
            return Response('Authentication expired', status=401)

        print upload_id
        if upload_id != '':
            # queryset = MyChunkedUpload.objects.all()
            # chunked_uploaded = queryset.filter(upload_id=upload_id)
            chunked_uploaded = get_object_or_404(MyChunkedUpload,
                                                 upload_id=upload_id)
            print chunked_uploaded
            try:
                print chunked_uploaded.file
                print type(chunked_uploaded.file)
                print chunked_uploaded.file.open
                size = chunked_uploaded.file.size
                print 'SIZE is: ' + str(size)
                return Response({'size': size}, status=200)
            except IOError:
                return Response({'size': 0}, status=200)
        else:
            return Response({'size': 0}, status=200)

    def options(request):
        # print "OPTIONS: SIZE"
        response = HttpResponse()
        return Response({'size': 0}, status=200)


class SaveView(ChunkedUploadView):
    field_name = 'file'
    model = MyChunkedUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        print "Everything fine..."
        pass

    def create_chunked_upload(self, save=False, **attrs):
        """
        Creates new chunked upload instance. Called if no 'upload_id' is
        found in the POST data.
        """
        # print "create_chunked_upload..."
        chunked_upload = self.model(**attrs)
        # print chunked_upload
        # file starts empty
        chunked_upload.file.save(name='', content=ContentFile(''), save=save)
        return chunked_upload

    def options(self, request):
        # print "OPTIONS CHUNKS..."
        return Response({'size': 0}, status=200)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        """
        print "POST starts..."
        try:
            token = request.POST.get('token')
            try:
                print jwt.decode(token, SECRET_KEY)
                print "Everything fine..."
            except:
                return Response('Authentication expired', status=401)
            return self._post(request, *args, **kwargs)
            # return Response({}, status=200)
        except ChunkedUploadError as error:
            return Response(error.data, status=error.status_code)


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):

    model = MyChunkedUpload
    do_md5_check = True

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file. E.g.:
        # * Store the uploaded file on another model:
        # SomeModel.objects.create(user=request.user, file=uploaded_file)
        # * Pass it as an argument to a function:
        # function_that_process_file(uploaded_file)
        upload_id = request.POST.get('upload_id')
        metadata = json.loads(request.POST.get('meta'))
        meta_uid = metadata['meta_uid']
        chunked_upload = get_object_or_404(self.get_queryset(request),
                                           upload_id=upload_id)
        chunked_upload.meta_uid = meta_uid
        chunked_upload.save()

    def get_response_data(self, chunked_upload, request):
        upload_id = request.POST.get('upload_id')
        uploaded = get_object_or_404(self.get_queryset(request),
                                           upload_id=upload_id)
        print uploaded
        print uploaded.meta_id
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (uploaded.filename, uploaded.offset)),
                'meta_id': uploaded.meta_id}

    def md5_check(self, chunked_upload, md5):
        """
        Verify if md5 checksum sent by client matches generated md5.
        """
        print chunked_upload.upload_id
        print '...........'
        print md5
        print '...........'
        print chunked_upload.md5
        print '...........'
        print chunked_upload.md5 == md5
        print '...........'
        if chunked_upload.md5 != md5:
            raise ChunkedUploadError(status=400,
                                     detail='md5 checksum does not match')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        """
        try:
            self.check_permissions(request)
            try:
                print jwt.decode(request.POST.get('token'), SECRET_KEY)
            except:
                return Response('Authentication expired', status=401)
            return self._post(request, *args, **kwargs)
        except ChunkedUploadError as error:
            return Response(error.data, status=error.status_code)
