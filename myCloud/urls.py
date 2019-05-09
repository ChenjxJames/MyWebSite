from django.urls import path
from myCloud import views

urlpatterns = [
    path('', views.index),    # /cloud 主页
    path('flist', views.get_file_list),    # /cloud/filelist # 获取指定文件夹下的目录
    path('upload', views.upload),    # /cloud/upload 文件上传
    path('download', views.download),    # /cloud/download 文件下载
    path('del', views.del_file),    # /cloud/del 删除文件
    path('setfilename', views.set_file_name),    # /cloud/setfilename 文件（夹）重命名
    path('movefile', views.move_file),    # /cloud/movefile 文件（夹）移动
    path('getinfo', views.get_info),    # /cloud/getinfo 获取文件（夹）详情
    path('about', views.get_about),    # /cloud/about 关于页面
]