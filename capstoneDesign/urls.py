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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.urls import re_path

import manage
import views
from views import sign_up_complete
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('', views.index, name='main_page'),
    path('index2/', views.index2, name='index2'),
    #path('index2/', views.index2, name='index2_page'),
    # path('login', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login3.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('common/', include('common.urls')),
    path('test/', views.test),
    path('index2', views.index, name='index_page'),
    path('sign_up/', views.sign_up, name='sign_up_page'),
    path('sign_up_complete/', views.sign_up_complete, ),


    #메모 관련
    path('add-memo/<str:video_id>/', views.add_memo, name='add_memo'),
    path('delete-memo/', views.delete_memo, name='delete_memo'),
    path('list-memo/<str:video_id>/', views.list_memo, name='list_memo'), #메모 보기
    path('edit-memo/', views.edit_memo, name='edit_memo'),



    path('index/', views.index, name='index'),
    path('<int:user_id>/password/', views.update_password, name='update_password'),
    path('history/<int:video_pk>/', views.history, name='history'),
    path('delete_history/<int:video_pk>/', views.delete_history, name='delete_history'),
    path('delete_history_All/', views.delete_history_All, name='delete_history_All'),

    path('question/<str:video_id>/', views.question, name='question'),

]

# url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT,  insecure=True)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns+=url(r'^media/(?P<path>.\*)$', serve, {
#     'document_root': settings.MEDIA_ROOT,
# })