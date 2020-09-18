from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from allauth.account.forms import SignupForm
from .models import CustomUser


class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':  "Drop Your Review",
        'class': "form-control",
        'row': 32,
        'style': "resize:none;"
    }))



class CheckoutForm(forms.Form):
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "class": "form-control",
       'placeholder': ' Enter Your Address'
    }))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "class": "form-control",
        'placeholder': ' Enter Your Phone Number'
    }))
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "class": "form-control",
              'placeholder': ' Enter Your State'
    }))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "class": "form-control",
              'placeholder': ' Enter Your Country'
    }))
    zip = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
              'placeholder': ' Enter Your Zip/Postal Code'
    }))
    default = forms.BooleanField(required=False)


class CouponForm(forms.Form):
    code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Name'
    }))
    email = forms.EmailField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email address'
    }))
    subject = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Subject'
    }))
    message = forms.CharField(max_length=300, required=True, widget=forms.Textarea(attrs={
         'style': 'resize:none;',
        'rows': '25',
        'class': 'form-control',
        'placeholder': 'Enter Message',
      
    }))



class NewsletterForm(forms.Form):
    email = forms.CharField(max_length=100, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Email Address'
    }))


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "First Name",
        'class': 'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Last Name",
        'class': 'form-control'
    }))
    class Meta:
        model = CustomUser
        fields = ("__all__")

    