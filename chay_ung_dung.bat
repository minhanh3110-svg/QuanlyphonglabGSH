@echo off
chcp 65001 >nul
title Quan Ly Phong Nuoi Cay Mo
echo.
echo ========================================
echo   QUAN LY PHONG NUOI CAY MO
echo ========================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Python chua duoc cai dat hoac khong co trong PATH!
    echo.
    echo Vui long cai dat Python tu: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python da duoc cai dat
echo.
echo Dang kiem tra va cai dat cac thu vien...
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [LOI] Khong the cai dat cac thu vien!
    echo.
    echo Thu cach khac...
    pip install -r requirements.txt
)

echo.
echo ========================================
echo   DANG KHOI DONG UNG DUNG...
echo ========================================
echo.
echo Ung dung se mo trong trinh duyet tai: http://localhost:8501
echo.
echo Neu trinh duyet khong tu dong mo, hay copy link tren va dan vao trinh duyet
echo.
echo Nhan Ctrl+C de dung ung dung
echo.
echo ========================================
echo.

REM Thu chay streamlit
python -m streamlit run app.py
if errorlevel 1 (
    echo.
    echo [LOI] Khong the khoi dong ung dung!
    echo.
    echo Thu cach khac...
    streamlit run app.py
)

pause

