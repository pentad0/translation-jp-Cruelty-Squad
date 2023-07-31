call ./00_config.bat

move %gameDir%\crueltysquad.pck %gameDir%\crueltysquad.pck.bak
robocopy %backupDir% %gameDir% /e

rem pause
