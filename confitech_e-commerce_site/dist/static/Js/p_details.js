const images = [
  "https://via.placeholder.com/600x700/667eea/ffffff?text=Galaxy+S24",
  "https://via.placeholder.com/600x700/764ba2/ffffff?text=View+2",
  "https://via.placeholder.com/600x700/f093fb/ffffff?text=View+3",
  "https://via.placeholder.com/600x700/4facfe/ffffff?text=View+4",
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

document.addEventListener("DOMContentLoaded", () => {
  toggleAccordion(0);
});
