; Telegraf Installer Script
; Inno Setup Configuration
; Version 2.0.0

#define MyAppName "Telegraf"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Telegraf Team"
#define MyAppURL "https://github.com/telegraf"
#define MyAppExeName "Telegraf.exe"
#define MyAppIcon "telegraf.ico"

[Setup]
; App information
AppId={{8F9A7B2C-3D4E-5F6A-7B8C-9D0E1F2A3B4C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; Allow user to change installation directory
DisableDirPage=no

; Output
OutputDir=installer
OutputBaseFilename=Telegraf_Setup
; SetupIconFile=assets\{#MyAppIcon}
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compression
Compression=lzma2/max
SolidCompression=yes

; Windows version
MinVersion=10.0
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Privileges
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; UI
WizardStyle=modern
; WizardImageFile=assets\wizard-image.bmp
; WizardSmallImageFile=assets\wizard-small.bmp

; License (optional)
; LicenseFile=LICENSE.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[CustomMessages]
russian.SelectDirLabel=Выберите папку для установки Telegraf
russian.SelectDirBrowseLabel=Нажмите "Далее" для продолжения или "Обзор" для выбора другой папки
russian.DiskSpaceRequired=Требуется места на диске:
russian.DiskSpaceFree=Свободно на диске:

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkablealone
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked checkablealone
Name: "startmenu"; Description: "Создать ярлык в меню Пуск"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkablealone

[Files]
; Main executable
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Configuration files
Source: "..\config\config.json"; DestDir: "{app}\config"; Flags: ignoreversion

; Assets (if needed)
; Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.bmp,*.ico"

; Documentation
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "..\QUICKSTART.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\INSTRUCTIONS.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenu
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; Tasks: startmenu
Name: "{group}\README"; Filename: "{app}\README.md"; Tasks: startmenu

; Desktop
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Quick Launch
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Option to launch after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up user data (optional - ask user)
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\data"
Type: files; Name: "{app}\*.log"

[Code]
// Custom installation logic

function InitializeSetup(): Boolean;
begin
  Result := True;
  // Check if app is already running
  if CheckForMutexes('TelegrafAppMutex') then
  begin
    MsgBox('Telegraf уже запущен. Пожалуйста, закройте его перед продолжением.', mbError, MB_OK);
    Result := False;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create data directories
    CreateDir(ExpandConstant('{app}\logs'));
    CreateDir(ExpandConstant('{app}\data'));
  end;
end;

function InitializeUninstall(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  // Ask if user wants to keep data
  if MsgBox('Вы хотите сохранить историю чатов и настройки?', mbConfirmation, MB_YESNO) = IDNO then
  begin
    // User wants to delete everything
    DelTree(ExpandConstant('{app}\logs'), True, True, True);
    DelTree(ExpandConstant('{app}\data'), True, True, True);
    DelTree(ExpandConstant('{app}\config'), True, True, True);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Final cleanup
    if DirExists(ExpandConstant('{app}')) then
    begin
      RemoveDir(ExpandConstant('{app}'));
    end;
  end;
end;
