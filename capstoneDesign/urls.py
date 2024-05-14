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
    path('', views.index, name='main_page'),
    path('index2/', views.index2, name='index2'),
    # path('login', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login3.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('common/', include('common.urls')),
    path('test/', views.test),
    path('index2', views.index, name='index_page'),
    path('sign_up/', views.sign_up, name='sign_up_page'),
    path('sign_up_complete/', views.sign_up_complete, ),
    path('memo/', views.add_memo, name='memo'),
    path('delete-memo/', views.delete_memo, name='delete_memo'),
    # path('memo2/', views.add_memo, name='memo'),
    # path('ajax_method/', views.add_memo, name='ajax_method'),
    path('my-ajax-url/', views.my_ajax_view, name='my_ajax_url'),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('edit-memo/', views.edit_memo, name='edit_memo'),
    path('index/', views.index, name='index'),
    path('<int:user_id>/password/', views.update_password, name='update_password'),
    path('history/<int:videoo_id>/', views.history,name='history'),

]

# url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT,  insecure=True)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns+=url(r'^media/(?P<path>.\*)$', serve, {
#     'document_root': settings.MEDIA_ROOT,
# })
