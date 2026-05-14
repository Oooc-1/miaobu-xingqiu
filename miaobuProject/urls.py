"""miaobuProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homeApp.views import home
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),#首页
    path('aboutApp/',include('aboutApp.urls')),#关于我们
    path('contactApp/',include('contactApp.urls')),#呼叫我们
    path('mapApp/',include('mapApp.urls')),#漫步地图
    path('newsApp/',include('newsApp.urls')),#猫眼世界
    path('noteApp/',include('noteApp.urls')),#铲屎官笔记
    path('shopApp/',include('shopApp.urls')),#肉垫体验
    
]
