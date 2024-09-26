from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login_view', views.login_view, name='login_view'),
    path('register_view', views.register_view, name='register_view'),
    path('home', views.home, name='home'),
    path('account', views.account, name='account'),
    path('register_user', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user/'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('pic_upload', views.pic_upload, name='pic_upload'),
    path('profile_upload', views.profile_update, name='profile_upload'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)