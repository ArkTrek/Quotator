// Main JavaScript for Quotator

window.addEventListener('load', () => {
    const loader = document.getElementById('page-loader');
    if (loader) {
        // Add a longer delay to ensure the writing animation is seen clearly
        setTimeout(() => {
            loader.classList.add('hidden');
            setTimeout(() => {
                loader.style.display = 'none';
                document.body.classList.add('loaded');
            }, 800); // Wait for fade out
        }, 2500); // Display loader for at least 2.5 seconds
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.opacity = '0';
                msg.style.transform = 'translateY(-10px)';
                msg.style.transition = 'all 0.5s ease';
                setTimeout(() => msg.remove(), 500);
            });
        }, 5000);
    }
});

// Toggle Like function
async function toggleLike(quoteId, btnElement) {
    if (btnElement.hasAttribute('disabled')) return;
    
    // Optimistic UI update
    const isLiked = btnElement.classList.contains('liked');
    const countSpan = btnElement.querySelector('.like-count');
    let currentCount = parseInt(countSpan.textContent);
    
    // Add micro-animation class
    btnElement.style.transform = 'scale(1.2)';
    setTimeout(() => btnElement.style.transform = '', 200);

    try {
        const response = await fetch(`/like/${quoteId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (data.status === 'liked') {
                btnElement.classList.add('liked');
            } else {
                btnElement.classList.remove('liked');
            }
            countSpan.textContent = data.likes;
        } else {
            console.error('Failed to toggle like', data);
            // Optional: Revert optimistic update if needed, but here we wait for server source of truth
        }
    } catch (error) {
        console.error('Error toggling like:', error);
    }
}
