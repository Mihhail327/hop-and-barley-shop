from django import forms

from .models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # Добавим стили Tailwind прямо в форму, чтобы они прокинулись в шаблон
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'Input', 'placeholder': 'example@mail.com'}),
        }
