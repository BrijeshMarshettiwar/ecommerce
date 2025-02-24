var updateBtns = document.getElementsByClassName('update-cart')

for(i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function () {
        var productId = this.dataset.product 
        var action = this.dataset.action
        console.log('productId:', productId ,'action:',action);

        console.log('User:',user);
        if (user === 'AnonymousUser') {
			addCookieItem(productId,action)
        }else{
			updateUserOrder(productId,action)
        }
    })
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
            console.log('data:',data);
            window.location.reload();
            // location.reload();
		});
}

function addCookieItem(productId,action){
	console.log('User is not authenticated');
	if(action == 'add'){
		if(cart[productId] == undefined){
			cart[productId] = {'quantity':1}
		}else{
			cart[productId]['quantity'] += 1
		}
	}
	
	if(action == 'remove'){
		cart[productId]['quantity'] -=1

		if(cart[productId]['quantity'] <= 0){
			console.log('Item should be delete')
			delete cart[productId]
		}
	}
	window.location.reload()
	console.log('Cart created ',cart)
    document.cookie = 'cart='+ JSON.stringify(cart) + ";domain=;path=/"
}

Results.prototype.displayMessage = function (params) {
	var escapeMarkup = this.options.get('escapeMarkup');

	this.clear();
	this.hideLoading();

	var $message = $(
		'<li role="alert" aria-live="assertive"' +
		' class="select2-results__option"></li>'
	);

	var message = this.options.get('translations').get(params.message);

	$message.append(
		escapeMarkup(
			message(params.args)
		)
	);

	$message[0].className += ' select2-results__message';

	this.$results.append($message);
};