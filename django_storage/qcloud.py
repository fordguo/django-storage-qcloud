# -*- coding: UTF-8 -*-
import tempfile
from pathlib import Path
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from qcloud_cos import CosConfig, CosS3Client


@deconstructible()
class QcloudStorage(Storage):
    def __init__(self, option=None):
        if not option:
            self.option = settings.QCLOUD_STORAGE_OPTION
        self.config = CosConfig(Region=self.option['Region'], SecretId=self.option['SecretId'],
                                SecretKey=self.option['SecretKey'], Token=self.option.get('Token'))
        self.bucket = self.option['Bucket']

    def _check_url(self, name):
        return name.startswith('http')

    def _open(self, name, mode='rb'):
        if self._check_url(name):
            return b''

        client = CosS3Client(self.config)
        response = client.get_object(self.bucket, name)
        tmpf = Path(tempfile.gettempdir(), name)
        parent = tmpf.parent
        if not parent.exists():
            parent.mkdir(parents=True)
        response['Body'].get_stream_to_file(tmpf)
        return open(tmpf, mode)

    def _save(self, name, content):
        if self._check_url(name):
            return name

        client = CosS3Client(self.config)
        _ = client.put_object(self.bucket, content, name)
        return name

    def exists(self, name):
        if self._check_url(name):
            return True

        client = CosS3Client(self.config)
        response = client.object_exists(self.bucket, name)
        return response

    def url(self, name):
        if self._check_url(name):
            return name

        if getattr(settings, 'COS_URL', ''):
            url = "{}/{}".format(settings.COS_URL, name)
        elif getattr(settings, 'COS_USE_CDN', False):
            url = "https://{}.file.myqcloud.com/{}".format(
                self.bucket, name)
        else:
            url = "https://{}.cos.{}.myqcloud.com/{}".format(
                self.bucket, self.option['Region'], name
            )

        return url

    def size(self, name):
        if self._check_url(name):
            return 0

        client = CosS3Client(self.config)
        response = client.head_object(self.bucket, name)
        return response['Content-Length']

    def delete(self, name):
        if self._check_url(name):
            return

        client = CosS3Client(self.config)
        client.delete_object(self.bucket, name)
