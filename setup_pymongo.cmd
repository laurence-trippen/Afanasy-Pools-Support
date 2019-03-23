@echo off

rem -------- pymongo cgru ----------------------------------

echo %CGRU_LOCATION%

set PY_EXE=%CGRU_LOCATION%\python\python.exe
set PY_INSTALL_PIP=%PY_EXE% -m ensurepip --default-pip
set PIP_INSTALL_PYMONGO=%PY_EXE% -m pip install pymongo

echo %PY_INSTALL_PIP%
call %PY_INSTALL_PIP%
call %PIP_INSTALL_PYMONGO%

rem ---------------------------------------------------------