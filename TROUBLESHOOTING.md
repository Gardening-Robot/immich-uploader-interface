# Troubleshooting Guide

## Connection Issues

### Error: "404 Cannot GET /api/user/me" or similar 404 errors

This means your **server URL is formatted incorrectly**.

**✅ CORRECT URL Format (from official Immich CLI docs):**
```
http://192.168.1.216:2283/api
```

**The URL must:**
- Start with `http://` (or `https://`)
- Include your server's IP address and port
- End with `/api` (NO trailing slash after api)

**❌ WRONG - Common Mistakes:**

```
http://192.168.1.100:2283           ← Missing /api
http://192.168.1.100:2283/          ← Missing /api
http://192.168.1.100:2283/api/      ← Extra trailing slash (WRONG!)
http://192.168.1.100/api            ← Missing port :2283
https://192.168.1.100:2283/api      ← Using HTTPS (only if you configured it)
```

### How to Find Your Correct URL

1. **Open Immich in your web browser**
   - Example: `http://192.168.1.100:2283`
   
2. **Log in normally**

3. **Your API URL is the same, but add `/api` at the end:**
   - If web is: `http://192.168.1.100:2283`
   - Then API is: `http://192.168.1.100:2283/api`

4. **Test it in your browser:**
   - Go to: `http://192.168.1.100:2283/api/server/about`
   - You should see JSON data like:
     ```json
     {"version":"v1.120.0","versionUrl":"https://github.com/immich-app/immich/releases/tag/v1.120.0"}
     ```

### Error: "401 Unauthorized"

Your **API key is wrong or doesn't have permissions**.

**Fix:**
1. Go to Immich web interface
2. Click your profile → Account Settings → API Keys
3. Check if your key exists
4. If not, create a new one with these permissions:
   - `asset.upload`
   - `album.read`
   - `album.create`
   - `albumAsset.create`
   - `user.read`
5. Copy the FULL key (it's long!)
6. Paste it into the uploader

### Error: "Connection refused" or "Cannot connect"

Your **Immich server isn't running** or **network issue**.

**Fix:**
1. **Check if Immich is running:**
   - Can you open Immich in a web browser?
   - If not, start your Immich server
   
2. **Check your IP address:**
   - Make sure you're using the correct IP
   - On Raspberry Pi, run: `hostname -I`
   
3. **Check if you're on the same network:**
   - Computer and Raspberry Pi must be on same WiFi/network
   
4. **Check firewall:**
   - Make sure port 2283 isn't blocked

### Error: "SSL Certificate Error"

You're using **HTTPS** but certificate is self-signed.

**Fix:**
1. **Option 1:** Use HTTP instead of HTTPS
   - Change `https://...` to `http://...`
   
2. **Option 2:** Add certificate verification skip (advanced)

## Upload Issues

### Uploads start but fail immediately

**Possible causes:**
1. **Wrong file permissions** - Check if app can read the files
2. **Files too large** - Try smaller test folder first
3. **Network timeout** - Try uploading fewer files at once

### "Album not found" error

The album creation failed.

**Fix:**
1. Check your API key has `album.create` permission
2. Try creating album manually in Immich first
3. Then uncheck "Use folder name as album" and upload

### Uploads are VERY slow

This is **normal** for photos/videos over network!

**Tips:**
- Use wired Ethernet instead of WiFi
- Upload smaller batches
- Be patient - 1000 photos might take 30+ minutes

## App Won't Start

### Windows: "This app can't run on your PC"

You downloaded the wrong version.

**Fix:**
- Download the Windows version (ImmichUploader.exe)
- Not the Mac or Linux version

### Windows Defender blocks it

Common with unsigned executables.

**Fix:**
1. Click "More info"
2. Click "Run anyway"
3. Or add exception in Windows Defender

### Mac: "Cannot be opened because the developer cannot be verified"

macOS security blocks unsigned apps.

**Fix:**
1. Right-click the app
2. Click "Open"
3. Click "Open" again in the popup
4. Future launches will work normally

### Linux: "Permission denied"

File isn't executable.

**Fix:**
```bash
chmod +x ImmichUploader
./ImmichUploader
```

## API Key Issues

### Can't find API Keys in Immich

You might have an older version.

**Check:**
1. What Immich version are you running?
2. API Keys were added in v1.106.0
3. Update Immich if needed

### API key works in browser but not in app

The app might be using old credentials.

**Fix:**
1. Delete the config file:
   - Windows: `C:\Users\YourName\.immich_uploader_config.json`
   - Mac/Linux: `~/.immich_uploader_config.json`
2. Restart the app
3. Enter credentials again

## Still Having Issues?

### Enable Debug Mode

Edit the Python file and add logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show detailed error messages.

### Test Your Setup

Try these tests:

**Test 1: Can you reach the server?**
```bash
ping 192.168.1.100
```

**Test 2: Can you access the API?**
```bash
curl http://192.168.1.100:2283/api/server/about
```

**Test 3: Is your API key valid?**
```bash
curl -H "x-api-key: YOUR_API_KEY" http://192.168.1.100:2283/api/user/me
```

If Test 3 returns JSON with your user info, everything is configured correctly!

## Quick Checklist

Before asking for help, verify:

- [ ] Server URL ends with `/api` (no trailing slash)
- [ ] Can open Immich web interface in browser
- [ ] API key is copied correctly (no spaces)
- [ ] API key has required permissions
- [ ] Computer and server on same network
- [ ] Immich server is running
- [ ] Port 2283 isn't blocked by firewall

## Get Help

If none of this works:
1. Check Immich GitHub issues
2. Join Immich Discord
3. Include these details:
   - Immich version
   - Error message (exact text)
   - What you've tried
   - Server URL format (hide IP if sharing publicly)
