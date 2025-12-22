// Cart JavaScript
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    
    // Quantity buttons
    const qtyBtns = document.querySelectorAll('.qty-btn');
    qtyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const action = this.dataset.action;
            const input = document.querySelector(`.qty-input[data-product-id="${productId}"]`);
            let quantity = parseInt(input.value);
            
            if (action === 'increase') {
                quantity++;
            } else if (action === 'decrease' && quantity > 1) {
                quantity--;
            }
            
            input.value = quantity;
            updateCartItem(productId, quantity);
        });
    });
    
    // Remove buttons
    const removeBtns = document.querySelectorAll('.cart-item-remove');
    removeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.productId;
            removeCartItem(productId);
        });
    });
});

function updateCartItem(productId, quantity) {
    fetch(`/cart/update/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartUI(data.cart_data);
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to update cart', 'error');
    });
}

function removeCartItem(productId) {
    if (!confirm('Remove this item from cart?')) {
        return;
    }
    
    fetch(`/cart/remove/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const item = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
            if (item) {
                item.style.opacity = '0';
                setTimeout(() => {
                    item.remove();
                    
                    if (data.cart_data.count === 0) {
                        location.reload();
                    } else {
                        updateCartUI(data.cart_data);
                    }
                }, 300);
            }
            
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to remove item', 'error');
    });
}

function updateCartUI(cartData) {
    // Update summary
    document.getElementById('summarySubtotal').textContent = `₹${parseFloat(cartData.subtotal).toFixed(0)}`;
    
    const shippingElement = document.getElementById('summaryShipping');
    if (parseFloat(cartData.shipping) === 0) {
        shippingElement.innerHTML = '<span class="free-shipping">FREE</span>';
    } else {
        shippingElement.textContent = `₹${parseFloat(cartData.shipping).toFixed(0)}`;
    }
    
    document.getElementById('summaryTotal').textContent = `₹${parseFloat(cartData.total).toFixed(0)}`;
    
    // Update cart count
    updateCartCount();
}

function updateCartCount() {
    fetch('/cart/count/')
        .then(response => response.json())
        .then(data => {
            const countElements = document.querySelectorAll('.cart-count, #cartCount');
            countElements.forEach(element => {
                element.textContent = data.count;
                element.style.display = data.count > 0 ? 'flex' : 'none';
            });
        });
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
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
