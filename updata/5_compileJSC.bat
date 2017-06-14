
@echo off
echo cur dir=%cd%

rd /s /q %cd%\app_s
mkdir %cd%\app_s

XCOPY %cd%\app\*.*  %cd%\app_s /S


rd /s /q %cd%\app_s\src
cocos jscompile -s %cd%\app -d %cd%\app_s


pause