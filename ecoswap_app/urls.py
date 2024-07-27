from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
# from . import exchangeView


app_name = 'ecoswap_app'

urlpatterns = [
    path('', views.index, name='index'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('item_detail/<int:item_id>/', views.item_detail, name='item_detail'),
    path('create_item/', views.create_item, name='create_item'),
    path('item/<int:item_id>/update/', views.update_item, name='update_item'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('my_items/', views.user_items, name='user_items'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/send/<int:exchange_id>/', views.send_message, name='send_message'),
    path('exchanges/', views.exchange_list, name='exchange_list'),
    path('item/<int:item_id>/request_exchange/', views.request_exchange, name='request_exchange'),
    path('all_accepted_request/', views.all_accepted_request, name='all_accepted_request'),
    path('exchange_requests/', views.user_exchange_requests, name='user_exchange_requests'),
    path('exchange/<int:exchange_id>/accept/', views.accept_request, name='accept_request'),
    path('exchange/<int:exchange_id>/reject/', views.reject_request, name='reject_request'),
    path('exchange/<int:exchange_id>/create_transaction/', views.create_transaction, name='create_transaction'),
    path('item/<int:item_id>/request_exchange/', views.request_exchange, name='request_exchange'),
]