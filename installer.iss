; AlocasiaTrack — Inno Setup installer script
; Build from the project root:
;   ISCC.exe installer.iss
; (or run build.ps1 which calls this automatically)

#define MyAppName      "AlocasiaTrack"
#define MyAppVersion   "1.0"
#define MyAppPublisher "AlocasiaTrack"
#define MyAppExeName   "AlocasiaTrack.exe"
#define MyAppDir       "dist\AlocasiaTrack"

[Setup]
AppId={{A3F72B14-8C41-4D9E-B506-1E2F9D3C7A88}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=
DefaultDirName={userpf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; No admin rights required — installs to user's Program Files
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=dist\installer
OutputBaseFilename=AlocasiaTrackSetup
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardSmallImageFile=
; Show the finish page with a launch checkbox
DisableFinishedPage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; The entire PyInstaller one-dir build
Source: "{#MyAppDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}";  Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; \
  Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; \
  Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove the user-data folder only if the user explicitly chose to
; (we intentionally leave inventory / config in AppData)

[Messages]
; Add a note on the finish page about the optional Facebook integration
FinishedLabel=Setup has finished installing [name] on your computer.%n%nTo use the Facebook Marketplace integration, open a command prompt and run:%n%n    playwright install chromium%n%nAll other features work without any additional steps.
