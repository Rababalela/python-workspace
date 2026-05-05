# GEOLOCTION TRACKER
#from dataclasses import field
#from unittest import result

import requests
import json
import os
from datetime import datetime

API_URL = "https://ip-api.com/json/"
SAVE_FILE = "geolocation_data.json"

# helpers
def separator(title = ""):
    width = 52
    if title:
        print(f"\n {'_' * 5} {title} {'_' * (width - len(title) - 7)}")
    else:
        print("_" * width)

def load_history():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(history):
    result = load_history()
    result.append(history)
    with open(SAVE_FILE, "w") as f:
        json.dump(result, f, indent = 2)

# core - fetch geoloction
def fetch_loction(ip="" ):
    """
    Fetch geolaction data for given ip address.
    If ip is empty, the API returns data for the caller's location( IP address).
    """

    URL = API_URL + ip if ip else API_URL
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "fail":
            print(f"\n Look up failed : {data['message','unknown error']}")
            return None
        return data
    except requests.exceptions.RequestException:
        print(f"\n No internet connection. Please check your internet connection.")
        return None
    except requests.exceptions.Timeout as e:
        print(f"\n Request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"\n Request error: {e}")
        return None

def display_history(data, ip_input=""):
    separator("Geolocation History")
    fields = [
        ("IP Address",  data.get("query","N/A")),
        ("City",  data.get("city","N/A")),
        ("Country", f"{data.get("country","N/A")}({data.get("countrycode","")})"),
        ("Region", data.get("regionNAME","N/A")),
        ("Timezone", data.get("timezone","N/A")),
        ("ISP", data.get("isp","N/A")),
        ("Zip Code", data.get("zipCode","N/A")),
        ("latitude", str(data.get("lat","N/A"))),
        ("longitude", str(data.get("lon","N/A"))),
    ]

    for label, value in fields:
        print(f"{label: < 16} : {value}")

    # Google maps link
    lat = data.get("lat","N/A")
    lon = data.get("lon","N/A")
    if lat and lon:
        separator()
        print(f"Google Maps: https://maps.google.com/maps?q={lat},{lon}")
    separator()

    # menu
def lookup_own_IP():
    separator("My IP Address")
    print(" Fetching  your public IP address")
    data = fetch_loction()
    if data:
        display_history(data)
        save_history({**data, "looked up at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        print(f" Result saved to {SAVE_FILE}")

def looked_custom_IP():
    separator("Custom IP Address")
    ip = input(" Enter IP address: ").strip()
    if not ip:
        print(" No  IP address entered")
        return
    print(f"\n Fetching loction for {ip}....")
    data = fetch_loction(ip)
    if data:
        display_history(data, ip)
        save_history({**data, "looked_up_at": datatime.now().strftime("%Y-%m-%d %H:%M:%S")})
        print(f" Result saved to {SAVE_FILE}")

def lookup_multiple():
    separator("Bulk IP Address")
    print(" Enter IP addresses one per line ")
    print(" Press Enter on empty line when done.\n ")

    ips = []
    while True:
        ip = input(" Enter IP address: ").strip()
        if not ip:
            break
        ips.append(ip)
    if not ips:
        print(" No  IP addresses entered")
        return
    for ip in ips:
        print(f"\n Fetching loction for {ip}....")
        data = fetch_loction(ip)
        if data:
            display_history(data)
            save_history({**data, "looked_up_at":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

def view_history():
    separator("Lookup History")
    result = load_history()
    if not result:
        print(" No results found")
        return
    print(f" {'#': < 4} {'IP': < 18} {'City': < 16} {'Country': < 20 } {'Looked up'}")
    separator()
    for i, r in enumerate(result, 1):
        print(f" {1: < 4 } {r.get('query','N/A'): < 18} {r.get('city', 'N/A'): < 16}"
            f"{r.get('Country','N/A'): < 20} {r.get('Looked_up_at','N/A')}")

def clear_history():
    separator("Clear History")
    confirm = input(" Are you sure you want to clear all history data? (y/n) ").strip().lower()
    if confirm == "y":
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        print(" History cleared")
    else:
        print(" Cancelled")

# main menu
def main():
    print("\n" + "=" * 52)
    print ("            GEOLOCATION TRACKER ")
    print("=" * 52)

    menu = {
        "1": ("lookup_own_IP",  lookup_own_IP),
        "2": ("lookup_multiple", lookup_multiple),
        "3": ("looked_custom_IP", looked_custom_IP),
        "4": ("view_history", view_history),
        "5": ("clear_history", clear_history),
        "6": ("exit", None)

    }
    while True:
        print("\n What would you like to do?")
        for key, (label, _) in menu.items():
            print(f" [{key}] {label}")

        choice = input(" > ").strip().lower()
        if choice == "6":
            print("Goodbye")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print(" Invalid choice. Entey 1-6")

if __name__ == "__main__":
    main()