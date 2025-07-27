// Get fully year on the footer
$("#year").text(new Date().getFullYear());

//Navbar background and color changes on scrooll
$(document).ready(function () {
  $(window).scroll(function () {
    if ($(document).scrollTop() > 20) {
      $(".navbar").addClass("active");
      $(".nav-link").addClass("nav-link-active ");
      $(".navbar .logo").addClass("nav-logo-active");
    } else {
      $(".navbar").removeClass("active");
      $(".nav-link").removeClass("nav-link-active");
      $(".navbar .logo").removeClass("nav-logo-active");
    }
  });
});
