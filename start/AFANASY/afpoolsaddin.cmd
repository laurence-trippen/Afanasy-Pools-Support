rem Name=Manage Pools
rem Icon=afanasy.png
rem Separator
call %0\..\_setup.cmd

"%CGRU_PYTHONEXE%" "%CGRU_LOCATION%\utilities\poolsaddin\poolsaddin.py" %*
