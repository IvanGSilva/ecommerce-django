//captura dos botões pressionados
var updateBtns = document.getElementsByClassName('update-cart')

// laço de repetição que adiciona eventListeners para todos os botões que tem a classe 'update-cart' e retorna o objeto do produto e a classe de evento 'action
for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        //melhor verificação do que está acontecendo no console web
        console.log('productId:', productId, 'action:', action)
        console.log('USUARIO:', user)

        updateUserOrder(productId, action)    
    })
}

//função para dar update nos itens do carrinho
function updateUserOrder(productId, action){
    var url = '/update_item/'
    // aqui estou usando a API fetch para retornar os dados para atualizar o carrinho como promise em forma de JSON
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            //crsf definido no main
            'X-CSRFToken':csrftoken,
        },
        //transformando a resposta da fetch em string
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}