#!/bin/bash

echo "========================================"
echo "Immich Uploader - Build Standalone App"
echo "========================================"
echo

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3 from: https://www.python.org/"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Install PyInstaller
echo "Installing PyInstaller..."
pip3 install pyinstaller
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyInstaller"
    exit 1
fi

echo
echo "Building executable..."
echo "This may take a few minutes..."
echo

# Build the executable
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    pyinstaller --onefile --windowed --name "ImmichUploader" immich_uploader.py
    echo
    echo "========================================"
    echo "Build Complete!"
    echo "========================================"
    echo
    echo "Your app is ready:"
    echo "  dist/ImmichUploader"
    echo
    echo "This is a STANDALONE app - no dependencies needed!"
else
    # Linux
    pyinstaller --onefile --name "ImmichUploader" immich_uploader.py
    echo
    echo "========================================"
    echo "Build Complete!"
    echo "========================================"
    echo
    echo "Your executable is ready:"
    echo "  dist/ImmichUploader"
    echo
    echo "This is a STANDALONE file - no dependencies needed!"
fi

echo
