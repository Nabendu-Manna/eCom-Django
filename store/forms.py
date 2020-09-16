from django import forms
from .models import *
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm


class uploadBrandForm(forms.ModelForm):
    # name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
    # image = forms.ImageField()
    
    class Meta():
        model = Brands
        fields = ['name', 'image']
        
#
class uploadCatagoryForm(forms.ModelForm):
    # name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
    # image = forms.ImageField()
    
    class Meta():
        model = Catagories
        fields = ['name', 'image']

#
class uploadProductForm(forms.ModelForm):
    # name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
    # image = forms.ImageField()
    
    class Meta():
        model = Product
        fields = ['name', 'price', 'details', 'catagoryId', 'brandId', 'image']
        
#
class signupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
#
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['customer', 'order', 'address', 'city', 'state', 'zipcode']
        
##################################