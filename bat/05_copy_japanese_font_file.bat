call ./00_config.bat

set newFontFile="kowaiFont\‚Ó‚§‚ñ‚Æ‚¤‚Í•|‚¢–¾’©‘Ì.otf"
rem set newFontFile="onryou\onryou.TTF"

set targetFontFiles="Envy Code R.ttf" "gamefont(1).ttf" "gamefont.ttf" "MingLiU-ExtB-01.ttf" "MS33558.ttf"

for %%a in (%targetFontFiles%) do (
    copy "%japaneseFontDir:~1,-1%/%newFontFile%" "%gameDir:~1,-1%/Fonts/%%a"
)

rem pause
