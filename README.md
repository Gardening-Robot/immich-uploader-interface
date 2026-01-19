# Immich Uploader - Python Standalone Version

✨ **NO Node.js Required!** ✨

This is a pure Python version that compiles to a **single executable** with **ZERO dependencies** for end users.

## ⚡ Key Features

- 🎯 **True Standalone** - Single .exe file, nothing else needed
- 🚫 **No Node.js** - No npm, no CLI tools, no external dependencies
- 📁 **Direct API Upload** - Talks directly to Immich's REST API
- 🎨 **Beautiful GUI** - Clean Tkinter interface
- 📊 **Progress Tracking** - Real-time upload progress and logging
- 💾 **Saves Settings** - Remembers your server URL and API key
- 🔄 **Smart Uploads** - Skip duplicates, create albums automatically

## 🚀 For Users (Running the App)

### If someone already built the .exe for you:

1. **Download** `ImmichUploader.exe` (Windows) or `ImmichUploader` (Mac/Linux)
2. **Double-click** to run
3. **Enter** your Immich server details
4. **Upload** your photos!

**That's it!** No installation, no dependencies, no setup. Just run it.

## 🛠️ For Developers (Building the Executable)

### One-Time Setup

1. **Install Python** (version 3.8 or higher)
   - Download from: https://www.python.org/
   - ⚠️ On Windows: Check "Add Python to PATH" during installation

2. **That's all!** Python is the only prerequisite.

### Build the Executable

It's a single command:

**Windows:**
```bash
# Just double-click:
build-windows.bat

# Or run in Command Prompt:
build-windows.bat
```

**Mac/Linux:**
```bash
# Make executable (first time only):
chmod +x build.sh

# Then run:
./build.sh
```

### What Happens During Build

1. Installs Python dependencies (requests, pyinstaller)
2. Bundles everything into a single file
3. Creates executable in `dist/` folder
4. Takes 2-5 minutes

### Output

After building, you'll find:

- **Windows**: `dist/ImmichUploader.exe` (~15-20 MB)
- **Mac**: `dist/ImmichUploader.app` (~20-25 MB)
- **Linux**: `dist/ImmichUploader` (~20-25 MB)

This single file is ALL you need. No installation package, no installer, just one file.

## 📦 What Gets Built Into the Executable

The PyInstaller build includes:
- ✅ Python interpreter
- ✅ All required libraries (requests, tkinter)
- ✅ Your application code
- ✅ Everything needed to run

The end user needs **absolutely nothing** else.

## 🎯 Distribution

### Share with Others

1. Build the executable (see above)
2. Copy `ImmichUploader.exe` (or equivalent) to any location
3. Share it via:
   - USB drive
   - Email
   - Cloud storage (Dropbox, Google Drive, etc.)
   - Network share

### User Instructions

Tell users:
1. Download/copy the file
2. Double-click to run
3. Enter Immich server URL and API key
4. Start uploading!

**No installation needed. No "run as administrator". Just double-click.**

## ⚙️ How It Works

Unlike the Node.js version that wraps the Immich CLI:

1. **Direct API Communication** - Uses Immich's REST API directly
2. **Pure Python** - Uses only standard libraries + requests
3. **Native GUI** - Tkinter (included with Python)
4. **Single Bundle** - PyInstaller packs everything together

## 🔧 Technical Details

### File Structure

```
immich-uploader-python/
├── immich_uploader.py      # Main application
├── requirements.txt        # Python dependencies (just requests)
├── build-windows.bat       # Windows build script
├── build.sh               # Mac/Linux build script
└── README.md              # This file
```

### Dependencies

**Runtime** (bundled in executable):
- Python 3.8+
- requests library
- tkinter (included with Python)

**Build time only**:
- pyinstaller

### API Endpoints Used

The app communicates with these Immich API endpoints:
- `GET /user/me` - Verify authentication
- `GET /album` - List albums
- `POST /album` - Create album
- `POST /asset/upload` - Upload files
- `PUT /album/{id}/assets` - Add assets to album

## 🎨 GUI Features

- **Setup Wizard** - First-run configuration
- **Folder Selection** - Browse for single or multiple folders
- **Upload Options** - Album names, skip duplicates
- **Progress Bar** - Visual upload progress
- **Log Window** - Detailed upload information
- **Status Indicator** - Connection status display

## 🐛 Troubleshooting

### Build Issues

**"Python not found"**
- Install Python from python.org
- On Windows, reinstall and check "Add Python to PATH"

**"pip not found"**
- Reinstall Python (pip is included)
- Or install manually: `python -m ensurepip`

**Build fails with import errors**
- Run: `pip install -r requirements.txt`
- Make sure you're in the project directory

### Runtime Issues

**Windows Defender blocks the .exe**
- This is normal for unsigned executables
- Click "More info" → "Run anyway"
- Or add to Windows Defender exceptions

**"Connection failed"**
- Check server URL format - it MUST end with `/api`
  - ✅ Correct: `http://192.168.1.100:2283/api`
  - ❌ Wrong: `http://192.168.1.100:2283`
  - ❌ Wrong: `http://192.168.1.100:2283/api/`
- Verify API key is correct
- Make sure Immich server is running
- Test server URL in web browser first (should see API docs)

**"Permission denied" on Linux/Mac**
- Make executable: `chmod +x ImmichUploader`
- Then run: `./ImmichUploader`

## 🆚 Comparison with Node.js Version

| Feature | Python Version | Node.js Version |
|---------|---------------|-----------------|
| End user needs | Nothing! | Node.js + Immich CLI |
| File size | ~20 MB | ~150 MB |
| Build time | 2-5 minutes | 5-15 minutes |
| Upload method | Direct API | Via CLI tool |
| GUI framework | Tkinter | Electron |
| Portability | Single file | Multiple files |

## 🎯 Recommended Use Cases

**Python version is better for:**
- ✅ Distribution to non-technical users
- ✅ Minimal dependencies
- ✅ Smaller file size
- ✅ Quick builds

**Node.js version is better for:**
- ✅ Feature parity with official CLI
- ✅ Modern web-based UI
- ✅ Extensive customization
- ✅ Active CLI development follows Immich updates

## 📝 Building for Different Platforms

### Cross-Platform Builds

⚠️ **Important**: You generally need to build ON the target platform:
- Build Windows .exe on Windows
- Build Mac app on Mac
- Build Linux executable on Linux

PyInstaller doesn't support true cross-compilation.

### GitHub Actions (Optional)

You can automate builds using GitHub Actions:

```yaml
name: Build Executables

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: pyinstaller --onefile --windowed --name ImmichUploader immich_uploader.py
      
      - uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.os }}-build
          path: dist/*
```

## 🔒 Security Notes

- API key is stored in `~/.immich_uploader_config.json`
- No credentials are sent anywhere except your Immich server
- All communication is between your computer and your server
- Open source - you can review the code

## 📄 License

MIT License - Free to use, modify, and distribute

## 🙏 Credits

- Built for the Immich community
- Uses the official Immich REST API
- Inspired by the need for a truly standalone uploader

---

**Questions?** Open an issue or check the Immich Discord!
