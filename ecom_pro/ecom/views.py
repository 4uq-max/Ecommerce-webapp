from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,HttpRequest
from .models import item, orderitem, order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib import messages

context = {

    'items' : item.objects.all()
}

def home(request):
    return render(request,'ecom/home.html')

def item_list(request):
    return render(request,'ecom/item_list.html', context)

class PostListView(ListView):
    model = item
    template_name = 'ecom/home.html'
    context_object_name = 'items'

class PostDetailView(DetailView):
    model = item
    template_name = "ecom/item_detail.html"

def about(request):
    return HttpResponse('<h1>this is the about page</h1>')

def add_to_cart(request , pk):
    item1 = get_object_or_404(item, pk = pk)
    order_item,created = orderitem.objects.get_or_create(item = item1,user = request.user, ordered=False)
    order_qs = order.objects.filter(user = request.user, ordered =False)
    if order_qs.exists():
        order1 = order_qs[0]
        # check if order item is in the order
        if order1.items.filter(item__pk = item1.pk).exists():
            order_item.quantity += 1
            order_item.save()     
            messages.info(request, "This item quantity was updated.")
        else:
            order1.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order1 = order.objects.create(user = request.user, ordered_date=ordered_date)
        order1.items.add(order_item)
    return redirect("item-detail", pk = pk)    


def remove_from_cart(request, pk):
    item1 = get_object_or_404(item, pk = pk)
    order_qs1 = order.objects.filter(user = request.user, ordered = False)
    if order_qs1.exists():
        order2 = order_qs1[0]
        #check if the order item is in the order 
        if order2.items.filter(item__pk = item1.pk).exists():
            order_item = orderitem.objects.filter(item = item1, user = request.user, ordered = False)[0]
            order.items.remove(order_item)
        else:
            return redirect("item-detail", pk = pk)
    else:
        return redirect("item-detail" ,pk = pk)
    return redirect("item-detail")

