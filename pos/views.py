from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import OrderForm, OrderItemFormSet
from .models import Order, MenuItem

@login_required
def home(request):
    """
    Post-login landing page: choose between taking a new order
    or viewing the kitchen dashboard.
    """
    return render(request, 'pos/home.html')


@login_required
def take_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = 'pending'
            order.save()
            formset = OrderItemFormSet(request.POST, instance=order, prefix='form')
            if formset.is_valid():
                formset.save()
                messages.success(request, "✅ Order placed successfully!")
                return redirect('take_order')
        else:
            formset = OrderItemFormSet(request.POST, prefix='form')
    else:
        form = OrderForm()
        dummy_order = Order()  # status defaults to 'pending'
        formset = OrderItemFormSet(instance=dummy_order, prefix='form')

    menu_items = list(MenuItem.objects.values('id', 'name', 'price', 'category'))
    return render(request, 'pos/order_form.html', {
        'form': form,
        'formset': formset,
        'menu_items': menu_items
    })


@login_required
def order_list(request):
    """
    Order History page: lists all orders with their items and total amount.
    """
    orders = Order.objects.prefetch_related('items__menu_item').order_by('-ordered_at')
    return render(request, 'pos/order_list.html', {
        'orders': orders
    })


@login_required
def kitchen_dashboard(request):
    """
    Kitchen Dashboard: allows staff to update each order's status,
    and passes along the initial seen_ids list for client‐side polling.
    """
    if request.method == 'POST':
        order_id   = request.POST.get('order_id')
        new_status = request.POST.get('status')
        if order_id and new_status in dict(Order.STATUS_CHOICES):
            Order.objects.filter(id=order_id).update(status=new_status)
        return redirect('kitchen_dashboard')

    # GET: build orders queryset and initial seen_ids list
    orders   = Order.objects.prefetch_related('items__menu_item').order_by('-ordered_at')
    seen_ids = list(orders.values_list('id', flat=True))

    return render(request, 'pos/kitchen_dashboard.html', {
        'orders':   orders,
        'seen_ids': seen_ids,
    })


@login_required
def kitchen_orders_api(request):
    """
    JSON endpoint for AJAX polling of kitchen orders.
    """
    orders = Order.objects.prefetch_related('items__menu_item').order_by('-ordered_at')
    data = []
    for order in orders:
        data.append({
            'id':              order.id,
            'ordered_at':      order.ordered_at.strftime('%Y-%m-%d %H:%M'),
            'table_number':    order.table_number,
            'customer_name':   order.customer_name,
            'special_request': order.special_request,
            'status':          order.status,
            'items': [
                {'name': item.menu_item.name, 'qty': item.quantity}
                for item in order.items.all()
            ],
        })
    return JsonResponse({'orders': data})
