from .models import Exchange

def exchange_request_count(request):
    if request.user.is_authenticated:
        request_count = Exchange.objects.filter(requested_by_user=request.user, status='Pending').count()
    else:
        request_count = 0
    return {'exchange_request_count': request_count}
