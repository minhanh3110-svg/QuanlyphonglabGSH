@echo off
chcp 65001 >nul
color 0A
title 🛡️ SAO LƯU DỮ LIỆU - QUẢN LÝ PHÒNG LAB

echo.
echo ═══════════════════════════════════════════════════════════
echo           🛡️  SAO LƯU DỮ LIỆU TỰ ĐỘNG
echo ═══════════════════════════════════════════════════════════
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Lỗi: Chưa cài Python!
    echo.
    pause
    exit /b 1
)

REM Chạy script backup
echo 📦 Đang sao lưu dữ liệu...
echo.
python backup_database.py

echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 💡 HƯỚNG DẪN:
echo    - Chạy file này TRƯỚC KHI cập nhật code
echo    - Backup được lưu trong thư mục: database_backups/
echo    - Backup cũ hơn 30 ngày sẽ tự động xóa
echo.
pause

