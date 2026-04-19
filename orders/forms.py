from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    """
    Form for capturing delivery details during checkout.
    Uses ModelForm to map directly to the Order model fields.
    """
    class Meta:
        model = Order
        # Берем только те поля, которые должен заполнить пользователь
        fields = ['city', 'address']

        # Добавляем стили, соответствующие твоему checkout.html
        widgets = {
            'city': forms.TextInput(attrs={
                'class': 'form-input', # Использует класс Tailwind из base.html
                'placeholder': 'Tallinn'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-input resize-none', # Использует класс Tailwind из base.html
                'placeholder': 'Pikk tn 1, krt 5',
                'rows': 3 # Делаем поле повыше, как в макете
            }),
        }