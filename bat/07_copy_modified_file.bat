call ./00_config.bat

robocopy %workDir% %gameDir% /s /xf *.gd *.remap /is

rem pause
