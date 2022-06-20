
function getCartItem() {
  $.ajax({
    url: "/api/cartitemApi/",
    type: "GET",
    success: function (res) {
      console.log(res.cartItem);
      $(".cartItem").html(res.cartItem);
    },
  });
}
//console.log("Cart:", cart);

/////////////////////////////////
var form = document.getElementById("form");
form.addEventListener("submit", function (e) {
  e.preventDefault();
  submitFormData();
});
function submitFormData() {
  console.log("submite button clicked");
  var userFormData = {
    name: null,
    phone: null,
    total: total,
  };
  var shippingInfo = {
    address: null,
    city: null,
    state: null,
    zipcode: null,
  };
  shippingInfo.address = form.address.value;
  shippingInfo.city = form.commun.value;
  shippingInfo.state = form.wilaya.value;
  shippingInfo.zipcode = form.zipcode.value;

  if (user == "AnonymousUser") {
    userFormData.name = form.name.value;
    userFormData.phone = form.phone.value;
  } else {
    userFormData.name = name;
    userFormData.phone = phone;
  }

  console.log("Shipping Info:", shippingInfo);
  console.log("User Info:", userFormData);

  var url = "/process_order/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "applicaiton/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ form: userFormData, shipping: shippingInfo }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      fireSweetAlert();
      cart = {};
      document.cookie =
        "cart=" + JSON.stringify(cart) + ";domain=;path=/";
      window.location.href = "{% url 'products' %}";
    })
    .catch((error) => {
      fireSweetAlertError();
      console.error("Error:", error);
    });
}
// function swite alert to hundel beutifule alert
// success alert
function fireSweetAlert() {
  const Toast = Swal.mixin({
    toast: true,
    position: "top",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener("mouseenter", Swal.stopTimer);
      toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
  });

  Toast.fire({
    icon: "success",
    title: "order sent successfully !",
  });
}
// error alert
function fireSweetAlertError() {
  const Toast = Swal.mixin({
    toast: true,
    position: "top",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener("mouseenter", Swal.stopTimer);
      toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
  });
  Toast.fire({
    icon: "error",
    title: "order has a problem !",
  });
}

//////////////////////////////////////////////

var swiper = new Swiper(".mySwiper", {
    spaceBetween: 30,
    centeredSlides: true,
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
  $(document).ready(function () {
    const tabs = document.querySelectorAll("[data-target]"),
    tabContents = document.querySelectorAll("[data-content]");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const target = document.querySelector(tab.dataset.target);
      tabContents.forEach((tc) => {
        tc.classList.remove("is-active");
      });
      target.classList.add("is-active");

      tabs.forEach((t) => {
        t.classList.remove("is-active");
      });
      tab.classList.add("is-active");
    });
  });

    
    $(".custom-select").niceSelect("destroy");

    //--------- script to hundel sidebar for mini devices---------//
    $("#sidebarCollapse").on("click", function () {
      $("#sidebar").addClass("active");
    });
    $("#sidebarCollapseX").on("click", function () {
      $("#sidebar").removeClass("active");
    });
    $("#sidebarCollapse").on("click", function () {
      if ($("#sidebar").hasClass("active")) {
        $(".overlay").addClass("visible");
        // console.log("it's working!");
      }
    });
    $("#sidebarCollapseX").on("click", function () {
      $(".overlay").removeClass("visible");
    });
    setTimeout(() => {
      if ($("#alert").length > 0) {
        $("#alert").fadeOut();
      }
    }, 4000);
    //--------end script to hundel sidebar for mini devices--------//
    /* -----script to meal rating-------*/
    $(".rating label").on("click", function () {
      //console.log(user_id);
      //console.log(this.dataset.rate);
      var content = $("#content").val();
      var stars = this.dataset.rate;
      var product_id = this.dataset.product;
      //console.log(content)
      //console.log(product_id);
      let data = {
        user_id: user_id,
        product_id: product_id,
        stars: stars,
        content: content,
      };
      if (user == "AnonymousUser") {
        window.location.href = "/login";
      } else {
        if (content.trim() == "") {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Please don't leave the comment field blank",
            confirmButtonColor: "#ffba00",
          });
        } else {
          fetch("/api/product_rating/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify(data),
          }).then((res) => {
            location.reload();
            console.log("Request complete! response:", res);
          });
        }
      }
    });

    /* ----- end script to meal rating-------*/

    //---------------script to copy in clipboard with web Api---------------//
const shareBtn=document.getElementById('copy');
const title="title";
const url=code_url;
//const ogBtnContent = shareBtn.textContent;
shareBtn.addEventListener('click', () => {
        if (navigator.share) {
          navigator.share({
            title,
            url
          }).then(() => {
            
          })
          .catch(err => {
            showMessage(shareBtn, `Couldn't share 🙁`);
          });
        } else {
          showMessage(shareBtn, 'Not supported 🙅‍');
        }
      });
      
      function showMessage(element, msg) {
        element.textContent = msg;
        setTimeout(() => {
          element.textContent = '';
        }, 2000);
      }
    ///////////////////////--Scripts to hundel requests (search product , filter data ) --///////////////////////////////////////////

    $("#username").keyup(function () {
        let username = $(this).val().trim();
        $.ajax({
          url: "/api/validate_username/",
          data: { username: username },
          dataType: "json",
          success: function (data) {
            if (data.is_exists) {
              console.log("existe");
              $("#username").addClass("is-invalid");
            } else {
              console.log("success");
              $("#username").removeClass("is-invalid").addClass("is-valid");
            }
          },
        });
      });
      //------ script realtime to test phone---//
      $("#phone").keyup(function () {
        let phone = $(this).val().trim();
        $.ajax({
          url: "/api/validate_username/",
          data: { phone: phone },
          dataType: "json",
          success: function (data) {
            if (data.is_number_exists) {
              console.log("existe");
              $("#phone").addClass("is-invalid");
            } else {
              if (phone.length == 10) {
                console.log("success");
                $("#phone").removeClass("is-invalid").addClass("is-valid");
              } else {
                $("#phone").addClass("is-invalid");
              }
            }
          },
        });
      });
      /////////////// script realtime search ///////////////////
      $("#search").keyup(function () {
        let search_data = $(this).val();
    //	let lower_value = $("#lower-value").html();
    //	let upper_value = $("#upper-value").html();
        if (search_data.trim().length > 0) {
          $.ajax({
            url: "/api/search_products/",
            data: {
              search_data: search_data,
             // lower_value: lower_value,
            //  upper_value: upper_value,
            },
            dataType: "json",
            success: function (data) {
              $("#list_product").html("");
              console.log(data);
              if (data.length == 0) {
                $("#list_product").html(
                  ' <div class="my-5" style="width: 100%;text-align: center;"> <img src="{% static "img/no_data.svg" %}" width="200" height="200" ><h1>No data found</h1></div>'
                );
              } else {
                data.forEach((element) => {
                  document.getElementById("list_product").innerHTML += `
          
                  <div class="showcase">

                    <div class="showcase-banner">
              
                      <img src="/media/${element.image}" alt="Mens Winter Leathers Jackets" width="300" class="product-img default">
                      <img src="/media/${element.image}" alt="Mens Winter Leathers Jackets" width="300" class="product-img hover">
              
                      <p class="showcase-badge">15%</p>
              
                      <div class="showcase-actions">
              
                        <button class="btn-action">
                          <ion-icon name="heart-outline"></ion-icon>
                        </button>
              
                        <button class="btn-action">
                          <ion-icon name="eye-outline"></ion-icon>
                        </button>
              
                        <button class="btn-action">
                          <ion-icon name="repeat-outline"></ion-icon>
                        </button>
              
                        <button class="btn-action update-cart"  data-action="add"
                        data-product="${element.id}">
                          <ion-icon name="bag-add-outline"></ion-icon>
                        </button>
              
                      </div>
              
                    </div>
              
                    <div class="showcase-content">
              
                      <a href="#" class="showcase-category">${element.category_id}</a>
              
                      <a href="">
                        <h3 class="showcase-title">${element.name}</h3>
                      </a>
              
                      <div class="showcase-rating">
                        {% if product.avg_rating == 5 %}
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        {% elif product.avg_rating == 4 %}
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star"></i>
              
                        {% elif product.avg_rating == 3 %}
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
              
                        {% elif product.avg_rating == 2 %}
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
              
                        {% elif product.avg_rating == 1 %}
                        <i class="fa fa-star text-warning"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        {% else %}
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        {% endif %}
                      </div>
              
                      <div class="price-box">
                        <p class="price">${element.price}</p>
                        <del>${element.price}</del>
                      </div>
              
                    </div>
              
                  </div>
          
          `;
                });
              }
            },
          });
        }
      });

$(".category").click(function () {
  let val = $(this).val();
  let lower_value = $("#lower-value").html();
  let upper_value = $("#upper-value").html();
  console.log(val);
  $.ajax({
    url: "/api/search_products/",
    data: {
      search_data: val,
      lower_value: lower_value,
      upper_value: upper_value,
    },
    dataType: "json",
    success: function (data) {
      $("#list_product").html("");
      console.log(data);
      if (data.length == 0) {
        $("#list_product").html(
          ' <div class="my-5" style="width: 100%;text-align: center;"> <img src="{% static "img/no_data.svg" %}" width="200" height="200" ><h1>No data found</h1></div>'
        );
      } else {
        data.forEach((element) => {
          document.getElementById("list_product").innerHTML += `
    
    <div class="col-lg-4 col-md-6">
        <div class="single-product" style="margin-bottom: 0;">
            <img  width="200" height="250" src="/media/${element.image}" alt="">
            <div class="product-details">
                <h6>${element.name}</h6>
                <div class="price">
                    <h6>${element.price}$</h6>
                    <h6 class="l-through">${element.price}$</h6>
                </div>
                <div class="prd-bottom">
                    <a data-action="add" data-product=${element.id} class="social-info update-cart" onclick=" if (user!='AnonymousUser'){updateUserOrder(${element.id}, 'add')}else {addCookieItem(${element.id}, 'add')};">
                        <span class="ti-bag"></span>
                        <p class="hover-text ">add to bag</p>
                    </a>
                    <a href="" class="social-info">
                        <span class="lnr lnr-heart"></span>
                        <p class="hover-text">Wishlist</p>
                    </a>
                    <a href="/products/${element.id}" class="social-info">
                        <span class="lnr lnr-select"></span>
                        <p class="hover-text">Show more</p>
                    </a>
      
                </div>
            </div>
        </div>
    </div>
    
    `;
        });
      }
    },
  });
});



    //--- script realtime filter ----//
 
    //--- END--script realtime filter ----//

    //////////////////////////////////////
    $(".category").click(function () {
        let val = $(this).val();
        let lower_value = $("#lower-value").html();
        let upper_value = $("#upper-value").html();
        console.log(val);
        $.ajax({
          url: "/search_products/",
          data: {
            search_data: val,
            lower_value: lower_value,
            upper_value: upper_value,
          },
          dataType: "json",
          success: function (data) {
            $("#list_product").html("");
            console.log(data);
            if (data.length == 0) {
              $("#list_product").html(
                ' <div class="my-5" style="width: 100%;text-align: center;"> <img src="{% static "img/no_data.svg" %}" width="200" height="200" ><h1>No data found</h1></div>'
              );
            } else {
              data.forEach((element) => {
                document.getElementById("list_product").innerHTML += `
          
          <div class="col-lg-4 col-md-6">
              <div class="single-product" style="margin-bottom: 0;">
                  <img  width="200" height="250" src="/media/${element.image}" alt="">
                  <div class="product-details">
                      <h6>${element.name}</h6>
                      <div class="price">
                          <h6>${element.price}$</h6>
                          <h6 class="l-through">${element.price}$</h6>
                      </div>
                      <div class="prd-bottom">
                          <a data-action="add" data-product=${element.id} class="social-info update-cart" onclick=" if (user!='AnonymousUser'){updateUserOrder(${element.id}, 'add')}else {addCookieItem(${element.id}, 'add')};">
                              <span class="ti-bag"></span>
                              <p class="hover-text ">add to bag</p>
                          </a>
                          <a href="" class="social-info">
                              <span class="lnr lnr-heart"></span>
                              <p class="hover-text">Wishlist</p>
                          </a>
                          <a href="/products/${element.id}" class="social-info">
                              <span class="lnr lnr-select"></span>
                              <p class="hover-text">Show more</p>
                          </a>
            
                      </div>
                  </div>
              </div>
          </div>
          
          `;
              });
            }
          },
        });
      });
      /////////////////////////////////////////////////////////////////////

	 var dropdown_panel = document.getElementById("dropdown_panel");
     $.ajax({
        url: "/api/category/",
        type: "GET",
        dataType: "json", // added data type
        success: function (data) {
      dropdown_panel.innerHTML = '';
      var i=0;
      data.forEach((element) => {
        var sub_cat=element.sub_cat;
        dropdown_panel.innerHTML += ` <ul class="dropdown-panel-list">
                  <li class="menu-title">
                    <a href="#">${element.name}</a>
                  </li>
                  <li class="panel-list-item panel_list_item" id="panel_list_item">
                  </li>
                  <li class="panel-list-item">
                    <a href="#">
                      <img src="${element.image}" alt="headphone collection" width="250"
                        height="119">
                    </a>
                  </li>
    
                </ul>`;
        var panel_list_item = document.getElementsByClassName("panel_list_item");
        var arr_panel_list_item=[];
          console.log(i);
          //panel_list_item[i].innerHTML='';
          sub_cat.forEach(cat=>{
          panel_list_item[i].innerHTML+=`<a href="#">${cat.name}</a>`;
          })
          console.log(arr_panel_list_item)
          i++;
      }); // data.forEach end
  
      }, //end success
  }); //ajax end
  ////////////////////////////////////////
  var wilaya_select=document.getElementsByClassName("wilaya");
  var commun_select=document.getElementById("commun");
  
      //wilaya_select[i].innerHTML='';
              $.ajax({
          url: "/getwilaya",
          type: 'GET',
          dataType: 'json', // added data type
          success: function(data) {
            arr=[];
            data.forEach(element=>{
            //console.log(element.name);
            for(var i=0;i<wilaya_select.length;i++){
            wilaya_select[i].innerHTML+=`<option name="state" value="${element.name}">${element.id} ${element.name}</option>`;
          }
            })
  
          }
        });
  wilaya_select[0].onchange=function(e){
          console.log(e.target.value);
          commun_select.innerHTML='';
          var current_wilaya=e.target.value;
          //display related communs 
          $.ajax({
          url: "/api/getcommunstrus/",
          type: 'GET',
          dataType: 'json', // added data type
          success: function(data) {
            data['communs'].forEach(element=>{
            if(element.wilaya_name==current_wilaya){
              commun_select.innerHTML+=
              `<option name="commun" value="${element.name}">${element.name}</option>`;}
            })
  
          },
        });
        var shipping = document.getElementById('shipping')
        // and display deliveryfees
        $.ajax({
          url: "/api/getcommunstrus/",
          type: 'GET',
          dataType: 'json', // added data type
          success: function(data) {
            data['deliveryfees'].forEach(element=>{
            if(element.wilaya_name==current_wilaya){
              shipping.innerHTML=`${element.desk_fee} DA`;
            }
            })
  
          },
        });
      };
  }); // end  document ready
  
  const mobileMenuOpenBtn = document.querySelectorAll('[data-mobile-menu-open-btn]');
const mobileMenu = document.querySelectorAll('[data-mobile-menu]');
const mobileMenuCloseBtn = document.querySelectorAll('[data-mobile-menu-close-btn]');
const overlay = document.querySelector('[data-overlay]');

for (let i = 0; i < mobileMenuOpenBtn.length; i++) {

  // mobile menu function
  const mobileMenuCloseFunc = function () {
    mobileMenu[i].classList.remove('active');
    overlay.classList.remove('active');
  }

  mobileMenuOpenBtn[i].addEventListener('click', function () {
    mobileMenu[i].classList.add('active');
    overlay.classList.add('active');
  });

  mobileMenuCloseBtn[i].addEventListener('click', mobileMenuCloseFunc);
  overlay.addEventListener('click', mobileMenuCloseFunc);

}





// accordion variables
const accordionBtn = document.querySelectorAll('[data-accordion-btn]');
const accordion = document.querySelectorAll('[data-accordion]');

for (let i = 0; i < accordionBtn.length; i++) {

  accordionBtn[i].addEventListener('click', function () {

    const clickedBtn = this.nextElementSibling.classList.contains('active');

    for (let i = 0; i < accordion.length; i++) {

      if (clickedBtn) break;

      if (accordion[i].classList.contains('active')) {

        accordion[i].classList.remove('active');
        accordionBtn[i].classList.remove('active');

      }

    }

    this.nextElementSibling.classList.toggle('active');
    this.classList.toggle('active');

  });

}