from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import CustomUser, Listing, Review

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'role', 'password1', 'password2')

class CustomLoginForm(AuthenticationForm):
    username=forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'})
    )


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'price', 'num_bedrooms', 'num_bathrooms', 'square_footage', 'address', 'image']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'square_footage': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        } 
               
  