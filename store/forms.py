from django import forms
from django.contrib.auth.models import User
from .models import Book, Order


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password != confirm:
            raise forms.ValidationError(
                "Passwords do not match"
            )

        return cleaned_data


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'description',
            'price',
            'stock',
            'category',
            'image'
        ]


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'name',
            'phone',
            'address'
        ]