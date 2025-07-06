const checkboxes_by_class = Array.from(document.getElementsByClassName('form-check-input'));
const currentUrl = new URL(location);
const buttons_add_to_cart = Array.from(document.getElementsByClassName('add_to_cart'));
const buttons_add_to_favorite = Array.from(document.getElementsByClassName('wishlist_btn'));

checkboxes_by_class.forEach(async function(elem){
    elem.addEventListener("change", async function(){
        const name = this.name;
        const value = this.value;
        if(this.checked){
            currentUrl.searchParams.append(name, value);
        } else {
            currentUrl.searchParams.delete(name, value);
        }
        updateURLAndFetch();
    });
});

const searchInput = document.getElementById("search-input");
searchInput.addEventListener("input", function() {
    const searchQuery = this.value;

    if (searchQuery) {
        currentUrl.searchParams.set("search", searchQuery);
    } else {
        currentUrl.searchParams.delete("search");
    }
    updateURLAndFetch();
});

function updateURLAndFetch(){
    history.pushState({}, "", currentUrl)
        fetch(urlProductList + '?' + currentUrl.searchParams.toString(), {method: "GET"})
        .then(async (response) => {
            const parser = new DOMParser();
            const textData = await response.text()
            const htmlData = parser.parseFromString(textData, "text/html");
            const productList = document.getElementById("id_product_list");
            productList.replaceWith(htmlData.getElementById("id_product_list"));
        })

}

buttons_add_to_cart.forEach(async function(elem){
    elem.addEventListener("click", async function(){
        const product_id = this.id;
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
            if (status == 'added'){
                elem.innerHTML = '<i class="fa-solid fa-star" style="color: #ff9500;"></i>';
                toastr.success('Successfully added to favorites');
            }
            else if (status == 'removed'){
                elem.innerHTML = '<i class="fa-solid fa-star""></i>';
                toastr.success('Successfully removed to favorites');
            }
            else {
                toastr.error('error');
            }

        })
    })
})