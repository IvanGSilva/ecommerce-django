from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
import datetime

def store(request):
    # criando os objetos da loja: usuario, pedido, itens do pedido...
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    products = Product.objects.all()
    
    # passando todas as informações por um contexto
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

# função que atualiza o carrinho
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # guarda o usuario, produtos e o carrinho em questão (atualiza um carrinho existente ou cria um carrinho novo)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #cria ou atualiza a quantidade de um item no carrinho
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    # adiciona ou remove o item no carrinho dependendo da classe do botão
    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    # salva as alterações
    orderitem.save()
    # deleta o item caso a quantidade seja <= 0
    if orderitem.quantity <= 0:
        orderitem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    # definindo o id da transação como a timestamp (+de 6 numeros)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    # garantindo que um usuário não possa realizar um pedido com mais itens do que foram adicionados e contabilizados no carrinho
    if total == order.get_cart_total:
        order.complete = True
    order.save()
        
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )
        
    return JsonResponse('pagamento completo', safe=False)