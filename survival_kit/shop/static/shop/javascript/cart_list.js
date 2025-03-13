const buttonsAddOne = Array.from(document.getElementsByClassName('add_to_cart_one'));
const buttonsRemoveOne = Array.from(document.getElementsByClassName('remove_from_cart_one'));
const csrftoken = '{{ csrf_token }}'

buttonsRemoveOne.forEach(async function(elem){
    elem.addEventListener("click", async function(){
        const itemId = this.id;
        let idP = itemId + '_quantity';
        let idPrice = itemId + '_price';
        let idBlock = itemId + '_block';
        let quantityElem = document.getElementById(idP);
        let quantityValue = Number(quantityElem.innerText) - 1;
        let data = await makeRequest("cartViewUrl", method='POST',
                                        body={'product_id': itemId, 'quantity': '-1'});
        let status = data.status;
        let isEmpty = data.queryset_isempty;
        let totalPrice = data.total_price;
        let priceByQuantity = data.price_by_quantity;
        let element = document.getElementById(idBlock);
        let emptyMessage = document.getElementById('empty-cart-info');
        if (status == 'success'){
            changePriceByQuntity(idPrice, priceByQuantity, totalPrice);
            if (quantityValue == 0) {
                element.remove();
            } else if(quantityValue == 1){
                elem.innerHTML = '<i class="fa-solid fa-trash"></i>';
                quantityElem.innerHTML = quantityValue;
            } else{
                quantityElem.innerHTML = quantityValue;
            }

        }
        if (isEmpty){
            emptyMessage.classList.remove("d-none");
        }
    })
})

buttonsAddOne.forEach(async function(elem){
    elem.addEventListener("click", async function(){
        const itemId = this.id;
        let idP = itemId + '_quantity';
        let idPrice = itemId + '_price';
        let quantityElem = document.getElementById(idP);
        let quantityValue = Number(quantityElem.innerText) + 1;
        let data = await makeRequest("{% url 'shop:cart_view' %}", method='POST', body={'product_id': itemId, 'quantity': 1});
        let status = data.status;
        let priceByQuantity = data.price_by_quantity;
        let totalPrice = data.total_price;
        if (status == 'success'){
            quantityElem.innerHTML = quantityValue;
            document.getElementById(itemId).innerHTML = '<i class="fa-solid fa-minus">';
            changePriceByQuntity(idPrice, priceByQuantity, totalPrice)
        }
    })
})

async function makeRequest(url, method, body) {

    let headers = {
        'Accept': 'application/json',
        'X-CSRFToken': csrftoken
    }

    return fetch(url, {
        method: method,
        headers: headers,
        body: JSON.stringify(body)
    })
    .then(async response => {
        return await response.json();
    })
}

function changePriceByQuntity(pId, priceByQuantity, totalPrice){
        document.getElementById(pId).innerHTML = priceByQuantity;
        document.getElementById('total-price').innerHTML = totalPrice;
}
