# 🍎 Immich Uploader for Mac (iMac)

## ✅ Yes, This Works on iMac!

This Python version runs perfectly on macOS. Here's everything you need to know.

## 🚀 Quick Start for Mac

### Step 1: Install Python (if not already installed)

Mac usually comes with Python, but let's make sure you have Python 3:

**Check if you have Python:**
```bash
python3 --version
```

If you see something like "Python 3.x.x", you're good! Skip to Step 2.

**If you need to install Python:**

**Option A: Official Installer (Easiest)**
1. Go to: https://www.python.org/downloads/macos/
2. Download the latest Python 3 installer
3. Open the .pkg file and follow the installer
4. Done!

**Option B: Homebrew (If you use it)**
```bash
brew install python3
```

### Step 2: Download the Project

Download and unzip `immich-uploader-python.zip` to your Downloads folder (or anywhere you like).

### Step 3: Build the Mac App

Open Terminal (Cmd+Space, type "Terminal", press Enter) and run:

```bash
# Navigate to the project folder
cd ~/Downloads/immich-uploader-python

# Make the build script executable
chmod +x build.sh

# Run the build script
./build.sh
```

**What happens:**
- Installs Python dependencies (takes ~1 minute)
- Builds the standalone app (takes ~2-5 minutes)
- Creates `dist/ImmichUploader` executable

### Step 4: Run Your App

After building:

```bash
# Run it from Terminal
./dist/ImmichUploader

# Or double-click the file in Finder
```

**First time you run it:**
- macOS will say "cannot be opened because it is from an unidentified developer"
- Right-click the app → Click "Open" → Click "Open" again
- This only needs to be done once

### Step 5: Use the App

1. Enter your Immich server URL: `http://your-raspberry-pi-ip:2283/api`
2. Enter your API key (from Immich Settings → API Keys)
3. Click "Connect to Immich"
4. Select folders to upload
5. Click "Start Upload"

Done! 🎉

## 📋 Full Build Instructions (Terminal Commands)

```bash
# 1. Go to the project folder
cd ~/Downloads/immich-uploader-python

# 2. Make build script executable (first time only)
chmod +x build.sh

# 3. Run the build
./build.sh

# 4. Run the app
./dist/ImmichUploader
```

## 🎯 Creating a Mac App Bundle (.app)

If you want a proper Mac app that you can put in Applications:

```bash
# After running the build script, run this:
pyinstaller --onefile --windowed --name "Immich Uploader" immich_uploader.py

# This creates: dist/Immich Uploader.app
# You can drag this to your Applications folder!
```

Then you can:
1. Open Finder
2. Go to `dist/` folder
3. Drag "Immich Uploader.app" to your Applications folder
4. Launch it from Applications like any other app!

## 💡 Tips for Mac Users

### Making it Easier to Launch

**Option 1: Add to Applications**
```bash
# After building
cp -r dist/ImmichUploader.app /Applications/
```

**Option 2: Create an Alias**
1. Right-click the app in Finder
2. Select "Make Alias"
3. Drag alias to Desktop or Dock

**Option 3: Add to Dock**
1. Open the app
2. Right-click its icon in Dock
3. Options → Keep in Dock

### Using with Apple Silicon (M1/M2/M3 Macs)

Everything works the same! Python and PyInstaller support Apple Silicon natively.

### Dealing with Security Warnings

**Method 1: Right-Click Open (Easiest)**
1. Right-click the app
2. Click "Open"
3. Click "Open" in the dialog
4. macOS will remember your choice

**Method 2: System Settings**
1. System Settings → Privacy & Security
2. Scroll down to "Security"
3. Click "Open Anyway" next to the blocked app

**Method 3: Command Line Override**
```bash
xattr -cr dist/ImmichUploader.app
```

## 🔍 Troubleshooting Mac Issues

### "python3: command not found"

Install Python:
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

### "pip3: command not found"

Python includes pip, but if it's missing:
```bash
python3 -m ensurepip --upgrade
```

### "Permission denied" when running build.sh

Make it executable:
```bash
chmod +x build.sh
```

### Build fails with "command not found"

Make sure you're in the right directory:
```bash
cd ~/Downloads/immich-uploader-python
ls  # Should see immich_uploader.py, build.sh, etc.
```

### App won't open (Security Block)

Right-click → Open (don't double-click)

### "Module not found" errors

Install dependencies manually:
```bash
pip3 install -r requirements.txt
pip3 install pyinstaller
```

### Want to rebuild?

Clean and rebuild:
```bash
rm -rf build dist *.spec
./build.sh
```

## 📦 Distribution to Other Macs

**Important**: The built app only works on similar Macs:
- Apps built on Intel Mac work on Intel Macs
- Apps built on Apple Silicon work on Apple Silicon Macs
- For universal support, you need to build "universal2" binaries (advanced)

**To share with other Mac users:**
1. Zip the .app file
2. Share the .zip
3. Recipients just unzip and run

## 🎨 Mac-Specific Features

The app uses native macOS features:
- ✅ Standard file picker dialogs
- ✅ macOS-style windows
- ✅ Keyboard shortcuts work
- ✅ Retina display support
- ✅ Works with Dark Mode

## 🔄 Updating

To update the app:
1. Download new version
2. Run build.sh again
3. Replace old app with new one

## 🆚 Mac vs Windows Builds

| Feature | Mac | Windows |
|---------|-----|---------|
| Build command | `./build.sh` | `build-windows.bat` |
| Output | `.app` bundle or executable | `.exe` file |
| Size | ~20-25 MB | ~15-20 MB |
| Security | Gatekeeper check | Windows Defender check |

## 💻 System Requirements

- **macOS**: 10.13 (High Sierra) or later
- **Python**: 3.8 or higher
- **Disk Space**: ~100 MB (for building)
- **RAM**: 2 GB minimum

## 🎓 Advanced: Auto-Build Script

Save this as `auto-build-mac.sh` for even easier building:

```bash
#!/bin/bash

echo "🍎 Immich Uploader - Mac Auto Builder"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Install from: https://www.python.org/"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Install deps
echo "📦 Installing dependencies..."
pip3 install -q -r requirements.txt
pip3 install -q pyinstaller

# Clean previous builds
rm -rf build dist *.spec

# Build
echo "🔨 Building Mac app..."
pyinstaller --onefile --windowed --name "Immich Uploader" immich_uploader.py

# Done
echo
echo "✅ Build complete!"
echo "📱 Your app: dist/Immich Uploader.app"
echo
echo "To install: cp -r 'dist/Immich Uploader.app' /Applications/"
echo
```

Make it executable: `chmod +x auto-build-mac.sh`
Run it: `./auto-build-mac.sh`

## 📞 Support

Having issues on your iMac?
1. Check the troubleshooting section above
2. Make sure Python 3.8+ is installed
3. Try running from Terminal to see error messages
4. Check the main README.md for more details

---

**Your iMac is perfect for this!** The Python version works great on macOS. 🍎✨
