from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            # Основные стили для соответствия дизайну Glassmorphism
            classes = (
                'w-full py-3 pl-12 pr-4 bg-white/10 border border-white/20 '
                'rounded-xl text-white placeholder-slate-400 focus:outline-none '
                'focus:ring-2 focus:ring-hop-green backdrop-blur-md transition-all'
            )
            self.fields[field_name].widget.attrs.update({
                'class': classes,
                'placeholder': self.fields[field_name].label
            })


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'Input', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'Input', 'placeholder': 'example@mail.com'}),
        }