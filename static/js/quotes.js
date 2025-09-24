document.addEventListener('DOMContentLoaded', () => {
  // Get DOM elements after DOM is loaded
  const addProductBtn = document.getElementById('display-product-modal-btn');
  let itemCounter = window.itemCounter || 0;

  // Utility to parse floats safely
  function parseNumber(value) {
    let n = parseFloat(value);
    return isNaN(n) ? 0 : n;
  }

  // Calculate totals for all items and update totals section
  function calculateTotals() {
    let items = document.querySelectorAll('#quote-items tr[data-item-id]');
    let subtotal = 0;
    let totalItemTax = 0;
    let totalDiscountAmount = 0;

    items.forEach(row => {
      let qty = parseNumber(row.querySelector('.item-quantity').value);
      let price = parseNumber(row.querySelector('.item-price').value);
      let discountPercent = parseNumber(row.querySelector('.item-discount').value);
      let taxRateSelect = row.querySelector('.tax-rate-select');
      let taxRate = taxRateSelect ? parseNumber(taxRateSelect.value) : 0;

      // Calculate amounts for this item
      let itemSubtotal = qty * price;
      let discountAmount = itemSubtotal * (discountPercent / 100);
      let taxableAmount = itemSubtotal - discountAmount;
      let taxAmount = taxableAmount * (taxRate / 100);
      let total = taxableAmount + taxAmount;

      // Update row totals display (assuming elements exist)
      let subtotalElem = row.querySelector('.item-subtotal');
      if (subtotalElem) subtotalElem.textContent = `$${itemSubtotal.toFixed(2)}`;

      let discountElem = row.querySelector('.item-discount-amount');
      if (discountElem) discountElem.textContent = `$${discountAmount.toFixed(2)}`;

      let taxElem = row.querySelector('.item-tax-amount');
      if (taxElem) taxElem.textContent = `$${taxAmount.toFixed(2)}`;

      let totalElem = row.querySelector('.item-total');
      if (totalElem) totalElem.textContent = `$${total.toFixed(2)}`;

      subtotal += itemSubtotal;
      totalItemTax += taxAmount;
      totalDiscountAmount += discountAmount;
    });

    // Apply overall discount percentage from input
    const discountInput = document.querySelector('input[name="discount_percentage"]');
    let discountPercent = discountInput ? parseNumber(discountInput.value) : 0;
    let discountAmount = subtotal * (discountPercent / 100);

    // Calculate final totals
    let subtotalAfterDiscount = subtotal - discountAmount;
    let quoteTax = 0; // You may want to calculate additional quote-level tax here
    let total = subtotalAfterDiscount + totalItemTax + quoteTax;

    // Update the totals in the DOM with safety checks
    const subtotalElem = document.getElementById('quote-subtotal');
    if (subtotalElem) subtotalElem.textContent = `$${subtotal.toFixed(2)}`;

    const itemTaxElem = document.getElementById('quote-item-tax');
    if (itemTaxElem) itemTaxElem.textContent = `$${totalItemTax.toFixed(2)}`;

    const quoteTaxElem = document.getElementById('quote-tax');
    if (quoteTaxElem) quoteTaxElem.textContent = `$${quoteTax.toFixed(2)}`;

    const totalElem = document.getElementById('quote-total');
    if (totalElem) totalElem.textContent = `$${total.toFixed(2)}`;
  }

  // Event listeners to recalculate totals on inputs change
  function setupEventListeners() {
    const container = document.getElementById('quote-items');
    if (!container) return;

    container.addEventListener('input', (e) => {
      // Only recalc if relevant input changed
      if (['item-quantity', 'item-price', 'item-discount'].some(cls => e.target.classList.contains(cls)) ||
          e.target.classList.contains('tax-rate-select')) {
        calculateTotals();
      }
    });

    // Discount percentage input
    const discountInput = document.querySelector('input[name="discount_percentage"]');
    if (discountInput) {
      discountInput.addEventListener('input', () => {
        calculateTotals();
      });
    }

    // Remove item button
    container.addEventListener('click', (e) => {
      if (e.target.closest('[data-action="remove-item"]')) {
        const row = e.target.closest('tr[data-item-id]');
        if (row) {
          row.remove();
          calculateTotals();
        }
      }
    });

    // Add new empty item row
    const addItemBtn = document.getElementById('add-item-btn');
    if (addItemBtn) {
      addItemBtn.addEventListener('click', () => {
        addNewItemRow();
      });
    }
  }

  // Function to add a new blank item row
  function addNewItemRow() {
    const tbody = document.getElementById('quote-items');
    if (!tbody) return;

    const index = tbody.children.length;

    const newRow = document.createElement('tr');
    newRow.setAttribute('data-item-id', `new-${itemCounter++}`);

    newRow.innerHTML = `
      <td>
        <button type="button" class="btn btn-sm btn-outline-danger" data-action="remove-item">
          <i class="bi bi-trash"></i>
        </button>
      </td>
      <td>
        <input type="text" class="form-control form-control-sm" name="items[${index}][name]" placeholder="Item">
        <textarea class="form-control form-control-sm mt-1" name="items[${index}][description]" rows="2" placeholder="Description"></textarea>
      </td>
      <td>
        <input type="number" class="form-control form-control-sm item-quantity" name="items[${index}][quantity]" step="0.01" data-calculate="item-total" value="1">
      </td>
      <td>
        <input type="number" class="form-control form-control-sm item-price" name="items[${index}][price]" step="0.01" data-calculate="item-total" value="0.00">
      </td>
      <td>
        <input type="number" class="form-control form-control-sm item-discount" name="items[${index}][discount]" step="0.01" data-calculate="item-total" value="0">
      </td>
      <td>
        <select class="form-select form-select-sm tax-rate-select" name="items[${index}][tax_rate]" data-calculate="item-total">
          <option value="0" selected>None (0%)</option>
          ${window.taxRates ? window.taxRates.map(taxRate => 
            `<option value="${taxRate.rate}">${taxRate.name} (${taxRate.rate}%)</option>`
          ).join('') : ''}
        </select>
      </td>
      <td class="item-subtotal">$0.00</td>
      <td class="item-discount-amount">$0.00</td>
      <td class="item-tax-amount">$0.00</td>
      <td class="item-total">$0.00</td>
    `;

    tbody.appendChild(newRow);
  }

  // Add product modal button logic
  if (addProductBtn) {
    addProductBtn.addEventListener('click', () => {
      const productModalInstance = window.productModalInstance || (window.ProductModal && window.ProductModal.getInstance && window.ProductModal.getInstance());
      if (productModalInstance && typeof productModalInstance.showModal === 'function') {
        productModalInstance.showModal();
      }
    });
  }

  // Initial setup
  setupEventListeners();
  calculateTotals();
});
