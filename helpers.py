import json
import os
import random
import string
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def get_path(filename):
    return os.path.join(DATA_DIR, filename)

def load_json(filename):
    path = get_path(filename)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_json(filename, data):
    path = get_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_id(prefix, length=6):
    suffix = ''.join(random.choices(string.digits, k=length))
    return f"{prefix}{suffix}"

def format_currency(amount, store_mode):
    if store_mode == "international":
        return f"${amount:,.2f}"
    return f"PKR {amount:,.0f}"

def get_currency_symbol(store_mode):
    return "$" if store_mode == "international" else "PKR"

def get_tax_rate(store_mode):
    return 0.08 if store_mode == "international" else 0.17

def get_tax_label(store_mode):
    return "GST (8%)" if store_mode == "international" else "GST (17%)"

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def today_str():
    return datetime.now().strftime("%Y-%m-%d")

def authenticate(username, password):
    users = load_json("users.json")
    for u in users:
        if u["username"] == username and u["password"] == password:
            return u
    return None

def get_low_stock_threshold():
    return 5

def get_overstock_threshold():
    return 100
