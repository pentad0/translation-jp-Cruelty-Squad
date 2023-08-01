call ./00_config.bat

powershell -Command "Expand-Archive -Path '%gdcProjectZipFile%' -DestinationPath '%gdcWorkDir%'"
robocopy "%gdcWorkDir:~1,-1%/%workDirName%" %gameDir% *.gdc /e
rd %gdcWorkDir% /s /q

robocopy %workDir% %gameDir% /s /xf *.gd /is

rem pause
