MyWebSite
----------------
The project consists of three modules.
* MyBlog
* MyCloud
* MyUsers


----------------
_中文_

我的个人网站
----------------
该项目由三个模块组成：
* 我的博客MyBlog
* 我的云盘MyCloud
* 用户管理MyUsers

### 运行指南（Windows）：
1. 安装python3.5.2；
2. 安装依赖：  
   在本目录下执行`pip install -r package.txt`命令安装项目所需依赖。
3. 连接数据库：  
   安装mysql，更改./MyWebSite/settings.py中DATABASES的参数连接数据库；  
   连接其他数据库如SQL server还需要更改./MyWebSite/\_\_init\_\_.py下的数据库模块引用。
4. 创建数据表：  
   执行`python manage.py makemigrations`命令生成迁移；  
   执行`python manage.py migrate`命令执行迁移（创建数据表）；  
6. 运行：  
   执行`python manage.py runserver 0:8000`命名运行项目（0为0.0.0.0的简写，端口8000）。
7. 浏览器url栏输入localhost:8000即可访问。

[Ubuntu apache2下部署本项目](https://www.chenjianxiong.cn/index.php/2018/11/13/ubuntu16_04_apache2_bu_shu_django2_xiang_mu/)




