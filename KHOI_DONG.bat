@echo off
title Quan Ly Phong Nuoi Cay Mo
chcp 65001 >nul
echo.
echo ========================================
echo   DANG KHOI DONG UNG DUNG...
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

REM Kiem tra Streamlit
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [LOI] Streamlit chua duoc cai dat!
    echo.
    echo Dang cai dat Streamlit...
    pip install streamlit pandas openpyxl plotly
    echo.
)

REM Kiem tra Plotly
python -c "import plotly" >nul 2>&1
if errorlevel 1 (
    echo [LOI] Plotly chua duoc cai dat!
    echo.
    echo Dang cai dat Plotly...
    pip install plotly
    echo.
)

REM Kiem tra cac thu vien khac
python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo Dang cai dat Pandas...
    pip install pandas
)

python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo Dang cai dat OpenPyXL...
    pip install openpyxl
)

echo [OK] Cac thu vien da san sang
echo.
echo ========================================
echo   DANG MO UNG DUNG...
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

