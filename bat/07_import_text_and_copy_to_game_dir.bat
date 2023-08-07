call ./00_config.bat

rmdir /s /q %workDir%
mkdir %workDir%
xcopy %backupDir% %workDir% /s /y

py ../py/import_Cruelty-Squad_text.py %workDir% %importFile%

robocopy %workDir% "%gdcProjectDir:~1,-1%/%workDirName%" *.gd /e

cd %gdcProjectDir%
%godotEngineExe% --export-pack "Windows Desktop" %gdcProjectZipFile%

powershell -Command "Expand-Archive -Path '%gdcProjectZipFile%' -DestinationPath '%gdcWorkDir%'"
robocopy "%gdcWorkDir:~1,-1%/%workDirName%" %gameDir% *.gdc /e /im /is
rd %gdcWorkDir% /s /q

robocopy %workDir% %gameDir% /s /xf *.gd /im /is

rem pause
