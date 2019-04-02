rem Name=Start Pool Server
rem Icon=afanasy.png

call %0\..\_setup.cmd

"%CGRU_PYTHONEXE%" "%CGRU_LOCATION%\utilities\poolssupport\poolserver\server.py" %*