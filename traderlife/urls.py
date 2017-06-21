"""traderlife URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView

from sign import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hubsite/index/', views.index2),
    url(r'^index', views.index),
    url(r'^login_action/$',views.login_action),
    # url(r'^event_manage', views.event_manage),
    url(r'^accounts/login/$', views.index),
    url(r'^gamepage', views.gamepage),
    url(r'^getOrder',views.getOrder), # 获取订单的ajax
    url(r'^updateWareHouse',views.updateWarehouse), # 更新warehouse ajax
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')), # 设置favicon

]
