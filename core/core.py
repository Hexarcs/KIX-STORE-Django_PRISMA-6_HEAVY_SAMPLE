# seu_app/cart.py

class KixCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('kix_cart')
        if not cart:
            cart = self.session['kix_cart'] = {}
        self.cart = cart

    def add(self, product_id, name, price_sats, quantity=1):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'name': name,
                'price_sats': int(price_sats),
                'quantity': 0
            }
        self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['kix_cart'] = {}
        self.save()

    def get_total_sats(self):
        return sum(item['price_sats'] * item['quantity'] for item in self.cart.values())

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True