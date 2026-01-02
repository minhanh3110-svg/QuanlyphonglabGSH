@echo off
chcp 65001 >nul
title Cai dat Plotly
echo.
echo ========================================
echo   CAI DAT PLOTLY
echo ========================================
echo.
echo Dang cai dat thu vien Plotly...
echo.

python -m pip install plotly

if errorlevel 1 (
    echo.
    echo [LOI] Khong the cai dat Plotly!
    echo.
    echo Thu cach khac...
    pip install plotly
)

echo.
echo ========================================
echo   HOAN TAT
echo ========================================
echo.
echo Plotly da duoc cai dat thanh cong!
echo.
echo Bay gio ban co the chay lai ung dung bang file KHOI_DONG.bat
echo.
pause

