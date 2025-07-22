## Quote & QuoteItem Data Dictionary Audit

This report documents the audit of all fields referenced in the `quotes/edit.html` template against the data dictionary in `quotes_schema.py`. It ensures every field exists, is spelled correctly, and matches the expected type.

---

### 1. Quote Fields (quotes table)

| Template Field Name         | Data Dictionary Field         | Exists? | Type / Notes                                  |
|----------------------------|------------------------------|---------|-----------------------------------------------|
| `id`                       | `id`                         | Yes     | INTEGER, PK                                   |
| `client_id`                | `client_id`                  | Yes     | INTEGER, FK                                   |
| `user_id`                  | `user_id`                    | Yes     | INTEGER, FK                                   |
| `quote_number`             | `quote_number`               | Yes     | VARCHAR(50), unique                           |
| `title`                    | `title`                      | Yes     | VARCHAR(255), nullable                        |
| `issue_date`               | `issue_date`                 | Yes     | DATE                                          |
| `valid_until`              | `valid_until`                | Yes     | DATE, nullable                                |
| `quote_pdf_password`       | `quote_pdf_password`         | Yes     | VARCHAR(255), nullable                        |
| `subtotal`                 | `subtotal`                   | Yes     | DECIMAL(10,2), default 0.00                   |
| `item_tax_total`           | `item_tax_total`             | Yes     | DECIMAL(10,2), default 0.00                   |
| `quote_discount_amount`    | `quote_discount_amount`      | Yes     | DECIMAL(10,2), default 0.00                   |
| `quote_tax_amount`         | `quote_tax_amount`           | Yes     | DECIMAL(10,2), default 0.00                   |
| `amount`                   | `amount`                     | Yes     | DECIMAL(10,2)                                 |
| `balance`                  | `balance`                    | Yes     | DECIMAL(10,2)                                 |
| `currency`                 | `currency`                   | Yes     | VARCHAR(3), default 'AUD'                     |
| `status_id`                | `status_id`                  | Yes     | INTEGER, FK                                   |
| `notes`                    | `notes`                      | Yes     | TEXT, nullable                                |
| `quote_tax_rate`           | `quote_tax_rate`             | Yes     | DECIMAL(5,2), default 0.00                    |
| `discount_percentage`      | `discount_percentage`        | Yes     | DECIMAL(5,2), default 0.00                    |
| `created_at`               | `created_at`                 | Yes     | DATETIME, default CURRENT_TIMESTAMP           |
| `updated_at`               | `updated_at`                 | Yes     | DATETIME, default CURRENT_TIMESTAMP           |

**Template/Model Notes:**
- The template uses `quote.status` (should be mapped to `status_id` and joined to `quote_statuses` for display).
- The template uses `quote.subtotal`, `quote.item_tax`, `quote.quote_tax`, `quote.total`:
  - `subtotal` → `subtotal`
  - `item_tax` → `item_tax_total`
  - `quote_tax` → `quote_tax_amount`
  - `total` → `amount`
- All fields referenced in the template exist in the data dictionary, but some computed fields in the template use slightly different names than the DB (see mapping above).

---

### 2. QuoteItem Fields (quote_items table)

| Template Field Name                | Data Dictionary Field         | Exists? | Type / Notes                                  |
|------------------------------------|------------------------------|---------|-----------------------------------------------|
| `id`                              | `id`                         | Yes     | INTEGER, PK                                   |
| `quote_id`                        | `quote_id`                   | Yes     | INTEGER, FK                                   |
| `product_id`                      | `product_id`                 | Yes     | INTEGER, FK, nullable                         |
| `item_name`                       | `item_name`                  | Yes     | VARCHAR(255)                                  |
| `description`                     | `description`                | Yes     | TEXT, nullable                                |
| `unit_price`                      | `unit_price`                 | Yes     | DECIMAL(10,2)                                 |
| `quantity`                        | `quantity`                   | Yes     | DECIMAL(10,2), default 1.00                   |
| `item_discount_percentage`        | `item_discount_percentage`   | Yes     | DECIMAL(5,2), default 0.00                    |
| `item_tax_rate`                   | `item_tax_rate`              | Yes     | DECIMAL(5,2), default 0.00                    |
| `subtotal`                        | `subtotal`                   | Yes     | DECIMAL(10,2)                                 |
| `discount_amount`                 | `discount_amount`            | Yes     | DECIMAL(10,2), default 0.00                   |
| `taxable_amount`                  | `taxable_amount`             | Yes     | DECIMAL(10,2)                                 |
| `tax_amount`                      | `tax_amount`                 | Yes     | DECIMAL(10,2), default 0.00                   |
| `total`                           | `total`                      | Yes     | DECIMAL(10,2)                                 |
| `sort_order`                      | `sort_order`                 | Yes     | INTEGER, default 0                            |
| `created_at`                      | `created_at`                 | Yes     | DATETIME, default CURRENT_TIMESTAMP           |
| `updated_at`                      | `updated_at`                 | Yes     | DATETIME, default CURRENT_TIMESTAMP           |

**Template/Model Notes:**
- The template uses `item.product_name` for display, but the DB field is `item_name`. If your model uses `product_name`, it should alias or map to `item_name`.
- The template uses `item.discount_percentage`, but the DB field is `item_discount_percentage`. This is a spelling mismatch and should be corrected in the model or template for consistency.
- The template uses `item.tax_rate`, but the DB field is `item_tax_rate`. This is a spelling mismatch and should be corrected in the model or template for consistency.

---

### 3. Key Mismatches & Recommendations

- **product_name vs item_name:**  
  - Template uses `product_name`, DB uses `item_name`.  
  - Recommendation: Use `item_name` in both model and template, or alias in the model.

- **discount_percentage vs item_discount_percentage:**  
  - Template uses `discount_percentage`, DB uses `item_discount_percentage`.  
  - Recommendation: Use `item_discount_percentage` in both model and template, or alias in the model.

- **tax_rate vs item_tax_rate:**  
  - Template uses `tax_rate`, DB uses `item_tax_rate`.  
  - Recommendation: Use `item_tax_rate` in both model and template, or alias in the model.

- **item_tax vs item_tax_total:**  
  - Template uses `item_tax`, DB uses `item_tax_total` (quote-level).  
  - Recommendation: Ensure correct mapping in backend context.

- **quote_tax vs quote_tax_amount:**  
  - Template uses `quote_tax`, DB uses `quote_tax_amount`.  
  - Recommendation: Ensure correct mapping in backend context.

- **total vs amount:**  
  - Template uses `total`, DB uses `amount` (quote-level).  
  - Recommendation: Ensure correct mapping in backend context.

---

### 4. Summary Table

| Template Field         | Data Dictionary Field         | Action Needed? |
|-----------------------|------------------------------|---------------|
| product_name          | item_name                    | Rename/alias  |
| discount_percentage   | item_discount_percentage     | Rename/alias  |
| tax_rate              | item_tax_rate                | Rename/alias  |
| item_tax              | item_tax_total               | Map context   |
| quote_tax             | quote_tax_amount             | Map context   |
| total (quote-level)   | amount                       | Map context   |

---

### 5. Conclusion

- All fields referenced in the template exist in the data dictionary, but some require renaming or aliasing for consistency.
- Update your models and/or template to use the exact field names from the data dictionary to prevent rollbacks and persistence issues.
- Computed fields should be provided in the backend context with the correct names expected by the template.

If you want a patch or code sample to fix these mismatches, let me know!