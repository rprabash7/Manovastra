// Bestsellers Carousel (existing code)
const bestsellersGrid = document.getElementById('bestsellersGrid');
const bestsellersPrev = document.getElementById('bestsellersPrev');
const bestsellersNext = document.getElementById('bestsellersNext');

if (bestsellersGrid && bestsellersPrev && bestsellersNext) {
    const scrollAmount = 300;

    bestsellersPrev.addEventListener('click', () => {
        bestsellersGrid.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    bestsellersNext.addEventListener('click', () => {
        bestsellersGrid.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
}

// Ready to Wear Carousel (NEW)
const readyToWearGrid = document.getElementById('readyToWearGrid');
const readyToWearPrev = document.getElementById('readyToWearPrev');
const readyToWearNext = document.getElementById('readyToWearNext');

if (readyToWearGrid && readyToWearPrev && readyToWearNext) {
    const scrollAmount = 300;

    readyToWearPrev.addEventListener('click', () => {
        readyToWearGrid.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    readyToWearNext.addEventListener('click', () => {
        readyToWearGrid.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
}

// Add to Cart for all products
const addToCartBtns = document.querySelectorAll('.product-add-cart');
addToCartBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const productId = e.currentTarget.dataset.productId;
        alert(`Product ${productId} added to cart!`);
        // TODO: Implement actual cart functionality
    });
});

const weddingGrid = document.getElementById('weddingGrid');
const weddingPrev = document.getElementById('weddingPrev');
const weddingNext = document.getElementById('weddingNext');

if (weddingGrid && weddingPrev && weddingNext) {
    const scrollAmount = 300;

    weddingPrev.addEventListener('click', () => {
        weddingGrid.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    weddingNext.addEventListener('click', () => {
        weddingGrid.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
}

// Quick View functionality (placeholder)
const quickViewIcons = document.querySelectorAll('.quick-view-icon');
quickViewIcons.forEach(icon => {
    icon.addEventListener('click', (e) => {
        e.preventDefault();
        const productCard = e.currentTarget.closest('.product-card');
        const productName = productCard.querySelector('.product-name').textContent;
        alert(`Quick View: ${productName}`);
        // TODO: Implement modal quick view
    });
});
