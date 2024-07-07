from django.contrib import admin
from .models import User, Item, Exchange, Transaction, Message

@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name"]

@admin.register(Item)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["item_name", "user", "item_condition"]

@admin.register(Exchange)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["offered_by_user", "offered_item", "requested_by_user", "requested_item","created_at","status"]

@admin.register(Transaction)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["exchange", "amount", "transaction_date"]

@admin.register(Message)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["exchange", "sender_user", "receiver_user", "message_text", "sent_at"]

