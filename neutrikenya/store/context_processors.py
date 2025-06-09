from .models import Cart

def cart_processor(request):
    """Add cart to context data for all templates."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.get('session_id')
        if session_id:
            try:
                cart = Cart.objects.get(session_id=session_id)
            except Cart.DoesNotExist:
                cart = None
        else:
            cart = None
    
    return {'cart': cart} 