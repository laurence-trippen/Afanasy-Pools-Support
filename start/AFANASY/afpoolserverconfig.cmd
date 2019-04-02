rem Name=Configure Pool Server
rem Icon=afanasy.png
rem Separator
call %0\..\_setup.cmd

"%CGRU_PYTHONEXE%" "%CGRU_LOCATION%\utilities\poolssupport\poolserver\configurator.py" %*