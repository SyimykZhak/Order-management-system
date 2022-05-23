from django import forms
from .models import Products, Order


class ProductForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['category'].empty_label = "Выберите категорию"

    class Meta:
        model = Products
        fields = ("category","title","description","price","kol","image",)


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'order_quantity']