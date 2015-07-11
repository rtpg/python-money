from __future__ import print_function

from django import forms
from django.shortcuts import render_to_response, get_object_or_404

from money.money import Money
from money.contrib.django.forms.fields import MoneyField
from money.tests.models import SimpleMoneyModel


class TestForm(forms.Form):
    price = MoneyField()


class TestModelForm(forms.ModelForm):
    class Meta:
        model = SimpleMoneyModel


def instance_view(request):
    money = Money('0.0', 'JPY')
    return render_to_response('view.html', {'money': money})


def model_view(request):
    instance = SimpleMoneyModel(price=Money('0.0', 'JPY'))
    money = instance.price
    return render_to_response('view.html', {'money': money})


def model_from_db_view(request, amount='0', currency='XXX'):
    # db roundtrip
    instance = SimpleMoneyModel.objects.create(price=Money(amount, currency))
    instance = SimpleMoneyModel.objects.get(pk=instance.pk)

    print(instance, instance.pk)

    money = instance.price
    return render_to_response('view.html', {'money': money})


def model_form_view(request, amount='0', currency='XXX'):
    cleaned_data = {}
    if request.method == 'POST':
        form = TestModelForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            form.save()
            # Most views would redirect here but we continue so we can render the data
    else:
        form = TestModelForm(initial={'price': Money(amount, currency)})

    return render_to_response('form.html', {'form': form, 'cleaned_data': cleaned_data})


def regular_form(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            price = form.cleaned_data['price']
            return render_to_response('form.html', {'price':price} )
    else:
        form = TestForm()
    return  render_to_response('form.html', {'form':form} )

def regular_form_edit(request, id):
    instance = get_object_or_404(SimpleMoneyModel, pk=id)
    if request.method == 'POST':
        form = TestForm(request.POST, initial={'price':instance.price})
        print(form.is_valid())
        if form.is_valid():
            price = form.cleaned_data['price']
            return render_to_response('form.html', {'price':price} )
    else:
        form = TestForm(initial={'price':instance.price})
    return  render_to_response('form.html', {'form':form} )



def model_form_edit(request, id):
    instance = get_object_or_404(SimpleMoneyModel, pk=id)
    if request.method == 'POST':
        form = TestModelForm(request.POST, instance=instance)
        print(form.is_valid())
        if form.is_valid():
            price = form.cleaned_data['price']
            form.save()
            return render_to_response('form.html', {'price':price} )
    else:
        form = TestModelForm(instance=instance)
    return  render_to_response('form.html', {'form':form} )
