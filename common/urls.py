from django.conf import settings
from django.conf.urls.static import static

app_name = 'common'

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.views.static import serve

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login2/', views.signup2),
    # path('memo/', views.add_memo, name='memo'),
    path('update/', views.update, name='update'),
    path('1/password/', views.update_password, name='update_password'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
