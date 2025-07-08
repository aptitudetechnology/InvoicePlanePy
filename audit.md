# Web Application Link Audit Report

## Summary
This report details broken links identified during an automated crawl of the InvoicePlanePy application. Issues are categorized by HTTP status code, with a proposed fix plan for each.

## Broken Links by Category

### Status 404: Not Found
These links point to resources that the server could not find.

* **Link:** [URL]
    * **Reason:** Status 404
    * **Proposed Fix Plan:**
        1.  **Verify URL:** Double-check the exact URL in the application's source code (e.g., HTML templates, JavaScript). Correct any typos.
        2.  **Route Definition:** Confirm that a corresponding route or endpoint exists in the backend application (e.g., in Flask/Django `routes.py`, PHP routing files). If not, create the necessary route.
        3.  **Resource Existence:** Ensure the underlying resource (e.g., a specific page, file, or data) that the endpoint is supposed to serve actually exists.
        4.  **Redirection/Removal:** If the page is intentionally removed or moved, implement a 301 (Permanent Redirect) or remove the link from the UI.
        5.  **Testing:** After implementing the fix, re-run the `test_links.py` script to confirm the 404 is resolved.

### Status 405: Method Not Allowed
These links are accessible, but the HTTP method used (GET by the crawler) is not permitted for the resource.

* **Link:** [URL]
    * **Reason:** Status 405
    * **Proposed Fix Plan:**
        1.  **Understand Endpoint Purpose:** For a `logout` endpoint, `GET` requests are typically disallowed to prevent CSRF. The application likely expects a `POST` request.
        2.  **Crawler Adjustment (Optional):** If the goal is to specifically test `POST` endpoints, the crawler's logic would need to be extended to send `POST` requests with appropriate data/CSRF tokens.
        3.  **UI/Backend Review:** Confirm that the UI correctly triggers `POST` requests for actions like logout. Ensure the backend correctly enforces method restrictions.
        4.  **Documentation:** If this is expected behavior for the crawler, consider adding a note or a filter to the crawler to ignore 405s for specific known endpoints.
        5.  **Testing:** Manually test the logout functionality in the browser to ensure it works as expected.

### Status 500: Internal Server Error
These indicate a generic server-side issue, meaning something went wrong when the server tried to process the request for the page.

* **Link:** [URL]
    * **Reason:** Status 500
    * **Proposed Fix Plan:**
        1.  **Check Server Logs:** This is the most critical first step. Access the server logs of the InvoicePlanePy application (e.g., `apache2/error.log`, `nginx/error.log`, or application-specific logs). The logs will contain detailed traceback information about the error.
        2.  **Reproduce Manually:** Visit the problematic URL in a web browser while logged in to the application. Observe if the error occurs consistently and if any specific error message is displayed in the browser.
        3.  **Code Review:** Based on the server logs, identify the relevant code section causing the error. Look for:
            * Unhandled exceptions (e.g., division by zero, `None` object access).
            * Database connection issues or incorrect queries.
            * Missing dependencies or configuration errors.
            * Permission issues on files or directories.
        4.  **Debugging:** Use a debugger or add print statements to trace the execution flow leading to the error.
        5.  **Fix and Test:** Implement the code fix, restart the application if necessary, and re-run `test_links.py` to confirm the 500 error is resolved. Also, perform manual regression testing on the affected functionality.


## Detailed Broken Links and Proposed Fixes

### Status 405: Not Allowed

- **http://simple.local:8080/auth/logout**
    - **Reason:** Status 405 (Method Not Allowed)
    - **Proposed Fix:**
        - This is likely a POST-only endpoint for security. Ensure the UI uses a POST (form or AJAX) for logout, not a GET link. Update the crawler to ignore this link or handle POST if you want to test it.

### Status 404: Not Found

- **http://simple.local:8080/settings/quote-settings**
- **http://simple.local:8080/settings/email**
- **http://simple.local:8080/settings/online-payment**
- **http://simple.local:8080/settings/projects**
- **http://simple.local:8080/settings/updates**
- **http://simple.local:8080/reports/invoice-aging**
- **http://simple.local:8080/products/1/edit**
- **http://simple.local:8080/products/2/edit**
- **http://simple.local:8080/products/3/edit**
- **http://simple.local:8080/clients/4/edit**
    - **Proposed Fix:**
        1. Check if these routes are missing in your FastAPI router or backend. If so, implement the missing endpoints and templates.
        2. If these features are not yet implemented, consider hiding or disabling the links in the UI until they are ready.
        3. For edit/detail pages (e.g., `/products/1/edit`), ensure the resource exists in the database before generating the link.

### Status 500: Internal Server Error

- **http://simple.local:8080/profile/security**
- **http://simple.local:8080/settings/users**
- **http://simple.local:8080/settings/invoice-groups**
- **http://simple.local:8080/settings/invoice-archive**
- **http://simple.local:8080/help/faq**
- **http://simple.local:8080/help/documentation**
- **http://simple.local:8080/products/1**
- **http://simple.local:8080/products/2**
- **http://simple.local:8080/products/3**
- **http://simple.local:8080/clients/2**
- **http://simple.local:8080/clients/2/edit**
- **http://simple.local:8080/clients/3**
- **http://simple.local:8080/clients/3/edit**
    - **Proposed Fix:**
        1. Check your server logs for stack traces or error messages for each 500 error.
        2. Visit each URL manually to see if the error is consistent and to get more details.
        3. Common causes: missing database records, unhandled exceptions, missing templates, or permission errors.
        4. For resource detail/edit pages, ensure the resource exists in the database and the backend handles missing resources gracefully (return 404, not 500).
        5. Fix the code or data issues, then re-run the link audit.