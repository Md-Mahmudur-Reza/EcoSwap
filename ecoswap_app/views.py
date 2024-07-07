from django.shortcuts import render
from .models import User, Item, Exchange, Transaction, Message
from django.shortcuts import render, get_object_or_404

def index(request):
    query = request.GET.get('q')
    if query:
        items = Item.objects.filter(item_name__icontains=query).order_by('-created_at')
    else:
        items = Item.objects.order_by('-created_at')
    context = {'items': items, 'query': query}
    return render(request, 'ecoswap_app/index.html', context)


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    context = {'item': item}
    return render(request, 'ecoswap_app/item_details.html', context)
