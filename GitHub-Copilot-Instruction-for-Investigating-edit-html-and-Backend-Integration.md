GitHub Copilot Instruction for Investigating edit.html and Backend Integration

Goal:
Analyze the edit.html template and backend code to identify any attribute mismatches or transaction issues affecting data retrieval and updates for the quote with ID 75.

Steps for Copilot to assist:

    Scan edit.html template:

        Extract all form fields and their name attributes.

        Check if these names correspond exactly to the expected keys/attributes in the backend model or form processing logic.

        Identify any fields that might be missing or extra compared to the backend data model.

        Verify if input types (e.g., text, number, select) match expected data types in the backend.

    Analyze backend quote retrieval and update logic:

        Identify the SQLAlchemy model used for quotes.

        List all expected model attributes and their types.

        Check the view/controller handling GET /quotes/<id> and POST or PUT for updates.

        Look for any mismatches between submitted form data keys and model attribute names.

        Confirm if the transaction rollback on GET is expected (usually read-only, so rollback after query is normal).

        Investigate POST/PUT handlers for any commit or rollback behavior; identify why a rollback might be triggered (validation failure, exception, missing commit).

    Cross-check logs with code behavior:

        Correlate logged parameter {'param_1': 75} to query executed in the backend.

        Identify if this query corresponds to fetching or updating the quote.

        Check if any exceptions or errors precede or follow the rollback in the logs.

    Form validation and submission handling:

        Check for server-side validation errors that could cause rollback.

        Identify if any field data is transformed or sanitized before database update.

        Look for mismatches in expected data formats or missing required fields.

    Generate a report or list:

        Summary of matched vs unmatched form attributes.

        Possible causes of rollback based on backend code.

        Recommendations for template fixes or backend corrections.