import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import sys
import time

# --- Configuration ---
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")
QUOTE_ID_TO_TEST = 74
USERNAME = os.environ.get("USERNAME", "admin")
PASSWORD = os.environ.get("PASSWORD", "admin123")

def extract_form_data(html_content, quote_id):
    soup = BeautifulSoup(html_content, 'html.parser')
    form = soup.find('form', {'action': f'/quotes/{quote_id}/edit', 'method': 'post'}) \
           or soup.find('form', {'method': 'post'})

    if not form or not form.find('input', {'name': 'quote_number'}):
        print(f"Error: Could not find the form for quote ID {quote_id} on the page.")
        return None

    form_data = {}
    for element in form.find_all(['input', 'select', 'textarea']):
        name = element.get('name')
        if not name:
            continue

        if element.name == 'input':
            input_type = element.get('type')
            if input_type == 'checkbox':
                if element.get('checked'):
                    form_data[name] = element.get('value', 'on')
            elif input_type == 'radio':
                if element.get('checked'):
                    form_data[name] = element.get('value', '')
            elif input_type == 'file':
                continue
            else:
                form_data[name] = element.get('value', '')
        elif element.name == 'select':
            selected_option = element.find('option', selected=True)
            form_data[name] = selected_option.get('value', '') if selected_option else \
                              element.find('option').get('value', '') if element.find('option') else ''
        elif element.name == 'textarea':
            form_data[name] = element.text.strip()

    return form_data

def test_quote_edit_process(session: requests.Session):
    edit_url = urljoin(BASE_URL, f'/quotes/{QUOTE_ID_TO_TEST}/edit')
    view_url = urljoin(BASE_URL, f'/quotes/{QUOTE_ID_TO_TEST}')

    print(f"--- Testing Quote Edit Process for Quote ID: {QUOTE_ID_TO_TEST} ---")
    print(f"Edit URL: {edit_url}")

    print("\n1. Fetching current quote data from edit page...")
    try:
        response_get = session.get(edit_url)
        response_get.raise_for_status()
        print(f"GET successful. Status Code: {response_get.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote edit page: {e}")
        return

    initial_form_data = extract_form_data(response_get.text, QUOTE_ID_TO_TEST)
    if not initial_form_data:
        print("Failed to extract initial form data. Exiting.")
        return

    print("Initial form data extracted (partial):")
    print(f"  Quote Number: {initial_form_data.get('quote_number')}")
    print(f"  Status: {initial_form_data.get('status')}")
    print(f"  Notes (initial): '{initial_form_data.get('notes', '')[:50]}...'")

    modified_form_data = initial_form_data.copy()

    # Add a timestamped note
    new_notes = f"This is an automated test note added at {time.strftime('%Y-%m-%d %H:%M:%S')}. Original notes: {initial_form_data.get('notes', '')}"
    modified_form_data['notes'] = new_notes

    # Auto-fill missing or invalid date fields
    today = time.strftime('%Y-%m-%d')
    future_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 7 * 86400))

    for date_field in ['quote_date', 'expires_at', 'invoice_date', 'valid_until']:
        if date_field in modified_form_data:
            if modified_form_data[date_field] in [None, '', 'None']:
                modified_form_data[date_field] = future_date
                print(f"  Auto-filled missing date field '{date_field}' with: {future_date}")

    # Fill in optional fields with safe defaults
    if 'discount_percentage' in modified_form_data and modified_form_data['discount_percentage'] in [None, '', 'None']:
        modified_form_data['discount_percentage'] = '0'
        print(f"  Auto-filled 'discount_percentage' with: 0")

    if 'quote_pdf_password' in modified_form_data and modified_form_data['quote_pdf_password'] in [None, 'None']:
        modified_form_data['quote_pdf_password'] = ''
        print(f"  Auto-filled 'quote_pdf_password' with empty string")

    # Modify first item quantity (if present)
    item_index = 0
    item_modified = False
    while True:
        item_name_key = f'items[{item_index}][name]'
        quantity_key = f'items[{item_index}][quantity]'
        if item_name_key in modified_form_data:
            try:
                current_quantity = float(modified_form_data.get(quantity_key, '0'))
            except ValueError:
                current_quantity = 0
            modified_form_data[quantity_key] = str(current_quantity + 1)
            print(f"  Modified item {item_index} quantity to: {modified_form_data[quantity_key]}")
            item_modified = True
            break
        else:
            if item_index == 0:
                print("No existing quote items found to modify quantity.")
            break
        item_index += 1

    print("\n[Debug] Checking form for empty or suspicious fields...")
    for k, v in modified_form_data.items():
        if v in [None, '', 'None']:
            print(f"  [Warning] Field '{k}' is empty or None")

    print("\n2. Sending POST request with modified form data...")
    try:
        response_post = session.post(edit_url, data=modified_form_data)
        response_post.raise_for_status()
        print(f"POST successful. Status Code: {response_post.status_code}")
        if response_post.history:
            print(f"  Redirected: {response_post.history[0].url} → {response_post.url}")
        else:
            print("  No redirect detected after POST.")
        print("\nPOST Response (first 500 chars):")
        print(response_post.text[:500])
    except requests.exceptions.RequestException as e:
        print(f"Error during POST: {e}")
        if e.response:
            print(f"  Status Code: {e.response.status_code}")
            print(f"  Response: {e.response.text}")
        return

    print(f"\n3. Verifying changes at {view_url}...")
    try:
        response_verify = session.get(view_url)
        response_verify.raise_for_status()
        soup = BeautifulSoup(response_verify.text, 'html.parser')

        # Verify Notes
        notes_element = soup.find('textarea', {'name': 'notes'})
        current_notes = notes_element.text.strip() if notes_element else ""
        print(f"  Notes after edit: '{current_notes[:50]}...'")
        if new_notes in current_notes:
            print("  ✅ Notes update VERIFIED.")
        else:
            print("  ❌ Notes update FAILED.")

        # Verify item quantity
        if item_modified:
            item_input = soup.find('input', {'name': 'items[0][quantity]'})
            current_qty = item_input.get('value') if item_input else None
            expected_qty = modified_form_data.get('items[0][quantity]')
            print(f"  Item 0 Quantity: {current_qty}")
            if current_qty == expected_qty:
                print("  ✅ Item quantity VERIFIED.")
            else:
                print(f"  ❌ Quantity mismatch. Expected: {expected_qty}")
    except requests.exceptions.RequestException as e:
        print(f"Error verifying changes: {e}")
        if e.response:
            print(f"  Status Code: {e.response.status_code}")
            print(f"  Response: {e.response.text}")

    print("\n--- Test Complete ---")

if __name__ == "__main__":
    print("--- Starting Quote Edit Process Test ---")
    print(f"Base URL: {BASE_URL}")
    print(f"Username: {USERNAME}")
    print("---------------------------------------")

    session = requests.Session()
    session.headers.update({'User-Agent': 'QuoteEditProcessTester/1.0'})

    print("🔐 Attempting to log in...")

    login_endpoints = ["/auth/login", "/login", "/api/auth/login"]
    login_success = False

    for endpoint in login_endpoints:
        try:
            login_url = urljoin(BASE_URL, endpoint)
            print(f"   Trying: {login_url}")
            response = session.post(login_url, data={"username": USERNAME, "password": PASSWORD}, timeout=30)
            if response.status_code == 200:
                print(f"✅ Login success via {endpoint}")
                login_success = True
                break
            else:
                print(f"   ❌ Failed: Status {response.status_code} — {response.text[:100]}")
        except Exception as e:
            print(f"   ⚠️ Error during login: {e}")

    if not login_success:
        print("❌ Login failed. Check credentials and endpoints.")
        sys.exit(1)

    test_quote_edit_process(session)
