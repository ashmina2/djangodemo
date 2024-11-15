
from cart.models import Cart
def count_items(request):
    u=request.user
    count=0
    try:
        if request.user.is_authenticated:
            c=Cart.objects.filter(user=u)
            count=0
            for i in c:
              count+=i.quantity

    except:
        count=0

    return {'c':count}