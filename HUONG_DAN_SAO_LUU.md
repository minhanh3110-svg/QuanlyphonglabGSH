# 🛡️ HƯỚNG DẪN SAO LƯU VÀ KHÔI PHỤC DỮ LIỆU

## ⚠️ QUAN TRỌNG: KHI NÀO CẦN SAO LƯU?

### ✅ LUÔN SAO LƯU TRƯỚC KHI:
1. **Cập nhật code mới** (`git pull`)
2. **Cài đặt thư viện mới** (`pip install`)
3. **Thay đổi cấu trúc database**
4. **Deploy lên server**
5. **Cuối mỗi ngày làm việc** (đề phòng)

### 🔒 DỮ LIỆU CỦA BẠN:
- **File database:** `data.db`
- **Vị trí:** Thư mục gốc dự án
- **Kích thước:** Khoảng vài MB
- **Chứa:** Tất cả nhật ký cấy, phòng sáng, mô soi, danh mục...

---

## 📦 CÁCH 1: SAO LƯU TỰ ĐỘNG (KHUYÊN DÙNG)

### Bước 1: Chạy file SAO LƯU
```
Double-click: SAO_LUU_DU_LIEU.bat
```

### Bước 2: Xem kết quả
```
✅ Sao lưu thành công!
📁 File: database_backups/data_backup_20260103_143025.db
📊 Kích thước: 2.45 MB
🕐 Thời gian: 2026-01-03 14:30:25

📋 Số lượng bản ghi:
   - nhat_ky_cay: 1250 bản ghi
   - danh_muc_ten_giong: 45 bản ghi
   - quan_ly_phong_sang: 890 bản ghi
   ...
```

---

## 📋 CÁCH 2: XEM DANH SÁCH BACKUP

```bash
python backup_database.py list
```

Kết quả:
```
📦 Tìm thấy 5 backup:

STT | Tên file                           | Kích thước | Ngày tạo
--------------------------------------------------------------------------------
  1 | data_backup_20260103_143025.db     |   2.45 MB | 2026-01-03 14:30:25
  2 | data_backup_20260103_100530.db     |   2.42 MB | 2026-01-03 10:05:30
  3 | data_backup_20260102_180015.db     |   2.38 MB | 2026-01-02 18:00:15
  4 | data_backup_20260102_090000.db     |   2.35 MB | 2026-01-02 09:00:00
  5 | data_backup_20260101_170530.db     |   2.30 MB | 2026-01-01 17:05:30
```

---

## ♻️ CÁCH 3: KHÔI PHỤC DỮ LIỆU

### Khi nào cần khôi phục?
- Mất dữ liệu sau khi cập nhật
- Database bị lỗi
- Muốn quay lại trạng thái cũ

### Các bước khôi phục:

**Bước 1:** Xem danh sách backup
```bash
python backup_database.py list
```

**Bước 2:** Chọn file cần khôi phục
```bash
python backup_database.py restore data_backup_20260103_143025.db
```

**Bước 3:** Xác nhận
```
✅ Đã backup file hiện tại: data_before_restore_20260103_150000.db
✅ Đã khôi phục thành công từ: data_backup_20260103_143025.db
```

---

## 🔄 SAO LƯU ĐỊNH KỲ TỰ ĐỘNG (Windows)

### Tạo Task Scheduler:

1. Mở **Task Scheduler** (Windows)
2. **Create Basic Task**
3. **Name:** "Backup Database Lab"
4. **Trigger:** Daily, 6:00 PM (sau giờ làm việc)
5. **Action:** Start a program
   - **Program:** `D:\QUANLYLAB\SAO_LUU_DU_LIEU.bat`
6. **Finish**

→ Hệ thống tự động backup mỗi ngày 6 giờ chiều!

---

## 📁 CẤU TRÚC THƯ MỤC

```
D:\QUANLYLAB\
├── data.db                          ← Database chính
├── app.py                           ← Code ứng dụng
├── backup_database.py               ← Script backup
├── SAO_LUU_DU_LIEU.bat             ← File chạy nhanh
├── database_backups\                ← Thư mục chứa backup
│   ├── data_backup_20260103_143025.db
│   ├── data_backup_20260103_100530.db
│   └── data_backup_20260102_180015.db
└── data_before_restore_*.db        ← Backup trước khi restore
```

---

## ⚙️ TÙY CHỈNH

### Thay đổi thời gian lưu backup:

Mở `backup_database.py`, tìm dòng:
```python
cleanup_old_backups(backup_dir, days=30)  # Đổi 30 thành số ngày bạn muốn
```

---

## 🆘 XỬ LÝ SỰ CỐ

### Sự cố 1: File data.db bị xóa
```bash
python backup_database.py list
python backup_database.py restore data_backup_[tên file gần nhất].db
```

### Sự cố 2: Database bị lỗi
1. Đổi tên file lỗi: `data.db` → `data_ERROR.db`
2. Khôi phục từ backup
3. Kiểm tra lại dữ liệu

### Sự cố 3: Mất dữ liệu sau cập nhật
- **Nguyên nhân:** Database có thể bị reset nếu cấu trúc thay đổi
- **Giải pháp:** Luôn backup TRƯỚC KHI `git pull`

---

## 📊 KIỂM TRA DỮ LIỆU

Để xem nhanh số lượng bản ghi:
```bash
python backup_database.py
```

→ Sẽ hiển thị số lượng bản ghi trong từng bảng

---

## 💡 MẸO HAY

1. **Backup trước mỗi lần cập nhật:**
   ```bash
   SAO_LUU_DU_LIEU.bat
   git pull
   ```

2. **Tạo backup nhanh:**
   - Copy file `data.db` → `data_SAFE.db`
   - Giữ ở nơi an toàn

3. **Backup ra USB:**
   - Copy thư mục `database_backups` ra USB
   - Lưu trữ lâu dài

4. **Đồng bộ Google Drive:**
   - Cài **Google Drive Desktop**
   - Di chuyển `database_backups` vào thư mục Google Drive
   - Tự động sync cloud

---

## ✅ CHECKLIST HÀNG NGÀY

- [ ] Sáng: Mở ứng dụng, kiểm tra dữ liệu
- [ ] Chiều: Chạy `SAO_LUU_DU_LIEU.bat`
- [ ] Trước cập nhật: Backup + kiểm tra file có lưu
- [ ] Cuối tuần: Copy backup ra USB

---

## 🔗 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra file `data.db` có tồn tại không
2. Xem danh sách backup: `python backup_database.py list`
3. Khôi phục từ backup gần nhất
4. Liên hệ admin nếu cần

---

**LƯU Ý:** Backup là BẢO HIỂM cho dữ liệu của bạn. Luôn backup trước khi thay đổi!

