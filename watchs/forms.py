

from django import forms

from .models import Product,Users,Comments,Comment_type
from django.contrib.auth.forms import AuthenticationForm




class Add_product(forms.ModelForm):
    class Meta:
        model=Product
        fields=["name",'price','image','description','componnent','utilizing_role','size','stock_count','order_count','discount'
            ,'category','published_time']

class Update_new(forms.ModelForm):
    class Meta:
        model=Product
        fields=["name",'price','image','description','componnent','utilizing_role','size','stock_count','order_count','discount',
                'category','published_time']


class Comments_form(forms.ModelForm):
    class Meta:
        model =Comment_type
        fields=["Afzalliklar","Kamchiliklari","Izoh"]


class Register_form(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput,label='Password')
    password_confirm=forms.CharField(widget=forms.PasswordInput,label='Confirm Password')


    class Meta:
        model=Users
        fields=["username","password"]

        labels = {
            "username" : "Username",
            "password" : "Password"
        }

        def clean(self):
            cleaned_data=super().clean()
            password=cleaned_data.get("password")
            password_confirm=cleaned_data.get("password_confirm")

            if password and password_confirm and password !=password_confirm:
                raise forms.ValidationError("Password is invalid")
            return cleaned_data

class Login_form(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
