// static/js/productModal.js
// Product selection modal functionality

class ProductModal {
  constructor() {
    this.modal = null;
    this.modalElement = null;
    this.selectedProducts = new Set();
    this.init();
  }

  init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setupModal());
    } else {
      this.setupModal();
    }
  }

  setupModal() {
    this.modalElement = document.getElementById('productModal');
    if (!this.modalElement) {
      console.warn('Product modal not found');
      return;
    }

    // Initialize Bootstrap modal
    this.modal = new bootstrap.Modal(this.modalElement);
    
    // Setup event listeners
    this.attachEventListeners();
    
    // Initialize selection summary
    this.updateSelectionSummary();
  }

  attachEventListeners() {
    // Family filter dropdown
    const familyFilter = document.getElementById('familyFilter');
    if (familyFilter) {
      familyFilter.addEventListener('change', () => this.filterProductsByFamily());
    }

    // Product name search input
    const productNameSearch = document.getElementById('productNameSearch');
    if (productNameSearch) {
      productNameSearch.addEventListener('keyup', () => this.filterProductsByName());
      // Also trigger on Enter key
      productNameSearch.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.searchProducts();
        }
      });
    }

    // Search and reset buttons
    const searchBtn = this.modalElement.querySelector('[onclick="searchProducts()"]');
    if (searchBtn) {
      searchBtn.removeAttribute('onclick');
      searchBtn.addEventListener('click', () => this.searchProducts());
    }

    const resetBtn = this.modalElement.querySelector('[onclick="resetProductSearch()"]');
    if (resetBtn) {
      resetBtn.removeAttribute('onclick');
      resetBtn.addEventListener('click', () => this.resetProductSearch());
    }

    // Add selected products button
    const addProductsBtn = document.getElementById('addProductsBtn');
    if (addProductsBtn) {
      addProductsBtn.removeAttribute('onclick');
      addProductsBtn.addEventListener('click', () => this.addSelectedProducts());
    }

    // Product checkboxes - use event delegation
    this.modalElement.addEventListener('change', (e) => {
      if (e.target.classList.contains('product-checkbox')) {
        this.updateSelectionSummary();
      }
    });

    // Product row clicks for expansion - use event delegation
    this.modalElement.addEventListener('click', (e) => {
      const productRow = e.target.closest('.product-row[style*="cursor: pointer"]');
      if (productRow && !e.target.classList.contains('product-checkbox')) {
        e.preventDefault();
        this.toggleProductDetails(productRow);
      }
    });

    // Prevent checkbox clicks from bubbling to row click
    this.modalElement.addEventListener('click', (e) => {
      if (e.target.classList.contains('product-checkbox')) {
        e.stopPropagation();
      }
    });
  }

  filterProductsByFamily() {
    const selectedFamily = document.getElementById('familyFilter').value;
    const rows = document.querySelectorAll('.product-row');
    
    rows.forEach(row => {
      const family = row.getAttribute('data-family');
      const shouldShow = !selectedFamily || family === selectedFamily;
      row.style.display = shouldShow ? '' : 'none';
      
      // Also hide corresponding details row if it exists
      const checkbox = row.querySelector('.product-checkbox');
      if (checkbox) {
        const productId = checkbox.getAttribute('data-product-id');
        const detailsRow = document.getElementById(`details-${productId}`);
        if (detailsRow) {
          detailsRow.style.display = shouldShow ? detailsRow.style.display : 'none';
        }
      }
    });
  }

  filterProductsByName() {
    const searchTerm = document.getElementById('productNameSearch').value.toLowerCase();
    const rows = document.querySelectorAll('.product-row');
    
    rows.forEach(row => {
      const productNameCell = row.cells[3];
      if (productNameCell) {
        const productName = productNameCell.textContent.toLowerCase();
        const shouldShow = !searchTerm || productName.includes(searchTerm);
        row.style.display = shouldShow ? '' : 'none';
        
        // Also hide corresponding details row if it exists
        const checkbox = row.querySelector('.product-checkbox');
        if (checkbox) {
          const productId = checkbox.getAttribute('data-product-id');
          const detailsRow = document.getElementById(`details-${productId}`);
          if (detailsRow) {
            detailsRow.style.display = shouldShow ? detailsRow.style.display : 'none';
          }
        }
      }
    });
  }

  searchProducts() {
    // Combine both filters
    this.filterProductsByFamily();
    this.filterProductsByName();
  }

  resetProductSearch() {
    // Clear filter inputs
    const familyFilter = document.getElementById('familyFilter');
    const productNameSearch = document.getElementById('productNameSearch');
    
    if (familyFilter) familyFilter.value = '';
    if (productNameSearch) productNameSearch.value = '';
    
    // Show all product rows
    const rows = document.querySelectorAll('.product-row');
    rows.forEach(row => {
      row.style.display = '';
    });

    // Hide all details rows
    const detailRows = document.querySelectorAll('.product-details-row');
    detailRows.forEach(row => {
      row.style.display = 'none';
    });

    // Reset expand icons
    const expandIcons = document.querySelectorAll('.expand-icon');
    expandIcons.forEach(icon => {
      icon.className = 'bi bi-chevron-right expand-icon';
    });
  }

  toggleProductDetails(row) {
    const checkbox = row.querySelector('.product-checkbox');
    if (!checkbox) return;

    const productId = checkbox.getAttribute('data-product-id');
    const detailsRow = document.getElementById(`details-${productId}`);
    const expandIcon = row.querySelector('.expand-icon');
    
    if (!detailsRow || !expandIcon) return;

    const isHidden = detailsRow.style.display === 'none';
    
    if (isHidden) {
      detailsRow.style.display = '';
      expandIcon.className = 'bi bi-chevron-down expand-icon';
    } else {
      detailsRow.style.display = 'none';
      expandIcon.className = 'bi bi-chevron-right expand-icon';
    }
  }

  updateSelectionSummary() {
    const selectedCheckboxes = document.querySelectorAll('.product-checkbox:checked');
    const summaryDiv = document.getElementById('selectionSummary');
    const addButton = document.getElementById('addProductsBtn');
    
    if (!summaryDiv || !addButton) return;

    if (selectedCheckboxes.length === 0) {
      summaryDiv.innerHTML = '<small class="text-muted">No products selected</small>';
      addButton.disabled = true;
    } else {
      summaryDiv.innerHTML = `<small class="text-success">${selectedCheckboxes.length} product(s) selected</small>`;
      addButton.disabled = false;
    }
  }

  addSelectedProducts() {
    const selectedCheckboxes = document.querySelectorAll('.product-checkbox:checked');
    
    if (selectedCheckboxes.length === 0) {
      console.warn('No products selected');
      return;
    }

    // Process each selected product
    selectedCheckboxes.forEach(checkbox => {
      const row = checkbox.closest('.product-row');
      if (!row) return;

      try {
        const productName = row.cells[3]?.textContent?.trim() || '';
        const priceText = row.cells[5]?.textContent?.replace('$', '') || '0';
        const price = parseFloat(priceText) || 0;
        const productId = checkbox.getAttribute('data-product-id');

        // Call external function to add product (must be defined in quotes.js or invoices.js)
        if (typeof window.addNewRowWithProduct === 'function') {
          window.addNewRowWithProduct(productName, price, productId);
        } else {
          console.error('addNewRowWithProduct function not found. Make sure quotes.js or invoices.js is loaded.');
        }
      } catch (error) {
        console.error('Error processing product:', error);
      }
    });
    
    // Clear selections and update UI
    this.clearSelections();
    this.hideModal();
  }

  clearSelections() {
    const selectedCheckboxes = document.querySelectorAll('.product-checkbox:checked');
    selectedCheckboxes.forEach(checkbox => {
      checkbox.checked = false;
    });
    this.updateSelectionSummary();
  }

  hideModal() {
    if (this.modal) {
      this.modal.hide();
    }
  }

  showModal() {
    if (this.modal) {
      this.modal.show();
    }
  }

  // Public API methods
  static getInstance() {
    if (!window.productModalInstance) {
      window.productModalInstance = new ProductModal();
    }
    return window.productModalInstance;
  }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  ProductModal.getInstance();
});

// Export for module systems (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProductModal;
}