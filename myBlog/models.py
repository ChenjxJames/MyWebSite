from django.db import models


class EssayInfo(models.Model):
    """
    文章信息模型类（文章编号， 文章标题， 文章主体， 文章是否公开， 文章上传时间， 文章所属用户编号）
    """
    eId = models.CharField(max_length=10, null=False, verbose_name='文章编号', primary_key=True)
    eTitle = models.CharField(max_length=64, null=False, verbose_name='文章标题')
    eText = models.TextField(null=False, verbose_name='文章主体')
    eIsPublic = models.BooleanField(null=False, verbose_name='文章是否公开')
    eUploadTime = models.DateTimeField(null=False, verbose_name='文章上传时间')
    eUserId = models.CharField(max_length=10, null=False, verbose_name='文章所属用户编号')
