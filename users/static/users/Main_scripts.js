/* Ajax request of adding food objects to the basket and checking if the objects are unique and not already their */
function run(food_title) {
  $.ajax({
    method: 'GET',
     url: '/ajax/basket/',
     dataType: 'json',
     success: function (data) {
     if (data.is_taken == "No_Login") {
          window.location.replace("/basket");
     }
    if(data.is_taken == "Not Copy") {
      document.getElementById("cart-number-id").innerHTML = Number(document.getElementById("cart-number-id").innerHTML) + 1
    }
    /* Code to change the contents of a tooltip to show if a food object is already in the basket */
    if(data.is_taken == "Copy") {
      $(document.getElementById(food_title)).tooltip('hide')
      .attr('data-original-title', 'Already In Basket')
      .tooltip('show');
    }

  },
     data: {
          "food_title": food_title
        },
   });
}

/* Deletes food object in basket so it stops displaying to the user and sends an ajax request to the server to delete the object from
the relational database aswell */
function food_element_destroy(food_title) {
  $.ajax({
    method: 'GET',
     url: '/ajax/checkout/',
     dataType: 'json',
     success: function (data) {
     $(".tooltip-hidden").tooltip('hide')
     element = document.getElementById(data.request);
     element.parentNode.removeChild(element);
     document.getElementById("cart-number-id").innerHTML = Number(document.getElementById("cart-number-id").innerHTML) - 1
     food_cost()
     $(".tooltip-hidden").tooltip('show')

  },
     data: {
          "food_title": food_title
        },
   });
}

/* Increases / Decreases the price of the checkout sum depending on what button the user clicks*/
function checkout_run(food_price,operator) {
food = document.getElementById(food_price).textContent
food = Number(food.replace("£", ""));
if (operator == "plus") {
  food = food + food_price
}
if (operator == "minus" && food - food_price > 0) {
  food = food - food_price
}
document.getElementById(food_price).innerHTML = "<b> £ " +food + "</b>"
food_cost()
}

/* Waits for document to be loaded then sets the tooltips up using jquery */
document.addEventListener("DOMContentLoaded", () => {
  $(".tooltip-hidden").tooltip({
    delay: {show: 0, hide: 500}
      });
  $(document).ready(function(){
 $('[data-toggle="tooltip"]').tooltip();
});
 });

/* Initializes the scroll-fade feature of elements within the application */
 $(document).on("scroll", function () {
 var pageTop = $(document).scrollTop()
 var pageBottom = pageTop + $(window).height()
 var tags = $("section")

 for (var i = 0; i < tags.length; i++) {
 var tag = tags[i]

 if ($(tag).position().top < pageBottom) {
 $(tag).addClass("visible")
 } else {
   $(tag).removeClass("visible")
 }
 }
 })

/* Function which is called upon within the checkout page and calculated the total cost of the food objects. */
function food_cost() {
  var total = 0;
  var price_list = document.getElementsByClassName("p-checkout");
  for (var i = 0; i < price_list.length; i++) {
  price = price_list[i].textContent
  price = Number(price.replace("£", ""))
  total = total + price
  }
  document.getElementById("final-checkout").innerHTML = "<b> Total Cost £" +total + "</b>"
  return(total)
}

/*Sets the total food cost for the stripe button, I know this actually should be done using quantity attributes on food objects :( */
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("Stripe_Button").addEventListener("click", function(){
    document.getElementById("cost-input").value = food_cost()
  });
 });
