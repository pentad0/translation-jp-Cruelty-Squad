call ./00_config.bat

robocopy %backupDir% %workDir% *.json *.tscn /s /xd addons
rd %backupDir% /s /q
xcopy %workDir% %backupDir% /i /s

rem pause
