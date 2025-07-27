// Newsletter subscription form handling
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.getElementById('newsletterForm');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = document.getElementById('newsletterEmail');
            const email = emailInput.value.trim();
            const feedbackEl = document.getElementById('newsletterFeedback');
            
            if (!email) {
                showToast('Please enter your email address', 'error', feedbackEl);
                return;
            }
            
            // Email validation regex
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showToast('Please enter a valid email address', 'error', feedbackEl);
                return;
            }
            
            // Send the subscription request to the server
            fetch('/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('Thank you for subscribing!', 'success', feedbackEl);
                    emailInput.value = '';
                } else {
                    showToast(data.message || 'Subscription failed. Please try again.', 'error', feedbackEl);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred. Please try again later.', 'error', feedbackEl);
            });
            
            // Show loading state
            const subscribeBtn = document.getElementById('subscribeBtn');
            const originalBtnText = subscribeBtn.innerHTML;
            subscribeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
            subscribeBtn.disabled = true;
            
            // Reset button after 2 seconds
            setTimeout(() => {
                subscribeBtn.innerHTML = originalBtnText;
                subscribeBtn.disabled = false;
            }, 2000);
        });
    }
    
    // Social media links
    const socialIcons = document.querySelectorAll('.social-icon');
    socialIcons.forEach(icon => {
        icon.addEventListener('click', function(e) {
            // If the link is just a placeholder (#), prevent default behavior
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
                showToast('Social media integration coming soon!', 'info');
            }
        });
    });
    
    // Footer links
    const footerBottomLinks = document.querySelectorAll('.footer-bottom-links a');
    footerBottomLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // If the link is just a placeholder (#), prevent default behavior
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
                showToast('This page is coming soon!', 'info');
            }
        });
    });
    
    // Toast notification function
    function showToast(message, type = 'info', feedbackEl = null) {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast element
        const toastId = 'toast-' + Date.now();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'primary'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.setAttribute('id', toastId);
        
        // Toast content
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        // Add toast to container
        toastContainer.appendChild(toast);
        
        // Initialize and show toast
        const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
        
        // Also update the form feedback element if provided
        if (feedbackEl) {
            feedbackEl.innerHTML = `<div class="alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} small">${message}</div>`;
            
            // Clear feedback after 5 seconds
            setTimeout(() => {
                feedbackEl.innerHTML = '';
            }, 5000);
        }
    }
});