// Shared utility for adding a new product/item row to a table (quotes, invoices, etc.)
// Usage: window.addNewRowWithProduct(productName, price, productId, tableBodyId = 'quote-items-body')

(() => {
  let itemCounter = window.itemCounter || 0;

  function addNewRowWithProduct(productName, price, productId, tableBodyId = 'quote-items-body') {
    itemCounter++;
    window.itemCounter = itemCounter; // persist globally if needed

    const tableBody = document.getElementById(tableBodyId);
    if (!tableBody) {
      console.error('Quote/Invoice items table body not found!');
      return;
    }

    // Create new row
    const row = document.createElement('tr');
    row.setAttribute('data-product-id', productId || '');

    row.innerHTML = `
      <td>${itemCounter}</td>
      <td><input type="text" name="product_name_${itemCounter}" value="${productName}" class="form-control" readonly></td>
      <td><input type="number" name="quantity_${itemCounter}" value="1" min="1" class="form-control quantity-input"></td>
      <td><input type="text" name="price_${itemCounter}" value="${parseFloat(price).toFixed(2)}" class="form-control price-input" readonly></td>
      <td><input type="text" name="total_${itemCounter}" value="${parseFloat(price).toFixed(2)}" class="form-control total-input" readonly></td>
      <td><input type="hidden" name="product_id_${itemCounter}" value="${productId || ''}"><button type="button" class="btn btn-danger btn-sm remove-row-btn">Remove</button></td>
    `;

    tableBody.appendChild(row);

    // Attach event listener for quantity changes to update total
    const quantityInput = row.querySelector('.quantity-input');
    const priceInput = row.querySelector('.price-input');
    const totalInput = row.querySelector('.total-input');
    if (quantityInput && priceInput && totalInput) {
      quantityInput.addEventListener('input', () => {
        const qty = parseInt(quantityInput.value) || 1;
        totalInput.value = (qty * parseFloat(priceInput.value)).toFixed(2);
        updateQuoteTotal(tableBodyId);
      });
    }

    // Remove row button
    const removeBtn = row.querySelector('.remove-row-btn');
    if (removeBtn) {
      removeBtn.addEventListener('click', () => {
        row.remove();
        updateQuoteTotal(tableBodyId);
      });
    }

    updateQuoteTotal(tableBodyId);
  }

  // Simple total update function
  function updateQuoteTotal(tableBodyId = 'quote-items-body') {
    const tableBody = document.getElementById(tableBodyId);
    if (!tableBody) return;
    const totalInputs = tableBody.querySelectorAll('.total-input');
    let grandTotal = 0;
    totalInputs.forEach(input => {
      grandTotal += parseFloat(input.value) || 0;
    });

    // Try to find a total display element in the same table
    let totalDisplay = null;
    // Look for a span with id ending in grand-total in the same table
    let table = tableBody.closest('table');
    if (table) {
      totalDisplay = table.querySelector('span[id$="grand-total"]');
    }
    // Fallback to global id
    if (!totalDisplay) {
      totalDisplay = document.getElementById('quote-grand-total') || document.getElementById('invoice-grand-total');
    }
    if (totalDisplay) {
      totalDisplay.textContent = grandTotal.toFixed(2);
    }
  }

  // Expose globally for modal and other scripts
  window.addNewRowWithProduct = addNewRowWithProduct;
  window.updateQuoteTotal = updateQuoteTotal;
})();