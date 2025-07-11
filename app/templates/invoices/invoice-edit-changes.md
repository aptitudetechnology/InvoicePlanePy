Here are the instructions for GitHub Copilot to update your invoice edit.html to handle tax rates the same way as your quotes template:

## GitHub Copilot Instructions

### Task: Update Invoice Edit Template to Use Dynamic Tax Rates from Backend

**Context**: Update the invoice edit template to fetch tax rates from the backend database instead of using hardcoded values, following the same pattern as the quotes edit template.

### Required Changes:

1. **Remove hardcoded tax rate options** from all tax rate select elements in the template
2. **Add dynamic tax rate loading** similar to quotes template
3. **Update JavaScript functions** to handle tax rates from API
4. **Maintain existing calculation logic** while using dynamic tax rates

### Specific Updates Needed:

#### 1. Replace hardcoded tax rate selects:
```html
<!-- REPLACE THIS: -->
<select class="form-select item-tax-rate" name="item_tax_rate_{{ loop.index0 }}">
    <option value="none">None</option>
    <option value="10">10% GST</option>
    <option value="15">15%</option>
    <option value="20">20%</option>
</select>

<!-- WITH THIS PATTERN: -->
<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_{{ loop.index0 }}">
    <option value="0">None (0%)</option>
    <!-- Dynamic options will be populated by JavaScript -->
</select>
```

#### 2. Add these JavaScript functions at the beginning of the script section:
```javascript
let taxRates = []; // Will be populated from database

// Load tax rates from database
async function loadTaxRates() {
    try {
        const response = await fetch('/tax_rates/api');
        if (!response.ok) throw new Error('Failed to load tax rates');
        const data = await response.json();
        taxRates = data.tax_rates || data;
        
        // Populate all existing tax rate dropdowns
        populateAllTaxRateDropdowns();
    } catch (error) {
        console.error('Error loading tax rates:', error);
        // Fallback to empty array if server fails
        taxRates = [];
    }
}

// Populate all tax rate dropdowns with current tax rates
function populateAllTaxRateDropdowns() {
    const taxRateSelects = document.querySelectorAll('.tax-rate-select');
    taxRateSelects.forEach(select => {
        populateTaxRateDropdown(select);
    });
}

// Populate a single tax rate dropdown
function populateTaxRateDropdown(selectElement) {
    const currentValue = selectElement.value;
    
    // Clear existing options except the "None" option
    selectElement.innerHTML = '<option value="0">None (0%)</option>';
    
    // Add tax rates from database
    taxRates.forEach(taxRate => {
        const option = document.createElement('option');
        option.value = taxRate.rate;
        option.textContent = `${taxRate.name} (${taxRate.rate.toFixed(2)}%)`;
        option.setAttribute('data-tax-id', taxRate.id);
        selectElement.appendChild(option);
    });
    
    // Restore selected value
    selectElement.value = currentValue;
}

// Create tax rate dropdown HTML for new rows
function createTaxRateDropdownHTML(itemIndex, selectedRate = 0) {
    let optionsHTML = '<option value="0">None (0%)</option>';
    
    taxRates.forEach(taxRate => {
        const selected = taxRate.rate == selectedRate ? 'selected' : '';
        optionsHTML += `<option value="${taxRate.rate}" data-tax-id="${taxRate.id}" ${selected}>${taxRate.name} (${taxRate.rate.toFixed(2)}%)</option>`;
    });
    
    return `<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_${itemIndex}">${optionsHTML}</select>`;
}
```

#### 3. Update the `addNewRow()` function to use dynamic tax rates:
- Replace hardcoded tax rate options in the function with `${createTaxRateDropdownHTML(itemCounter)}`

#### 4. Update the DOMContentLoaded event listener:
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // ... existing code ...
    
    // Load tax rates first, then calculate totals
    loadTaxRates().then(() => {
        calculateTotals();
    });
});
```

#### 5. Add the `tax-rate-select` class to existing tax rate select elements in both the loop and fallback sections

#### 6. Update calculation logic to handle numeric tax rates:
- Change `parseFloat(taxRateSelect.value) || 0` to handle the new format
- Ensure tax rate values are treated as numbers, not strings

### Key Requirements:
- Maintain all existing functionality
- Use the same API endpoint `/tax_rates/api`
- Keep the same calculation logic
- Preserve form field naming conventions
- Add proper error handling for API failures
- Ensure backward compatibility with existing data

### Testing Notes:
- Verify tax rates load correctly on page load
- Test adding new rows with dynamic tax rates
- Confirm calculations work with database tax rates
- Check that existing invoice data displays correctly


## GitHub Copilot Instructions (Continued)

### Task: Complete the Invoice Edit Template Tax Rate Updates

**Context**: Complete the remaining updates to make the invoice edit template use dynamic tax rates from the backend database.

### Additional Changes Required:

#### 7. Update existing tax rate select elements in the HTML template:

**In the items loop section (around line 119):**
```html
<!-- FIND THIS: -->
<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_{{ loop.index0 }}" onchange="calculateItemTotal(this)"></select>
<input type="hidden" class="initial-tax-rate" value="{{ item.tax_rate if item.tax_rate is not none else 0 }}">

<!-- UPDATE TO: -->
<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_{{ loop.index0 }}" onchange="calculateItemTotal(this)">
    <option value="0">None (0%)</option>
    <!-- Options will be populated by JavaScript -->
</select>
<input type="hidden" class="initial-tax-rate" value="{{ item.tax_rate if item.tax_rate is not none else 0 }}">
```

**In the fallback section (around line 148):**
```html
<!-- FIND THIS: -->
<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_0" onchange="calculateItemTotal(this)"></select>
<input type="hidden" class="initial-tax-rate" value="0">

<!-- UPDATE TO: -->
<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_0" onchange="calculateItemTotal(this)">
    <option value="0">None (0%)</option>
    <!-- Options will be populated by JavaScript -->
</select>
<input type="hidden" class="initial-tax-rate" value="0">
```

#### 8. Update the `addNewRow()` function (around line 386):

**FIND the tax rate select creation part:**
```html
<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_${itemCounter}" onchange="calculateItemTotal(this)"></select>
```

**REPLACE with:**
```html
<select class="form-select item-tax-rate tax-rate-select" name="item_tax_rate_${itemCounter}" onchange="calculateItemTotal(this)">
    <option value="0">None (0%)</option>
    <!-- Options will be populated by JavaScript -->
</select>
```

**Then ADD this line after `tbody.appendChild(newRow);`:**
```javascript
// Populate tax rate select for the new row
const newTaxSelect = newRow.querySelector('.item-tax-rate');
fillTaxRateSelect(newTaxSelect, taxRates, 0);
```

#### 9. Update the `populateTaxRateDropdown()` function to handle initial values:

**REPLACE the existing function with:**
```javascript
function populateTaxRateDropdown(selectElement) {
    // Get initial value from hidden input if it exists
    const initialValueInput = selectElement.closest('td').querySelector('.initial-tax-rate');
    const initialValue = initialValueInput ? parseFloat(initialValueInput.value) : 0;
    
    // Clear existing options
    selectElement.innerHTML = '<option value="0">None (0%)</option>';
    
    // Add tax rates from database
    taxRates.forEach(taxRate => {
        const option = document.createElement('option');
        option.value = taxRate.rate;
        option.textContent = `${taxRate.name} (${taxRate.rate.toFixed(2)}%)`;
        option.setAttribute('data-tax-id', taxRate.id);
        selectElement.appendChild(option);
    });
    
    // Set the initial value
    const matchingOption = Array.from(selectElement.options).find(opt => 
        parseFloat(opt.value) === initialValue
    );
    if (matchingOption) {
        matchingOption.selected = true;
    } else {
        selectElement.value = '0';
    }
}
```

#### 10. Update the DOMContentLoaded event listener (around line 274):

**FIND the existing tax rate loading section:**
```javascript
// Load tax rates first, then populate all selects and perform initial calculation
fetchTaxRates().then(rates => {
    taxRates = rates;
    document.querySelectorAll('.item-tax-rate').forEach((select, idx) => {
        // Get initial value from hidden input
        const initialValueInput = select.closest('td').querySelector('.initial-tax-rate');
        const initialValue = initialValueInput ? parseFloat(initialValueInput.value) : 0;
        fillTaxRateSelect(select, taxRates, initialValue);
    });
    calculateTotals();
});
```

**REPLACE with:**
```javascript
// Load tax rates first, then populate all selects and perform initial calculation
loadTaxRates().then(() => {
    calculateTotals();
});
```

#### 11. Update the `fillTaxRateSelect()` function to match the new format:

**REPLACE the existing function with:**
```javascript
function fillTaxRateSelect(selectElement, rates, selectedRate = 0) {
    selectElement.innerHTML = '<option value="0">None (0%)</option>';
    rates.forEach(rate => {
        const option = document.createElement('option');
        option.value = rate.rate;
        option.textContent = `${rate.name} (${parseFloat(rate.rate).toFixed(2)}%)`;
        option.setAttribute('data-tax-id', rate.id);
        if (parseFloat(rate.rate) === parseFloat(selectedRate)) {
            option.selected = true;
        }
        selectElement.appendChild(option);
    });
    if (!selectElement.value) {
        selectElement.value = '0';
    }
}
```

#### 12. Remove or update the `fetchTaxRates()` function:

**Since we're now using `loadTaxRates()`, either:**
- Remove the `fetchTaxRates()` function entirely, OR
- Update it to be an alias: `const fetchTaxRates = loadTaxRates;`

#### 13. Add error handling for tax rate loading:

**Update the `loadTaxRates()` function to include better error handling:**
```javascript
async function loadTaxRates() {
    try {
        const response = await fetch('/tax_rates/api');
        if (!response.ok) throw new Error('Failed to load tax rates');
        const data = await response.json();
        taxRates = data.tax_rates || data;
        
        // Populate all existing tax rate dropdowns
        populateAllTaxRateDropdowns();
    } catch (error) {
        console.error('Error loading tax rates:', error);
        // Fallback to empty array if server fails
        taxRates = [];
        // Still populate dropdowns with just the "None" option
        populateAllTaxRateDropdowns();
    }
}
```

### Final Verification Steps:

1. **Check all tax rate select elements** have the `tax-rate-select` class
2. **Verify all hardcoded tax rate options** are removed from HTML
3. **Confirm JavaScript functions** are properly integrated
4. **Test that existing invoice data** loads correctly with proper tax rates selected
5. **Ensure new rows** get proper tax rate options
6. **Verify calculations** work with the new tax rate structure

### Testing Checklist:
- [ ] Page loads without JavaScript errors
- [ ] Tax rates populate from database on page load
- [ ] Existing invoice items show correct tax rates selected
- [ ] Adding new rows creates proper tax rate dropdowns
- [ ] Calculations work correctly with database tax rates
- [ ] Error handling works if tax rate API fails
- [ ] Form submission includes correct tax rate values

**Important**: Make sure to preserve all existing functionality while implementing these changes. The invoice edit form should work exactly as before, but now with dynamic tax rates from the database.