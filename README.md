# searchable_encryption
## 该项目前后端分离，前端采用vue后端Django,实现了简单的可搜索加密。
## 服务器采用ngnix和uwsgi进行搭建
### 网站静态文件也需要收集，在站点处配置
```
location / {
  include uwsgi_params;
  uwsgi_pass 127.0.0.1:9888; #端口要和uwsgi里配置的一样
  uwsgi_param UWSGI_SCRIPT searchable_encryption.wsgi; #wsgi.py所在的目录名+.wsgi
  uwsgi_param UWSGI_CHDIR /www/wwwroot/8.130.40.196/; #项目路径
}
location /static/ {
  alias /www/wwwroot/8.130.40.196/dist/static/; #静态资源路径
}
```
### 收集静态文件命令 python manage.py collectstatic
### ngnix配置
```
location / {
  uwsgi_pass 127.0.0.1:9888;
  # 允许 所有头部 所有域 所有方法
  #允许跨域请求的域，* 代表所有
  add_header 'Access-Control-Allow-Origin' *;
  #允许带上cookie请求
  add_header 'Access-Control-Allow-Credentials' 'true';
  #允许请求的方法，比如 GET/POST/PUT/DELETE
  add_header 'Access-Control-Allow-Methods' *;
  #允许请求的header
  add_header 'Access-Control-Allow-Headers' *;
  # OPTIONS 直接返回204
  if ($request_method = 'OPTIONS') {
    return 204;
  }
}
location /api {
  # 允许 所有头部 所有域 所有方法
  #允许跨域请求的域，* 代表所有
  uwsgi_pass 127.0.0.1:9888;
  add_header 'Access-Control-Allow-Origin' *;
  #允许带上cookie请求
  add_header 'Access-Control-Allow-Credentials' 'true';
  #允许请求的方法，比如 GET/POST/PUT/DELETE
  add_header 'Access-Control-Allow-Methods' *;
  #允许请求的header
  add_header 'Access-Control-Allow-Headers' *;
  # OPTIONS 直接返回204
  if ($request_method = 'OPTIONS') {
    return 204;
  }
}
location /file {
  uwsgi_pass 127.0.0.1:9888;
  # 允许 所有头部 所有域 所有方法
  #允许跨域请求的域，* 代表所有
  add_header 'Access-Control-Allow-Origin' *;
  #允许带上cookie请求
  add_header 'Access-Control-Allow-Credentials' 'true';
  #允许请求的方法，比如 GET/POST/PUT/DELETE
  add_header 'Access-Control-Allow-Methods' *;
  #允许请求的header
  add_header 'Access-Control-Allow-Headers' *;
  # OPTIONS 直接返回204
  if ($request_method = 'OPTIONS') {
    return 204;
  }
}
```
### uwsgi配置
```
# 添加配置选择
[uwsgi]
#配置和nginx连接的socket连接
socket=0.0.0.0:9888
http = 0.0.0.0:8000
#配置项目路径，项目的所在目录
chdir=/www/wwwroot/8.130.40.196/
#配置wsgi接口模块文件路径,也就是wsgi.py这个文件所在的目录
wsgi-file= /www/wwwroot/8.130.40.196/searchable_encryption/wsgi.py
#配置启动的进程数
processes=4
#配置每个进程的线程数
threads=2
#配置启动管理主进程
master=True
#配置存放主进程的进程号文件
pidfile=uwsgi.pid
#配置uwsgi日志记录
daemonize=/www/wwwroot/8.130.40.196/uwsgi_01.log
```
###注意uwsgi和socket之间交互的端口和后端http访问url地址的端口不能一样，许多博客上的做法都会导致出现后端请求接收不到，原因是socket端口无法访问。
