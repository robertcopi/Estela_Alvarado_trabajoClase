from decimal import Decimal
from django.conf import settings
from .models import Articulo

class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, articulo, cantidad=1, update_quantity=False):
        """Add an article to the cart or update its quantity."""
        articulo_id = str(articulo.articulo_id)
        if articulo_id not in self.cart:
            # We assume we use the first price from ListaPrecio if available, or 0.
            # Usually, precio is passed or we get it from articulo.listaprecio
            try:
                precio = str(articulo.listaprecio.precio_1)
            except:
                precio = '0.00'
                
            self.cart[articulo_id] = {'cantidad': 0, 'precio': precio}
        
        if update_quantity:
            self.cart[articulo_id]['cantidad'] = cantidad
        else:
            self.cart[articulo_id]['cantidad'] += cantidad
        self.save()

    def remove(self, articulo):
        """Remove an article from the cart."""
        articulo_id = str(articulo.articulo_id)
        if articulo_id in self.cart:
            del self.cart[articulo_id]
            self.save()

    def save(self):
        """Mark the session as modified to make sure it gets saved."""
        self.session.modified = True

    def __iter__(self):
        """Iterate over the items in the cart and get the articles from the database."""
        articulo_ids = self.cart.keys()
        articulos = Articulo.objects.filter(articulo_id__in=articulo_ids)
        
        cart = self.cart.copy()
        for articulo in articulos:
            cart[str(articulo.articulo_id)]['articulo'] = articulo

        for item in cart.values():
            item['precio'] = Decimal(item['precio'])
            item['total_precio'] = item['precio'] * item['cantidad']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['cantidad'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate total price of items in cart."""
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.cart.values())

    def clear(self):
        """Remove cart from session."""
        del self.session['cart']
        self.save()
