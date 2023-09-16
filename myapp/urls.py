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
    # path('signout/', views.logoutUser, name="signout"),
    # path('activate_user/<uidb64>/<token>', views.activate_user, name="activate"),
    # path('auth', views.activate_user, name="activate"),

    #   PassWord Reset Urls 
    # path('reset_password/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='reset_password'),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),
    # path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),name='password_reset_confirm'),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_complete'),
    # path('auth/', TokenObtainPairView.as_view(), name='login_view'),
    path('merge-csv/', MergeCSV.as_view(), name='merge-csv'),
    
    
    


   
]