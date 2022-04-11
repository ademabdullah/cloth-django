from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
from datetime import datetime as dtime
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def payments (request):
    # store transaction details inside the payment model
    body = json.loads(request.body)
    # print (body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save() #saves the payment to the database
    order.payment = payment#update the order model to reference this payment
    order.is_ordered = True #the order has been successful
    order.save()

    # move cart_items to the orderproduct table

    cart_items = CartItem.objects.filter (user = request.user) #filter objects by user

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True #as by now the payment has been successful
        orderproduct.save()

    # reduce the quantity of the item sold

        product = Product.objects.get(id = item.product.id) #pointing to the product
        product.stock -= item.quantity
        product.save()

    # clear the cart
    CartItem.objects.filter(user = request.user).delete()


    # send order recieved email to the customer
    # functionality to be implemented in the future
    # using core.mail


    # using a JSON response to send order number and
    # transaction_ID back to sendData method using a
    # JSON response

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


''' This method retrieves the data from the billing form
    and instantiates an order model with this '''
def place_order(request, total = 0, quantity = 0):
    current_user = request.user

# if there are no items in the cart, redirect the user back to the store
    cart_items = CartItem.objects.filter(user= current_user) # get the user's cart_items
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect ('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax


    if request.method == 'POST':
        form = OrderForm(request.POST) #get the form from the post request
        if form.is_valid():

            ''' store all billing information inside order table
                create a new instance of the order class
                then set its attributes to be data from the form POST request
                cleaned data is needed to do ths.
            '''

            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.phone = form.cleaned_data['phone']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.tax = tax
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR') # this will retrieve the user's IP address, will be unique

            #Generate a unique order number using the current time and date
            # Used the following tutorial @ https://www.programiz.com/python-programming/datetime/strftime


            now = dtime.now() # current date and time

            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")
            time = now.strftime("%H:%M:%S")
            current_time_date = now.strftime("%H:%M:%S_%m/%d/%Y_")

            # the order number will be a combination of the current date and
            # the user's IP address
            order_number = current_time_date + str(data.ip)
            data.order_number = order_number
            data.save() # saves the model

            order = Order.objects.get(user=current_user, is_ordered = False, order_number = order_number) #get the order
            context = {'order': order,
                       'cart_items': cart_items,
                       'total' : total,
                       'tax' : tax,
                       'grand_total': grand_total,
                      }

            return render (request, 'orders/payments.html', context)
    else:
        return redirect ('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number') #get the order_id
    transID = request.GET.get('payment_id') #get the payment_id

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True) #point to the order
        ordered_products = OrderProduct.objects.filter(order_id=order.id) # point to the product's orders

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist): #handling the payment does not exist and order does not exist errors
        return redirect('home')
