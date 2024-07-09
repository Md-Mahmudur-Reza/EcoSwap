from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


app_name = 'ecoswap_app'

urlpatterns = [
    path('', views.index, name='index'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('item/<int:item_id>/', views.item_detail, name='item_detail'),

]