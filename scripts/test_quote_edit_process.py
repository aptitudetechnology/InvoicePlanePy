import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "http://localhost:8080"
LOGIN_ENDPOINT = "/auth/login"
USERNAME = "admin"
PASSWORD = "admin"

QUOTE_ID = 74
EDIT_ENDPOINT = f"/quotes/{QUOTE_ID}/edit"
EDIT_URL = f"{BASE_URL}{EDIT_ENDPOINT}"

def extract_form_fields(html):
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form")
    fields = {}
    for input_tag in form.find_all(["input", "textarea", "select"]):
        name = input_tag.get("name")
        if not name:
            continue
        if input_tag.name == "textarea":
            value = input_tag.text or ""
        elif input_tag.name == "select":
            selected = input_tag.find("option", selected=True)
            value = selected["value"] if selected else ""
        else:
            value = input_tag.get("value", "")
        fields[name] = value
    return fields

def login(session):
    print("🔐 Attempting to log in...")
    login_url = BASE_URL + LOGIN_ENDPOINT
    resp = session.get(login_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    token = soup.find("input", {"name": "_token"})
    token_val = token["value"] if token else ""

    payload = {
        "_token": token_val,
        "username": USERNAME,
        "password": PASSWORD
    }
    r = session.post(login_url, data=payload, allow_redirects=True)
    if r.status_code == 200 and "dashboard" in r.url:
        print("✅ Login success via /auth/login")
        return True
    print("❌ Login failed")
    return False

def run_test():
    session = requests.Session()

    print("--- Starting Quote Edit Process Test ---")
    print(f"Base URL: {BASE_URL}")
    print(f"Username: {USERNAME}")
    print("---------------------------------------")

    if not login(session):
        return

    print(f"--- Testing Quote Edit Process for Quote ID: {QUOTE_ID} ---")
    print(f"Edit URL: {EDIT_URL}")

    print("\n1. Fetching current quote data from edit page...")
    r = session.get(EDIT_URL)
    if r.status_code != 200:
        print(f"❌ Failed to fetch quote edit page. Status: {r.status_code}")
        return
    print("GET successful. Status Code: 200")
    initial_form_data = extract_form_fields(r.text)
    print("Initial form data extracted (partial):")
    print(f"  Quote Number: {initial_form_data.get('quote_number', 'N/A')}")
    print(f"  Status: {initial_form_data.get('status', 'N/A')}")
    print(f"  Notes (initial): '{initial_form_data.get('notes', '')[:30]}...'")

    modified_form_data = initial_form_data.copy()

    # Auto-fill missing required fields
    today = time.strftime('%Y-%m-%d')
    future_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 7 * 86400))
    for date_field in ['quote_date', 'expires_at', 'invoice_date', 'valid_until']:
        if date_field in modified_form_data and modified_form_data[date_field] in [None, '', 'None']:
            modified_form_data[date_field] = future_date
            print(f"  Auto-filled missing date field '{date_field}' with: {future_date}")

    if 'discount_percentage' in modified_form_data and not modified_form_data['discount_percentage']:
        modified_form_data['discount_percentage'] = '0'
        print("  Auto-filled 'discount_percentage' with: 0")

    if 'quote_pdf_password' in modified_form_data and modified_form_data['quote_pdf_password'] in [None, 'None']:
        modified_form_data['quote_pdf_password'] = ''

    print("\n[Debug] Checking form for empty or suspicious fields...")
    for field in ['quote_pdf_password', 'valid_until', 'discount_percentage']:
        if modified_form_data.get(field) in [None, '', 'None']:
            print(f"  [Warning] Field '{field}' is empty or None")

    # Modify notes and items
    new_notes = f"[TEST] Updated via test script at {time.strftime('%Y-%m-%d %H:%M:%S')}"
    modified_form_data['notes'] = new_notes

    # Check for existing items or add a new one
    item_modified = False
    item_keys = [key for key in modified_form_data if key.startswith("items[") and key.endswith("[name]")]
    if item_keys:
        first_item = item_keys[0]
        modified_form_data[first_item] = "Updated test item name"
        item_index = first_item.split('[')[1].split(']')[0]
        modified_form_data[f"items[{item_index}][quantity]"] = "2"
        item_modified = True
    else:
        print("⚠️  No quote items found. Adding a dummy item for testing.")
        modified_form_data['items[0][name]'] = "Test Item"
        modified_form_data['items[0][description]'] = "Added via test script"
        modified_form_data['items[0][quantity]'] = "1"
        modified_form_data['items[0][price]'] = "50.00"
        modified_form_data['items[0][tax_rate_id]'] = "0"
        item_modified = True

    print("\n2. Sending POST request with modified form data...")
    try:
        post_resp = session.post(EDIT_URL, data=modified_form_data, allow_redirects=True)
        post_resp.raise_for_status()
        print(f"POST successful. Status Code: {post_resp.status_code}")
        if post_resp.history:
            print(f"  Redirected: {post_resp.history[0].url} → {post_resp.url}")
        print("\nPOST Response (first 500 chars):")
        print(post_resp.text[:500])
    except Exception as e:
        print(f"Error during POST: {e}")
        return

    # Optional: re-fetch to verify
    print(f"\n3. Verifying changes at {BASE_URL}/quotes/{QUOTE_ID}...")
    verify_resp = session.get(f"{BASE_URL}/quotes/{QUOTE_ID}")
    if verify_resp.status_code == 200:
        if new_notes in verify_resp.text:
            print("✅ Notes update verified successfully.")
        else:
            print("❌ Notes update FAILED.")
    print("\n--- Test Complete ---")

if __name__ == "__main__":
    run_test()
