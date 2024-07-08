from django.shortcuts import render
from .models import User, Item, Exchange, Transaction, Message
from django.shortcuts import render, get_object_or_404

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
