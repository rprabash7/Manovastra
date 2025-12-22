// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileSidebar = document.getElementById('mobileSidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const sidebarClose = document.getElementById('sidebarClose');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileSidebar.classList.add('active');
        sidebarOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
}

if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
}

if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
}

function closeSidebar() {
    mobileSidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

// Mobile Sidebar Dropdown
const sidebarDropdowns = document.querySelectorAll('.sidebar-dropdown > .sidebar-link');
sidebarDropdowns.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const parent = link.parentElement;
        const isActive = parent.classList.contains('active');
        
        // Close all dropdowns
        document.querySelectorAll('.sidebar-dropdown').forEach(item => {
            item.classList.remove('active');
        });
        
        // Toggle current dropdown
        if (!isActive) {
            parent.classList.add('active');
        }
    });
});

// Search Overlay
const searchBtn = document.getElementById('searchBtn');
const searchOverlay = document.getElementById('searchOverlay');
const searchClose = document.getElementById('searchClose');

if (searchBtn) {
    searchBtn.addEventListener('click', () => {
        searchOverlay.classList.add('active');
        document.body.style.overflow = 'hiddedinen';
    });
}

if (searchClose) {
    searchClose.addEventListener('click', () => {
        searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
    });
}

if (searchOverlay) {
    searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay) {
            searchOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// Search Functionality
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const searchProducts = document.getElementById('searchProducts');
const searchLoading = document.getElementById('searchLoading');
const searchNoResults = document.getElementById('searchNoResults');

let searchTimeout;

if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        
        // Clear previous timeout
        clearTimeout(searchTimeout);
        
        // Hide all states
        searchProducts.innerHTML = '';
        searchLoading.style.display = 'none';
        searchNoResults.style.display = 'none';
        
        if (query.length < 2) {
            return;
        }
        
        // Show loading
        searchLoading.style.display = 'block';
        
        // Debounce search
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Clear search on overlay open
    searchBtn.addEventListener('click', () => {
        searchInput.value = '';
        searchProducts.innerHTML = '';
        searchLoading.style.display = 'none';
        searchNoResults.style.display = 'none';
        
        // Focus on input
        setTimeout(() => {
            searchInput.focus();
        }, 100);
    });
}

function performSearch(query) {
    fetch(`/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            searchLoading.style.display = 'none';
            
            if (data.count === 0) {
                searchNoResults.style.display = 'block';
                return;
            }
            
            displaySearchResults(data.products);
        })
        .catch(error => {
            console.error('Search error:', error);
            searchLoading.style.display = 'none';
            searchNoResults.style.display = 'block';
        });
}

function displaySearchResults(products) {
    searchProducts.innerHTML = products.map(product => `
        <a href="${product.url}" class="search-product-item">
            <div class="search-product-info">
                <div class="search-product-category">${product.category}</div>
            </div>
        </a>
    `).join('');
}

// Close search on product click
if (searchProducts) {
    searchProducts.addEventListener('click', (e) => {
        if (e.target.closest('.search-product-item')) {
            searchOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

