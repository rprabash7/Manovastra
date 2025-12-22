// Wishlist Functionality
document.addEventListener('DOMContentLoaded', function() {
    updateWishlistCount();
    
    // Add to wishlist buttons
    const wishlistBtns = document.querySelectorAll('.wishlist-btn');
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const productId = this.dataset.productId;
            const productName = this.dataset.productName;
            
            addToWishlist(productId, productName, this);
        });
    });
    
    // Remove from wishlist buttons
    const removeBtns = document.querySelectorAll('.wishlist-remove');
    removeBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            removeFromWishlist(productId, this);
        });
    });
});

function addToWishlist(productId, productName, button) {
    fetch(`/wishlist/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            button.classList.add('active');
            updateWishlistCount();
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to add to wishlist', 'error');
    });
}

function removeFromWishlist(productId, button) {
    fetch(`/wishlist/remove/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove item from page
            const item = button.closest('.wishlist-item');
            if (item) {
                item.style.opacity = '0';
                setTimeout(() => {
                    item.remove();
                    
                    // Check if wishlist is empty
                    const grid = document.querySelector('.wishlist-grid');
                    if (grid && grid.children.length === 0) {
                        location.reload();
                    }
                }, 300);
            }
            
            updateWishlistCount();
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to remove from wishlist', 'error');
    });
}

function updateWishlistCount() {
    fetch('/wishlist/count/')
        .then(response => response.json())
        .then(data => {
            const countElement = document.getElementById('wishlistCount');
            if (countElement) {
                countElement.textContent = data.count;
                countElement.style.display = data.count > 0 ? 'flex' : 'none';
            }
        })
        .catch(error => console.error('Error updating wishlist count:', error));
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4caf50' : '#f44336'};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
