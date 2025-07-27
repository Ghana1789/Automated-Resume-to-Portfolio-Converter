document.addEventListener('DOMContentLoaded', function() {
    // Initialize counters and animations
    initializeCounters();
    initializeTypewriter();
    
    // Initialize download functionality
    initializeDownload();
    
    // Get all sections that have an ID defined
    const sections = document.querySelectorAll('section[id]');
    // Get all sidebar links
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    
    // Add an event listener for scroll
    window.addEventListener('scroll', function() {
        // Get current scroll position
        let scrollY = window.pageYOffset;
        
        // Loop through sections to determine which one is currently in view
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 100; // Offset for better UX
            const sectionId = current.getAttribute('id');
            
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                // Find the corresponding sidebar link and add active class
                sidebarLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('active');
                    }
                });
            }
        });
        
        // Parallax effect for header
        const header = document.querySelector('.portfolio-header');
        if (header) {
            const scrollPosition = window.pageYOffset;
            header.style.backgroundPositionY = scrollPosition * 0.5 + 'px';
        }
    });
    
    // Add smooth scrolling for sidebar links
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                window.scrollTo({
                    top: targetSection.offsetTop - 50,
                    behavior: 'smooth'
                });
                
                // Update active class
                sidebarLinks.forEach(link => link.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
    
    // Add hover effects to skill items
    document.querySelectorAll('.skill-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            const progressBar = this.querySelector('.progress-bar');
            progressBar.style.width = progressBar.getAttribute('aria-valuenow') + '%';
            progressBar.classList.add('progress-bar-animated');
        });
        
        item.addEventListener('mouseleave', function() {
            const progressBar = this.querySelector('.progress-bar');
            progressBar.classList.remove('progress-bar-animated');
        });
    });
    
    // Add animation to project cards
    document.querySelectorAll('.project-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        });
    });
});

// Initialize counters for skills
function initializeCounters() {
    const skillPercentages = document.querySelectorAll('.skill-percentage');
    
    skillPercentages.forEach(percentage => {
        const targetValue = parseInt(percentage.textContent);
        let currentValue = 0;
        
        const counter = setInterval(() => {
            if (currentValue >= targetValue) {
                clearInterval(counter);
            } else {
                currentValue += 1;
                percentage.textContent = currentValue + '%';
            }
        }, 20);
    });
}

// Initialize typewriter effect for subtitle
function initializeTypewriter() {
    const subtitle = document.querySelector('.portfolio-subtitle');
    
    if (subtitle && subtitle.textContent.trim() !== '') {
        const text = subtitle.textContent;
        subtitle.textContent = '';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                subtitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        };
        
        setTimeout(typeWriter, 1000);
    }
}

// Initialize download functionality
function initializeDownload() {
    const downloadBtn = document.getElementById('downloadPortfolio');
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show download animation
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Preparing CV...';
            this.classList.add('downloading');
            
            // Simulate download process (in a real app, this would be an actual download)
            setTimeout(() => {
                // Create a PDF from the portfolio content
                // In a real implementation, this would use a library like html2pdf.js or jsPDF
                // or make an AJAX request to a server-side PDF generation endpoint
                
                // For now, we'll just simulate the download with a success message
                this.innerHTML = '<i class="fas fa-check me-2"></i>Downloaded!';
                this.classList.remove('downloading');
                this.classList.add('downloaded');
                
                // Reset button after a delay
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-download me-2"></i>Download CV';
                    this.classList.remove('downloaded');
                }, 3000);
                
                // Show success toast
                showToast('CV downloaded successfully!', 'success');
            }, 2000);
        });
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'primary'} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    // Toast content
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add toast to container
    toastContainer.appendChild(toastEl);
    
    // Initialize and show toast
    const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
    toast.show();
    
    // Remove toast after it's hidden
    toastEl.addEventListener('hidden.bs.toast', function() {
        toastEl.remove();
    });
}