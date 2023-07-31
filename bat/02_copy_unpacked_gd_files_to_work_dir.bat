call ./00_config.bat

robocopy %backupDir% %workDir% *.gd /s /xd addons
rd %backupDir% /s /q
mkdir %backupDir%

rem pause
