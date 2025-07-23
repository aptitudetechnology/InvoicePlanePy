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
    this.extractContextData();

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
    const form = document.querySelector('form[action*="/quotes/"]');
    if (form) {
      const matches = form.action.match(/\/quotes\/(\d+)\/edit/);
      this.quoteId = matches ? matches[1] : null;
    }

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

    // Item management buttons (updated selectors to IDs for clarity)
    const addRowBtn = document.getElementById('add-item-btn');
    if (addRowBtn) {
      addRowBtn.addEventListener('click', () => this.addNewRow());
    }

    const displayProductModalBtn = document.getElementById('display-product-modal-btn');
    if (displayProductModalBtn) {
      displayProductModalBtn.addEventListener('click', () => this.displayProductModal());
    }

    this.cleanupInlineHandlers();

    // Discount percentage change
    const discountInput = document.querySelector('input[name="discount_percentage"]');
    if (discountInput) {
      discountInput.addEventListener('change', () => this.calculateTotals());
    }

    // Event delegation for dynamic item rows
    const itemsTable = document.getElementById('quote-items');
    if (itemsTable) {
      itemsTable.addEventListener('click', (e) => {
        if (e.target.closest('.btn-outline-danger') || e.target.closest('.remove-item-btn')) {
          this.removeItem(e.target.closest('tr'));
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
    if (!tbody) return;

    const taxRateDropdownContent = this.createTaxRateDropdownHTML(this.itemCounter);

    const newRow = document.createElement('tr');
    newRow.innerHTML = `
      <td>
        <button type="button" class="btn btn-sm btn-outline-danger remove-item-btn" aria-label="Remove item">
          <i class="bi bi-trash"></i>
        </button>
      </td>
      <td>
        <input type="text" class="form-control form-control-sm" name="items[${this.itemCounter}][name]" placeholder="Item">
        <textarea class="form-control form-control-sm mt-1" name="items[${this.itemCounter}][description]" rows="2" placeholder="Description"></textarea>
        <input type="hidden" name="items[${this.itemCounter}][product_id]" value="">
      </td>
      <td>
        <input type="number" class="form-control form-control-sm" name="items[${this.itemCounter}][quantity]" value="1" step="0.01" min="0">
      </td>
      <td>
        <input type="number" class="form-control form-control-sm" name="items[${this.itemCounter}][price]" value="0.00" step="0.01" min="0">
      </td>
      <td>
        <input type="number" class="form-control form-control-sm" name="items[${this.itemCounter}][discount]" value="0.00" step="0.01" min="0">
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

    // Attach event listeners to new inputs for recalculation
    this.attachEventListeners();
  }

  addNewRowWithProduct(productName, price, productId) {
    this.addNewRow();

    const tbody = document.getElementById('quote-items');
    const lastRow = tbody.lastElementChild;

    if (lastRow) {
      const nameInput = lastRow.querySelector(`input[name*="[name]"]`);
      if (nameInput) nameInput.value = productName;

      const priceInput = lastRow.querySelector(`input[name*="[price]"]`);
      if (priceInput) {
        priceInput.value = price.toFixed(2);
        this.calculateItemTotal(priceInput);
      }

      const quantityInput = lastRow.querySelector(`input[name*="[quantity]"]`);
      if (quantityInput) quantityInput.value = '1';

      const productIdInput = lastRow.querySelector(`input[name*="[product_id]"]`);
      if (productIdInput && productId) productIdInput.value = productId;
    }
  }

  removeItem(row) {
    if (!row) return;
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
    const quoteTax = 0; // Implement if needed

    const total = subtotal - totalDiscount - additionalDiscount + itemTax +
