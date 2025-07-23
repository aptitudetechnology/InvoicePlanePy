// Shared utility for adding a new product/item row to a table (quotes, invoices, etc.)
// Usage: window.addNewRowWithProduct(productName, price, productId, tableBodyId = 'quote-items-body', defaultTaxRates = [])

(() => {
  let itemCounter = window.itemCounter || 0; // Initialize or retrieve from global scope

  function addNewRowWithProduct(productName, price, productId, tableBodyId = 'quote-items', defaultTaxRates = []) {
    itemCounter++;
    window.itemCounter = itemCounter; // Persist globally if needed

    const tableBody = document.getElementById(tableBodyId);
    if (!tableBody) {
      console.error('Quote/Invoice items table body not found!');
      return;
    }

    // Create new row
    const row = document.createElement('tr');
    row.setAttribute('data-product-id', productId || '');
    row.setAttribute('data-item-id', itemCounter); // Add a unique identifier for the row

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
      <td>${itemCounter}</td>
      <td>
          <input type="text" name="product_name_${itemCounter}" value="${productName}" class="form-control" readonly>
          <textarea name="description_${itemCounter}" class="form-control mt-1" placeholder="Description"></textarea>
      </td>
      <td><input type="number" name="quantity_${itemCounter}" value="${initialQuantity}" min="1" class="form-control quantity-input"></td>
      <td><input type="text" name="price_${itemCounter}" value="${initialPrice.toFixed(2)}" class="form-control price-input"></td>
      <td><input type="text" name="item_discount_amount_${itemCounter}" value="${initialItemDiscountAmount.toFixed(2)}" class="form-control item-discount-input"></td>
      <td>
          <select name="tax_rate_${itemCounter}" class="form-control tax-rate-select">
              ${taxOptionsHtml}
          </select>
      </td>
      <td><input type="text" name="subtotal_${itemCounter}" value="${initialSubtotal.toFixed(2)}" class="form-control subtotal-input" readonly></td>
      <td><input type="text" name="calculated_item_discount_${itemCounter}" value="${initialItemCalculatedDiscount.toFixed(2)}" class="form-control calculated-item-discount-input" readonly></td>
      <td><input type="text" name="tax_amount_${itemCounter}" value="${initialTax.toFixed(2)}" class="form-control item-tax-input" readonly></td>
      <td><input type="text" name="line_total_${itemCounter}" value="${initialLineTotal.toFixed(2)}" class="form-control line-total-input" readonly></td>
      <td>
          <input type="hidden" name="product_id_${itemCounter}" value="${productId || ''}">
          <button type="button" class="btn btn-danger btn-sm remove-row-btn">Remove</button>
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


  // Expose globally for modal and other scripts
  window.addNewRowWithProduct = addNewRowWithProduct;
  window.updateQuoteOverallTotal = updateQuoteOverallTotal; // Renamed for clarity
})();