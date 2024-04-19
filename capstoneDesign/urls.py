"""capstoneDesign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views

import manage
import views
from views import sign_up_complete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main_page'),
    path('index2/', views.index2, name='index2_page'),
    # path('login', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login3.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('common/', include('common.urls')),
    path('test/', views.test),
    path('index2', views.index, name='index_page'),
    path('sign_up/', views.sign_up, name='sign_up_page'),
    path('sign_up_complete/', views.sign_up_complete, ),
    path('memo/', views.add_memo, name='memo'),

    # path('ajax_method/', views.add_memo, name='ajax_method'),
    path('my-ajax-url/', views.my_ajax_view, name='my_ajax_url'),
    path('my-ajax-url/', views.my_ajax_delete, name='my_ajax_delete')

]
