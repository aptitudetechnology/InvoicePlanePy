// static/js/quotes.js
// Quote management functionality

class QuoteManager {
  constructor() {
    this.itemCounter = 0;
    this.taxRates = [];
    this.products = [];
    this.quoteId = null;
    this.init();
  }

  init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setupQuote());
    } else {
      this.setupQuote();
    }
  }

  setupQuote() {
    // Get quote context data from template
    this.extractContextData();
    
    // Load data and setup event listeners
    this.loadTaxRates().then(() => {
      this.calculateTotals();
    });
    this.loadProducts();
    this.attachEventListeners();
    
    // Expose addNewRowWithProduct globally for ProductModal integration
    window.addNewRowWithProduct = (productName, price, productId) => {
      this.addNewRowWithProduct(productName, price, productId);
    };
  }

  extractContextData() {
    // Extract quote ID from the form action or URL
    const form = document.querySelector('form[action*="/quotes/"]');
    if (form) {
      const matches = form.action.match(/\/quotes\/(\d+)\/edit/);
      this.quoteId = matches ? matches[1] : null;
    }
    
    // Count existing items to set initial counter
    const existingItems = document.querySelectorAll('#quote-items tr');
    this.itemCounter = existingItems.length;
  }

  attachEventListeners() {
    // Action buttons
    document.querySelector('[onclick="addQuoteTax()"]')?.addEventListener('click', () => this.addQuoteTax());
    document.querySelector('[onclick="downloadPDF()"]')?.addEventListener('click', () => this.downloadPDF());
    document.querySelector('[onclick="sendEmail()"]')?.addEventListener('click', () => this.sendEmail());
    document.querySelector('[onclick="quoteToInvoice()"]')?.addEventListener('click', () => this.quoteToInvoice());
    document.querySelector('[onclick="copyQuote()"]')?.addEventListener('click', () => this.copyQuote());
    document.querySelector('[onclick="deleteQuote()"]')?.addEventListener('click', () => this.deleteQuote());

    // Item management buttons
    document.querySelector('[onclick="addNewRow()"]')?.addEventListener('click', () => this.addNewRow());
    document.querySelector('[onclick="displayProductModal()"]')?.addEventListener('click', () => this.displayProductModal());

    // Remove inline onclick attributes (will be done via cleanup)
    this.cleanupInlineHandlers();

    // Quote discount percentage change
    const discountInput = document.querySelector('input[name="discount_percentage"]');
    if (discountInput) {
      discountInput.addEventListener('change', () => this.calculateTotals());
    }

    // Event delegation for dynamic item rows
    const itemsTable = document.getElementById('quote-items');
    if (itemsTable) {
      itemsTable.addEventListener('click', (e) => {
        if (e.target.closest('.btn-outline-danger')) {
          this.removeItem(e.target.closest('.btn-outline-danger'));
        }
      });

      itemsTable.addEventListener('change', (e) => {
        if (e.target.matches('input[name*="[quantity]"], input[name*="[price]"], input[name*="[discount]"], select[name*="[tax_rate]"]')) {
          this.calculateItemTotal(e.target);
        }
      });
    }
  }

  cleanupInlineHandlers() {
    // Remove onclick attributes that we've replaced with event listeners
    const elementsToClean = [
      '[onclick="addQuoteTax()"]',
      '[onclick="downloadPDF()"]', 
      '[onclick="sendEmail()"]',
      '[onclick="quoteToInvoice()"]',
      '[onclick="copyQuote()"]',
      '[onclick="deleteQuote()"]',
      '[onclick="addNewRow()"]',
      '[onclick="displayProductModal()"]',
      '[onclick="removeItem(this)"]',
      '[onchange="calculateItemTotal(this)"]',
      '[onchange="calculateTotals()"]'
    ];

    elementsToClean.forEach(selector => {
      document.querySelectorAll(selector).forEach(element => {
        element.removeAttribute('onclick');
        element.removeAttribute('onchange');
      });
    });
  }

  async loadTaxRates() {
    try {
      const response = await fetch('/tax_rates/api');
      if (!response.ok) throw new Error('Failed to load tax rates');
      const data = await response.json();
      this.taxRates = data.tax_rates || data;
      this.populateAllTaxRateDropdowns();
    } catch (error) {
      console.error('Error loading tax rates:', error);
      this.taxRates = [];
    }
  }

  async loadProducts() {
    try {
      const response = await fetch('/products/api');
      if (!response.ok) throw new Error('Failed to load products');
      const data = await response.json();
      this.products = data.products || data;
    } catch (error) {
      console.error('Error loading products:', error);
      this.products = [];
    }
  }

  populateAllTaxRateDropdowns() {
    const taxRateSelects = document.querySelectorAll('.tax-rate-select');
    taxRateSelects.forEach(select => {
      this.populateTaxRateDropdown(select);
    });
  }

  populateTaxRateDropdown(selectElement) {
    const currentValue = selectElement.value;
    selectElement.innerHTML = '<option value="0">None (0%)</option>';

    this.taxRates.forEach(taxRate => {
      const option = document.createElement('option');
      option.value = taxRate.rate;
      option.textContent = `${taxRate.name} (${taxRate.rate.toFixed(2)}%)`;
      option.setAttribute('data-tax-id', taxRate.id);
      selectElement.appendChild(option);
    });

    selectElement.value = currentValue;
  }

  createTaxRateDropdownHTML(itemIndex, selectedRate = 0) {
    let optionsHTML = '<option value="0">None (0%)</option>';

    this.taxRates.forEach(taxRate => {
      const selected = taxRate.rate == selectedRate ? 'selected' : '';
      optionsHTML += `<option value="${taxRate.rate}" data-tax-id="${taxRate.id}" ${selected}>${taxRate.name} (${taxRate.rate.toFixed(2)}%)</option>`;
    });

    return `<select class="form-select form-select-sm tax-rate-select" name="items[${itemIndex}][tax_rate]">${optionsHTML}</select>`;
  }

  addNewRow() {
    const tbody = document.getElementById('quote-items');
    const newRow = document.createElement('tr');
    const taxRateDropdownContent = this.createTaxRateDropdownHTML(this.itemCounter);

    newRow.innerHTML = `
      <td>
        <button type="button" class="btn btn-sm btn-outline-danger">
          <i class="bi bi-trash"></i>
        </button>
      </td>
      <td>
        <input type="text" class="form-control form-control-sm" name="items[${this.itemCounter}][name]" placeholder="Item">
        <textarea class="form-control form-control-sm mt-1" name="items[${this.itemCounter}][description]" rows="2" placeholder="Description"></textarea>
        <input type="hidden" name="items[${this.itemCounter}][product_id]" value="">
      </td>
      <td>
        <input type="number" class="form-control form-control-sm" name="items[${this.itemCounter}][quantity]" value="1" step="0.01">
      </td>
      <td>
        <input type="number" class="form-control form-control-sm" name="items[${this.itemCounter}][price]" value="0.00" step="0.01">
      </td>
      <td>
        <input type="number" class="form-control form-control-sm" name="items[${this.itemCounter}][discount]" value="0.00" step="0.01">
      </td>
      <td>
        ${taxRateDropdownContent}
      </td>
      <td class="item-subtotal">$0.00</td>
      <td class="item-discount-amount">$0.00</td>
      <td class="item-tax-amount">$0.00</td>
      <td class="item-total">$0.00</td>
    `;
    
    tbody.appendChild(newRow);
    this.itemCounter++;
  }

  addNewRowWithProduct(productName, price, productId) {
    this.addNewRow();
    
    const tbody = document.getElementById('quote-items');
    const lastRow = tbody.lastElementChild;
    
    if (lastRow) {
      const nameInput = lastRow.querySelector('input[name*="[name]"]');
      if (nameInput) nameInput.value = productName;
      
      const priceInput = lastRow.querySelector('input[name*="[price]"]');
      if (priceInput) {
        priceInput.value = price.toFixed(2);
        this.calculateItemTotal(priceInput);
      }
      
      const quantityInput = lastRow.querySelector('input[name*="[quantity]"]');
      if (quantityInput) quantityInput.value = '1';
      
      const productIdInput = lastRow.querySelector('input[name*="[product_id]"]');
      if (productIdInput && productId) productIdInput.value = productId;
    }
  }

  removeItem(button) {
    const row = button.closest('tr');
    row.remove();
    this.calculateTotals();
  }

  calculateItemTotal(input) {
    const row = input.closest('tr');
    const quantity = parseFloat(row.querySelector('input[name*="[quantity]"]').value) || 0;
    const price = parseFloat(row.querySelector('input[name*="[price]"]').value) || 0;
    const discount = parseFloat(row.querySelector('input[name*="[discount]"]').value) || 0;
    const taxRate = parseFloat(row.querySelector('select[name*="[tax_rate]"]').value) || 0;

    const subtotal = quantity * price;
    const discountAmount = subtotal * (discount / 100);
    const taxableAmount = subtotal - discountAmount;
    const taxAmount = taxableAmount * (taxRate / 100);
    const total = taxableAmount + taxAmount;

    row.querySelector('.item-subtotal').textContent = `$${subtotal.toFixed(2)}`;
    row.querySelector('.item-discount-amount').textContent = `$${discountAmount.toFixed(2)}`;
    row.querySelector('.item-tax-amount').textContent = `$${taxAmount.toFixed(2)}`;
    row.querySelector('.item-total').textContent = `$${total.toFixed(2)}`;

    this.calculateTotals();
  }

  calculateTotals() {
    let subtotal = 0;
    let itemTax = 0;
    let totalDiscount = 0;

    document.querySelectorAll('#quote-items tr').forEach(row => {
      const itemSubtotal = parseFloat(row.querySelector('.item-subtotal')?.textContent?.replace('$', '')) || 0;
      const itemDiscountAmount = parseFloat(row.querySelector('.item-discount-amount')?.textContent?.replace('$', '')) || 0;
      const itemTaxAmount = parseFloat(row.querySelector('.item-tax-amount')?.textContent?.replace('$', '')) || 0;

      subtotal += itemSubtotal;
      totalDiscount += itemDiscountAmount;
      itemTax += itemTaxAmount;
    });

    const discountPercentage = parseFloat(document.querySelector('input[name="discount_percentage"]')?.value) || 0;
    const additionalDiscount = (subtotal - totalDiscount) * (discountPercentage / 100);
    const quoteTax = 0; // This would need to be calculated based on your business logic

    const total = subtotal - totalDiscount - additionalDiscount + itemTax + quoteTax;

    const subtotalEl = document.getElementById('quote-subtotal');
    const itemTaxEl = document.getElementById('quote-item-tax');
    const quoteTaxEl = document.getElementById('quote-tax');
    const totalEl = document.getElementById('quote-total');

    if (subtotalEl) subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
    if (itemTaxEl) itemTaxEl.textContent = `$${itemTax.toFixed(2)}`;
    if (quoteTaxEl) quoteTaxEl.textContent = `$${quoteTax.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `$${total.toFixed(2)}`;
  }

  // Quote action methods
  displayProductModal() {
    if (window.ProductModal) {
      window.ProductModal.getInstance().showModal();
    } else {
      console.error('ProductModal not available');
    }
  }

  addQuoteTax() {
    console.log('Add Quote Tax clicked');
    // Implement add quote tax functionality
  }

  downloadPDF() {
    if (this.quoteId) {
      window.location.href = `/quotes/${this.quoteId}/pdf`;
    }
  }

  sendEmail() {
    if (this.quoteId) {
      window.location.href = `/quotes/${this.quoteId}/email`;
    }
  }

  quoteToInvoice() {
    if (confirm('Convert this quote to an invoice?')) {
      if (this.quoteId) {
        window.location.href = `/quotes/${this.quoteId}/convert-to-invoice`;
      }
    }
  }

  copyQuote() {
    if (confirm('Create a copy of this quote?')) {
      if (this.quoteId) {
        window.location.href = `/quotes/${this.quoteId}/copy`;
      }
    }
  }

  deleteQuote() {
    if (confirm('Are you sure you want to delete this quote? This action cannot be undone.')) {
      if (this.quoteId) {
        fetch(`/quotes/${this.quoteId}/delete`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        .then(response => {
          if (response.ok) {
            window.location.href = '/quotes';
          } else {
            alert('Error deleting quote');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Error deleting quote');
        });
      }
    }
  }

  // Static method to get instance
  static getInstance() {
    if (!window.quoteManagerInstance) {
      window.quoteManagerInstance = new QuoteManager();
    }
    return window.quoteManagerInstance;
  }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  QuoteManager.getInstance();
});

// Export for module systems (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = QuoteManager;
}