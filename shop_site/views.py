from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem, Address, Payment, Coupon, Refund, Category, subcategory, Invoice, Dispatch
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import AddressForm, CouponeForm, RefundForm, AddItem, PaymentMethodForm, AddCategory, AddCoupon, AddSubcategory, DispatchForm
from django.contrib.auth.decorators import login_required
import stripe
import random
import string
from django.core.paginator import Paginator

stripe.api_key = 'sk_test_TjwJ8KIE4pM0zUDkkubD4kvV00PipgfR59'

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def create_invoice_code():
    return ''.join(random.choices(string.digits, k=15))

def HomeView(request):
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category' : Category.objects.all(),
        'subcategory' : subcategory.objects.all()
        }
    return render(request, 'home.html', context)
    
    
@login_required
def ItemDetailView(request, pk):
    item = Item.objects.get(pk=pk)
    
    try:
        order = Order.objects.get(user=request.user,ordered=False)
        order_item = order.items.all()
        ids = []
        for ord in range(len(order_item)):
            ids.append(order_item[ord].item.id)
            
        if item.id in ids:
            index = ids.index(item.id)
            product_quantity = order_item[index].quantity
        else:
            product_quantity = 0

    except ObjectDoesNotExist:
        product_quantity = 0
        
    context = {
        'object': item,
        'product_quantity' : product_quantity
    }
    return render(request, "product.html", context)

@login_required
def checkout(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/checkout-system/')
    else:
        form = AddressForm()

    return render(request, 'checkout.html', {'form': form})


@login_required
def add_to_Cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk = item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, 'Quantity added of this item')
        else:
            messages.success(request, 'This Item Is Added To Your Cart')
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, 'This Item Is Added To Your Cart')
        
    return redirect('/product/'+str(pk)+'/')

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item has been removed from your cart.")
            return redirect('/product/'+str(pk)+'/')
        else:
            messages.warning(request, "This item is not in your cart")
            return redirect('/product/'+str(pk)+'/')
    else:
        messages.warning(request, "You do not have an active order")
        return redirect('/product/'+str(pk)+'/')

@login_required
def OrderSummaryView(request):
    template_name = 'order_summary.html'
    try:
        order = Order.objects.get(user=request.user, ordered=False)

    except ObjectDoesNotExist:
        messages.error(request,"No Active Order Found")
        return redirect("/")

    return render(request, template_name, {'object':order})

@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(    
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            return redirect("/order-summary/")

@login_required
def minus_quantity(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(    
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            return redirect('/product/'+str(pk)+'/')
    
@login_required
def decrease_quantity(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            return redirect('/product/'+str(pk)+'/')

@login_required
def add_single_to_Cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk = item.id).exists():
            order_item.quantity += 1
            order_item.save()
        
    return redirect('/order-summary/')

@login_required
def plus_quantity(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk = item.id).exists():
            order_item.quantity += 1
            order_item.save()
        
    return redirect('/product/'+str(pk)+'/')

@login_required   
def reset_cart(request, pk):
    order = OrderItem.objects.all()
    order.delete()
    return redirect('/order-summary/')

@login_required
def payment(request):
    return render(request, "payment.html")

@login_required
def charge(request):
    order = get_object_or_404(Order, user=request.user, ordered=False)
    amount = order.get_bill_amount()
    if request.method == 'POST':

        cus_name = request.POST["cus_name"]

        try:

            customer = stripe.Customer.create (
                name = cus_name,
                source = request.POST["stripeToken"]
            )

            charge = stripe.Charge.create (
                customer = customer,
                amount = int(amount)*100,
                currency = 'INR',
                description = 'Latest Payment Successful'
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = request.user
            payment.amount = amount
            payment.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()
            

        except stripe.error.CardError as e:
            messages.error(request, f'{e.error.message}')
            return redirect("/")

        except stripe.error.RateLimitError as e:
            messages.error(request, f'Rate Limit Error')
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            messages.error(request, f'Invalid parameters')
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            messages.error(request, f'Authentication Error')
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            messages.error(request, f'Network Error')
            return redirect("/")

        except stripe.error.StripeError as e:
            messages.error(request, f'Something went wrong. You are not Charged. Please Try Again.')
            return redirect("/")

        except Exception as e:
            messages.error(request, f"Some Serious issue has been poped.")  
            return redirect("/")

    return render(request, 'success_payment.html',{'amount':amount})

@login_required
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon

    except ObjectDoesNotExist:
        messages.error(request, 'No Active Order Found')
        return redirect("/")

@login_required
def redem_coupon(request):
    if request.method == 'POST':
        form = CouponeForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user, ordered=False)
                my_coupon = get_coupon(request, code)
                today = timezone.now()
                if today >= my_coupon.valid_from and today <= my_coupon.valid_till:
                    order.coupon = my_coupon
                    order.save()
                    messages.success(request, 'Coupon Applied')
                    return redirect('/checkout-system/')
                else:
                    messages.error(request, 'Your Coupon has been expired')
                    my_coupon.status = False
                    my_coupon.save()
                    return redirect('/checkout-system/')

            except ObjectDoesNotExist:
                messages.error(request, 'No Active Order Found')
                return redirect("/")

    return None

def change_promo(request):
    order = Order.objects.get(user=request.user, ordered=False)

    order.coupon = None
    order.save()

    messages.warning(request, "Change Your Coupon")
    return redirect('/checkout-system/')

def Request_Refund(request):
    if request.method == 'POST':
        form = RefundForm(request.POST or None)
        if form.is_valid():
            try:
                ref_code = form.cleaned_data.get('ref_code')
                message = form.cleaned_data.get('message')
                email = form.cleaned_data.get('email')
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

        
                messages.success(request, "Your Request Was Recived By the Admins")
                return redirect('/request-refund/')
            
            except ObjectDoesNotExist:
                messages.error(request, "This Order Does Not Exists")
                return redirect('/request-refund/')

    else:
        form = RefundForm()

    return render(request, 'request_refund.html', {'form' : form})


def add_item(request):
    if request.method == 'POST':
        form = AddItem(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, 'Item Added Successfully')
            return redirect('/add-item/')
    else:
        form = AddItem()
    return render(request, 'add_item.html',{'form': form})

def add_category(request):
    if request.method == 'POST':
        form = AddCategory(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, 'Category Added Successfully')
                return redirect('/add-category/')
            except ValueError:
                messages.error(request, 'Data Invalid Or Redudancy Occured')
                return redirect('/add-category/')
    else:
        form = AddCategory()
    return render(request, 'add_category.html',{'form': form})

def add_subcategory(request):
    if request.method == 'POST':
        form = AddSubcategory(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, 'SubCategory Added Successfully')
            return redirect('/add-subcategory/')
    else:
        form = AddSubcategory()
    return render(request, 'add_subcategory.html',{'form': form})

def add_coupon(request):
    if request.method == 'POST':
        form = AddCoupon(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, 'Coupon Added Successfully')
            return redirect('/add-coupon/')
    else:
        form = AddCoupon()
    return render(request, 'add_coupon.html',{'form': form})

def address_select(request):
    address_id = request.POST['get_address']
    address = Address.objects.get(id=int(address_id))
    order = Order.objects.get(user=request.user, ordered=False)
    order.shipping_address = address
    order.billing_address = address
    order.save()

    return redirect('/get-payment-method/') 

def checkout_system(request):
    address = Address.objects.filter(user=request.user)
    if address:
        context = {
            'address':address,
            'object': Order.objects.get(user=request.user, ordered=False),
            'couponeform' : CouponeForm(),
            'coupon' : Coupon.objects.all().filter(status=True)
        }
        return render(request, 'address.html', context)
    else:
        return redirect('/checkout/')

def get_payment_method(request):
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        form = PaymentMethodForm(request.POST or None)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            if payment_method == 'S':
                return redirect('/payment/')
            else:
                messages.error(request,'invalid option')
                return redirect('/')
        else:
            form = PaymentMethodForm()
    else:
        messages.error(request,"Order Does Not Exists")
        return redirect('/')


    return render(request, 'payment-method.html', {'form':form})

def order_history(request):
    if request.user.is_superuser:
        order = Order.objects.filter(ordered=True)
    else:
        order = Order.objects.filter(user=request.user, ordered=True)

    invoice_array = []
    dispatch_array = []
    for i in Invoice.objects.all():
        invoice_array.append(i.order.id)
    for i in Dispatch.objects.all():
        dispatch_array.append(i.order.id)
    context = {
        'order' : order,
        'inv_array' : invoice_array,
        'disp_array' : dispatch_array,
        'invoice' : Invoice.objects.all(),
        'dispatch' : Dispatch.objects.all()
    }
    return render(request, 'order_history.html', context)


def invoice(request,pk):
    order = Order.objects.get(pk=pk)

    context = {
        'order' : order
    }
    return render(request, 'invoice-create.html', context)

def invoice_action(request):
    order_pk = request.POST['order']
    order_ref_code = request.POST['order_ref_code']
    amount_paid = request.POST['amount_paid']

    invoice = Invoice()
    invoice.InvoiceId = create_invoice_code()
    invoice.order = Order.objects.get(pk=order_pk)
    invoice.order_ref_code = order_ref_code
    invoice.amount_paid = float(amount_paid)
    invoice.save()
    messages.success(request, 'Billing Completed! Proceed To Dispatch')
    return redirect('/order-history/')

def create_dispatch(request,pk):
    order = Order.objects.get(pk=pk)
    if Invoice.objects.filter(order=order):
        if Dispatch.objects.filter(order=order):
            messages.info(request,'Already releashed Dispatch')
            return redirect('/order-history/')
        else:    
            if request.method == 'POST':
                form = DispatchForm(request.POST or None)
                if form.is_valid():
                    transpoter_name = form.cleaned_data['transpoter_name']
                    delivery_date = form.cleaned_data['delivery_date']
                    
                    dispatch = Dispatch()
                    dispatch.transpoter_name = transpoter_name
                    dispatch.delivery_date = delivery_date
                    dispatch.invoice = Invoice.objects.get(order=order)
                    dispatch.order = order
                    dispatch.save()
                    print(dispatch)
                    return redirect('/order-history/')
            else:
                form = DispatchForm()
            
            context = {
                'form' : form
            }

            return render(request, "dispatch.html", context)

    else:
        messages.error(request,'Invoice Not Created')
        return redirect('/order-history/')
        
        

def Invoice_View(request,pk):
    context = {
        'invoice' : Invoice.objects.filter(order=Order.objects.get(pk=pk))
    }
    return render(request, 'invoice.html', context)

def Dispatch_View(request,pk):
    context = {
        'dispatch' : Dispatch.objects.filter(order=Order.objects.get(pk=pk))
    }
    return render(request, 'dispatch-view.html', context)