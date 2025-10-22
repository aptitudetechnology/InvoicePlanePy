// static/js/productModal.js
// Product selection modal functionality
console.log('productModal.js loading...');

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
    console.log('ProductModal.setupModal() called');
    this.modalElement = document.getElementById('productModal');
    console.log('Modal element found:', !!this.modalElement);
    if (!this.modalElement) {
      console.warn('Product modal not found');
      return;
    }

    // Initialize Bootstrap modal
    this.modal = new bootstrap.Modal(this.modalElement);
    console.log('Bootstrap modal initialized:', !!this.modal);

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
    const searchBtn = document.getElementById('searchProductsBtn');
    if (searchBtn) {
      searchBtn.addEventListener('click', () => this.searchProducts());
    }

    const resetBtn = document.getElementById('resetProductSearchBtn');
    if (resetBtn) {
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
    document.getElementById('productNameSearch').value = '';
    document.getElementById('familyFilter').value = '';
    this.loadProducts();
  }

  updateSelectionSummary() {
    const selectedCount = this.selectedProducts.size;
    const summaryElement = document.getElementById('selectionSummary');
    if (summaryElement) {
      summaryElement.textContent = `${selectedCount} product${selectedCount !== 1 ? 's' : ''} selected`;
    }

    // Enable/disable add button
    const addBtn = document.getElementById('addProductsBtn');
    if (addBtn) {
      addBtn.disabled = selectedCount === 0;
    }
  }

  // Load families from API and populate filter dropdown
  async loadFamilies() {
    console.log('=== loadFamilies() START ===');
    console.log('loadFamilies called - checking if modal is visible');
    const modalElement = document.getElementById('productModal');
    console.log('Modal element:', modalElement);
    console.log('Modal is visible:', modalElement && modalElement.classList.contains('show'));

    // Add a small delay to ensure modal is fully rendered
    await new Promise(resolve => setTimeout(resolve, 100));
    console.log('Delay completed, proceeding with API call');

    try {
      console.log('Fetching families from /products/api/families');
      const response = await fetch('/products/api/families' /* removed credentials for testing */);
      console.log('Families response status:', response.status);

      if (!response.ok) {
        if (response.status === 401) {
          console.error('Authentication required for families API');
          alert('You must be logged in to access product data.');
          return;
        }
        const errorText = await response.text();
        console.error('API error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      const data = await response.json();
      console.log('Families data received:', data);
      console.log('Number of families:', data.families ? data.families.length : 'no families key');

      const familyFilter = document.getElementById('familyFilter');
      console.log('familyFilter element found:', !!familyFilter);
      if (familyFilter) {
        console.log('Current familyFilter HTML:', familyFilter.innerHTML);
        // Clear existing options except "Any family"
        familyFilter.innerHTML = '<option value="">Any family</option>';

        // Add family options
        if (data.families && data.families.length > 0) {
          console.log('Adding', data.families.length, 'family options');
          data.families.forEach(family => {
            const option = document.createElement('option');
            option.value = family.id;
            option.textContent = family.name;
            familyFilter.appendChild(option);
            console.log('Added family option:', family.name, 'with value:', family.id);
          });
          console.log('Family dropdown updated, final HTML:', familyFilter.innerHTML);
        } else {
          console.log('No families received from API');
        }
      } else {
        console.error('familyFilter element not found in DOM!');
        console.log('All select elements:', document.querySelectorAll('select'));
      }
    } catch (error) {
      console.error('Error in loadFamilies:', error);
      alert('Error loading product families: ' + error.message);
    }
    console.log('=== loadFamilies() END ===');
  }

  // Load products from API and populate table
  async loadProducts(search = '', familyId = '') {
    console.log('loadProducts called with search:', search, 'familyId:', familyId);
    try {
      let url = '/products/api?limit=1000'; // Load all products for modal
      if (search) {
        url += `&search=${encodeURIComponent(search)}`;
      }
      if (familyId) {
        url += `&family_id=${encodeURIComponent(familyId)}`;
      }

      console.log('Fetching products from:', url);
      const response = await fetch(url);
      console.log('Products response status:', response.status);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Products data received, count:', data.products ? data.products.length : 0);

      this.renderProductsTable(data.products || []);
    } catch (error) {
      console.error('Error loading products:', error);
      this.renderProductsTable([]);
    }
  }

  renderProductsTable(products) {
    const tbody = document.getElementById('productsTableBody');
    if (!tbody) {
      console.error('Products table body not found');
      return;
    }

    if (products.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="text-center">No products found</td></tr>';
      return;
    }

    tbody.innerHTML = products.map(product => `
      <tr>
        <td>
          <input type="checkbox" class="product-checkbox"
                 value="${product.id}"
                 data-name="${product.name}"
                 data-price="${product.price || 0}"
                 data-sku="${product.sku}">
        </td>
        <td>${product.name}</td>
        <td>${product.sku}</td>
        <td>${product.price ? '$' + parseFloat(product.price).toFixed(2) : 'N/A'}</td>
        <td>${product.family ? product.family.name : 'No family'}</td>
      </tr>
    `).join('');
  }

  addSelectedProducts() {
    const selectedCheckboxes = document.querySelectorAll('.product-checkbox:checked');
    const selectedProducts = Array.from(selectedCheckboxes).map(cb => ({
      id: cb.value,
      name: cb.getAttribute('data-name'),
      price: parseFloat(cb.getAttribute('data-price')) || 0,
      sku: cb.getAttribute('data-sku')
    }));

    console.log('Adding selected products:', selectedProducts);

    // Dispatch custom event with selected products
    const event = new CustomEvent('productsSelected', {
      detail: { products: selectedProducts }
    });
    document.dispatchEvent(event);

    // Close modal
    this.hideModal();
  }

  hideModal() {
    if (this.modal) {
      this.modal.hide();
    }
  }

  showModal() {
    console.log('ProductModal.showModal() called');
    if (this.modal) {
      console.log('Showing modal and calling loadFamilies/loadProducts');
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
    console.log('window.productModalInstance exists:', !!window.productModalInstance);
    if (!window.productModalInstance) {
      console.log('Creating new ProductModal instance...');
      window.productModalInstance = new ProductModal();
      console.log('Created instance:', window.productModalInstance);
      console.log('Instance has showModal method:', typeof window.productModalInstance.showModal);
    } else {
      console.log('Using existing instance:', window.productModalInstance);
    }
    return window.productModalInstance;
  }
}

console.log('ProductModal class defined:', typeof ProductModal);
console.log('ProductModal.getInstance method:', typeof ProductModal.getInstance);

// Auto-initialize when DOM is ready
console.log('Setting up ProductModal auto-initialization...');
console.log('Current document.readyState:', document.readyState);
console.log('Modal element exists at startup:', !!document.getElementById('productModal'));

if (document.readyState === 'loading') {
  console.log('DOM not ready, waiting...');
  document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired, modal element now exists:', !!document.getElementById('productModal'));
    console.log('Calling ProductModal.getInstance()');
    ProductModal.getInstance();
  });
} else {
  console.log('DOM already ready, modal element exists:', !!document.getElementById('productModal'));
  console.log('Calling ProductModal.getInstance()');
  ProductModal.getInstance();
}

// Export for module systems (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProductModal;
}
