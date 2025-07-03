const addToCartButton = document.getElementById('add-to-cart-button-{{ product.id }}');
const csrftoken = '{{ csrf_token }}';

addToCartButton.addEventListener("click", async function(){
    const productId = this.id.split('add-to-cart-button-')[1];
    const inputValue = document.getElementById('product-quantity-input-value').value;
    console.log(productId, inputValue);
    fetch("{% url 'shop:cart_view' %}", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'product_id': 1, 'quantity': inputValue})
    })
    .then(async response => {
        let data = await response.json();
        let status = await data.status;
        if (status == 'success'){
            toastr.success('Have fun storming the castle!', 'Miracle Max Says');
        }
        else{
            toastr.error('error');
        }
    })
})