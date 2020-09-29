from apps.core.models import Product


class Cart:

    def __init__(self, request):
        """ Инициализация корзины пользователя """
        self.session = request.session
        cart = self.session.get('cart', {})
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """ Добавление товара в корзину пользователя
            или обновление количеста товара
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.actual_price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """ Сохранение данных в сессию """
        self.session['cart'] = self.cart
        self.session.modified = True  # сессия изменена

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """ Итерация по корзине """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = round(
                float(item['price']) * int(item['quantity']), 2
            )
            yield item

    def __len__(self):
        """ Количество товаров """
        return sum([int(item['quantity']) for item in self.cart.values()])

    def clear(self):
        del self.session['cart']
        self.session.modified = True
