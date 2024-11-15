from django.shortcuts import render,redirect,HttpResponse
from shop.models import Categories,Product
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def categories(request):
    c=Categories.objects.all()
    context={'cat':c}
    return render(request,'categories.html',context)

def products(request,p):                    #here p receives the category id
    c=Categories.objects.get(id=p)         #reads a particular category object using id
    p=Product.objects.filter(category=c)   #reads all products under a particular category object
    context={'cat':c,'product':p}

    return render(request,'products.html',context)

def details(request,p):
    pro=Product.objects.get(id=p)
    context={'product':pro}
    return render(request,'details.html',context)

def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        if (p == cp):
            user = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            user.save()
            return redirect('shop:categories')
        else:
            return HttpResponse("Passwords are not same")


    return render(request,'register.html')

def user_login(request):
        if (request.method == "POST"):
            u = request.POST['u']
            p = request.POST['p']
            user = authenticate(username=u, password=p)
            if user:
                login(request, user)
                return redirect('shop:categories')
            else:
                return HttpResponse("Invalid Credentials")
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('shop:login')

def addcategory(request):
    if(request.method=="POST"):

        n = request.POST['n']
        i = request.FILES['i']
        de = request.POST['de']
        c=Categories.objects.create(name=n,image=i, description=de)
        c.save()
        return redirect('shop:categories')
    return render(request,'addcategory.html')


def addproduct(request):
    if (request.method == "POST"):
        n = request.POST['n']
        i = request.FILES['i']
        d = request.POST['d']
        s = request.POST['s']
        p = request.POST['p']
        c = request.POST['c']

        cat=Categories.objects.get(name=c)

        p=Product.objects.create(name=n,image=i,desc=d,stock=s,price=p,category=cat)
        p.save()
        return redirect('shop:categories')

    return render(request,'addproduct.html')

def addstock(request,i):
    product=Product.objects.get(id=i)
    if(request.method=="POST"):
        product.stock=request.POST['s']
        product.save()
        return redirect('shop:details',i)

    context={'pro':product}
    return render(request,'addstock.html',context)
