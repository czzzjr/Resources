
@echo off
echo cur dir=%cd%

set /p newversion=Enter new version:

set newversion_DIR=%cd%\app_v%newversion%
echo newversion_DIR=%newversion_DIR%
set src_DIR=%cd%\..\..\frameworks\runtime-src\proj.android\assets
echo src_DIR=%src_DIR%

mkdir %newversion_DIR%
XCOPY %src_DIR%\*.*  %newversion_DIR% /S 



pause
