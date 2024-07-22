# from django.shortcuts import render, redirect
# from .models import User, Item, Exchange, Transaction, Message
# from .forms import CustomUserCreationForm, CustomAuthenticationForm, ItemForm, ExchangeForm, TransactionForm
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
# from django.contrib import messages
# #chatbox
# from django.contrib.auth import get_user_model
# from .models import Exchange, Message
# from .forms import MessageForm
#
# from django.urls import reverse
#
#
# @login_required(login_url='ecoswap_app:login')
# def request_exchange(request, item_id):
#     requested_item = get_object_or_404(Item, id=item_id)
#     if requested_item.user == request.user:
#         messages.error(request, "You cannot request your own item.")
#         return redirect('item_detail', item_id=item_id)
#
#     if request.method == 'POST':
#         form = ExchangeForm(request.POST, user=request.user)
#         if form.is_valid():
#             exchange = form.save(commit=False)
#             exchange.requested_item = requested_item
#             exchange.offered_by_user = request.user
#             exchange.requested_by_user = requested_item.user
#             exchange.save()
#             messages.success(request, 'Exchange request sent successfully.')
#             return redirect('ecoswap_app:item_detail', item_id=item_id)
#     else:
#         form = ExchangeForm(user=request.user)
#
#     context = {
#         'form': form,
#         'requested_item': requested_item
#     }
#     return render(request, 'ecoswap_app/request_exchange.html', context)
#
#
# @login_required(login_url='ecoswap_app:login')
# def create_transaction(request, exchange_id):
#     exchange = get_object_or_404(Exchange, id=exchange_id)
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             transaction = form.save(commit=False)
#             transaction.exchange = exchange
#             transaction.save()
#
#             # Mark the items as exchanged
#             exchange.offered_item.item_status = 'Exchanged'
#             exchange.offered_item.save()
#             exchange.requested_item.item_status = 'Exchanged'
#             exchange.requested_item.save()
#
#             # Update exchange status
#             exchange.status = 'Completed'
#             exchange.save()
#
#             messages.success(request, 'Transaction completed successfully.')
#             return redirect('ecoswap_app:index')
#     else:
#         form = TransactionForm(initial={
#             'paid_by_user': exchange.offered_by_user,
#             'received_by_user': exchange.requested_by_user
#         })
#     return render(request, 'ecoswap_app/create_transaction.html', {'form': form})