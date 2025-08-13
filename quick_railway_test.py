import requests

print("Testing Railway deployment...")
try:
    r = requests.get('https://intellisustain-production.up.railway.app/health', timeout=10)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Response: {data}")
    else:
        print(f"Error: {r.text}")
except Exception as e:
    print(f"Error: {e}")
