"""
Script tự động sao lưu database
Chạy script này để backup dữ liệu
"""
import sqlite3
import shutil
from datetime import datetime
import os

def backup_database():
    """Sao lưu database với timestamp"""
    
    # Tên file database gốc
    source_db = 'data.db'
    
    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(source_db):
        print("❌ Không tìm thấy file data.db!")
        return False
    
    # Tạo thư mục backup nếu chưa có
    backup_dir = 'database_backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✅ Đã tạo thư mục {backup_dir}/")
    
    # Tạo tên file backup với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f'data_backup_{timestamp}.db')
    
    try:
        # Copy file database
        shutil.copy2(source_db, backup_file)
        
        # Lấy kích thước file
        size_mb = os.path.getsize(backup_file) / (1024 * 1024)
        
        print(f"✅ Sao lưu thành công!")
        print(f"📁 File: {backup_file}")
        print(f"📊 Kích thước: {size_mb:.2f} MB")
        print(f"🕐 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Đếm số lượng bản ghi
        conn = sqlite3.connect(backup_file)
        c = conn.cursor()
        
        tables = ['nhat_ky_cay', 'danh_muc_ten_giong', 'danh_muc_chu_ky', 
                  'danh_muc_moi_truong', 'quan_ly_phong_sang', 'mo_soi']
        
        print("\n📋 Số lượng bản ghi:")
        for table in tables:
            try:
                c.execute(f"SELECT COUNT(*) FROM {table}")
                count = c.fetchone()[0]
                print(f"   - {table}: {count} bản ghi")
            except:
                pass
        
        conn.close()
        
        # Xóa các backup cũ hơn 30 ngày
        cleanup_old_backups(backup_dir, days=30)
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi sao lưu: {str(e)}")
        return False

def cleanup_old_backups(backup_dir, days=30):
    """Xóa các backup cũ hơn N ngày"""
    try:
        now = datetime.now()
        deleted_count = 0
        
        for filename in os.listdir(backup_dir):
            if filename.startswith('data_backup_') and filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                
                # Lấy thời gian file
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                # Nếu cũ hơn N ngày thì xóa
                if (now - file_time).days > days:
                    os.remove(filepath)
                    deleted_count += 1
        
        if deleted_count > 0:
            print(f"\n🗑️  Đã xóa {deleted_count} backup cũ (>{days} ngày)")
            
    except Exception as e:
        print(f"⚠️  Không thể dọn dẹp backup cũ: {str(e)}")

def list_backups():
    """Liệt kê tất cả các backup"""
    backup_dir = 'database_backups'
    
    if not os.path.exists(backup_dir):
        print("❌ Chưa có backup nào!")
        return
    
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.startswith('data_backup_') and filename.endswith('.db'):
            filepath = os.path.join(backup_dir, filename)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append((filename, size_mb, file_time))
    
    if not backups:
        print("❌ Chưa có backup nào!")
        return
    
    print(f"\n📦 Tìm thấy {len(backups)} backup:\n")
    print("STT | Tên file                           | Kích thước | Ngày tạo")
    print("-" * 80)
    
    for i, (name, size, time) in enumerate(sorted(backups, key=lambda x: x[2], reverse=True), 1):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{i:3} | {name:35} | {size:6.2f} MB | {time_str}")

def restore_backup(backup_filename):
    """Khôi phục từ backup"""
    backup_dir = 'database_backups'
    backup_path = os.path.join(backup_dir, backup_filename)
    
    if not os.path.exists(backup_path):
        print(f"❌ Không tìm thấy file: {backup_filename}")
        return False
    
    try:
        # Backup file hiện tại trước khi restore
        if os.path.exists('data.db'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2('data.db', f'data_before_restore_{timestamp}.db')
            print(f"✅ Đã backup file hiện tại: data_before_restore_{timestamp}.db")
        
        # Restore
        shutil.copy2(backup_path, 'data.db')
        print(f"✅ Đã khôi phục thành công từ: {backup_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi khôi phục: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("🛡️  HỆ THỐNG SAO LƯU DATABASE - QUẢN LÝ PHÒNG LAB")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_backups()
        elif sys.argv[1] == "restore" and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("Cách dùng:")
            print("  python backup_database.py          → Tạo backup mới")
            print("  python backup_database.py list     → Xem danh sách backup")
            print("  python backup_database.py restore <tên_file> → Khôi phục")
    else:
        backup_database()
    
    print("\n" + "=" * 60)

