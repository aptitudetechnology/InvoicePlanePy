import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import os
import sys # Import sys for exiting if login fails
import time # For the timestamp in notes

# --- Configuration ---
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080") # Use env var or default
QUOTE_ID_TO_TEST = 74               # Replace with an actual quote ID from your database

# Authentication Configuration (copied from comprehensive-tax-rate-api-test.py)
USERNAME = os.environ.get("USERNAME", "admin") # Use env var or default
PASSWORD = os.environ.get("PASSWORD", "admin123") # Use env var or default

# --- Helper function to extract form data from HTML ---
def extract_form_data(html_content, quote_id):
    """
    Parses the HTML content of the quote edit page and extracts form data.
    This function is designed to mimic how a browser would submit the form.
    It now takes quote_id as an argument for more dynamic form finding.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # Look for the form that posts to the specific quote edit URL
    form = soup.find('form', {'action': f'/quotes/{quote_id}/edit', 'method': 'post'})

    if not form:
        # Also try to find a form that just has method post and look for relevant inputs
        # This can be a fallback if action attribute is relative or missing from exact match
        form = soup.find('form', {'method': 'post'})
        if form and not form.find('input', {'name': 'quote_number'}): # Basic check to ensure it's a quote form
             form = None # Not the form we're looking for

    if not form:
        print(f"Error: Could not find the form for quote ID {quote_id} on the page.")
        return None

    form_data = {}

    # Extract all input, select, and textarea elements
    for element in form.find_all(['input', 'select', 'textarea']):
        name = element.get('name')
        if not name:
            continue

        if element.name == 'input':
            input_type = element.get('type')
            if input_type == 'checkbox':
                # Checkboxes are only sent if checked. If not checked, don't include them
                # or set them to a value that signifies "off" like "False" or ""
                # For this test, we'll mimic browser behavior: send value if checked.
                if element.get('checked'): # 'checked' attribute usually means it's checked
                    form_data[name] = element.get('value', 'on') # Default 'on' if no value
                else:
                    # If you need to explicitly send 'false' for unchecked, add it here
                    # For many forms, unchecked checkboxes are simply omitted from POST data
                    pass
            elif input_type == 'radio':
                if element.get('checked'):
                    form_data[name] = element.get('value', '')
            elif input_type == 'file':
                # Skip file inputs as we don't upload files in this test
                continue
            else:
                form_data[name] = element.get('value', '')
        elif element.name == 'select':
            selected_option = element.find('option', selected=True)
            if selected_option:
                form_data[name] = selected_option.get('value', '')
            else:
                # If no option is explicitly selected, take the first option's value
                # This mimics browser behavior for many forms
                first_option = element.find('option')
                if first_option:
                    form_data[name] = first_option.get('value', '')
        elif element.name == 'textarea':
            form_data[name] = element.text.strip()

    return form_data

# --- Main Test Script ---
def test_quote_edit_process(session: requests.Session):
    edit_url = urljoin(BASE_URL, f'/quotes/{QUOTE_ID_TO_TEST}/edit')
    view_url = urljoin(BASE_URL, f'/quotes/{QUOTE_ID_TO_TEST}') # URL to verify changes

    print(f"--- Testing Quote Edit Process for Quote ID: {QUOTE_ID_TO_TEST} ---")
    print(f"Edit URL: {edit_url}")

    # Step 1: Fetch the current quote edit page to get initial form data
    print("\n1. Fetching current quote data from edit page...")
    try:
        response_get = session.get(edit_url) # Use the authenticated session
        response_get.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"GET Request successful. Status Code: {response_get.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote edit page: {e}")
        return

    initial_form_data = extract_form_data(response_get.text, QUOTE_ID_TO_TEST)

    if not initial_form_data:
        print("Failed to extract initial form data. Exiting.")
        return

    print("Initial form data extracted (partial view):")
    # Print a few key fields to confirm extraction
    print(f"  Quote Number: {initial_form_data.get('quote_number')}")
    print(f"  Status: {initial_form_data.get('status')}")
    print(f"  Notes (initial): '{initial_form_data.get('notes', '')[:50]}...'") # Show first 50 chars of notes

    # Step 2: Modify some fields for the POST request
    modified_form_data = initial_form_data.copy()

    # Example modifications:
    # 1. Change the notes field
    # Ensure current time is formatted for string, not raw float
    new_notes = f"This is an automated test note added at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}. Original notes: {initial_form_data.get('notes', '')}"
    modified_form_data['notes'] = new_notes

    # 2. Modify the quantity of the first item (if items exist)
    # This requires careful handling of the 'items[index][field]' naming convention
    # We need to find the existing item inputs and modify them.
    # For simplicity, let's just assume we want to modify the first item's quantity.
    # A more robust script would iterate through all items.

    # Identify existing item fields and update them
    item_index = 0
    item_modified = False
    while True:
        item_name_key = f'items[{item_index}][name]'
        if item_name_key in modified_form_data:
            # Modify quantity of the first item found
            current_quantity_str = modified_form_data.get(f'items[{item_index}][quantity]', '0')
            try:
                current_quantity = float(current_quantity_str)
            except ValueError:
                current_quantity = 0.0 # Default if current quantity is not a valid number

            modified_form_data[f'items[{item_index}][quantity'] = str(current_quantity + 1) # Increment quantity
            print(f"  Modified item {item_index} quantity to: {modified_form_data[f'items[{item_index}][quantity]']}")
            item_modified = True
            break # Only modify the first item for this test
        else:
            # If no items are found, or we've iterated past existing items, break
            if item_index == 0:
                print("No existing quote items found to modify quantity.")
            break
        item_index += 1


    print("\n2. Preparing modified data for POST request...")
    print(f"  New Notes: '{modified_form_data.get('notes', '')[:50]}...'")
    if item_modified:
        print(f"  New Quantity for item 0: {modified_form_data.get('items[0][quantity]')}")


    # Step 3: Send the POST request with modified data
    print(f"\n3. Sending POST request to {edit_url}...")
    try:
        response_post = session.post(edit_url, data=modified_form_data) # Use the authenticated session
        response_post.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"POST Request completed. Status Code: {response_post.status_code}")

        # Check for redirects, which usually indicate success
        if response_post.history:
            print(f"  Redirected from {response_post.history[0].url} to {response_post.url}")
            print("  This often indicates a successful form submission and redirect.")
        else:
            print("  No redirect observed. Check response content for success/failure.")

        # Print response content (useful for debugging if not redirecting)
        print("\nPOST Response Content (first 500 characters):")
        print(response_post.text[:500])

    except requests.exceptions.RequestException as e:
        print(f"Error during POST request: {e}")
        if e.response:
            print(f"  Response Status Code: {e.response.status_code}")
            print(f"  Response Content: {e.response.text}")
        return

    # Step 4: Verify the changes by fetching the quote page again
    print(f"\n4. Verifying changes by fetching {view_url}...")
    try:
        response_verify = session.get(view_url) # Use the authenticated session
        response_verify.raise_for_status()
        print(f"Verification GET Request successful. Status Code: {response_verify.status_code}")

        # Parse the page to find the updated notes and item quantity
        soup_verify = BeautifulSoup(response_verify.text, 'html.parser')

        # Check notes - Notes might be displayed in a textarea or just as text
        # Try to find a textarea first, then fallback to general text if not found.
        notes_element = soup_verify.find('textarea', {'name': 'notes'})
        current_notes = ""
        if notes_element:
            current_notes = notes_element.text.strip()
        else:
            # Fallback: try to find the note content in a div/p/span based on common patterns
            # This is a generic approach; you might need to adjust based on your actual HTML structure
            potential_notes_div = soup_verify.find('div', class_='quote-notes') or soup_verify.find('p', class_='notes')
            if potential_notes_div:
                current_notes = potential_notes_div.get_text(separator=' ', strip=True)

        print(f"  Notes on page after edit: '{current_notes[:50]}...'")
        if new_notes in current_notes: # Check if our new note is part of the content
            print("  Notes update VERIFIED: The new note content is present.")
        else:
            print("  Notes update FAILED: The new note content is NOT present.")


        # Check item quantity (this is trickier as it's a value in an input)
        # We need to find the specific input for the modified item.
        # This assumes the item order doesn't change.
        if item_modified:
            item_quantity_input = soup_verify.find('input', {'name': f'items[0][quantity]'})
            if item_quantity_input:
                current_item_quantity = item_quantity_input.get('value')
                print(f"  Quantity of first item on page after edit: {current_item_quantity}")
                expected_quantity = modified_form_data.get(f'items[0][quantity]')
                if expected_quantity and current_item_quantity == expected_quantity:
                    print("  Item quantity update VERIFIED: Quantity matches expected value.")
                else:
                    print(f"  Item quantity update FAILED: Quantity '{current_item_quantity}' does not match expected '{expected_quantity}'.")
            else:
                print("  Could not find input for first item quantity on verification page.")
        else:
            print("  Skipping item quantity verification as no items were modified.")

    except requests.exceptions.RequestException as e:
        print(f"Error verifying changes: {e}")
        if e.response:
            print(f"  Response Status Code: {e.response.status_code}")
            print(f"  Response Content: {e.response.text}")

    print("\n--- Test Complete ---")

if __name__ == "__main__":
    print("--- Starting Quote Edit Process Test ---")
    print(f"Base URL: {BASE_URL}")
    print(f"Username: {USERNAME}")
    print("---------------------------------------")

    # Create session to handle cookies and authentication
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'QuoteEditProcessTester/1.0' # Custom User-Agent for clarity in logs
    })

    print("🔐 Attempting to log in...")

    # Try common login endpoints (as seen in your tax rate script)
    login_endpoints = [
        "/auth/login",
        "/login",
        "/api/auth/login"
    ]

    login_success = False
    for endpoint in login_endpoints:
        try:
            login_url = urljoin(BASE_URL, endpoint)
            print(f"   Trying login endpoint: {login_url}")

            login_data = {"username": USERNAME, "password": PASSWORD}
            # Use 'data' for form-urlencoded (common for web logins)
            login_response = session.post(login_url, data=login_data, timeout=30)

            if login_response.status_code == 200:
                print(f"✅ Login successful via {endpoint}")
                login_success = True
                break # Exit loop on first successful login
            else:
                print(f"   ❌ Login failed for {endpoint}. Status: {login_response.status_code}. Response: {login_response.text[:200]}...")

        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error during login attempt to {endpoint}: {e}")
            if e.response:
                print(f"     Response Status Code: {e.response.status_code}")
                print(f"     Response Content: {e.response.text}")
        except Exception as e:
            print(f"   An unexpected error occurred during login attempt to {endpoint}: {e}")

    if not login_success:
        print("\n❌ Could not log in with any of the configured endpoints.")
        print("   Please check your BASE_URL, USERNAME, PASSWORD, and the application's login endpoint.")
        sys.exit(1) # Exit the script if login fails

    # If login was successful, proceed with the quote edit test
    test_quote_edit_process(session)