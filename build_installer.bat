@echo off
rem Build a Windows installer using Inno Setup
set ISSCRIPT=installer.iss
set ISCC="%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"

if not exist "%ISCC%" (
    echo Inno Setup compiler not found. Please install Inno Setup 6.
    exit /b 1
)

if not exist dist\GeroGPTBrowser.exe (
    echo Executable not found. Run build_exe.bat first.
    exit /b 1
)

"%ISCC%" %ISSCRIPT%
if %ERRORLEVEL% NEQ 0 (
    echo Inno Setup failed.
    exit /b %ERRORLEVEL%
)

echo Installer created as GeroGPTBrowserSetup.exe in the current directory.
