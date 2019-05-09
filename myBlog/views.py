from django.shortcuts import render


# 博客首页
def index(request):
    return render(request, 'myBlog/index.html')
