const images = [
  "static/images/products/smartwatch/S24_ultra.jpg",
  "static/images/products/smartwatch/S24_ultra_amoled.jpg",
  "static/images/products/smartwatch/S24_ultra_waterproof.jpg",
  "static/images/products/smartwatch/S24_ultra_bluetooth.jpg",
];

function changeImage(index) {
  document.getElementById("mainImage").src = images[index];
  document.querySelectorAll('[onclick^="changeImage"]').forEach((thumb, i) => {
    thumb.classList.toggle("thumbnail-active", i === index);
  });
}

function selectSize(button) {
  document
    .querySelectorAll(".size-button")
    .forEach((btn) => btn.classList.remove("active"));
  button.classList.add("active");
}

function increaseQuantity() {
  const input = document.getElementById("quantityInput");
  let value = parseInt(input.value);
  if (value < 10) input.value = value + 1;
}

function decreaseQuantity() {
  const input = document.getElementById("quantityInput");
  let value = parseInt(input.value);
  if (value > 1) input.value = value - 1;
}

//product middle navbar
function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId);
  const navTabs = document.querySelectorAll(".nav-tab");

  // Remove active class from all tabs
  navTabs.forEach((tab) => tab.classList.remove("active"));

  // Add active class to clicked tab
  event.target.classList.add("active");

  // Smooth scroll to section
  section.scrollIntoView({ behavior: "smooth", block: "start" });
}

// Intersection Observer for sticky nav
const sections = ["product-overview", "product-features", "product-reviews"];
const navTabs = document.querySelectorAll(".nav-tab");

const observerOptions = {
  root: null,
  rootMargin: "-100px 0px 0px 0px",
  threshold: 0.1,
};

// Product information dropdown
function toggleAccordion(index) {
  const contents = document.querySelectorAll(".accordion-content");
  const icons = document.querySelectorAll(".accordion-icon");
  const content = contents[index];
  const icon = icons[index];

  content.classList.toggle("active");
  icon.style.transform = content.classList.contains("active")
    ? "rotate(180deg)"
    : "rotate(0deg)";
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const sectionId = entry.target.id;
      navTabs.forEach((tab, index) => {
        tab.classList.remove("active");
        if (sections[index] === sectionId) {
          tab.classList.add("active");
        }
      });
    }
  });
}, observerOptions);

sections.forEach((sectionId) => {
  const section = document.getElementById(sectionId);
  if (section) observer.observe(section);
});

document.addEventListener("DOMContentLoaded", () => {
  toggleAccordion(0);
});
