@echo off
chcp 65001 >nul
echo ================================================
echo    KHOI DONG LAI UNG DUNG VOI LOGO MOI
echo ================================================
echo.

echo [1/2] Dang kiem tra logo...
if exist "logo.png" (
    echo [OK] Da tim thay file logo.png
) else (
    echo [!] Chua co file logo.png
    echo     Vui long luu logo vao thu muc nay truoc!
    pause
    exit /b 1
)

echo.
echo [2/2] Dang khoi dong ung dung...
echo     Ung dung se tu dong mo trong trinh duyet
echo     Nhan Ctrl+C de dung ung dung
echo.
echo ================================================
echo.

python -m streamlit run app.py

pause

