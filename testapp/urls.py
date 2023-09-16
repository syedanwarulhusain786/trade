# from .views import RegisterAPI
from django.urls import path
from .views import *

from . import views
from django.contrib.auth import views as auth_views

from django.utils.translation import gettext as _
from myapp.views import *

from django.urls import path,include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('', views.test, name='test'),
    path('upload_file/', views.upload_file, name='upload_file'),
    
    
    


   
]