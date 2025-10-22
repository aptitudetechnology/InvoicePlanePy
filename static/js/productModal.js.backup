// static/js/productModal.js
// Product selection modal functionality

// Simple test to see if script loads
console.log('=== PRODUCT MODAL JS LOADING ===');
console.log('productModal.js loaded successfully at:', new Date().toISOString());

try {
  console.log('Testing basic JavaScript execution...');
  const test = 'test';
  console.log('Basic JS works:', test);
} catch (e) {
  console.error('Basic JS error:', e);
}

class ProductModal {
  constructor() {
    this.modal = null;
    this.modalElement = null;
    this.selectedProducts = new Set();
    console.log('ProductModal constructor called');
    this.init();
  }

  init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      console.log('DOM loading, waiting...');
      document.addEventListener('DOMContentLoaded', () => this.setupModal());
    } else {
      console.log('DOM ready, setting up modal...');
      this.setupModal();
    }
  }

  setupModal() {
    console.log('Setting up modal...');
    this.modalElement = document.getElementById('productModal');
    if (!this.modalElement) {
      console.warn('Product modal not found');
      return;
    }

    console.log('Modal element found, initializing Bootstrap modal...');
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
    const searchTerm = document.getElementById('productNameSearch').value;
    this.loadProducts(searchTerm, selectedFamily);
  }

  filterProductsByName() {
    const searchTerm = document.getElementById('productNameSearch').value;
    const selectedFamily = document.getElementById('familyFilter').value;
    this.loadProducts(searchTerm, selectedFamily);
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
    
    // Reload all products
    this.loadProducts();
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

  // Load families from API and populate filter dropdown
  async loadFamilies() {
    console.log('Loading families...');
    try {
      const response = await fetch('/products/api/families');
      console.log('Families response status:', response.status);
      if (!response.ok) {
        if (response.status === 401) {
          console.error('Authentication required for families API');
          alert('You must be logged in to access product data.');
          return;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Families data:', data);
      
      const familyFilter = document.getElementById('familyFilter');
      if (familyFilter) {
        // Clear existing options except "Any family"
        familyFilter.innerHTML = '<option value="">Any family</option>';
        
        // Add family options
        if (data.families && data.families.length > 0) {
          data.families.forEach(family => {
            const option = document.createElement('option');
            option.value = family.id;
            option.textContent = family.name;
            familyFilter.appendChild(option);
          });
          console.log(`Added ${data.families.length} family options`);
        } else {
          console.log('No families found in response');
        }
      } else {
        console.error('familyFilter element not found');
      }
    } catch (error) {
      console.error('Error loading families:', error);
    }
  }

  // Load products from API and populate table
  async loadProducts(search = '', familyId = '') {
    try {
      let url = '/products/api?limit=1000'; // Load all products for modal
      if (search) {
        url += `&search=${encodeURIComponent(search)}`;
      }
      if (familyId) {
        url += `&family_id=${encodeURIComponent(familyId)}`;
      }
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      
      this.renderProducts(data.products);
    } catch (error) {
      console.error('Error loading products:', error);
    }
  }

  // Render products in the table
  renderProducts(products) {
    const tbody = document.getElementById('productTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    products.forEach(product => {
      const row = document.createElement('tr');
      row.className = 'product-row';
      row.setAttribute('data-family', product.family ? product.family.name.toLowerCase().replace(/\s+/g, '-') : '');
      
      row.innerHTML = `
        <td>
          <input type="checkbox" class="form-check-input product-checkbox" 
                 value="${product.id}" data-product-id="${product.id}">
        </td>
        <td>${product.sku || ''}</td>
        <td>${product.family ? product.family.name : ''}</td>
        <td>${product.name}</td>
        <td>${product.description || ''}</td>
        <td>$${parseFloat(product.price || 0).toFixed(2)}</td>
      `;
      
      tbody.appendChild(row);
    });
  }

  showModal() {
    console.log('showModal called');
    if (this.modal) {
      console.log('Showing modal and loading data...');
      this.modal.show();
      // Load families and products when modal opens
      this.loadFamilies();
      this.loadProducts();
    } else {
      console.error('Modal not initialized');
    }
  }

  // Public API methods
  static getInstance() {
    console.log('ProductModal.getInstance() called');
    if (!window.productModalInstance) {
      console.log('Creating new ProductModal instance');
      window.productModalInstance = new ProductModal();
    } else {
      console.log('Returning existing ProductModal instance');
    }
    return window.productModalInstance;
  }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    ProductModal.getInstance();
  });
} else {
  // DOM already loaded
  ProductModal.getInstance();
}

// Export for module systems (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProductModal;
}