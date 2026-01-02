@echo off
chcp 65001 >nul
title Kiem Tra He Thong
echo.
echo ========================================
echo   KIEM TRA HE THONG
echo ========================================
echo.

echo [1] Kiem tra Python...
python --version
if errorlevel 1 (
    echo [LOI] Python chua duoc cai dat!
    goto :end
) else (
    echo [OK] Python da duoc cai dat
)
echo.

echo [2] Kiem tra Streamlit...
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)" 2>nul
if errorlevel 1 (
    echo [LOI] Streamlit chua duoc cai dat!
    echo.
    echo Ban co muon cai dat ngay bay gio? (Y/N)
    set /p install="Nhap Y de cai dat: "
    if /i "%install%"=="Y" (
        echo Dang cai dat...
        pip install streamlit pandas openpyxl
    )
) else (
    echo [OK] Streamlit da duoc cai dat
)
echo.

echo [3] Kiem tra Pandas...
python -c "import pandas; print('Pandas version:', pandas.__version__)" 2>nul
if errorlevel 1 (
    echo [LOI] Pandas chua duoc cai dat!
) else (
    echo [OK] Pandas da duoc cai dat
)
echo.

echo [4] Kiem tra file app.py...
if exist app.py (
    echo [OK] File app.py ton tai
) else (
    echo [LOI] File app.py khong ton tai!
)
echo.

echo ========================================
echo   KET QUA KIEM TRA
echo ========================================
echo.
echo Neu tat ca deu [OK], ban co the chay ung dung bang file KHOI_DONG.bat
echo.

:end
pause

