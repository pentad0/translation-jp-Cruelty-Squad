rem set gameDir="F:\SteamLibrary/steamapps/common/Cruelty Squad"
set gameDir="%PROGRAMFILES(X86)%/Steam/SteamApps/common/Cruelty Squad"

set tempDir="C:\Temp/Cruelty Squad"
set backupDir="%tempDir:~1,-1%/pck_bak"
set workDirName=pck
set workDir="%tempDir:~1,-1%/%workDirName%"

rem set tsvDir="../tsv"
set tsvDir="%tempDir:~1,-1%/tsv"
set exportFile="%tsvDir:~1,-1%/Cruelty-Squad_text_English.tsv"
set importFile="%tsvDir:~1,-1%/Cruelty-Squad_text_Japanese.tsv"

set japaneseFontDir="%tempDir:~1,-1%/japanese_font"

set gdcProjectDir="%tempDir:~1,-1%/gdc_project"

set godotEngineExe="%tempDir:~1,-1%/Godot_v3.5.2-stable_win64.exe/Godot_v3.5.2-stable_win64.exe"
set gdcProjectZipFile="%tempDir:~1,-1%/gdc_project.zip"
set gdcWorkDir="%tempDir:~1,-1%/gdc_project_work"
