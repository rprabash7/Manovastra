let currentSlide = 0;
let slideInterval;
const slides = document.querySelectorAll('.slideshow-slide');
const dots = document.querySelectorAll('.slideshow-dots .dot');
const autoplayDelay = 5000; // 5 seconds

// Initialize slideshow
if (slides.length > 0) {
    startAutoplay();
}

function showSlide(index) {
    // Reset if out of bounds
    if (index >= slides.length) {
        currentSlide = 0;
    } else if (index < 0) {
        currentSlide = slides.length - 1;
    } else {
        currentSlide = index;
    }

    // Hide all slides
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));

    // Show current slide
    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');
}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
    resetAutoplay();
}

function goToSlide(index) {
    showSlide(index);
    resetAutoplay();
}

function nextSlide() {
    showSlide(currentSlide + 1);
}

function startAutoplay() {
    slideInterval = setInterval(nextSlide, autoplayDelay);
}

function resetAutoplay() {
    clearInterval(slideInterval);
    startAutoplay();
}

// Pause on hover
const carousel = document.querySelector('.slideshow-carousel');
if (carousel) {
    carousel.addEventListener('mouseenter', () => {
        clearInterval(slideInterval);
    });

    carousel.addEventListener('mouseleave', () => {
        startAutoplay();
    });
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        changeSlide(-1);
    } else if (e.key === 'ArrowRight') {
        changeSlide(1);
    }
});

// Touch swipe support (mobile)
let touchStartX = 0;
let touchEndX = 0;

carousel?.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

carousel?.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    if (touchEndX < touchStartX - 50) {
        changeSlide(1); // Swipe left
    }
    if (touchEndX > touchStartX + 50) {
        changeSlide(-1); // Swipe right
    }
}
