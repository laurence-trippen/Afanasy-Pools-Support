rem Name=Manage Pools
rem Icon=afanasy.png
call %0\..\_setup.cmd

"%CGRU_PYTHONEXE%" "%CGRU_LOCATION%\utilities\poolssupport\poolmanager\main.py" %*
