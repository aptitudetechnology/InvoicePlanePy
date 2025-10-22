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

  // Load families from API and populate filter dropdown
  async loadFamilies() {
    try {
      const response = await fetch('/products/api/families', {
        credentials: 'same-origin'
      });
      if (!response.ok) {
        if (response.status === 401) {
          console.error('Authentication required for families API');
          alert('You must be logged in to access product data.');
          return;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

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
        }
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

      const response = await fetch(url, {
        credentials: 'same-origin'
      });
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

    if (!products || products.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No products found</td></tr>';
      return;
    }

    products.forEach(product => {
      const row = document.createElement('tr');
      row.className = 'product-row';

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

  addSelectedProducts() {
    const selectedCheckboxes = document.querySelectorAll('.product-checkbox:checked');
    
    if (selectedCheckboxes.length === 0) {
      console.warn('No products selected');
      return;
    }

    // Determine context (invoice vs quote) based on URL or page content
    const isInvoicePage = window.location.pathname.includes('/invoices/') || 
                         document.querySelector('#items_table') !== null;

    // Process each selected product
    selectedCheckboxes.forEach(checkbox => {
      const row = checkbox.closest('.product-row');
      if (!row) return;

      try {
        const productName = row.cells[3]?.textContent?.trim() || '';
        const priceText = row.cells[5]?.textContent?.replace('$', '') || '0';
        const price = parseFloat(priceText) || 0;
        const productId = checkbox.getAttribute('data-product-id');

        if (isInvoicePage) {
          // Use invoice-specific function
          this.addProductToInvoice(productName, price, productId);
        } else {
          // Use quote-specific function
          if (typeof window.addNewRowWithProduct === 'function') {
            window.addNewRowWithProduct(productName, price, productId);
          } else {
            console.error('addNewRowWithProduct function not found. Make sure addNewRowWithProduct.js is loaded.');
          }
        }
      } catch (error) {
        console.error('Error processing product:', error);
      }
    });
    
    // Clear selections and update UI
    this.clearSelections();
    this.hideModal();
  }

  addProductToInvoice(productName, price, productId) {
    // Get the invoice table body
    const tbody = document.querySelector('#items_table tbody') || document.getElementById('quote-items');
    if (!tbody) {
      console.error('Invoice items table body not found!');
      return;
    }

    // Get the current item counter from the global scope
    let itemCounter = window.itemCounter || 0;

    // Create new row using invoice format
    const newRow = document.createElement('tr');

    newRow.innerHTML = `
        <td>
            <input type="hidden" name="item_id_${itemCounter}" value="">
            <input type="text" class="form-control item-name" name="item_name_${itemCounter}" value="${productName}" placeholder="Item name" onchange="calculateItemTotal(this)">
            <textarea class="form-control mt-2 item-description" name="item_description_${itemCounter}" rows="2" placeholder="Description"></textarea>
        </td>
        <td>
            <input type="number" class="form-control item-quantity" name="item_quantity_${itemCounter}" min="1" value="1" onchange="calculateItemTotal(this)">
            <select class="form-select mt-2 item-unit" name="item_unit_${itemCounter}">
                <option value="none">None</option>
                <option value="piece">Piece</option>
                <option value="hour">Hour</option>
                <option value="day">Day</option>
                <option value="month">Month</option>
            </select>
        </td>
        <td>
            <input type="number" class="form-control item-price" name="item_price_${itemCounter}" min="0" step="0.01" value="${price.toFixed(2)}" onchange="calculateItemTotal(this)">
        </td>
        <td>
            <input type="number" class="form-control item-discount" name="item_discount_${itemCounter}" min="0" step="0.01" placeholder="0.00" value="0.00" onchange="calculateItemTotal(this)">
        </td>
        <td>
            ${this.createTaxRateDropdownHTML(itemCounter)}
            <input type="hidden" class="initial-tax-rate" value="0">
        </td>
        <td>
            <input type="number" class="form-control item-total" name="item_total_${itemCounter}" value="${price.toFixed(2)}" readonly>
        </td>
        <td>
            <button type="button" class="btn btn-sm btn-danger remove-row-btn" onclick="removeRow(this)">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    `;

    tbody.appendChild(newRow);

    // Populate tax rate select for the new row
    const newTaxSelect = newRow.querySelector('.item-tax-rate');
    if (typeof populateTaxRateDropdown === 'function') {
      populateTaxRateDropdown(newTaxSelect);
    }

    // Update counters
    itemCounter++;
    window.itemCounter = itemCounter;
    const itemsCountInput = document.getElementById('items_count');
    if (itemsCountInput) {
      itemsCountInput.value = itemCounter;
    }

    // Recalculate totals
    if (typeof calculateTotals === 'function') {
      calculateTotals();
    }
  }

  createTaxRateDropdownHTML(itemIndex) {
    // Get tax rates from global scope (set by the template)
    const taxRates = window.taxRates || [];
    let optionsHTML = '<option value="0">None (0%)</option>';

    taxRates.forEach(rate => {
      optionsHTML += `<option value="${rate.rate}">${rate.name} (${rate.rate}%)</option>`;
    });

    return `<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_${itemIndex}" onchange="calculateItemTotal(this)">${optionsHTML}</select>`;
  }  clearSelections() {
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
      // Load families and products when modal opens
      this.loadFamilies();
      this.loadProducts();
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
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    ProductModal.getInstance();
  });
} else {
  // DOM already ready
  ProductModal.getInstance();
}

// Export for module systems (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProductModal;
}
