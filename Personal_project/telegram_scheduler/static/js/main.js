/**
 * Main JavaScript for the Telegram Message Scheduler web interface.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Set up authentication modal listeners
    setupAuthModalListeners();
    
    // Set up polling for auth status
    setupAuthStatusPolling();
});

/**
 * Set up event listeners for the authentication modal
 */
function setupAuthModalListeners() {
    // Authentication code form submission
    const authCodeForm = document.getElementById('authCodeForm');
    if (authCodeForm) {
        authCodeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const code = document.getElementById('auth_code').value;
            
            fetch("/auth_code", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'auth_code=' + encodeURIComponent(code)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Show 2FA form if needed or close modal
                    document.getElementById('twoFactorForm').style.display = 'block';
                    document.getElementById('authCodeForm').style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
    
    // 2FA password form submission
    const authPasswordForm = document.getElementById('authPasswordForm');
    if (authPasswordForm) {
        authPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const password = document.getElementById('auth_password').value;
            
            fetch("/auth_password", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'auth_password=' + encodeURIComponent(password)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Close the modal
                    const authModal = bootstrap.Modal.getInstance(document.getElementById('authModal'));
                    if (authModal) {
                        authModal.hide();
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
}

/**
 * Set up polling for authentication status
 * This would be used to show the auth modal when needed
 */
function setupAuthStatusPolling() {
    // This would normally poll a server endpoint to check if auth is needed
    // For now, we'll just have a placeholder function that can be extended later
    
    // Example of showing the auth modal when needed:
    // const authModal = new bootstrap.Modal(document.getElementById('authModal'));
    // authModal.show();
}

/**
 * Show the authentication modal
 */
function showAuthModal() {
    const authModal = new bootstrap.Modal(document.getElementById('authModal'));
    authModal.show();
    
    // Reset the forms
    document.getElementById('authCodeForm').style.display = 'block';
    document.getElementById('twoFactorForm').style.display = 'none';
    document.getElementById('auth_code').value = '';
    document.getElementById('auth_password').value = '';
}

/**
 * Helper function to confirm deletions
 */
function confirmDelete(event, itemType) {
    if (!confirm(`Are you sure you want to delete this ${itemType}?`)) {
        event.preventDefault();
    }
}

// Add click listeners to all delete buttons
document.addEventListener('DOMContentLoaded', function() {
    // Add confirmation to message deletion
    const deleteMessageButtons = document.querySelectorAll('form[action^="/delete_message/"] button');
    deleteMessageButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            confirmDelete(e, 'message');
        });
    });
    
    // Add confirmation to target deletion
    const deleteTargetButtons = document.querySelectorAll('form[action^="/delete_target/"] button');
    deleteTargetButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            confirmDelete(e, 'target');
        });
    });
});