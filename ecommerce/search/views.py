from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
# Create your views here.



def search_products(request):
    p = None
    query= ""
    if(request.method=="POST"):
        query=request.POST.get('q')  #READS THE QUERY VALUE
        if query:
            p=Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))  #FILTER THE RECORDS MATCHING WITH QUERY
    context={'pro':p,'query':query}
    return render(request,'search.html',context)