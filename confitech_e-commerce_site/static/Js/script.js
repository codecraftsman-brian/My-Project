class HeroCarousel {
  constructor() {
    this.currentSlide = 1;
    this.totalSlides = 3;
    this.slides = [];
    this.dots = [];
    this.autoScrollInterval = null;

    this.init();
  }

  init() {
    // Get all slide elements
    for (let i = 1; i <= this.totalSlides; i++) {
      this.slides.push(document.getElementById(`slide${i}`));
    }

    // Get all dot elements
    this.dots = document.querySelectorAll(".dot");

    // Add event listeners
    document
      .getElementById("prevBtn")
      .addEventListener("click", () => this.prevSlide());
    document
      .getElementById("nextBtn")
      .addEventListener("click", () => this.nextSlide());

    // Add click listeners to dots
    this.dots.forEach((dot, index) => {
      dot.addEventListener("click", () => this.goToSlide(index + 1));
    });

    // Start auto-scroll
    this.startAutoScroll();

    // Pause auto-scroll on hover
    const carousel = document.querySelector(".lg\\:col-span-3");
    carousel.addEventListener("mouseenter", () => this.pauseAutoScroll());
    carousel.addEventListener("mouseleave", () => this.startAutoScroll());
  }

  goToSlide(slideNumber) {
    // Hide current slide
    this.slides[this.currentSlide - 1].style.opacity = "0";
    this.slides[this.currentSlide - 1].classList.remove("slide-in");
    this.slides[this.currentSlide - 1].classList.add("slide-out");

    // Update current slide
    this.currentSlide = slideNumber;

    // Show new slide
    setTimeout(() => {
      this.slides[this.currentSlide - 1].style.opacity = "1";
      this.slides[this.currentSlide - 1].classList.remove("slide-out");
      this.slides[this.currentSlide - 1].classList.add("slide-in");
    }, 100);

    // Update dots
    this.updateDots();
  }

  nextSlide() {
    const nextSlideNumber =
      this.currentSlide === this.totalSlides ? 1 : this.currentSlide + 1;
    this.goToSlide(nextSlideNumber);
  }

  prevSlide() {
    const prevSlideNumber =
      this.currentSlide === 1 ? this.totalSlides : this.currentSlide - 1;
    this.goToSlide(prevSlideNumber);
  }

  updateDots() {
    this.dots.forEach((dot, index) => {
      if (index + 1 === this.currentSlide) {
        dot.classList.remove("bg-white/30");
        dot.classList.add("bg-white/50");
      } else {
        dot.classList.remove("bg-white/50");
        dot.classList.add("bg-white/30");
      }
    });
  }

  startAutoScroll() {
    this.autoScrollInterval = setInterval(() => {
      this.nextSlide();
    }, 5000); // Change slide every 5 seconds
  }

  pauseAutoScroll() {
    if (this.autoScrollInterval) {
      clearInterval(this.autoScrollInterval);
      this.autoScrollInterval = null;
    }
  }
}

class FlashSaleTimer {
  constructor() {
    this.endTime =
      new Date().getTime() + 12 * 60 * 60 * 1000 + 34 * 60 * 1000 + 56 * 1000; // 12h 34m 56s from now
    this.updateTimer();
    setInterval(() => this.updateTimer(), 1000);
  }

  updateTimer() {
    const now = new Date().getTime();
    const distance = this.endTime - now;

    if (distance < 0) {
      // Reset timer when it expires
      this.endTime = new Date().getTime() + 24 * 60 * 60 * 1000; // Reset to 24 hours
    }

    const hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("hours").textContent = hours
      .toString()
      .padStart(2, "0");
    document.getElementById("minutes").textContent = minutes
      .toString()
      .padStart(2, "0");
    document.getElementById("seconds").textContent = seconds
      .toString()
      .padStart(2, "0");
  }
}

class TVCarousel {
  constructor() {
    this.currentSlide = 1;
    this.totalSlides = 3;
    this.slides = [];
    this.dots = [];
    this.autoScrollInterval = null;

    this.init();
  }

  init() {
    // Get all TV slide elements
    for (let i = 1; i <= this.totalSlides; i++) {
      this.slides.push(document.getElementById(`tvSlide${i}`));
    }

    // Get all TV dot elements
    this.dots = document.querySelectorAll(".tv-dot");

    // Add event listeners
    document
      .getElementById("tvPrevBtn")
      .addEventListener("click", () => this.prevSlide());
    document
      .getElementById("tvNextBtn")
      .addEventListener("click", () => this.nextSlide());

    // Add click listeners to dots
    this.dots.forEach((dot, index) => {
      dot.addEventListener("click", () => this.goToSlide(index + 1));
    });

    // Start auto-scroll
    this.startAutoScroll();

    // Pause auto-scroll on hover
    const tvCarousel = document.querySelector(".flex-1 .rounded-2xl");
    if (tvCarousel) {
      tvCarousel.addEventListener("mouseenter", () => this.pauseAutoScroll());
      tvCarousel.addEventListener("mouseleave", () => this.startAutoScroll());
    }
  }

  goToSlide(slideNumber) {
    // Hide current slide
    this.slides[this.currentSlide - 1].style.opacity = "0";

    // Update current slide
    this.currentSlide = slideNumber;

    // Show new slide
    setTimeout(() => {
      this.slides[this.currentSlide - 1].style.opacity = "1";
    }, 100);

    // Update dots
    this.updateDots();
  }

  nextSlide() {
    const nextSlideNumber =
      this.currentSlide === this.totalSlides ? 1 : this.currentSlide + 1;
    this.goToSlide(nextSlideNumber);
  }

  prevSlide() {
    const prevSlideNumber =
      this.currentSlide === 1 ? this.totalSlides : this.currentSlide - 1;
    this.goToSlide(prevSlideNumber);
  }

  updateDots() {
    this.dots.forEach((dot, index) => {
      if (index + 1 === this.currentSlide) {
        dot.classList.remove("bg-white/30");
        dot.classList.add("bg-white/50");
      } else {
        dot.classList.remove("bg-white/50");
        dot.classList.add("bg-white/30");
      }
    });
  }

  startAutoScroll() {
    this.autoScrollInterval = setInterval(() => {
      this.nextSlide();
    }, 4000); // Change slide every 4 seconds
  }

  pauseAutoScroll() {
    if (this.autoScrollInterval) {
      clearInterval(this.autoScrollInterval);
      this.autoScrollInterval = null;
    }
  }
}

// Initialize carousel when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new HeroCarousel();
  new FlashSaleTimer();
  new TVCarousel();
});
