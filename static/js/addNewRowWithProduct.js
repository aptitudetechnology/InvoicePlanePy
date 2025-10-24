// Shared utility for adding a new product/item row to a table (quotes, invoices, etc.)
// Usage: window.addNewRowWithProduct(productName, price, productId, tableBodyId = 'quote-items-body', defaultTaxRates = [])

(() => {
  console.log('addNewRowWithProduct.js: IIFE starting');
  let itemCounter = window.itemCounter || 0; // Initialize or retrieve from global scope

  function addNewRowWithProduct(productName, price, productId, tableBodyId = 'quote-items', defaultTaxRates = []) {
    const tableBody = document.getElementById(tableBodyId);
    if (!tableBody) {
      console.error('Quote/Invoice items table body not found!');
      return;
    }

    // Get the current index based on existing rows
    const index = tableBody.children.length;

    // Create new row
    const row = document.createElement('tr');
    row.setAttribute('data-product-id', productId || '');
    row.setAttribute('data-item-id', `new-${index}`); // Add a unique identifier for the row

    // Generate tax rate options
    let taxOptionsHtml = '<option value="0">None (0%)</option>';
    defaultTaxRates.forEach(rate => {
      taxOptionsHtml += `<option value="${rate.value}">${rate.name} (${rate.value}%)</option>`;
    });

    // Initial values for calculations
    const initialQuantity = 1;
    const initialPrice = parseFloat(price) || 0;
    const initialItemDiscountAmount = 0; // Assume 0 discount initially
    const initialTaxRate = 0; // Assume 0% tax initially

    let initialSubtotal = (initialQuantity * initialPrice);
    let initialItemCalculatedDiscount = initialItemDiscountAmount; // This will be updated if it's a percentage
    let initialTax = (initialSubtotal - initialItemCalculatedDiscount) * (initialTaxRate / 100);
    let initialLineTotal = initialSubtotal - initialItemCalculatedDiscount + initialTax;


    row.innerHTML = `
      <td>
        <button type="button" class="btn btn-danger btn-sm remove-row-btn">Remove</button>
      </td>
      <td>
          <input type="text" name="items[${index}][name]" value="${productName}" class="form-control" readonly>
          <textarea name="items[${index}][description]" class="form-control mt-1" placeholder="Description"></textarea>
      </td>
      <td><input type="number" name="items[${index}][quantity]" value="${initialQuantity}" min="1" class="form-control quantity-input"></td>
      <td><input type="text" name="items[${index}][price]" value="${initialPrice.toFixed(2)}" class="form-control price-input"></td>
      <td><input type="text" name="items[${index}][discount]" value="${initialItemDiscountAmount.toFixed(2)}" class="form-control item-discount-input"></td>
      <td>
          <select name="items[${index}][tax_rate]" class="form-control tax-rate-select">
              ${taxOptionsHtml}
          </select>
      </td>
      <td><input type="text" name="subtotal_${index}" value="${initialSubtotal.toFixed(2)}" class="form-control subtotal-input" readonly></td>
      <td><input type="text" name="calculated_item_discount_${index}" value="${initialItemCalculatedDiscount.toFixed(2)}" class="form-control calculated-item-discount-input" readonly></td>
      <td><input type="text" name="tax_amount_${index}" value="${initialTax.toFixed(2)}" class="form-control item-tax-input" readonly></td>
      <td><input type="text" name="line_total_${index}" value="${initialLineTotal.toFixed(2)}" class="form-control line-total-input" readonly></td>
      <td>
          <input type="hidden" name="product_id_${index}" value="${productId || ''}">
      </td>
    `;

    tableBody.appendChild(row);

    // --- Attach Event Listeners for Dynamic Calculations ---
    const quantityInput = row.querySelector('.quantity-input');
    const priceInput = row.querySelector('.price-input');
    const itemDiscountInput = row.querySelector('.item-discount-input');
    const taxRateSelect = row.querySelector('.tax-rate-select');

    const subtotalInput = row.querySelector('.subtotal-input');
    const calculatedItemDiscountInput = row.querySelector('.calculated-item-discount-input');
    const itemTaxInput = row.querySelector('.item-tax-input');
    const lineTotalInput = row.querySelector('.line-total-input');

    // Function to calculate and update a single row's values
    const updateRowCalculations = () => {
      const qty = parseFloat(quantityInput.value) || 0;
      const price = parseFloat(priceInput.value) || 0;
      const itemDiscount = parseFloat(itemDiscountInput.value) || 0; // This is an absolute discount amount
      const taxRate = parseFloat(taxRateSelect.value) || 0;

      const currentSubtotal = (qty * price);
      const currentItemDiscount = Math.min(itemDiscount, currentSubtotal); // Ensure discount doesn't exceed subtotal
      const amountAfterDiscount = currentSubtotal - currentItemDiscount;
      const currentTax = amountAfterDiscount * (taxRate / 100);
      const currentLineTotal = amountAfterDiscount + currentTax;

      subtotalInput.value = currentSubtotal.toFixed(2);
      calculatedItemDiscountInput.value = currentItemDiscount.toFixed(2);
      itemTaxInput.value = currentTax.toFixed(2);
      lineTotalInput.value = currentLineTotal.toFixed(2);

      updateQuoteOverallTotal(tableBodyId); // Update the grand total after row changes
    };

    // Attach event listeners for input changes
    quantityInput.addEventListener('input', updateRowCalculations);
    priceInput.addEventListener('input', updateRowCalculations);
    itemDiscountInput.addEventListener('input', updateRowCalculations);
    taxRateSelect.addEventListener('change', updateRowCalculations); // 'change' for select elements

    // Remove row button
    const removeBtn = row.querySelector('.remove-row-btn');
    if (removeBtn) {
      removeBtn.addEventListener('click', () => {
        row.remove();
        updateQuoteOverallTotal(tableBodyId); // Update the grand total after row removal
      });
    }

    // Perform initial calculations for the newly added row
    updateRowCalculations();
  }

  // Function to update the quote's overall totals (Subtotal, Discount, Tax, Total at the bottom)
  function updateQuoteOverallTotal(tableBodyId = 'quote-items') { // Changed default ID to match your usage
    const tableBody = document.getElementById(tableBodyId);
    if (!tableBody) return;

    let totalSubtotal = 0;
    let totalCalculatedItemDiscount = 0;
    let totalTax = 0;
    let grandTotal = 0;

    const rows = tableBody.querySelectorAll('tr[data-item-id]'); // Select only item rows

    rows.forEach(row => {
      const subtotalInput = row.querySelector('.subtotal-input');
      const calculatedItemDiscountInput = row.querySelector('.calculated-item-discount-input');
      const itemTaxInput = row.querySelector('.item-tax-input');
      const lineTotalInput = row.querySelector('.line-total-input');

      totalSubtotal += parseFloat(subtotalInput.value) || 0;
      totalCalculatedItemDiscount += parseFloat(calculatedItemDiscountInput.value) || 0;
      totalTax += parseFloat(itemTaxInput.value) || 0;
      grandTotal += parseFloat(lineTotalInput.value) || 0;
    });

    // Update display elements for overall totals
    document.getElementById('overall-subtotal-display').textContent = totalSubtotal.toFixed(2);
    document.getElementById('overall-discount-display').textContent = totalCalculatedItemDiscount.toFixed(2); // Assuming this is the sum of item discounts
    document.getElementById('overall-tax-display').textContent = totalTax.toFixed(2);
    document.getElementById('overall-grand-total-display').textContent = grandTotal.toFixed(2);

    // If you have a separate global discount input, you'd incorporate that here:
    // const globalDiscountInput = document.getElementById('global-discount-input');
    // const globalDiscount = parseFloat(globalDiscountInput.value) || 0;
    // grandTotal = grandTotal - globalDiscount;
    // document.getElementById('overall-grand-total-display').textContent = grandTotal.toFixed(2);
  }


  // Function to add a new product row to invoice table (different structure than quotes)
  function addNewRowWithProductForInvoice(productName, price, productId, tableBodyId = 'quote-items') {
    const tableBody = document.getElementById(tableBodyId);
    if (!tableBody) {
      console.error('Invoice items table body not found!');
      return;
    }

    // Get the current index based on existing rows
    const index = tableBody.children.length;

    // Create new row with invoice-specific structure
    const row = document.createElement('tr');
    row.setAttribute('data-product-id', productId || '');
    row.setAttribute('data-item-id', `new-${index}`);

    row.innerHTML = `
      <td>
        <input type="hidden" name="item_id_${index}" value="">
        <input type="text" class="form-control item-name" name="item_name_${index}" value="${productName}" placeholder="Item name" onchange="calculateItemTotal(this)">
        <textarea class="form-control mt-2 item-description" name="item_description_${index}" rows="2" placeholder="Description"></textarea>
      </td>
      <td>
        <input type="number" class="form-control item-quantity" name="item_quantity_${index}" min="1" value="1" onchange="calculateItemTotal(this)">
        <select class="form-select mt-2 item-unit" name="item_unit_${index}">
          <option value="none">None</option>
          <option value="piece">Piece</option>
          <option value="hour">Hour</option>
          <option value="day">Day</option>
          <option value="month">Month</option>
        </select>
      </td>
      <td>
        <input type="number" class="form-control item-price" name="item_price_${index}" min="0" step="0.01" value="${parseFloat(price).toFixed(2)}" onchange="calculateItemTotal(this)">
      </td>
      <td>
        <input type="number" class="form-control item-discount" name="item_discount_${index}" min="0" step="0.01" value="0" onchange="calculateItemTotal(this)">
      </td>
      <td>
        <select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_${index}" onchange="calculateItemTotal(this)">
          <option value="0">None (0%)</option>
        </select>
        <input type="hidden" class="initial-tax-rate" value="0">
      </td>
      <td>
        <input type="number" class="form-control item-total" name="item_total_${index}" value="${parseFloat(price).toFixed(2)}" readonly>
      </td>
      <td>
        <button type="button" class="btn btn-sm btn-danger remove-row-btn" onclick="removeRow(this)">
          <i class="bi bi-trash"></i>
        </button>
      </td>
    `;

    tableBody.appendChild(row);

    // Populate tax rate dropdown for the new row
    const taxRateSelect = row.querySelector('.tax-rate-select');
    if (taxRateSelect && typeof populateTaxRateDropdown === 'function') {
      populateTaxRateDropdown(taxRateSelect);
    }

    // Trigger calculation for the new row
    const firstInput = row.querySelector('.item-name');
    if (firstInput && typeof calculateItemTotal === 'function') {
      calculateItemTotal(firstInput);
    }
  }

  // Expose globally for modal and other scripts
  window.addNewRowWithProduct = addNewRowWithProduct;
  window.updateQuoteOverallTotal = updateQuoteOverallTotal; // Renamed for clarity

  // Expose the invoice function globally
  window.addNewRowWithProductForInvoice = addNewRowWithProductForInvoice;
  
  console.log('addNewRowWithProduct.js: Functions exposed:', {
    addNewRowWithProduct: !!window.addNewRowWithProduct,
    addNewRowWithProductForInvoice: !!window.addNewRowWithProductForInvoice,
    updateQuoteOverallTotal: !!window.updateQuoteOverallTotal
  });
  console.log('addNewRowWithProduct.js: IIFE completed successfully');
})();