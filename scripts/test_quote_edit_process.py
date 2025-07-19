import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "http://localhost:8080"
LOGIN_ENDPOINT = "/auth/login"
USERNAME = "admin"
PASSWORD = "admin123"

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

    soup = BeautifulSoup(r.text, "html.parser")
    token_input = soup.find("input", {"name": "_token"})
    if token_input:
        initial_form_data["_token"] = token_input["value"]

    modified_form_data = initial_form_data.copy()
    today = time.strftime('%Y-%m-%d')
    future_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 7 * 86400))
    for date_field in ['issue_date', 'valid_until', 'quote_date', 'expires_at', 'invoice_date']:
        if date_field in modified_form_data and modified_form_data[date_field] in [None, '', 'None']:
            modified_form_data[date_field] = future_date
            print(f"  Auto-filled missing date field '{date_field}' with: {future_date}")

    # Ensure required core fields
    required_defaults = {
        'client_id': '1',
        'user_id': '1',
        'quote_number': f"QUO-{QUOTE_ID:04}",
        'status': 'draft',
        'currency_code': 'USD',
        'exchange_rate': '1',
        'discount_percentage': '0',
        'quote_pdf_password': ''
    }
    for k, v in required_defaults.items():
        if not modified_form_data.get(k):
            modified_form_data[k] = v
            print(f"  Defaulted required field '{k}' to: {v}")

    new_notes = f"[TEST] Updated via v2 script at {time.strftime('%Y-%m-%d %H:%M:%S')}"
    modified_form_data['notes'] = new_notes

    # Fix items in modified_form_data to match backend expected field names and types
    item_keys = [key for key in modified_form_data if key.startswith("items[") and key.endswith("[name]")]
    if item_keys:
        first_item = item_keys[0]
        item_index = first_item.split('[')[1].split(']')[0]

        # Update required fields
        modified_form_data[f"items[{item_index}][name]"] = "Updated test item name"
        modified_form_data[f"items[{item_index}][quantity]"] = "2"
        modified_form_data[f"items[{item_index}][price]"] = "100.00"  # example price

        # Rename tax_rate_id to tax_rate if present
        tax_rate_id_key = f"items[{item_index}][tax_rate_id]"
        tax_rate_key = f"items[{item_index}][tax_rate]"
        if tax_rate_id_key in modified_form_data:
            modified_form_data[tax_rate_key] = modified_form_data.pop(tax_rate_id_key)
        else:
            # If tax_rate not present, set default
            modified_form_data[tax_rate_key] = "0"

    else:
        print("⚠️  No quote items found. Adding a dummy item for testing.")
        modified_form_data['items[0][name]'] = "Test Item"
        modified_form_data['items[0][description]'] = "Added via script"
        modified_form_data['items[0][quantity]'] = "1"
        modified_form_data['items[0][price]'] = "50.00"
        modified_form_data['items[0][tax_rate]'] = "0"

    print("\n2. Sending POST request with modified form data...")
    try:
        post_resp = session.post(EDIT_URL, data=modified_form_data, allow_redirects=True)
        post_resp.raise_for_status()
        print("POST response status:", post_resp.status_code)
        print("POST response headers:", post_resp.headers)
        print("POST response content snippet:", post_resp.text[:500])  # print first 500 chars

        print(f"✅ POST successful. Status Code: {post_resp.status_code}")
        if post_resp.history:
            print(f"  Redirected: {post_resp.history[0].url} → {post_resp.url}")
            except requests.exceptions.HTTPError as e:
            print(f"❌ Error during POST: {e}")
            print("POST response status:", post_resp.status_code)
            print("POST response headers:", post_resp.headers)
            print("POST response content snippet:")
            print(post_resp.text[:1000])  # First 1000 chars of response body for debugging
        return


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
