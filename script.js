/* ==============================
   MOBILE MENU
============================== */

function toggleMenu(){

    let nav =
    document.getElementById(
    "navLinks"
    );

    nav.classList.toggle(
    "active"
    );
}

/* ==============================
   ADD TO CART
============================== */

let cart = [];

function addToCart(
name,
price
){

    cart.push({

        name:name,
        price:price
    });

    updateCartCount();

    showToast(
    name +
    " added to cart"
    );
}

/* ==============================
   CART COUNT
============================== */

function updateCartCount(){

    let count =
    document.getElementById(
    "cartCount"
    );

    if(count){

        count.innerText =
        cart.length;
    }
}

/* ==============================
   SEARCH PRODUCTS
============================== */

function searchProducts(){

    let input =
    document.getElementById(
    "searchInput"
    ).value.toLowerCase();

    let products =
    document.querySelectorAll(
    ".product-card"
    );

    products.forEach(product=>{

        let text =
        product.innerText
        .toLowerCase();

        if(text.includes(input)){

            product.style.display =
            "block";
        }

        else{

            product.style.display =
            "none";
        }
    });
}

/* ==============================
   TOAST NOTIFICATION
============================== */

function showToast(message){

    let toast =
    document.createElement(
    "div"
    );

    toast.className =
    "toast";

    toast.innerText =
    message;

    document.body.appendChild(
    toast
    );

    setTimeout(()=>{

        toast.classList.add(
        "show"
        );

    },100);

    setTimeout(()=>{

        toast.remove();

    },3000);
}

/* ==============================
   DARK MODE
============================== */

function toggleDarkMode(){

    document.body.classList.toggle(
    "dark-mode"
    );
}

/* ==============================
   PAGE LOADER
============================== */

window.onload = function(){

    let loader =
    document.getElementById(
    "loader"
    );

    if(loader){

        loader.style.display =
        "none";
    }
};