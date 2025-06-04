@echo off
rem Build standalone executable with PyInstaller
pyinstaller --onefile --name GeroGPTBrowser cli.py

if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller failed.
    exit /b %ERRORLEVEL%
)

echo Build complete. Executable is located in the dist folder.
