import time

from django.db import models


class FileInfo(models.Model):
    """
    文件信息模型类（文件编号， 文件名， 文件所在父文件夹编号， 是否为文件夹， 文件上传时间， 文件（路径），文件后缀，文件md5码， 文件所属的用户编号）
    """
    def user_directory_path(self, *args, **kwargs):
        return 'cloud_files/user_{0}/{1}/{2}'.format(self.fUserId,
                                                     time.strftime('%Y/%m/%d', time.localtime(time.time())), self.fId)

    fId = models.CharField(max_length=10, null=False, verbose_name='文件编号', primary_key=True)
    fName = models.CharField(max_length=255, null=False, verbose_name='文件名')
    fFolderId = models.CharField(max_length=10, null=False, verbose_name='文件所在父文件夹编号')
    fIsFolder = models.BooleanField(null=False, verbose_name='是否为文件夹')
    fUploadTime = models.DateTimeField(auto_now_add=True, null=False, verbose_name='文件上传时间')
    fFile = models.FileField(upload_to=user_directory_path, blank=True, null=True,
                             verbose_name='文件（路径）')
    fExtension = models.CharField(max_length=10, blank=True, null=True, verbose_name='文件后缀')
    fmd5 = models.CharField(max_length=32, blank=True, null=True, verbose_name='文件md5码')
    fUserId = models.CharField(max_length=10, null=False, verbose_name='文件所属的用户编号')


class FileTypeInfo(models.Model):
    """
    文件类型模型类（文件后缀，文件类型）
    """
    fExtension = models.CharField(max_length=10, null=False, verbose_name='文件后缀', primary_key=True)
    fType = models.CharField(max_length=16, null=False, verbose_name='文件类型')