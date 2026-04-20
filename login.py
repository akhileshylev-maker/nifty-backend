from kiteconnect import KiteConnect
import webbrowser

API_KEY = "chd1njoljnzyu2n6"
API_SECRET = "icmgyo7sz5yvs7nbtbqzffhbo8b7ei9z"   # ← Paste your secret

kite = KiteConnect(api_key=API_KEY)

print("Opening Zerodha login...")
webbrowser.open(kite.login_url())

request_token = input("\nAfter login, paste the 'request_token' from URL here: ").strip()

try:
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    token = data["access_token"]
    
    with open("kite_access_token.txt", "w") as f:
        f.write(token)
    
    print("\n✅ Token saved successfully!")
    print("You can now deploy/update the backend.")
except Exception as e:
    print(f"Error: {e}")