from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages


from .forms import CustomerForm
from .models import Customer
# Create your views here.

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Created Successfully.')
            return HttpResponseRedirect(reverse('customer:customer_list'))
        else:
            messages.error(request, 'Phone Number already exists.')
            return HttpResponseRedirect(reverse('customer:create_customer'))
    else:
        form = CustomerForm()
        context = {
            "title": "Create Customer",
            "form": form,
        }
        return render(request, 'customer/add.html', context)

def customer_list(request):
    query_set = Customer.objects.filter(is_deleted=False)
    context = {
        "title": "Customers",
        "instances": query_set,
    }
    return render(request, 'customer/list.html', context)


def update_customer(request, pk):
    instance = get_object_or_404(Customer , pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully.')
            return HttpResponseRedirect(reverse('customer:customer_list'))
        else:
            messages.error(request, 'Something went wrong.')
            return HttpResponseRedirect(reverse('customer:update_customer',kwargs={'pk':pk}))
    else:
        form = CustomerForm(instance=instance)
        context = {
            "title": "Edit Customer",
            "form": form,
            "instance": instance
        }
        return render(request, 'customer/add.html', context)


def delete_customer(request, pk):
    Customer.objects.filter(pk=pk).update(is_deleted=True)
    messages.success(request, 'Deleted Successfully.')
    return HttpResponseRedirect(reverse('customer:customer_list'))
