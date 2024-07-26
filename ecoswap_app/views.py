from django.shortcuts import render, redirect
from .models import User, Item, Exchange, Transaction, Message
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ItemForm, ExchangeForm, TransactionForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
#chatbox
from django.contrib.auth import get_user_model
from .models import Exchange, Message
from .forms import MessageForm

from django.urls import reverse

CATEGORIES = [
    {'id': 1, 'name': 'Vehicle'},
    {'id': 2, 'name': 'Electronics'},
    {'id': 3, 'name': 'Furniture'},
    {'id': 4, 'name': 'Clothing'},
    {'id': 5, 'name': 'Books'},
    {'id': 6, 'name': 'Home Appliances'},
    {'id': 7, 'name': 'Toys'},
    {'id': 8, 'name': 'Sports Equipment'},
    {'id': 9, 'name': 'Jewelry'},
    {'id': 10, 'name': 'Collectibles'},
    {'id': 11, 'name': 'Others'},
]

def index(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    items = Item.objects.all().order_by('-created_at')
    
    if query:
        items = items.filter(item_name__icontains=query)

    if category_id:
        category = (CATEGORIES[int(category_id)-1])
        items = items.filter(item_category=category['name'])
    
    context = {
        'items': items,
        'query': query,
        'categories': CATEGORIES,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'ecoswap_app/index.html', context)


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    context = {'item': item}
    return render(request, 'ecoswap_app/item_details.html', context)


@login_required(login_url='ecoswap_app:login')
def user_items(request):
    items = Item.objects.filter(user=request.user).order_by('-created_at')
    context = {'items': items}
    return render(request, 'ecoswap_app/user_items.html', context)


@login_required(login_url='ecoswap_app:login')
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Item created successfully.')
            return redirect('ecoswap_app:item_detail', item_id=item.id)    # Redirect to a page showing the list of items or item details
    else:
        form = ItemForm()
    return render(request, 'ecoswap_app/create_item.html', {'form': form})


@login_required(login_url='ecoswap_app:login')
def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('ecoswap_app:item_detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'ecoswap_app/update_item.html', {'form': form, 'item': item})

@login_required(login_url='ecoswap_app:login')
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully.')
        return redirect('ecoswap_app:user_items')  # Redirect to the user's items page
    return render(request, 'ecoswap_app/confirm_delete.html', {'item': item})


@login_required(login_url='ecoswap_app:login')
def request_exchange(request, item_id):
    requested_item = get_object_or_404(Item, id=item_id)
    if requested_item.user == request.user:
        messages.error(request, "You cannot request your own item.")
        return redirect('item_detail', item_id=item_id)
    
    if request.method == 'POST':
        form = ExchangeForm(request.POST, user=request.user)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.requested_item = requested_item
            exchange.offered_by_user = request.user
            exchange.requested_by_user = requested_item.user
            exchange.save()
            messages.success(request, 'Exchange request sent successfully.')
            return redirect('ecoswap_app:item_detail', item_id=item_id)
    else:
        form = ExchangeForm(user=request.user)
    
    context = {
        'form': form,
        'requested_item': requested_item
    }
    return render(request, 'ecoswap_app/request_exchange.html', context)

# chatbox

User = get_user_model()

@login_required
def message_list(request):
    # Fetch both received and sent messages
    messages_received = Message.objects.filter(receiver_user=request.user).order_by('-sent_at')
    messages_sent = Message.objects.filter(sender_user=request.user).order_by('-sent_at')
    messages = messages_received | messages_sent  # Combine both querysets

    return render(request, 'ecoswap_app/message_list.html', {'messages': messages})

@login_required
def send_message(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender_user = request.user
            message.exchange = exchange
            
            # Determine the receiver user based on the exchange details
            if exchange.offered_by_user == request.user:
                message.receiver_user = exchange.requested_by_user
            else:
                message.receiver_user = exchange.offered_by_user

            message.save()
            return redirect('ecoswap_app:message_list')
    else:
        form = MessageForm(user=request.user)

    return render(request, 'ecoswap_app/send_message.html', {'form': form, 'exchange': exchange})

@login_required
def exchange_list(request):
    exchanges = Exchange.objects.filter(offered_by_user=request.user) | Exchange.objects.filter(requested_by_user=request.user)
    return render(request, 'ecoswap_app/exchange_list.html', {'exchanges': exchanges})



# User authentication and athorization
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ecoswap_app:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'ecoswap_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ecoswap_app:index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'ecoswap_app/login.html', {'form': form})

@login_required(login_url='ecoswap_app:login')
def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to view your profile.")
        return redirect('ecoswap_app:login')
    return render(request, 'ecoswap_app/profile.html', {'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('ecoswap_app:login')


@login_required(login_url='ecoswap_app:login')
def user_exchange_requests(request):
    received_requests = Exchange.objects.filter(requested_by_user=request.user, status='Pending')
    context = {'received_requests': received_requests}
    return render(request, 'ecoswap_app/user_exchange_requests.html', context)

@login_required(login_url='ecoswap_app:login')
def all_accepted_request(request):
    accepted_requests = Exchange.objects.filter(requested_by_user=request.user, status='Accepted')
    context = {'accepted_requests': accepted_requests}
    return render(request, 'ecoswap_app/all_accepted_request.html', context)

@login_required(login_url='ecoswap_app:login')
def accept_request(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id, requested_by_user=request.user)
    if exchange.status == 'Pending':
        exchange.status = 'Accepted'
        exchange.offered_item.item_status = 'Pending'
        exchange.requested_item.item_status = 'Pending'
        exchange.save()
        messages.success(request, 'Exchange request accepted. Please complete the transaction details.')
        return redirect(reverse('ecoswap_app:create_transaction', args=[exchange.id]))
    else:
        messages.error(request, 'Cannot accept this exchange request.')
    return redirect('ecoswap_app:user_exchange_requests')

@login_required(login_url='ecoswap_app:login')
def reject_request(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id, requested_by_user=request.user)
    if exchange.status == 'Pending':
        exchange.status = 'Rejected'
        exchange.offered_item.item_status = 'Available'
        exchange.requested_item.item_status = 'Available'
        exchange.offered_item.save()
        exchange.requested_item.save()
        exchange.save()
        messages.success(request, 'Exchange request rejected.')
    else:
        messages.error(request, 'Cannot reject this exchange request.')
    return redirect('ecoswap_app:user_exchange_requests')



@login_required(login_url='ecoswap_app:login')
def request_exchange(request, item_id):
    requested_item = get_object_or_404(Item, id=item_id)
    if requested_item.user == request.user:
        messages.error(request, "You cannot request your own item.")
        return redirect('item_detail', item_id=item_id)

    if request.method == 'POST':
        form = ExchangeForm(request.POST, user=request.user)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.requested_item = requested_item
            exchange.offered_by_user = request.user
            exchange.requested_by_user = requested_item.user
            exchange.save()
            messages.success(request, 'Exchange request sent successfully.')
            return redirect('ecoswap_app:item_detail', item_id=item_id)
    else:
        form = ExchangeForm(user=request.user)

    context = {
        'form': form,
        'requested_item': requested_item
    }
    return render(request, 'ecoswap_app/request_exchange.html', context)


@login_required(login_url='ecoswap_app:login')
def create_transaction(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.exchange = exchange
            transaction.save()

            # Mark the items as exchanged
            exchange.offered_item.item_status = 'Exchanged'
            exchange.offered_item.save()
            exchange.requested_item.item_status = 'Exchanged'
            exchange.requested_item.save()

            # Update exchange status
            exchange.status = 'Completed'
            exchange.save()

            messages.success(request, 'Transaction completed successfully.')
            return redirect('ecoswap_app:index')
    else:
        form = TransactionForm(initial={
            'paid_by_user': exchange.offered_by_user,
            'received_by_user': exchange.requested_by_user
        })
    return render(request, 'ecoswap_app/create_transaction.html', {'form': form})