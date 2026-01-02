@echo off
chcp 65001 >nul
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         🚀 PUSH CODE LÊN GITHUB                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Kiểm tra Git đã cấu hình chưa
git config user.name >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Cấu hình Git...
    git config user.name "GSH Lab"
    git config user.email "gsh@lab.com"
    echo ✅ Đã cấu hình Git user
    echo.
)

echo 📋 Trạng thái hiện tại:
git log --oneline -3
echo.

echo 📤 Đang push code lên GitHub...
echo.

REM Thử push
git push origin main 2>nul
if errorlevel 1 (
    echo.
    echo ⚠️  Chưa có remote! Hãy chạy lệnh sau:
    echo.
    echo git remote add origin https://github.com/USERNAME/QuanLyPhongLabGSH.git
    echo git branch -M main
    echo git push -u origin main
    echo.
    echo 📖 Xem thêm: PUSH_TO_GITHUB.md
    pause
    exit /b 1
)

echo.
echo ✅ Push thành công!
echo.
echo 🌐 App trên Streamlit Cloud sẽ tự động cập nhật trong vài phút.
echo 📝 Hoặc vào https://share.streamlit.io và Reboot app
echo.
pause

