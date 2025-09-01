document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('newsletterForm');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const responseDiv = document.getElementById('newsletterResponse');
            
            // Clear previous messages and show loading
            responseDiv.innerHTML = '<div class="loading">Submitting...</div>';
            responseDiv.style.display = 'block';
            responseDiv.style.opacity = '1';
            
            try {
                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                });

                const data = await response.json();
                
                if (!response.ok) {  // This will catch 400 errors
                    throw data;  // Throw the error data to be caught below
                }
                
                // Success case
                responseDiv.innerHTML = `
                    <div class="success-message">
                        <svg viewBox="0 0 24 24" width="48" height="48">
                            <path fill="#4CAF50" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                        </svg>
                        <h3>Thank You!</h3>
                        <p>Subscription successful!</p>
                    </div>
                `;
                form.reset();
                
                // Hide message after 5 seconds
                setTimeout(() => {
                    responseDiv.style.opacity = '0';
                    setTimeout(() => {
                        responseDiv.style.display = 'none';
                    }, 500);
                }, 5000);
                
            } catch (error) {
                // Error handling - this will catch both network errors and our 400 response
                console.error('Error:', error);
                
                let errorMessage = 'An error occurred';
                if (error.errors) {
                    // Handle server validation errors
                    if (error.errors.email) {
                        errorMessage = error.errors.email[0]; // Get first email error
                    } else if (typeof error.errors === 'string') {
                        errorMessage = error.errors;
                    } else {
                        errorMessage = Object.values(error.errors)[0][0];
                    }
                }
                
                responseDiv.innerHTML = `
                    <div class="error-message">
                        <svg viewBox="0 0 24 24" width="48" height="48">
                            <path fill="#f44336" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                        </svg>
                        <h3>Error</h3>
                        <p>${errorMessage}</p>
                    </div>
                `;
            }
        });
    }
});