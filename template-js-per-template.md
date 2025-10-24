# Template JavaScript Audit: Per-Template Report

This section provides a per-template summary of JavaScript presence, complexity, and migration recommendations.

---

## Quotes
### quotes/edit.html
- Extensive JS: item row management, tax rates, product modal, calculations, AJAX calls.
- Multiple functions for UI logic and calculations.
- **Migration Priority:** Highest. Move all logic to `static/js/quotes.js`.

### quotes/create.html
- JS for date picker, form logic, initial value setup.
- **Migration Priority:** High. Move to `static/js/quotes.js`.

### quotes/view.html
- JS for quote actions (add tax, download PDF, email, etc.).
- **Migration Priority:** High. Move to `static/js/quotes.js`.

### modals/add_product_modal.html
- JS for modal logic, product selection.
- **Migration Priority:** Medium. Move to `static/js/products.js` or `static/js/quotes.js`.

---

## Invoices
### invoices/edit.html
- Extensive JS: item management, tax rates, calculations, AJAX calls.
- Multiple functions for UI logic and calculations.
- **Migration Priority:** Highest. Move all logic to `static/js/invoices.js`.

### invoices/create.html
- JS for form logic, initial value setup.
- **Migration Priority:** High. Move to `static/js/invoices.js`.

### invoices/details.html
- JS for item management, calculations.
- **Migration Priority:** High. Move to `static/js/invoices.js`.

### invoices/view.html
- JS for item management, actions (add/remove row, update client details).
- **Migration Priority:** High. Move to `static/js/invoices.js`.

---

## Products
### products/list.html
- JS for product table rendering, filtering, loading, error handling.
- Multiple utility functions.
- **Migration Priority:** Medium. Move to `static/js/products.js`.

### products/create.html
- JS for tax rate selection, form logic.
- **Migration Priority:** Medium. Move to `static/js/products.js`.

### products/edit.html
- JS for product editing logic.
- **Migration Priority:** Medium. Move to `static/js/products.js`.

---

## Clients
### clients/create.html
- JS for input formatting, validation.
- **Migration Priority:** Medium. Move to `static/js/clients.js`.

### clients/edit.html
- JS for client editing logic.
- **Migration Priority:** Medium. Move to `static/js/clients.js`.

---

## Settings
### settings/users.html
- JS for user management, table rendering, delete confirmation.
- **Migration Priority:** Medium. Move to `static/js/settings.js`.

### settings/tax_rates.html
- JS for tax rate management, editing, table rendering.
- **Migration Priority:** Medium. Move to `static/js/settings.js`.

### settings/new_custom_field.html
- JS for custom field logic, option management.
- **Migration Priority:** Medium. Move to `static/js/settings.js`.

### settings/system.html
- JS for API key management, alerts.
- **Migration Priority:** Medium. Move to `static/js/settings.js`.

---

## Other
### base.html
- JS includes for Bootstrap and app.js, some inline logic.
- **Migration Priority:** Low. Inline logic should be minimal; keep only initialization if needed.

### auth/login.html
- JS includes for Bootstrap.
- **Migration Priority:** Low. No custom logic detected.

---

## Migration Recommendations
- Start with the largest/most complex templates (quotes/edit.html, invoices/edit.html).
- Create feature-specific JS modules in `static/js/`.
- Move all inline JS logic to modules, refactor for reuse.
- Update templates to reference new JS files.
- Test thoroughly after migration.

---

## Event Handler Setup During Migration

When moving JS out of templates, all event handler logic should be migrated to the new JS modules:

- **Attach event listeners in JS, not in HTML.**
  - Use `document.addEventListener('DOMContentLoaded', ...)` or module-level init functions.
  - Example: `document.getElementById('addRowBtn').addEventListener('click', addNewRow);`
- **Avoid inline event attributes** (`onclick`, `onchange`, etc.) in HTML templates.
- **Use event delegation** for dynamic elements (e.g., rows/items added after page load).
- **Group event handlers by feature** in the appropriate module (e.g., all quote item handlers in `quotes.js`).
- **For context-specific data**, pass via JSON or data attributes, then consume in JS for event logic.
- **Test all event-driven features** after migration to ensure correct behavior.

**Example:**
```js
// static/js/quotes.js
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('addRowBtn').addEventListener('click', addNewRow);
  document.getElementById('quoteForm').addEventListener('submit', handleQuoteSubmit);
  // ...other handlers
});
```

---

**Proper event handler setup in JS modules will ensure maintainable, robust, and testable UI logic.**

---

**This per-template report will help prioritize and organize the migration of JavaScript out of templates.**
