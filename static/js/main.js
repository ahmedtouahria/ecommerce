$(document).ready(function () {
 // "use strict";
  //------- Active Nice Select --------//
  $("select").niceSelect();
  /*=================================
    Javascript for single product area carousel
    ==================================*/
  $(".s_Product_carousel").owlCarousel({
    items: 1,
    autoplay: false,
    autoplayTimeout: 5000,
    loop: true,
    nav: false,
    dots: true,
  });

  /*================================
    Javascript for exclusive area carousel
    ==================================*/

  $(".quick-view-carousel-details").owlCarousel({
    loop: true,
    dots: true,
    items: 1,
  });

  //----- Active No ui slider --------//

  $(function () {
    if (document.getElementById("price-range")) {
      var nonLinearSlider = document.getElementById("price-range");

      noUiSlider.create(nonLinearSlider, {
        connect: true,
        behaviour: "tap",
        start: [500, 4000],
        range: {
          // Starting at 500, step the value by 500,
          // until 4000 is reached. From there, step by 1000.
          min: [0],
          "10%": [500, 500],
          "50%": [4000, 1000],
          max: [10000],
        },
      });

      var nodes = [
        document.getElementById("lower-value"), // 0
        document.getElementById("upper-value"), // 1
      ];

      // Display the slider value and how far the handle moved
      // from the left edge of the slider.
      nonLinearSlider.noUiSlider.on(
        "update",
        function (values, handle, unencoded, isTap, positions) {
          nodes[handle].innerHTML = values[handle];
        }
      );
    }
  });

  //-------- Have Cupon Button Text Toggle Change -------//

  $(".have-btn").on("click", function (e) {
    e.preventDefault();
    $(".have-btn span").text(function (i, text) {
      return text === "Have a Coupon?" ? "Close Coupon" : "Have a Coupon?";
    });
    $(".cupon-code").fadeToggle("slow");
  });

  $(".load-more-btn").on("click", function (e) {
    e.preventDefault();
    $(".load-product").fadeIn("slow");
    $(this).fadeOut();
  });
});
///////////////////////////////////////////////////////////////////////

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

/* /////////////////////////////////
var form = $("#form");
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
} */
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

  try {
    const shareBtn = document.getElementById("copy");
    const title = "title";
    const url = code_url;
    //const ogBtnContent = shareBtn.textContent;
    shareBtn.addEventListener("click", () => {
      if (navigator.share) {
        navigator
          .share({
            title,
            url,
          })
          .then(() => {})
          .catch((err) => {
            showMessage(shareBtn, `Couldn't share 🙁`);
          });
      } else {
        showMessage(shareBtn, "Not supported 🙅‍");
      }
    });
  } catch {
    console.log("copy is not defined");
  }
  function showMessage(element, msg) {
    element.textContent = msg;
    setTimeout(() => {
      element.textContent = "";
    }, 2000);
  }

  var dropdown_panel = document.getElementById("dropdown_panel");
  $.ajax({
    url: "/api/category/",
    type: "GET",
    dataType: "json", // added data type
    success: function (data) {
      dropdown_panel.innerHTML = "";
      var i = 0;
      data.forEach((element) => {
        var sub_cat = element.sub_cat;
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
        var panel_list_item =
          document.getElementsByClassName("panel_list_item");
        var arr_panel_list_item = [];
        console.log(i);
        //panel_list_item[i].innerHTML='';
        sub_cat.forEach((cat) => {
          panel_list_item[i].innerHTML += `<a href="#">${cat.name}</a>`;
        });
        console.log(arr_panel_list_item);
        i++;
      }); // data.forEach end
    }, //end success
  }); //ajax end
  ////////////////////////////////////////
  var wilaya_select = document.getElementsByClassName("wilaya");
  var commun_select = $("#commun");

  //wilaya_select[i].innerHTML='';
  $.ajax({
    url: "/getwilaya",
    type: "GET",
    dataType: "json", // added data type
    success: function (data) {
      arr = [];
      data.forEach((element) => {
        //console.log(element.name);
        for (var i = 0; i < wilaya_select.length; i++) {
          wilaya_select[
            i
          ].innerHTML += `<option name="state" value="${element.name}">${element.id} ${element.name}</option>`;
        }
      });
    },
  });
  wilaya_select[0].onchange = function (e) {
    console.log(e.target.value);
    commun_select.innerHTML = "";
    var current_wilaya = e.target.value;
    //display related communs
    $.ajax({
      url: "/api/getcommunstrus/",
      type: "GET",
      dataType: "json", // added data type
      success: function (data) {
        data["communs"].forEach((element) => {
          if (element.wilaya_name == current_wilaya) {
            commun_select.innerHTML += `<option name="commun" value="${element.name}">${element.name}</option>`;
          }
        });
      },
    });
    var shipping = document.getElementById("shipping");
    // and display deliveryfees
    $.ajax({
      url: "/api/getcommunstrus/",
      type: "GET",
      dataType: "json", // added data type
      success: function (data) {
        data["deliveryfees"].forEach((element) => {
          if (element.wilaya_name == current_wilaya) {
            shipping.innerHTML = `${element.desk_fee} DA`;
          }
        });
      },
    });
  };
}); // end  document ready


// modal variables
const modal = document.querySelector("[data-modal]");
const modalCloseBtn = document.querySelector("[data-modal-close]");
const modalCloseOverlay = document.querySelector("[data-modal-overlay]");

// modal function
const modalCloseFunc = function () {
  modal.classList.add("closed");
};

// modal eventListener
modalCloseOverlay.addEventListener("click", modalCloseFunc);
modalCloseBtn.addEventListener("click", modalCloseFunc);

// notification toast variables
const notificationToast = document.querySelector("[data-toast]");
const toastCloseBtn = document.querySelector("[data-toast-close]");

// notification toast eventListener
toastCloseBtn.addEventListener("click", function () {
  notificationToast.classList.add("closed");
});

// mobile menu variables
const mobileMenuOpenBtn = document.querySelectorAll(
  "[data-mobile-menu-open-btn]"
);
const mobileMenu = document.querySelectorAll("[data-mobile-menu]");
const mobileMenuCloseBtn = document.querySelectorAll(
  "[data-mobile-menu-close-btn]"
);
const overlay = document.querySelector("[data-overlay]");

for (let i = 0; i < mobileMenuOpenBtn.length; i++) {
  // mobile menu function
  const mobileMenuCloseFunc = function () {
    mobileMenu[i].classList.remove("active");
    overlay.classList.remove("active");
  };

  mobileMenuOpenBtn[i].addEventListener("click", function () {
    mobileMenu[i].classList.add("active");
    overlay.classList.add("active");
  });

  mobileMenuCloseBtn[i].addEventListener("click", mobileMenuCloseFunc);
  overlay.addEventListener("click", mobileMenuCloseFunc);
}

// accordion variables
const accordionBtn = document.querySelectorAll("[data-accordion-btn]");
const accordion = document.querySelectorAll("[data-accordion]");

for (let i = 0; i < accordionBtn.length; i++) {
  accordionBtn[i].addEventListener("click", function () {
    const clickedBtn = this.nextElementSibling.classList.contains("active");

    for (let i = 0; i < accordion.length; i++) {
      if (clickedBtn) break;

      if (accordion[i].classList.contains("active")) {
        accordion[i].classList.remove("active");
        accordionBtn[i].classList.remove("active");
      }
    }

    this.nextElementSibling.classList.toggle("active");
    this.classList.toggle("active");
  });
}
