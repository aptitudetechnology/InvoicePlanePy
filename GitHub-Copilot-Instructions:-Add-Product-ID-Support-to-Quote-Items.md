# GitHub Copilot Instructions: Add Product ID Support to Quote Items

## Context
We need to add `product_id` field support to quote items in the edit quote template. Currently, when products are selected from the modal, the `product_id` is not being captured or stored with the quote items.

## Required Changes

### 1. Update `addSelectedProducts()` function in product modal
```javascript
// MODIFY: Extract product_id from checkbox and pass to addProductToQuote
function addSelectedProducts() {
    const selectedCheckboxes = document.querySelectorAll('.product-checkbox:checked');
    
    selectedCheckboxes.forEach(checkbox => {
        const row = checkbox.closest('.product-row');
        const productName = row.cells[3].textContent.trim();
        const price = row.cells[5].textContent.replace('$', '');
        // ADD: Get product_id from data attribute
        const productId = checkbox.getAttribute('data-product-id');
        
        // MODIFY: Pass productId as third parameter
        addProductToQuote(productName, price, productId);
    });
    
    // ... rest unchanged
}
```

### 2. Update `addProductToQuote()` function in product modal
```javascript
// MODIFY: Add productId parameter and include hidden product_id input
function addProductToQuote(productName, price, productId = null) {
    const tbody = document.getElementById('quote-items');
    const newRow = document.createElement('tr');
    
    const taxRateDropdownContent = createTaxRateDropdownHTML(itemCounter);
    
    newRow.innerHTML = `
        // ... existing HTML ...
        <td>
            <input type="text" class="form-control form-control-sm" name="items[${itemCounter}][name]" value="${productName}" placeholder="Item">
            <textarea class="form-control form-control-sm mt-1" name="items[${itemCounter}][description]" rows="2" placeholder="Description"></textarea>
            // ADD: Hidden product_id field
            <input type="hidden" name="items[${itemCounter}][product_id]" value="${productId || ''}">
        </td>
        // ... rest unchanged ...
    `;
    // ... rest unchanged
}
```

### 3. Update `addNewRow()` function in main edit.html
```javascript
// MODIFY: Add hidden product_id field to manually added rows
function addNewRow() {
    // ... existing code ...
    newRow.innerHTML = `
        // ... existing HTML ...
        <td>
            <input type="text" class="form-control form-control-sm" name="items[${itemCounter}][name]" placeholder="Item">
            <textarea class="form-control form-control-sm mt-1" name="items[${itemCounter}][description]" rows="2" placeholder="Description"></textarea>
            // ADD: Empty product_id field for manual items
            <input type="hidden" name="items[${itemCounter}][product_id]" value="">
        </td>
        // ... rest unchanged ...
    `;
    // ... rest unchanged
}
```

### 4. Update existing quote items template in edit.html
```html
<!-- MODIFY: Add product_id hidden field to existing items -->
{% for item in quote.items %}
<tr data-item-id="{{ item.id }}">
    <!-- ... existing columns ... -->
    <td>
        <input type="text" class="form-control form-control-sm"
            name="items[{{ loop.index0 }}][name]" value="{{ item.name }}" placeholder="Item">
        <textarea class="form-control form-control-sm mt-1"
            name="items[{{ loop.index0 }}][description]" rows="2"
            placeholder="Description">{{ item.description }}</textarea>
        <!-- ADD: Hidden product_id field -->
        <input type="hidden" name="items[{{ loop.index0 }}][product_id]" value="{{ item.product_id or '' }}">
    </td>
    <!-- ... rest unchanged ... -->
</tr>
{% endfor %}
```

## Key Points for Copilot:
- Add `product_id` as hidden input field in all quote item rows
- Capture `data-product-id` attribute from selected product checkboxes
- Pass product ID through function parameters when creating new rows
- Handle both product-selected items (with ID) and manual items (empty ID)
- Maintain backward compatibility with existing quote items
- Use `value="${item.product_id or ''}"` pattern for optional fields in templates

## Expected Outcome:
- Product selections from modal will include `product_id` in form submission
- Manual quote items will have empty `product_id` field
- Existing quotes will maintain their product relationships
- Backend will receive `items[X][product_id]` field for each item