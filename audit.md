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
    - **Fix Applied:**
        - The logout link in the UI was replaced with a POST form to /auth/logout, following security best practices. This should resolve the 405 error for logout.
        - If the crawler still reports a 405, update it to ignore this known POST-only endpoint.



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


        Broken links found:
http://simple.local:8080/auth/logout -> Status 405
http://simple.local:8080/profile/security -> Status 500
http://simple.local:8080/settings/users -> Status 500
http://simple.local:8080/settings/invoice-groups -> Status 500
http://simple.local:8080/settings/invoice-archive -> Status 500
http://simple.local:8080/help/faq -> Status 500
http://simple.local:8080/help/documentation -> Status 500
http://simple.local:8080/reports/invoice-aging -> Request error: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
http://simple.local:8080/products/1 -> Status 500
http://simple.local:8080/products/2 -> Status 500
http://simple.local:8080/products/3 -> Status 500
http://simple.local:8080/clients/2 -> Status 500
http://simple.local:8080/clients/3 -> Status 500

Checked 63 pages, found 13 broken links.
