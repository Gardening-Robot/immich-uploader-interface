# ⚡ Quick Start Guide

## For Users (Just Want to Use It)

### If you have the .exe file:

1. **Double-click** `ImmichUploader.exe`
2. **Enter** your Immich server details:
   - Server URL: `http://your-pi-ip:2283/api`
   - API Key: Get from Immich Settings → API Keys
3. **Click** "Connect to Immich"
4. **Browse** for folders to upload
5. **Click** "Start Upload"

**Done!** No installation needed.

---

## For Developers (Want to Build It)

### Step 1: Install Python

Download from: https://www.python.org/

⚠️ **Windows users**: Check "Add Python to PATH" during installation

### Step 2: Build

**Windows:**
```
Double-click: build-windows.bat
```

**Mac/Linux:**
```bash
chmod +x build.sh
./build.sh
```

### Step 3: Get Your Executable

Find it in the `dist/` folder:
- Windows: `ImmichUploader.exe`
- Mac: `ImmichUploader.app`
- Linux: `ImmichUploader`

### Step 4: Share

Copy that file anywhere. It runs standalone with **zero dependencies**.

---

## That's It!

🎯 **The executable is completely standalone**
- No Node.js needed
- No npm needed  
- No Immich CLI needed
- No dependencies at all

Just Python to build it, then the .exe works everywhere.

---

## Troubleshooting

**Windows Defender blocks the file?**
→ Click "More info" → "Run anyway"

**"Python not found" when building?**
→ Install Python from python.org

**"Connection failed" when using the app?**
→ Check your server URL ends with `/api`
→ Verify your API key is correct

---

**Full documentation in README.md**
