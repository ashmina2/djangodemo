import razorpay
from django.shortcuts import render,redirect
from shop.models import Product
from cart.models import Cart,Payment,Order_details
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.
@login_required
def addtocart(request,i):
    p=Product.objects.get(id=i)
    u=request.user

    try:                                                #If a particular product for a particular user already exits
        c=Cart.objects.get(product=p,user=u)
        if(p.stock>0):
            c.quantity+=1
            c.save()
            p.stock-=1
            p.save()
    except:                                             #if particular record does not exist
       if(p.stock>0):
            c=Cart.objects.create(product=p,user=u,quantity=1)
            c.save()
            p.stock-=1
            p.save()

    return redirect('cart:cart')

def cart_view(request):
    u=request.user
    total=0

    c=Cart.objects.filter(user=u)
    total=0
    for i in c:
        total+=i.quantity*i.product.price

    context={'cart':c,'total':total}
    return render(request,'cart.html',context)

@login_required
def cart_remove(request,i):
    p=Product.objects.get(id=i)
    u=request.user

    try:                                                #If a particular product for a particular user already exits
        c=Cart.objects.get(product=p,user=u)
        if(c.quantity >1):
            c.quantity-=1
            c.save()
            p.stock+=1
            p.save()

        else:
            c.delete()
            p.stock +=1
            p.save()

    except:
        pass

    return redirect('cart:cart')

@login_required
def delete(request,i):
    p = Product.objects.get(id=i)
    u = request.user

    try:
        c = Cart.objects.get(product=p, user=u)
        c.delete()
        p.stock += c.quantity
        p.save()

    except:
        pass

    return redirect('cart:cart')
@login_required
def orderform(request):
    if(request.method=="POST"):
        address=request.POST['a']
        phone=request.POST['pn']
        pin=request.POST['p']
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
        total1=int(total*100)
      


        client=razorpay.Client(auth=('rzp_test_OrPSKIbnVhJEFd','6evKSZ2OWGi9dIu2SEowiOzc'))     #creates a client connection using razorpay id and secret code

        response_payment=client.order.create(dict(amount=total1,currency="INR")) #CREATES an order id with razorpay using razorpay client

        print(response_payment)

        order_id=response_payment['id']       #Retrieves the order_id from response
        status=response_payment['status']     #retrieves status from response

        if(status == 'created'): #if status is created then store order_id in Payment and Order_details table
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:      #for each item creates a record inside Order_details table
                o=Order_details.objects.create(product=i.product,user=u,no_of_items=i.quantity,address=address,phone_no=phone,pin=pin,order_id=order_id)
                o.save()

        response_payment['name']=u.username
        context={'payment':response_payment}
        return render(request,'payment.html',context)

    return render(request,'orderform.html')

from django.contrib.auth import login
@csrf_exempt
def payment_status(request,u):
    usr = User.objects.get(username=u)
    if not request.user.is_authenticated:
        login(request,usr)

    if (request.method == "POST"):
        response=request.POST
        print(response)

        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_OrPSKIbnVhJEFd', '6evKSZ2OWGi9dIu2SEowiOzc'))
        print(client)
        try:
            status=client.utility.verify_payment_signature(param_dict) #to check the authenticity of the razorpay signature
            print(status)

            #To retrieve a particular record from Payment Table matching with razorpay response order id
            p=Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id=response['razorpay_payment_id']
            p.paid=True
            p.save()

            #to retrieves  a record from Order_details Table matching with raxorpay response order id
            o=Order_details.objects.filter(order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status="completed"
                i.save()

            #after payment delete particular record from carts
            c=Cart.objects.filter(user=usr) #filter all records matching with particular user
            c.delete()
        except:
            pass

    return render(request,'payment_status.html',{'status':status})


@login_required
def order_view(request):
    u=request.user
    o=Order_details.objects.filter(user=u)
    print(o)
    context={'orders':o}
    return render(request,'orderview.html',context)


