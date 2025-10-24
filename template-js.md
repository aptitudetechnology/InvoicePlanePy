# JavaScript in Templates Audit Report

This report documents the presence of JavaScript code in Jinja2 HTML templates and recommends migration to external JS modules for maintainability and clarity.

---

## Summary
Many template files in `app/templates/` contain embedded JavaScript code within `<script>` tags. This increases template size and complexity, making them harder to maintain. Moving JavaScript to external modules will:
- Improve readability and maintainability of templates
- Enable code reuse and easier debugging
- Allow for better separation of concerns

---

## Templates with Embedded JavaScript

### Quotes
- `quotes/edit.html`: Extensive JS for item management, tax rates, product modal, calculations
- `quotes/create.html`: JS for date picker, form logic
- `quotes/view.html`: JS for quote actions (add tax, download PDF, email, etc.)
- `modals/add_product_modal.html`: JS for modal logic

### Invoices
- `invoices/edit.html`: Extensive JS for item management, tax rates, calculations
- `invoices/create.html`: JS for form logic
- `invoices/details.html`: JS for item management
- `invoices/view.html`: JS for item management, actions

### Products
- `products/list.html`: JS for product table, filtering, loading
- `products/create.html`: JS for tax rate selection
- `products/edit.html`: JS for product editing

### Clients
- `clients/create.html`: JS for input formatting
- `clients/edit.html`: JS for client editing

### Settings
- `settings/users.html`: JS for user management
- `settings/tax_rates.html`: JS for tax rate management
- `settings/new_custom_field.html`: JS for custom field logic
- `settings/system.html`: JS for system settings

### Other
- `base.html`: JS includes and some inline logic
- `auth/login.html`: JS includes

---

## Common JS Patterns Found
- Item row management (add/remove/update)
- Tax rate loading and dropdown population
- Product modal logic
- Form validation and formatting
- Calculation functions (totals, discounts, taxes)
- AJAX/fetch API calls for dynamic data
- UI updates and event listeners

---

## Recommendations
1. **Move all inline `<script>` blocks to external JS files/modules.**
   - Create a `static/js/` directory for feature-specific modules (e.g., `quotes.js`, `invoices.js`, `products.js`).
   - Reference these modules in templates using `<script src="/static/js/quotes.js"></script>`.
2. **Refactor duplicated logic into reusable functions.**
   - E.g., item row management, tax rate dropdowns, calculation functions.
3. **Use ES6 modules for better structure.**
   - Export/import functions as needed.
4. **Minimize template JS to only initialization or context passing.**
   - E.g., pass initial data via JSON in a `<script>` block, then let external JS handle logic.
5. **Test all features after migration to ensure no breakage.**

---

## Next Steps

### 1. Inventory & Prioritize
- Review all templates listed above and document each `<script>` block and its purpose.
- Prioritize migration starting with the largest/most complex templates: `quotes/edit.html`, `invoices/edit.html`, etc.

### 2. Create External JS Modules
- For each feature area (quotes, invoices, products, etc.), create a dedicated JS file in `static/js/` (e.g., `quotes.js`, `invoices.js`).
- Use ES6 module syntax for better structure and maintainability.

### 3. Migrate Logic
- Move all inline JS logic from templates into the appropriate external JS module.
- Refactor duplicated logic into reusable functions and utilities.
- For context-specific data (e.g., initial values from backend), pass via a small inline `<script>` block or data attributes, then consume in the external JS.

### 4. Update Template References
- Remove inline `<script>` blocks from templates.
- Add `<script src="/static/js/[feature].js"></script>` at the end of each template or in `base.html` as appropriate.

### 5. Refactor & Test
- Refactor code for clarity, modularity, and reuse.
- Test all features in the browser to ensure no breakage or regressions.
- Use browser dev tools to verify that JS modules are loaded and functioning as expected.

### 6. Document Migration
- Update project documentation to reflect new JS module structure and usage.
- Provide examples for future contributors on how to add JS logic to modules instead of templates.

---

**Following these steps will result in cleaner templates, reusable JS modules, and a more maintainable codebase.**

---

**Moving JS out of templates will greatly improve maintainability and developer experience.**
