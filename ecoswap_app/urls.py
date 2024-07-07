from django.urls import path

from . import views

app_name = 'ecoswap_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),

]