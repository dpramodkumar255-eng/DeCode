document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    
    // Simple micro-animation on input focus for icons
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            const icon = this.previousElementSibling;
            if (icon && icon.classList.contains('input-icon')) {
                icon.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    icon.style.transform = 'scale(1)';
                }, 200);
            }
        });
    });

    // Handle form submission and send data to backend
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = loginForm.querySelector('.submit-btn');
        const originalContent = btn.innerHTML;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Show loading state
        btn.innerHTML = `
            <svg class="spinner" viewBox="0 0 50 50" width="20" height="20" style="animation: rotate 2s linear infinite;">
                <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-dasharray="1, 200" stroke-dashoffset="0" style="animation: dash 1.5s ease-in-out infinite;"></circle>
            </svg>
            <span>Signing In...</span>
        `;
        
        // Add spinner styles dynamically if not present
        if (!document.getElementById('spinner-styles')) {
            const style = document.createElement('style');
            style.id = 'spinner-styles';
            style.innerHTML = `
                @keyframes rotate { 100% { transform: rotate(360deg); } }
                @keyframes dash {
                    0% { stroke-dasharray: 1, 200; stroke-dashoffset: 0; }
                    50% { stroke-dasharray: 90, 200; stroke-dashoffset: -35px; }
                    100% { stroke-dasharray: 90, 200; stroke-dashoffset: -124px; }
                }
            `;
            document.head.appendChild(style);
        }

        try {
            // Actual API call to our new Python backend
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            // Restore button original content
            btn.innerHTML = originalContent;
            const submitText = btn.querySelector('span');
            
            if (submitText) {
                const oldText = submitText.innerText;
                
                if (response.ok && data.status === 'success') {
                    submitText.innerText = 'Success! Redirecting...';
                    btn.style.backgroundColor = '#10b981'; // Success green
                    
                    // Redirect to dashboard after a short delay
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1000);
                } else {
                    submitText.innerText = data.message || 'Login Failed';
                    btn.style.backgroundColor = '#ef4444'; // Error red
                    
                    // Reset to default state after 2 seconds only for errors
                    setTimeout(() => {
                        submitText.innerText = oldText;
                        btn.style.backgroundColor = '';
                    }, 2000);
                }
            }
        } catch (error) {
            // Handle network errors
            btn.innerHTML = originalContent;
            const submitText = btn.querySelector('span');
            if (submitText) {
                const oldText = submitText.innerText;
                submitText.innerText = 'Error connecting';
                btn.style.backgroundColor = '#ef4444'; // Error red
                setTimeout(() => {
                    submitText.innerText = oldText;
                    btn.style.backgroundColor = '';
                }, 2000);
            }
        }
    });
});
