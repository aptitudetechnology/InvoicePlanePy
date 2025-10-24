# GitHub Copilot Code Audit Instructions for InvoicePlanePy

## Overview
Audit the InvoicePlanePy codebase to identify opportunities for improvement using modern Python libraries. Focus on replacing custom implementations with well-tested, performant libraries while maintaining functionality and improving code readability.

## General Audit Guidelines

### 1. Data Processing & Manipulation
**Look for:**
- Custom data filtering, sorting, or grouping logic
- Manual CSV/Excel file handling
- Complex data transformations
- Date/time parsing and formatting
- Data validation routines

**Suggest replacements with:**
- **Pandas** for data manipulation, CSV/Excel handling, and complex operations
- **Polars** for high-performance data processing (alternative to Pandas)
- **Pydantic** for data validation and serialization
- **Arrow** or **Pendulum** for better date/time handling than datetime

### 2. File System Operations
**Look for:**
- `os.path.join()` and similar path manipulations
- File existence checks with `os.path.exists()`
- Directory creation with `os.makedirs()`
- File reading/writing with manual error handling

**Suggest replacements with:**
- **Pathlib** for cleaner, cross-platform path handling
- **shutil** for advanced file operations

### 3. HTTP Requests & API Interactions
**Look for:**
- Usage of `urllib` or manual HTTP handling
- Custom JSON parsing
- Basic authentication implementations
- Session management

**Suggest replacements with:**
- **Requests** or **httpx** for modern HTTP client functionality
- **aiohttp** for async HTTP operations if applicable

### 4. Database Operations (PostgreSQL)
**Look for:**
- Synchronous database calls that could be async
- Raw SQL string concatenation
- Manual connection management
- Repetitive CRUD operations
- Missing connection pooling
- Lack of prepared statements

**Suggest replacements with:**
- **asyncpg** for high-performance async PostgreSQL operations
- **SQLAlchemy 2.0** with async support for ORM capabilities
- **databases** library for simple async database operations
- **Alembic** for database migrations
- **psycopg3** for modern synchronous PostgreSQL operations if async isn't needed

### 5. Configuration Management
**Look for:**
- Manual config file parsing
- Hardcoded configuration values
- Environment variable handling with `os.environ`

**Suggest replacements with:**
- **Pydantic Settings** for type-safe configuration management
- **python-dotenv** for environment variable loading
- **dynaconf** for advanced configuration management

## Specific Areas to Audit in InvoicePlanePy

### 1. Invoice Processing Module
**Focus on:**
- Invoice data parsing and validation
- PDF generation logic
- Template rendering
- Data export functionality

**Questions to ask:**
- Can invoice data be represented as Pandas DataFrames for easier manipulation?
- Is PDF generation using ReportLab or similar library, or custom implementation?
- Can template rendering be improved with Jinja2?
- Are data exports handled efficiently?

### 2. PostgreSQL Database Layer
**Focus on:**
- Connection management and pooling
- Query building and execution
- Data models and relationships
- Migration handling
- Async database operations

**Questions to ask:**
- Is the project using async database drivers (asyncpg, databases)?
- Are database queries using SQLAlchemy Core/ORM or raw SQL?
- Is connection pooling properly configured?
- Are there proper database transaction management patterns?
- Is Alembic being used for migrations?

### 3. FastAPI Interface
**Focus on:**
- Dependency injection patterns
- Response models and serialization
- Background tasks
- Middleware implementation
- OpenAPI documentation

**Questions to ask:**
- Are Pydantic models being used effectively for request/response validation?
- Can dependency injection be leveraged more for database connections?
- Are background tasks using FastAPI's BackgroundTasks or Celery?
- Is async/await being used consistently throughout the API?

### 4. CLI Interface
**Focus on:**
- Command parsing with argparse
- User input handling
- Progress indicators
- Error handling and user feedback

**Suggest:**
- **Typer** for modern CLI with automatic help generation
- **Rich** for beautiful terminal output and progress bars
- **Click** as alternative to argparse

### 5. Reports Module (Incomplete Section) - Jinja2 Integration
**Audit for potential improvements:**
- Data aggregation and analysis logic
- Chart/graph generation
- Export formats (PDF, Excel, CSV)
- Jinja2 template optimization and organization

**Suggest modern libraries that work well with your stack:**
- **Pandas** for data aggregation and pivot tables
- **Plotly** for interactive charts (JSON serializable for FastAPI)
- **Jinja2** template inheritance and macro optimization
- **WeasyPrint** or **ReportLab** for PDF generation from HTML templates
- **OpenPyXL** for Excel report generation
- **FastAPI's BackgroundTasks** for async report generation

**Example audit prompt for reports:**
```
# Audit the reports module for:
1. Data aggregation that could use Pandas with PostgreSQL integration
2. Chart creation that could use Plotly (works great with FastAPI JSON responses)
3. Jinja2 template organization - are macros and inheritance being used effectively?
4. PDF generation - can HTML templates be converted to PDF with WeasyPrint?
5. Async report generation using FastAPI BackgroundTasks
6. Data export that leverages pandas.to_sql() for PostgreSQL
```

### 6. Data Export Functionality (Incomplete Section)
**Look for opportunities to use:**
- **Pandas** for DataFrame-based exports
- **OpenPyXL** for advanced Excel formatting
- **ReportLab** for professional PDF reports
- **Jinja2** for template-based exports

### 7. Error Handling & Logging
**Focus on:**
- Custom exception classes
- Logging implementations
- Error message formatting
- Debugging utilities

**Suggest:**
- **Loguru** for simpler, more powerful logging
- **Sentry** integration for error tracking
- **Rich** for beautiful error formatting

## Audit Prompts by Code Section

### For Each Python File:
```
Audit this Python file for opportunities to replace custom code with standard libraries:

1. DATA PROCESSING: Can any loops, filters, or data transformations be replaced with Pandas operations?
2. FILE HANDLING: Are there os.path operations that could use Pathlib instead?
3. HTTP/API: Is urllib being used where Requests would be cleaner?
4. CLI: Can argparse be replaced with Typer for better UX?
5. VALIDATION: Are there manual validation checks that Pydantic could handle?
6. DATES: Is datetime handling complex enough to benefit from Arrow/Pendulum?
7. TEMPLATES: Are there string formatting operations that could use Jinja2?
8. ASYNC: Are there blocking operations that could benefit from async libraries?

For each suggestion, provide:
- The current code pattern
- The improved version using the library
- Why the library approach is better (performance, readability, maintainability)
- Any potential breaking changes or migration considerations
```

### For FastAPI Routes:
```
Audit FastAPI route handlers for:
1. ASYNC OPERATIONS: Are database calls using async/await properly?
2. PYDANTIC MODELS: Are request/response models fully utilizing Pydantic features?
3. DEPENDENCY INJECTION: Can database connections, authentication, or common logic be moved to dependencies?
4. BACKGROUND TASKS: Are long-running operations (reports, exports) using BackgroundTasks?
5. ERROR HANDLING: Are HTTPExceptions being used appropriately with proper status codes?
6. VALIDATION: Is Pydantic handling all input validation, or are there manual checks?
7. SERIALIZATION: Are complex objects being serialized efficiently for JSON responses?

For each route, consider:
- Can the endpoint be made async for better performance?
- Are database operations properly awaited?
- Is proper exception handling in place?
- Are response models comprehensive and well-documented?
```

### For PostgreSQL Database Files:
```
Audit PostgreSQL-related code for:
1. ASYNC DRIVERS: Is asyncpg or databases being used for async operations?
2. CONNECTION POOLING: Is connection pooling configured for production use?
3. QUERY OPTIMIZATION: Are queries using proper indexes and avoiding N+1 problems?
4. TRANSACTIONS: Are database transactions being managed properly with async context managers?
5. MIGRATIONS: Is Alembic being used for schema migrations?
6. SQL INJECTION: Are all queries using parameterized statements?
7. BULK OPERATIONS: Can bulk inserts/updates use more efficient PostgreSQL-specific methods?

Specific to PostgreSQL:
- Are JSONB columns being used effectively for flexible data?
- Can array operations replace multiple queries?
- Are database functions/stored procedures needed for complex operations?
```

### For Incomplete Modules:
```
For incomplete/placeholder code, suggest:
1. Which libraries would best implement the intended functionality
2. Code structure recommendations using modern Python patterns
3. Dependencies that should be added to requirements.txt
4. Testing approaches using pytest fixtures and mocks
5. Documentation patterns using modern tools like mkdocs
```

## Output Format for Each Suggestion

For each improvement opportunity, provide:

### 1. Current Code Analysis
```python
# Current implementation example
# Point out specific issues or complexity
```

### 2. Improved Implementation
```python
# Suggested replacement using modern library
# Show how it's cleaner/more efficient
```

### 3. Benefits
- Performance improvements
- Code readability
- Maintainability gains
- Error handling improvements
- Testing advantages

### 4. Migration Notes
- Dependencies to add
- Potential breaking changes
- Testing requirements
- Documentation updates needed

## Priority Levels

**HIGH PRIORITY:**
- Security improvements (SQL injection, input validation)
- Performance bottlenecks
- Error-prone custom implementations

**MEDIUM PRIORITY:**
- Code readability improvements
- Maintenance burden reduction
- Developer experience enhancements

**LOW PRIORITY:**
- Style/convention improvements
- Minor optimizations
- Nice-to-have features

## Final Checklist

After auditing, verify:
- [ ] All suggestions maintain existing functionality
- [ ] Dependencies are actively maintained libraries
- [ ] Changes don't introduce unnecessary complexity
- [ ] Migration path is clear and documented
- [ ] Testing strategy is considered for each change
- [ ] Performance implications are evaluated

additions from chatgpt:

Thanks for sharing the context and the legacy template. No new code or Copilot instructions will be provided until you explicitly request it.

Here’s a structured review of areas in that legacy PHP template that are ripe for **improvement or modernization** using Python libraries in the Python version of InvoicePlane:

---

### 🔧 **Area for Improvement #1: Templating Engine**

**Current (PHP):** Handwritten inline PHP with `echo`, interspersed logic, and hard-to-read conditionals.

**Recommended (Python):** Use a **template engine** like **Jinja2**.

#### Benefits:

* Separation of logic and presentation.
* Readable and maintainable templates.
* Inheritance (`base.html`, `invoice_gst.html`, etc.).
* Looping, conditionals, filters all in a Pythonic way.
* Easy to test, version, and extend.

---

### 📦 **Area for Improvement #2: HTML Escaping & Formatting**

**Current (PHP):**

* Custom `htmlsc()`, `format_currency()`, `format_amount()`, etc.

**Recommended (Python):**

* Use Jinja2's built-in escaping (`{{ var }}` auto-escapes).
* Formatters and filters can be added:

  * `{{ amount|currency }}` or `{{ tax_rate|percentage }}` via custom filters.

---

### 🌐 **Area for Improvement #3: Internationalization (i18n)**

**Current (PHP):**

* Uses `_trans()` for string translations.

**Recommended (Python):**

* Use **Babel** or **gettext** with Jinja2 integration for `_()` or `trans()` style translation.
* Allows locale-aware date and number formatting too.

---

### 💳 **Area for Improvement #4: Currency, Date, Number Formatting**

**Current (PHP):**

* Manual formatting via `format_currency()` and `date_from_mysql()`.

**Recommended (Python):**

* Use **Babel** for:

  * `format_currency(value, currency="AUD", locale="en_AU")`
  * `format_date(date, locale="en_AU")`
* Keeps formatting consistent and localized.

---

### 🧩 **Area for Improvement #5: Document Structure and Reusability**

**Current (PHP):**

* One massive PHP file with repeated layout blocks.

**Recommended (Python):**

* Jinja2 template inheritance:

  * Base layout (`base_invoice.html`)
  * Block overrides for AU GST version (`invoice_au_gst.html`)
  * Shared partials: `client_info.html`, `company_info.html`, `item_row.html`, etc.

---

### 📄 **Area for Improvement #6: Static Assets & CSS**

**Current (PHP):**

* Dynamically loads styles via PHP logic: `base_url()`, `get_setting()`.

**Recommended (Python):**

* Serve CSS with `url_for('static', filename='css/templates.css')` in Flask.
* Static folder structure for themes:

  ```
  static/
    invoiceplane/
      css/
      img/
  ```

---

### 🧠 **Area for Improvement #7: Conditional Logic**

**Current (PHP):**

* Mix of `if`, `foreach`, and inline rendering.

**Recommended (Python):**

* Use clean Jinja2 logic:

  ```jinja2
  {% if invoice.client_address_1 %}
    <div>{{ invoice.client_address_1 }}</div>
  {% endif %}
  ```

---

### 🧾 **Area for Improvement #8: Custom Fields & Metadata**

**Current (PHP):**

* `custom_fields['client']['Company Name']`

**Recommended (Python):**

* Pass structured dictionaries or objects to the template.
* Access them via Jinja like `invoice.custom_fields.client["Company Name"]`.

---

### 🧪 **Area for Improvement #9: Template Testing**

**Current (PHP):** Testing the rendered output is hard.

**Recommended (Python):**

* Use **pytest + Jinja2** to write tests for rendered invoices with sample data.
* Snapshot testing is possible with tools like **pytest-regressions**.

---

Would you like to proceed with any of these areas in more detail? Or say “please” when you’re ready for suggested implementation code or Copilot instructions.
