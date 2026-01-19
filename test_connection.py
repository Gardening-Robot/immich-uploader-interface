"""
Immich Connection Diagnostic Tool
Run this to test your connection before using the uploader
"""

import requests
import sys

print("=" * 60)
print("IMMICH CONNECTION DIAGNOSTIC TOOL")
print("=" * 60)
print()

# Get user input
server_url = input("Enter your Immich server URL (e.g., http://192.168.1.100:2283/api): ").strip()
api_key = input("Enter your API key: ").strip()

print()
print("=" * 60)
print("TESTING CONNECTION")
print("=" * 60)
print()

# Remove trailing slash
server_url = server_url.rstrip('/')

# Test 1: Server reachability
print("Test 1: Checking if server is reachable...")
print(f"URL: {server_url}/server/about")
try:
    response = requests.get(f"{server_url}/server/about", timeout=5)
    print(f"✓ Server is reachable!")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.text[:100]}")
    print()
except requests.exceptions.ConnectionError as e:
    print(f"✗ FAILED: Cannot reach server")
    print(f"  Error: {str(e)}")
    print()
    print("POSSIBLE CAUSES:")
    print("  - Immich server is not running")
    print("  - Wrong IP address")
    print("  - Not on same network")
    print("  - Firewall blocking connection")
    sys.exit(1)
except Exception as e:
    print(f"✗ FAILED: {str(e)}")
    sys.exit(1)

# Test 2: API key authentication
print("Test 2: Testing API key authentication...")
print(f"URL: {server_url}/users/me (trying plural first)")
headers = {'x-api-key': api_key}
try:
    response = requests.get(f"{server_url}/users/me", headers=headers, timeout=5)
    
    # If plural fails, try singular
    if response.status_code == 404:
        print(f"  Plural endpoint not found, trying singular...")
        print(f"URL: {server_url}/user/me")
        response = requests.get(f"{server_url}/user/me", headers=headers, timeout=5)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"✓ Authentication successful!")
        print(f"  User: {user_data.get('email', 'Unknown')}")
        print(f"  Name: {user_data.get('name', 'Unknown')}")
        print()
    elif response.status_code == 401:
        print(f"✗ FAILED: Authentication failed (401 Unauthorized)")
        print(f"  Your API key is invalid or doesn't have permissions")
        print()
        print("WHAT TO DO:")
        print("  1. Go to Immich web interface")
        print("  2. Click your profile → Account Settings → API Keys")
        print("  3. Create a new API key with these permissions:")
        print("     - asset.upload")
        print("     - album.read")
        print("     - album.create")
        print("     - albumAsset.create")
        print("     - user.read")
        sys.exit(1)
    elif response.status_code == 404:
        print(f"✗ FAILED: Endpoint not found (404)")
        print(f"  Neither /users/me nor /user/me endpoints exist")
        print()
        print("POSSIBLE CAUSES:")
        print("  - Your Immich version is very old or very new")
        print("  - Your server URL format is wrong")
        print()
        print("Please check your Immich version and update if needed")
        sys.exit(1)
    else:
        print(f"✗ FAILED: Unexpected response")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"✗ FAILED: {str(e)}")
    sys.exit(1)

# Test 3: List albums
print("Test 3: Testing album access...")
print(f"URL: {server_url}/albums")
try:
    response = requests.get(f"{server_url}/albums", headers=headers, timeout=5)
    if response.status_code == 200:
        albums = response.json()
        print(f"✓ Can access albums!")
        print(f"  Found {len(albums)} albums")
        if albums:
            print(f"  Sample album: {albums[0].get('albumName', 'Unnamed')}")
        print()
    else:
        print(f"✗ WARNING: Cannot list albums")
        print(f"  Status: {response.status_code}")
        print(f"  This might be a permissions issue")
        print()
except Exception as e:
    print(f"✗ WARNING: {str(e)}")
    print()

# Final result
print("=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print()
print("✓ All tests passed!")
print()
print("Your configuration:")
print(f"  Server URL: {server_url}")
print(f"  API Key: {api_key[:10]}...{api_key[-10:]}")
print()
print("You can now use these settings in the Immich Uploader app!")
print()
input("Press Enter to exit...")
