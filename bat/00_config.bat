rem set gameDir="F:\SteamLibrary/steamapps/common/Cruelty Squad"
set gameDir="%PROGRAMFILES(X86)%/Steam/SteamApps/common/Cruelty Squad"

set tempDir="C:\Temp/Cruelty Squad"
set backupDir="%tempDir:~1,-1%/crueltysquad_pck_bak"
set workDir="%tempDir:~1,-1%/crueltysquad_pck"

rem set tsvDir="../tsv"
set tsvDir="%tempDir:~1,-1%/tsv"
set exportFile="%tsvDir:~1,-1%/Cruelty-Squad_text_English.tsv"
set importFile="%tsvDir:~1,-1%/Cruelty-Squad_text_Japanese.tsv"

set japaneseFontDir="%tempDir:~1,-1%/japanese_font"
