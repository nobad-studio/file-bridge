; Inno Setup script for NOBAD File Bridge (same shape as NOBAD VPN's installer).
; Build after PyInstaller:  iscc /DMyAppVersion=0.5.1 packaging\windows\installer.iss
; Output:                   dist-installer\NobadFileBridge-Setup-<version>.exe
;
; File Bridge needs no services or drivers, so it installs for the current user by default (no admin prompt).
; Setup offers "install for all users" too, which asks for admin rights.
#ifndef MyAppVersion
  #define MyAppVersion "0.0.0"
#endif
#define MyAppName "NOBAD File Bridge"
#define MyAppExe "NobadFileBridge.exe"

[Setup]
AppId={{3DC92F55-C855-4C37-88DA-AE4AA38BA0D8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher=NOBAD
AppPublisherURL=https://github.com/nobad-studio/file-bridge
AppSupportURL=https://github.com/nobad-studio/file-bridge/issues
AppUpdatesURL=https://github.com/nobad-studio/file-bridge/releases
VersionInfoVersion={#MyAppVersion}
VersionInfoProductName={#MyAppName}
VersionInfoCompany=NOBAD
VersionInfoDescription={#MyAppName} Setup
DefaultDirName={autopf}\NOBAD File Bridge
DefaultGroupName=NOBAD File Bridge
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog commandline
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.17763
OutputDir=..\..\dist-installer
OutputBaseFilename=NobadFileBridge-Setup-{#MyAppVersion}
SetupIconFile=..\..\resources\branding\nobad-file-bridge.ico
UninstallDisplayIcon={app}\{#MyAppExe}
UninstallDisplayName={#MyAppName}
Compression=lzma2/max
SolidCompression=yes
CloseApplications=yes
RestartApplications=no
WizardStyle=modern

[Files]
Source: "..\..\dist\NobadFileBridge\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
Source: "..\..\LICENSE"; DestDir: "{app}"; DestName: "LICENSE.txt"; Flags: ignoreversion
Source: "..\..\THIRD-PARTY-NOTICES.md"; DestDir: "{app}"; Flags: ignoreversion

[InstallDelete]
; An upgrade replaces the whole app folder, so files dropped by an older version never linger.
Type: filesandordirs; Name: "{app}\_internal"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; AppUserModelID: "NOBAD.FileBridge"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExe}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
const
  WebView2Id = '{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}';
  WebView2Page = 'https://developer.microsoft.com/microsoft-edge/webview2/';

// Microsoft's documented check: the runtime is installed when "pv" is set and isn't 0.0.0.0.
function WebView2At(Root: Integer; Key: String): Boolean;
var
  v: String;
begin
  Result := RegQueryStringValue(Root, Key, 'pv', v) and (v <> '') and (v <> '0.0.0.0');
end;

function WebView2Installed: Boolean;
begin
  Result := WebView2At(HKLM, 'SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\' + WebView2Id) or
            WebView2At(HKLM, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\' + WebView2Id) or
            WebView2At(HKCU, 'Software\Microsoft\EdgeUpdate\Clients\' + WebView2Id);
end;

// Stop a running copy so its files can be replaced (the Restart Manager asks first; this catches the rest).
procedure StopApp;
var
  rc: Integer;
begin
  Exec(ExpandConstant('{sys}\taskkill.exe'), '/IM {#MyAppExe} /T', '', SW_HIDE, ewWaitUntilTerminated, rc);
  Sleep(1000);
  Exec(ExpandConstant('{sys}\taskkill.exe'), '/F /IM {#MyAppExe} /T', '', SW_HIDE, ewWaitUntilTerminated, rc);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  if FileExists(ExpandConstant('{app}\{#MyAppExe}')) then
    StopApp;
end;

// Nothing is downloaded by Setup: if WebView2 is missing, it says so and offers Microsoft's page.
procedure CurStepChanged(CurStep: TSetupStep);
var
  rc: Integer;
begin
  if (CurStep = ssPostInstall) and (not WebView2Installed) and (not WizardSilent) then
    if MsgBox('NOBAD File Bridge draws its window with Microsoft Edge WebView2, which isn''t installed on this PC.' + #13#10 + #13#10 +
              'Open Microsoft''s WebView2 download page now? Install the "Evergreen" runtime, then start File Bridge.',
              mbConfirmation, MB_YESNO) = IDYES then
      ShellExec('open', WebView2Page, '', '', SW_SHOWNORMAL, ewNoWait, rc);
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  data: String;
begin
  if CurUninstallStep = usUninstall then
    StopApp;
  if CurUninstallStep = usPostUninstall then
  begin
    // Your connections, vault, settings and logs live in %USERPROFILE%\.remote-file-manager. Kept unless you say so.
    data := ExpandConstant('{%USERPROFILE}\.remote-file-manager');
    if DirExists(data) and (not UninstallSilent) and
       (MsgBox('Also delete your NOBAD File Bridge data (saved connections, encrypted vault, settings and logs)?' + #13#10 + #13#10 +
               data + #13#10 + #13#10 + 'Choose No to keep it for a later reinstall.',
               mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES) then
      DelTree(data, True, True, True);
  end;
end;
