from django.db import models
from django.contrib.auth.models import User

#aqui estou usando o metodo  models.OneToOneField() para apontar o objeto do usuário, usar uma foreign key poderia acabar fazendo o 
# codigo retornar uma query ao envés do objeto do usuário, pois a foreign key é uma relação "muitos para um", enquanto que models.OneToOneField é uma
#relação exclusivamente "um para um"
#colocando em termos simples, quer dizer que cada usuário só pode ter UM cliente e cada cliente pode ter apenas UM usuário, evitando bugs 
# e erros nas contas de usuário e compras
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    
    #função que tenta randerizar a imagem do produto, caso não exista uma imagem associada ao produto, 
    # retorna uma string vazia, que anula um erro ocasionado por tentar randerizar uma imagem não existente
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.name

#aqui estou usando uma foreign key normalmente pois não existe problema em um cliente ter mais de um pedido, relação de "muitos para um"
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
#indicador se um carrinho esta aberto ainda ou ja é um pedido fechado
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    #função que retorna o valor total da quantidade de cada item no  carrinho
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=False)
    #mudar para CEP
    zipcode = models.CharField(max_length=255, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address