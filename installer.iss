[Setup]
AppName=GeroGPT Browser
AppVersion=1.0
DefaultDirName={pf}\GeroGPTBrowser
OutputBaseFilename=GeroGPTBrowserSetup
SetupIconFile=dist\GeroGPTBrowser.exe
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\GeroGPTBrowser.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\GeroGPT Browser"; Filename: "{app}\GeroGPTBrowser.exe"
