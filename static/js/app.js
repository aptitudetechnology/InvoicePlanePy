// InvoicePlane Python - Custom JavaScript

// Utility functions
const InvoicePlane = {
    // Show loading spinner
    showLoading: function(element) {
        if (element) {
            element.innerHTML = '<span class="loading-spinner"></span> Loading...';
            element.disabled = true;
        }
    },

    // Hide loading spinner
    hideLoading: function(element, originalText) {
        if (element) {
            element.innerHTML = originalText || 'Submit';
            element.disabled = false;
        }
    },

    // Format currency
    formatCurrency: function(amount, currency = '$') {
        return currency + parseFloat(amount).toFixed(2);
    },

    // Calculate invoice totals
    calculateInvoiceTotal: function() {
        let subtotal = 0;
        document.querySelectorAll('.item-total').forEach(function(input) {
            subtotal += parseFloat(input.value) || 0;
        });
        
        const tax = 0; // TODO: Implement tax calculation
        const total = subtotal + tax;
        
        // Update display
        const subtotalEl = document.getElementById('invoice-subtotal');
        const taxEl = document.getElementById('invoice-tax');
        const totalEl = document.getElementById('invoice-total');
        
        if (subtotalEl) subtotalEl.textContent = this.formatCurrency(subtotal);
        if (taxEl) taxEl.textContent = this.formatCurrency(tax);
        if (totalEl) totalEl.innerHTML = '<strong>' + this.formatCurrency(total) + '</strong>';
    },

    // Auto-save functionality
    autoSave: function(formData) {
        // TODO: Implement auto-save to localStorage or server
        console.log('Auto-saving...', formData);
    },

    // Confirmation dialogs
    confirmDelete: function(message) {
        return confirm(message || 'Are you sure you want to delete this item?');
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-calculate totals on invoice form
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('quantity') || e.target.classList.contains('price')) {
            const row = e.target.closest('.item-row');
            if (row) {
                const quantity = parseFloat(row.querySelector('.quantity').value) || 0;
                const price = parseFloat(row.querySelector('.price').value) || 0;
                const total = quantity * price;
                
                const totalInput = row.querySelector('.total');
                if (totalInput) {
                    totalInput.value = total.toFixed(2);
                }
                
                InvoicePlane.calculateInvoiceTotal();
            }
        }
    });

    // Confirm delete actions
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn-delete, .delete-btn')) {
            if (!InvoicePlane.confirmDelete()) {
                e.preventDefault();
                return false;
            }
        }
    });

    // Form submission loading states
    document.addEventListener('submit', function(e) {
        const submitBtn = e.target.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.innerHTML;
            InvoicePlane.showLoading(submitBtn);
            
            // Reset after 5 seconds as fallback
            setTimeout(() => {
                InvoicePlane.hideLoading(submitBtn, originalText);
            }, 5000);
        }
    });
});
