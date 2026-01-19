# Building for Multiple Platforms

You **cannot** build a Mac executable on Windows. But you have several good options:

## Option 1: GitHub Actions (EASIEST - Free & Automatic!)

GitHub will build Windows, Mac, AND Linux versions for you automatically!

### Setup (One Time - 5 Minutes)

1. **Create a GitHub account** (if you don't have one)
   - Go to: https://github.com/signup

2. **Create a new repository**
   - Click the "+" in top right → "New repository"
   - Name it: `immich-uploader`
   - Make it Public
   - Click "Create repository"

3. **Upload your files**
   - Click "uploading an existing file"
   - Drag all files from `immich-uploader-python` folder
   - Commit changes

4. **That's it!** GitHub will automatically:
   - Build Windows .exe
   - Build Mac .app
   - Build Linux binary
   - Store them for 90 days

### Download Your Builds

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click on the latest workflow run
4. Scroll down to "Artifacts"
5. Download:
   - `ImmichUploader-Windows` (contains .exe)
   - `ImmichUploader-macOS` (contains Mac app)
   - `ImmichUploader-Linux` (contains Linux binary)

### Trigger Manual Build

After initial setup, you can rebuild anytime:
1. Go to "Actions" tab
2. Click "Build Executables for All Platforms"
3. Click "Run workflow"
4. Wait 5-10 minutes
5. Download your builds!

**Cost:** FREE (GitHub Actions is free for public repositories)

---

## Option 2: Use a Mac Virtual Machine

### Using a Cloud Mac

Services that provide Mac VMs:
- **MacStadium** - $50-100/month
- **AWS EC2 Mac Instances** - ~$1/hour
- **MacinCloud** - Pay per minute
- **Anka Build** - For CI/CD

**Process:**
1. Rent a Mac VM for 1 hour (~$1)
2. Install Python
3. Run the build script
4. Download the .exe
5. Done!

### Using Virtualbox/VMware (NOT RECOMMENDED)

macOS license prohibits running on non-Apple hardware, so this isn't really an option.

---

## Option 3: Ask a Friend with a Mac

Literally:
1. Send them the project folder
2. They run: `./build.sh`
3. They send you back the executable
4. Takes 5 minutes

---

## Option 4: Build on Mac Later

Just build the Windows version now:
1. Run `build-windows.bat` on your Windows PC
2. You get `ImmichUploader.exe`
3. Windows users can use it right away!
4. Build Mac version later when you have access to a Mac

---

## Option 5: Wait for Universal Packaging (Future)

Tools like **PyOxidizer** and **Briefcase** aim to support cross-compilation, but they're not ready for prime-time yet.

---

## Recommended Approach

**Use GitHub Actions!**

Here's why:
- ✅ Completely free
- ✅ Builds all 3 platforms simultaneously
- ✅ Takes 5-10 minutes
- ✅ No Mac needed
- ✅ No Windows needed
- ✅ Automatic on every code change
- ✅ Stores builds for 90 days

Just:
1. Push code to GitHub
2. Wait 10 minutes
3. Download Windows, Mac, AND Linux executables
4. Distribute to users!

---

## Step-by-Step: GitHub Actions Setup

### 1. Create Repository

```bash
# In your project folder:
git init
git add .
git commit -m "Initial commit"
```

### 2. Push to GitHub

On GitHub.com:
- Create new repository
- Follow the instructions to push existing code

Or use GitHub Desktop (easier for beginners):
- Download: https://desktop.github.com/
- File → Add Local Repository
- Select your folder
- Publish repository

### 3. Builds Start Automatically

- Go to your repo on GitHub
- Click "Actions" tab
- Watch builds run (takes ~10 minutes)
- Download artifacts when done!

### 4. Share Executables

Download all three builds:
- Windows users get `ImmichUploader.exe`
- Mac users get `ImmichUploader` (Mac version)
- Linux users get `ImmichUploader` (Linux version)

---

## File Sizes

After building:
- **Windows .exe**: ~15-20 MB
- **Mac .app**: ~20-25 MB  
- **Linux binary**: ~20-25 MB

All completely standalone with zero dependencies!

---

## Questions?

**"Do I need to pay GitHub?"**
→ No! Free for public repos.

**"Can I make the repo private?"**
→ Yes, but GitHub Actions has limited free minutes for private repos. Use a public repo for unlimited builds.

**"How often can I build?"**
→ As many times as you want!

**"Can users download directly from GitHub?"**
→ Yes! Under Releases or Artifacts.

**"What if I want to make changes?"**
→ Just update your code, push to GitHub, and it rebuilds automatically!

---

**Bottom line:** You can't cross-compile to Mac on Windows, but GitHub Actions makes it so easy you don't need to!
