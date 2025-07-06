const buttons_add_to_favorite = Array.from(document.getElementsByClassName('wishlist_btn'));
const buttons_add_to_cart = Array.from(document.getElementsByClassName('add_to_cart'));


buttons_add_to_favorite.forEach(async function(elem){
    elem.addEventListener("click", async function(){
        const product_id = this.id;
        let idItemFavoriteCard = product_id + '_product';

        fetch(favoriteProductPageUrl, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'product_id': product_id})
        })
        .then(async response => {
            let data = await response.json();
            let status = await data.status;
            let element = document.getElementById(idItemFavoriteCard);
            if (status == 'removed'){
                element.remove();
                toastr.success('Successfully removed to favorites');
            }
            else {
                toastr.error('error');
            }

        })
    })
})

buttons_add_to_cart.forEach(async function(elem){
    elem.addEventListener("click", async function(){
        const product_id = this.id;
        console.log(shopCartViewUrl)
        fetch(shopCartViewUrl, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'product_id': product_id, 'quantity': 1})
        })
        .then(async response => {
            let data = await response.json();
            let status = await data.status;
            if (status == 'success'){
                toastr.success('Item successfully added to your cart');
            }
            else{
                toastr.error('Item was not added to the cart');
            }
        })
    })
})