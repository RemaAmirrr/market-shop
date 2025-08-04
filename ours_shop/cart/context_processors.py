from .cart import Cart
from django.conf import settings

def cart(request):
    return {'cart':Cart(request)}



def my_flag_processor(request):
    """
    Adds a 'my_flag' variable to the template context,
    retrieved from the session or a default value.
    """
    my_flag = request.session.get('my_flag', settings.MY_FLAG_DEFAULT)
    return {'my_flag': my_flag}



