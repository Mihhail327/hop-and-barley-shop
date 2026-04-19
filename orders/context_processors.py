from .cart import Cart

def cart(request):
    """Делает объект корзины доступным во всех шаблонах."""
    return {'cart': Cart(request)}