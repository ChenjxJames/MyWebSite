import os
import time
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.utils.http import urlquote

from base import MD5
from myCloud import models
from myUsers.views import is_login, get_username, get_userid


# MyCloud主页
# 通过函数修饰器限定用户必须登录访问
@is_login
def index(request):
    return render(request, "myCloud/index.html")


# 获取指定文件夹的目录
# 通过函数修饰器限定用户必须登录访问
@is_login
def get_file_list(request):
    if request.method == "POST":
        jsonStr = []
        user_id = get_userid(request)
        try:
            fId = int(request.POST.get('fFolderId'))
            objs = models.FileInfo.objects.filter(fFolderId=fId, fUserId=user_id)
            if objs:
                data = []
                for obj in objs:
                    fType = ""
                    if models.FileTypeInfo.objects.filter(fExtension=obj.fExtension):
                        fType = models.FileTypeInfo.objects.get(fExtension=obj.fExtension).fType
                    data.append({'fId': obj.fId,
                                 'fName': obj.fName,
                                 'fIsFolder': obj.fIsFolder,
                                 'fExtension': obj.fExtension,
                                 'fType': fType})
                data.sort(key=lambda x: x['fName'])  # 通过文件名将文件（夹）列表升序排序
                data.sort(key=lambda x: x['fIsFolder'], reverse=True)  # 通过是否为文件夹将文件（夹）列表降序排序
                jsonStr = [{'state': '0', 'info': '检索成功!'}, data]
            elif models.FileInfo.objects.filter(fId=fId, fUserId=user_id):
                jsonStr = [{'state': '1', 'info': '文件夹为空!'}]
            elif fId == 0:
                jsonStr = [{'state': '1', 'info': '您还没有上传过文件!'}]
            else:
                jsonStr = [{'state': '-2', 'info': '文件检索错误!'}]
        except ValueError as err:
            print(err)
            jsonStr = [{'state': '-1', 'info': '参数错误!'}]
        except Exception as err:
            print(err)
            jsonStr = [{'state': '-3', 'info': '服务器错误!'}]
        finally:
            return JsonResponse(jsonStr, safe=False)


# 文件上传（及新建文件夹）
# 通过函数修饰器限定用户必须登录访问
@is_login
def upload(request):
    if request.method == "POST":
        # try:
        fileInfo = models.FileInfo()
        fileInfo.fName = request.POST.get('filename', None)
        fileInfo.fFolderId = request.POST.get('fFolderId', None)
        fileInfo.fIsFolder = bool(request.POST.get('fIsFolder', None))
        fileInfo.fUserId = get_userid(request)
        fId = time.strftime('%Y%m%d', time.localtime(time.time())) + "00"
        while True:
            if len(models.FileInfo.objects.filter(fId=fId)) == 0:
                break
            fId = str(int(fId) + 1)
        fileInfo.fId = fId
        # 判断该目录下是否有同名文件（允许一个文件夹和一个文件同名）
        if models.FileInfo.objects.filter(fName=fileInfo.fName,
                                          fFolderId=fileInfo.fFolderId,
                                          fIsFolder=fileInfo.fIsFolder,
                                          fUserId=fileInfo.fUserId):
            jsonStr = {'state': '-2', 'info': '文件上传失败，有同名文件！'}
        else:
            if not fileInfo.fIsFolder:  # 对于文件，需要上传文件本身，提取文件后缀，计算文件md5码
                fileInfo.fFile = request.FILES.get('inputfile', None)
                fileInfo.fExtension = fileInfo.fFile.name.split('.')[-1].lower()  # 获取文件后缀
                fileInfo.save()
                filePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                        'upload/',
                                        fileInfo.fFile.url)
                fileInfo.fmd5 = MD5.get_file_md5(filePath)
            fileInfo.save()
            jsonStr = {'state': '0', 'info': '文件上传成功'}
        # except Exception as err:
            # print(err)
            # jsonStr = {'state': '-4', 'info': '服务器错误!'}
        return JsonResponse(jsonStr, safe=False)


# 文件下载
# 通过函数修饰器限定用户必须登录访问
@is_login
def download(request):
    if request.method == "GET":
        try:
            fId = request.GET.get("fId", None)
            if models.FileInfo.objects.filter(fId=fId):  # 检索文件信息
                obj = models.FileInfo.objects.get(fId=fId)
                if obj.fUserId == get_userid(request):  # 判断文件是否属于该用户
                    filePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                            'upload/',
                                            obj.fFile.url)
                    file = open(filePath, 'rb')
                    response = FileResponse(file)
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = 'attachment;filename=' + urlquote(
                        obj.fName + '.' + obj.fExtension)
                    return response
                else:
                    jsonStr = {'state': '-2', 'info': '您没有访问该文件的权限！'}
            else:
                jsonStr = {'state': '-1', 'info': '参数错误！'}
        except Exception as err:
            print(err)
            jsonStr = {'state': '-4', 'info': '服务器错误！'}

        return JsonResponse(jsonStr, safe=False)


# 删除文件(夹)
# 通过函数修饰器限定用户必须登录访问
@is_login
def del_file(request):
    if request.method == "POST":
        fId = request.POST.get('fId', None)
        try:
            obj = models.FileInfo.objects.get(fId=fId)  # 检索文件信息
            if obj.fUserId == get_userid(request):  # 判断文件（夹）是否属于该用户

                # inner函数用于进行删除操作（文件对象），其中遇文件夹对象进行递归删除
                def del_file_inner(file_obj):
                    if file_obj.fIsFolder:  # 若对象为文件夹，则递归删除文件夹下所有文件（夹）
                        objs = models.FileInfo.objects.filter(fFolderId=file_obj.fId)
                        if objs:
                            for f_obj in objs:
                                del_file_inner(f_obj)
                    else:  # 若对象为文件，则删除文件
                        filePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                'upload/',
                                                file_obj.fFile.url)
                        os.remove(filePath)
                    file_obj.delete()  # 删除文件对象

                del_file_inner(obj)  # 调用inner函数
                jsonStr = {'state': '0', 'info': '删除成功！'}
            else:
                jsonStr = {'state': '-2', 'info': '您没有访问该文件的权限！'}
        except Exception as err:
            print(err)
            jsonStr = {'state': '-4', 'info': '服务器错误！'}

        return JsonResponse(jsonStr, safe=False)


# 更改文件（夹）名称
# 通过函数修饰器限定用户必须登录访问
@is_login
def set_file_name(request):
    if request.method == "POST":
        try:
            fId = request.POST.get('fId', None)
            fName = request.POST.get('fName', None)
            if fName:  # 检索文件信息 and 新的文件名不能为空
                obj = models.FileInfo.objects.get(fId=fId)
                if obj.fUserId == get_userid(request):  # 判断文件是否属于该用户
                    obj.fName = fName
                    obj.save()
                    jsonStr = {'state': '0', 'info': '文件名更改成功！'}
                else:
                    jsonStr = {'state': '-2', 'info': '您没有访问该文件的权限！'}
            else:
                jsonStr = {'state': '-1', 'info': '参数错误！'}
        except Exception as err:
            print(err)
            jsonStr = {'state': '-4', 'info': '服务器错误！'}

        return JsonResponse(jsonStr, safe=False)


# 移动文件位置（更改数据库中文件对象的父文件夹ID）
# 通过函数修饰器限定用户必须登录访问
@is_login
def move_file(request):
    if request.method == "POST":
        fFolderId = int(request.POST.get('fFolderId', None))
        fIdList = request.POST.getlist('fIdList', None)
        if (models.FileInfo.objects.filter(fId=fFolderId) or fFolderId == 0) and len(fIdList):  # 检索文件夹信息（判断该文件夹是否存在）
            count = 0
            for fId in fIdList:
                obj = models.FileInfo.objects.get(fId=fId)  # 检索文件信息
                if obj.fUserId == get_userid(request):  # 判断文件是否属于该用户
                    obj.fFolderId = fFolderId
                    obj.save()
                    count += 1
            if count == len(fIdList):
                jsonStr = {'state': '0', 'info': '文件移动成功！'}
            elif count > 0:
                jsonStr = {'state': '-2', 'info': '部分文件移动失败！'}
            else:
                jsonStr = {'state': '-3', 'info': '全部文件移动失败！'}
        else:
            jsonStr = {'state': '-1', 'info': '参数错误！'}
        return JsonResponse(jsonStr, safe=False)


# 获取文件信息
# 通过函数修饰器限定用户必须登录访问
@is_login
def get_info(request):
    if request.method == "POST":
        fId = request.POST.get('fId', None)
        try:
            obj = models.FileInfo.objects.get(fId=fId)  # 检索文件信息
            if obj.fUserId == get_userid(request):  # 判断文件是否属于该用户
                fType = ''
                if obj.fExtension:
                    fType = models.FileTypeInfo.objects.get(fExtension=obj.fExtension).fType
                data = {'name': obj.fName,
                        'isFolder': obj.fIsFolder,
                        'type': fType,
                        'extension': obj.fExtension,
                        'md5': obj.fmd5,
                        'uploadTime': obj.fUploadTime,
                        'username': get_username(request)}
                jsonStr = [{'state': '0', 'info': '文件名更改成功！'}, data]
            else:
                jsonStr = {'state': '-2', 'info': '您没有访问该文件的权限！'}
        except Exception as err:
            print(err)
            jsonStr = {'state': '-1', 'info': '参数错误！'}

        return JsonResponse(jsonStr, safe=False)


# 关于MyCloud
# 通过函数修饰器限定用户必须登录访问
@is_login
def get_about(request):
    return render(request, "myCloud/about.html")
