call ./00_config.bat

rmdir /s /q %workDir%
mkdir %workDir%
xcopy %backupDir% %workDir% /s /y

py ../py/import_Cruelty-Squad_text.py %workDir% %importFile%

robocopy %workDir% "%gdcProjectDir:~1,-1%/%workDirName%" *.gd /e

rem pause
