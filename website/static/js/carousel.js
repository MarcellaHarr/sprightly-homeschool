
document.addEventListener("DOMContentLoaded", function () {
  const prevBtn = document.querySelector(".carousel-control-prev");
  const nextBtn = document.querySelector(".carousel-control-next");
  prevBtn.addEventListener("click", function () {
    const carousel = document.getElementById("myCarousel");
    const activeItem = carousel.querySelector(".carousel-item.active");
    if (activeItem.previousElementSibling) {
      activeItem.classList.remove("active");
      activeItem.previousElementSibling.classList.add("active");
    } else {
      // If there is no previous item, go to the last item
      const lastItem = carousel.querySelector(".carousel-item:last-child");
      activeItem.classList.remove("active");
      lastItem.classList.add("active");
    }
  });
  nextBtn.addEventListener("click", function () {
    const carousel = document.getElementById("myCarousel");
    const activeItem = carousel.querySelector(".carousel-item.active");
    if (activeItem.nextElementSibling) {
      activeItem.classList.remove("active");
      activeItem.nextElementSibling.classList.add("active");
    } else {
      // If there is no next item, go to the first item
      const firstItem = carousel.querySelector(
        ".carousel-item:first-child"
      );
      activeItem.classList.remove("active");
      firstItem.classList.add("active");
    }
  });
});
