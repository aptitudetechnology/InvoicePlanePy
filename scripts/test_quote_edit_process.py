import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

# --- Configuration ---
BASE_URL = "http://localhost:8080"  # Replace with your application's base URL
QUOTE_ID_TO_TEST = 74               # Replace with an actual quote ID from your database

# --- Helper function to extract form data from HTML ---
def extract_form_data(html_content):
    """
    Parses the HTML content of the quote edit page and extracts form data.
    This function is designed to mimic how a browser would submit the form.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    form = soup.find('form', {'action': f'/quotes/{QUOTE_ID_TO_TEST}/edit', 'method': 'post'})

    if not form:
        print(f"Error: Could not find the form for quote ID {QUOTE_ID_TO_TEST} on the page.")
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
                form_data[name] = element.get('value') if element.get('checked') else ''
            elif input_type == 'radio':
                if element.get('checked'):
                    form_data[name] = element.get('value')
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
                # Default to first option if nothing selected
                first_option = element.find('option')
                if first_option:
                    form_data[name] = first_option.get('value', '')
        elif element.name == 'textarea':
            form_data[name] = element.text.strip()

    return form_data

# --- Main Test Script ---
def test_quote_edit_process():
    edit_url = urljoin(BASE_URL, f'/quotes/{QUOTE_ID_TO_TEST}/edit')
    view_url = urljoin(BASE_URL, f'/quotes/{QUOTE_ID_TO_TEST}') # URL to verify changes

    print(f"--- Testing Quote Edit Process for Quote ID: {QUOTE_ID_TO_TEST} ---")
    print(f"Edit URL: {edit_url}")

    session = requests.Session() # Use a session to maintain cookies if needed

    # Step 1: Fetch the current quote edit page to get initial form data
    print("\n1. Fetching current quote data from edit page...")
    try:
        response_get = session.get(edit_url)
        response_get.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"GET Request successful. Status Code: {response_get.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote edit page: {e}")
        return

    initial_form_data = extract_form_data(response_get.text)

    if not initial_form_data:
        print("Failed to extract initial form data. Exiting.")
        return

    print("Initial form data extracted (partial view):")
    # Print a few key fields to confirm extraction
    print(f"  Quote Number: {initial_form_data.get('quote_number')}")
    print(f"  Status: {initial_form_data.get('status')}")
    print(f"  Notes (initial): '{initial_form_data.get('notes')[:50]}...'") # Show first 50 chars of notes

    # Step 2: Modify some fields for the POST request
    modified_form_data = initial_form_data.copy()

    # Example modifications:
    # 1. Change the notes field
    new_notes = f"This is an automated test note added at {requests.utils.to_native_string(requests.utils.time.time())}. Original notes: {initial_form_data.get('notes', '')}"
    modified_form_data['notes'] = new_notes

    # 2. Modify the quantity of the first item (if items exist)
    # This requires careful handling of the 'items[index][field]' naming convention
    # We need to find the existing item inputs and modify them.
    # For simplicity, let's just assume we want to modify the first item's quantity.
    # A more robust script would iterate through all items.
    
    # Identify existing item fields and update them
    item_index = 0
    while True:
        item_name_key = f'items[{item_index}][name]'
        if item_name_key in modified_form_data:
            # Modify quantity of the first item found
            current_quantity = float(modified_form_data.get(f'items[{item_index}][quantity]', 0))
            modified_form_data[f'items[{item_index}][quantity]'] = str(current_quantity + 1) # Increment quantity
            print(f"  Modified item {item_index} quantity to: {modified_form_data[f'items[{item_index}][quantity]']}")
            break # Only modify the first item for this test
        else:
            # If no items are found, or we've iterated past existing items, break
            # This handles cases where there might be no items initially
            if item_index == 0:
                print("No existing quote items found to modify quantity.")
            break
        item_index += 1


    print("\n2. Preparing modified data for POST request...")
    print(f"  New Notes: '{modified_form_data.get('notes')[:50]}...'")

    # Step 3: Send the POST request with modified data
    print(f"\n3. Sending POST request to {edit_url}...")
    try:
        response_post = session.post(edit_url, data=modified_form_data)
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
        response_verify = session.get(view_url)
        response_verify.raise_for_status()
        print(f"Verification GET Request successful. Status Code: {response_verify.status_code}")

        # Parse the page to find the updated notes and item quantity
        soup_verify = BeautifulSoup(response_verify.text, 'html.parser')

        # Check notes
        notes_element = soup_verify.find('textarea', {'name': 'notes'})
        if notes_element:
            current_notes = notes_element.text.strip()
            print(f"  Notes on page after edit: '{current_notes[:50]}...'")
            if new_notes in current_notes: # Check if our new note is part of the content
                print("  Notes update VERIFIED: The new note content is present.")
            else:
                print("  Notes update FAILED: The new note content is NOT present.")
        else:
            print("  Could not find notes textarea on verification page.")

        # Check item quantity (this is trickier as it's a value in an input)
        # We need to find the specific input for the modified item.
        # This assumes the item order doesn't change.
        item_quantity_input = soup_verify.find('input', {'name': f'items[0][quantity]'})
        if item_quantity_input:
            current_item_quantity = item_quantity_input.get('value')
            print(f"  Quantity of first item on page after edit: {current_item_quantity}")
            expected_quantity = modified_form_data.get(f'items[0][quantity]')
            if expected_quantity and current_item_quantity == expected_quantity:
                print("  Item quantity update VERIFIED: Quantity matches expected value.")
            else:
                print("  Item quantity update FAILED: Quantity does not match expected value.")
        else:
            print("  Could not find input for first item quantity on verification page.")


    except requests.exceptions.RequestException as e:
        print(f"Error verifying changes: {e}")
        if e.response:
            print(f"  Response Status Code: {e.response.status_code}")
            print(f"  Response Content: {e.response.text}")

    print("\n--- Test Complete ---")

if __name__ == "__main__":
    test_quote_edit_process()
