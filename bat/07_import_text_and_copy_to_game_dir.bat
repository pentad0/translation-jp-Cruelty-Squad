call ./00_config.bat

rmdir /s /q %workDir%
mkdir %workDir%
xcopy %backupDir% %workDir% /s /y

py ../py/import_Cruelty-Squad_text.py %workDir% %importFile%

robocopy %workDir% "%gdcProjectDir:~1,-1%/%workDirName%" *.gd /e

cd %gdcProjectDir%
%godotEngine% --export-pack "Windows Desktop" %gdcProjectZipFile%

powershell -Command "Expand-Archive -Path '%gdcProjectZipFile%' -DestinationPath '%gdcWorkDir%'"
robocopy "%gdcWorkDir:~1,-1%/%workDirName%" %gameDir% *.gdc /e
rd %gdcWorkDir% /s /q

robocopy %workDir% %gameDir% /s /xf *.gd /is

rem 
pause
