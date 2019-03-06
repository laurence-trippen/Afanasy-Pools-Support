@echo off

echo %CGRU_LOCATION%

set PYSIDE_UIC_EXE=%CGRU_LOCATION%\python\Scripts\pyside-uic.exe
set POOLSADDIN_UI=%CGRU_LOCATION%\utilities\poolsaddin\ui

call %PYSIDE_UIC_EXE% -o %POOLSADDIN_UI%\mainwindow.py %POOLSADDIN_UI%\mainwindow.ui