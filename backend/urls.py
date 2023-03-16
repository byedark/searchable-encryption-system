from django.urls import path
from .views import account,user_attribute

app_name="backend"

urlpatterns = [
  path("login/",account.login,name="login"), # 调用account里的login函数，另一种写法视图函数as_view()
  path("register/",account.register,name="register"),  # 调用account里的register函数，另一种写法视图函数as_view()
  path("dataowner/",account.dataowner,name="dataowner"),  # 调用account里的dataowner函数，另一种写法视图函数as_view()
  path("login_confirm/",account.login_confirm,name="login_confirm"), # 调用account里的dataowner函数，另一种写法视图函数as_view()
  path("logout/",account.logout,name="logout"),
  path("get_user_attribute/",user_attribute.get_user_attribute,name="get_user_attribute"),
  path("delete_user_attribute/",user_attribute.delete_user_attribute,name="delete_user_attribute"),
  path("add_user_attribute/",user_attribute.add_user_attribute,name="add_user_attribute"),
  path("get_own_attribute/",user_attribute.get_own_attribute,name="get_own_attribute"),
]