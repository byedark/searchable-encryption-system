from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from backend.models import User, EncryptFile
from config.config import SUCCESS, ERROR
from .pb_fun import judge_user

# 日志对象
from config.logger import logger_backend


# 登录的后端相应文件
def login(request):
  user_response = judge_user(request)
  # 数据库里找不到，直接返回一个None
  if type(user_response) != User:
    return JsonResponse(user_response)
  # 把对象赋值给使用者
  user = user_response
  if user.dataowner == True:
    #数据拥有者不能在使用者处登录
    response = JsonResponse({
      "status": ERROR,
      "dataowner": True
    })
  else:
    # 可以登录
    response = JsonResponse({
      "status": SUCCESS,
      "dataowner": False
    })
  #DEBUG
  logger_backend.debug("用户:{} 登录 dataowner={}".format(user.username,user.dataowner))
  return response


#注册的后端响应文件
def register(request):
  if request.method != "POST":
    return JsonResponse({
      "status":ERROR,
      "information":"请求方式错误"
    })
  username = request.POST["username"]
  password = request.POST["password"]
  try:
    User.objects.get(username=username)
  except User.DoesNotExist:
    user = User(username=username,password=password)
    user.save()
  else:
    return JsonResponse({"status":ERROR,"information":"用户名重复"})
  # debug时偷看一下
  logger_backend.debug("用户:{} 注册 password={}".format(username,password))
  return JsonResponse({"status":SUCCESS})


# 登录确定的相应文件
def login_confirm(request):
  user_response = judge_user(request)
  if type(user_response) != User:
    return JsonResponse(user_response)
  user = user_response
  response = {
    "status":SUCCESS
  }
  if user.dataowner == True:
    response["dataowner"] = True
  else:
    response["dataowner"] = False
  if EncryptFile.objects.count() > 0:
    response["builded"] = True
  else:
    response["builded"] = False
  return JsonResponse(response)


# 登出文件
def logout(request):
  user_response = judge_user(request)
  if type(user_response) != User:
    return JsonResponse(user_response)

  response = JsonResponse({
    "status":SUCCESS
  })

  response.set_cookie("searchable_encryption_username","",max_age=-1)
  response.set_cookie("searchable_encryption_password","",max_age=-1)

  return response


def dataowner(request):
  # 对前端发来的JSON数据进行判断
  print("有移动端登录")
  user_response = judge_user(request)
  if type(user_response) != User:
    return JsonResponse(user_response)
  user = user_response
  if user.dataowner == True:
    response = JsonResponse({
      "status": SUCCESS,
      "dataowner": True
    })
  else:
    response = JsonResponse({
      "status": ERROR,
      "dataowner": False
    })
  # debug
  logger_backend.debug("用户:{} 登录 dataowner={}".format(user.username, user.dataowner))
  return response
