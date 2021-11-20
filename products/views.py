from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput,NumberInput,Select


from .forms import ProductForm,QuotationForm,QuotationItemForm
from .models import Product,Quotation,QuotationItem
from .utils import update_quantity
# Create your views here.


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Created Successfully.')
            return HttpResponseRedirect(reverse('product:product_list'))
        else:
            messages.error(request, 'Something went wrong.')
            return HttpResponseRedirect(reverse('product:create_product'))
    else:
        form = ProductForm(request.POST)
        context = {
            "title": "Create product",
            "form": form,
        }
        return render(request, 'product/add.html', context)

def product_list(request):
    query_set = Product.objects.filter(is_deleted=False)
    context = {
        "title": "Products",
        "instances": query_set,
    }
    return render(request, 'product/list.html', context)



def update_product(request, pk):
    instance = get_object_or_404(Product , pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully.')
            return HttpResponseRedirect(reverse('product:product_list'))
        else:
            messages.error(request, 'Something went wrong.')
            return HttpResponseRedirect(reverse('product:update_product',kwargs={'pk':pk}))
    else:
        form = ProductForm(instance=instance)
        context = {
            "title": "Edit Product",
            "form": form,
            "instance": instance
        }
        return render(request, 'product/add.html', context)


def delete_product(request, pk):
    Product.objects.filter(pk=pk).update(is_deleted=True)
    messages.success(request, 'Deleted Successfully.')
    return HttpResponseRedirect(reverse('product:product_list'))


"""Quotation views """

def create_quotation(request):
    QuotationFormset = formset_factory(QuotationItemForm,extra=1)
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        quotation_formset = QuotationFormset(request.POST,prefix="quotation_formset")
        if form.is_valid() and quotation_formset.is_valid():
            discount = form.cleaned_data['discount']
            data = form.save()

            subtotal = 0
            for form in quotation_formset:
                product = form.cleaned_data['product']
                qty = form.cleaned_data['qty']
                price = product.price
                sub = price * qty
                subtotal += sub
                QuotationItem.objects.create(
                    product=product,
                    qty=qty,
                    quotation=data,
                )
                #updating quantity
                update_quantity(product.pk,qty,"decrease")

            total = subtotal - discount
            data.subtotal = subtotal
            data.total = total
            data.save()

            messages.success(request, 'Created Successfully.')
            return HttpResponseRedirect(reverse('product:single_quotation',kwargs={'pk':data.pk}))
        else:
            messages.error(request, 'Something went wrong.')
            return HttpResponseRedirect(reverse('product:create_quotation'))
    else:
        form = QuotationForm()
        quotation_formset = QuotationFormset(prefix="quotation_formset")
        context = {
            "title": "Create Quotation",
            "form": form,
            "quotation_formset":quotation_formset,
        }
        return render(request, 'quotation/add.html', context)


def single_quotation(request,pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation_item = QuotationItem.objects.filter(quotation=quotation)
    context = {
            "title": "Quotation for " + quotation.customer.name,
            "quotation": quotation,
            "quotation_item":quotation_item,
        }
    return render(request, 'quotation/single.html', context)


def quotation_list(request):
    query_set = Quotation.objects.filter(is_deleted=False)
    context = {
        "title": "Quotations",
        "instances": query_set,
    }
    return render(request, 'quotation/list.html', context)



def update_quotation(request, pk):
    instance = get_object_or_404(Quotation ,pk=pk)
    if QuotationItem.objects.filter(quotation=instance).exists():
        extra = 0
    else:
        extra = 1
        
    QuotationFormset = inlineformset_factory(
        Quotation,
        QuotationItem,
        can_delete=True,
        extra=extra,
        exclude=('quotation',),
        widgets= {
            'product': Select(attrs={'class': 'required form-control', 'placeholder': 'Product'}),
            'qty': NumberInput(attrs={'class': 'required form-control', 'placeholder': 'Quantity'}),
        }
    )
    if request.method == 'POST':
        form = QuotationForm(request.POST, instance=instance)
        quotation_formset = QuotationFormset(
            request.POST, prefix='quotation_formset', instance=instance)

        if form.is_valid() and quotation_formset.is_valid():

            items = {}
            for f in quotation_formset:
                if f not in quotation_formset.deleted_forms:
                    product = f.cleaned_data['product']
                    qty = f.cleaned_data['qty']
                    if str(product.pk) in items:
                        q = items[str(product.pk)]["qty"]
                        items[str(product.pk)]["qty"] = q + qty
                    else:
                        dic = {
                            "qty": qty,
                        }
                        items[str(product.pk)] = dic

            discount = form.cleaned_data['discount']
            data = form.save()


            #Delete prev item and update stocks
            prev_quotation_item = QuotationItem.objects.filter(quotation=instance)
            for p in prev_quotation_item:
                prev_qty = p.qty
                update_quantity(p.product.pk, prev_qty, "increase")
            prev_quotation_item.delete()


            subtotal = 0
            #save items
            for key,value in items.items():
                product = Product.objects.get(pk=key)
                qty = value["qty"]
                price = product.price
                subtotal += qty * price
                test_items = QuotationItem(
                    quotation = data,
                    product=product,
                    qty=qty
                )
                test_items.save()
                update_quantity(product.pk, qty, "decrease")
            
            total = subtotal - discount
            data.subtotal = subtotal
            data.total = total
            data.save()
        
            messages.success(request, 'Updated Successfully.')
            return HttpResponseRedirect(reverse('product:single_quotation',kwargs={'pk':data.pk}))
        else:
            messages.error(request, 'Something went wrong.')
            return HttpResponseRedirect(reverse('product:update_quotation',kwargs={"pk":data.pk}))
    else:
        form = QuotationForm(instance=instance)
        quotation_formset = QuotationFormset(prefix="quotation_formset",instance=instance)
        context = {
            "title": "Edit Quotation "+ instance.customer.name,
            "form": form,
            "quotation_formset":quotation_formset,
            "instance": instance
        }
        return render(request, 'quotation/add.html', context)


def delete_quotation(request, pk):
    instance = get_object_or_404(Quotation, pk=pk)
    quotation_items = QuotationItem.objects.filter(quotation=instance)
    for q in quotation_items:
        qty = q.qty
        update_quantity(q.product.pk, qty, "increase")
    instance.is_deleted = True
    instance.save()
    messages.success(request, 'Deleted Successfully.')
    return HttpResponseRedirect(reverse('product:quotation_list'))
