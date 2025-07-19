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
    for date_field in ['quote_date', 'expires_at', 'invoice_date', 'valid_until']:
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

    new_notes = f"[TEST]_
