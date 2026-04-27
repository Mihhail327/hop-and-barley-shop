from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import UserEditForm, CustomUserCreationForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Согласно твоим settings.py, можно редиректить сюда
            return redirect('products:product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    """
    Личный кабинет: отображает историю заказов и форму редактирования профиля.
    Соответствует ТЗ 3.5.
    """
    # Получаем заказы через related_name 'orders' из твоей модели Order
    orders = request.user.orders.all().order_by('-created_at')

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'account.html', {
        'orders': orders,
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('products:product_list')
