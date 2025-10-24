// Pagination functionality
document.querySelectorAll(".pagination-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    document
      .querySelectorAll(".pagination-btn")
      .forEach((b) => b.classList.remove("active"));
    this.classList.add("active");
  });
});
