#!/bin/bash
# Build standalone executable with PyInstaller
set -e
pyinstaller --onefile --name GeroGPTBrowser cli.py

if [ $? -ne 0 ]; then
    echo "PyInstaller failed." >&2
    exit 1
fi

echo "Build complete. Executable is located in the dist folder."
