# 🔬 HƯỚNG DẪN QUẢN LÝ MÔ SOI

## Khái niệm "Mô Soi"

**Mô Soi** là kết quả kiểm tra từ chu kỳ trước (Phòng Sáng) - chính là nguồn cung cấp **Mô Mẹ** cho chu kỳ tiếp theo.

### Quy trình:

```
Chu kỳ N-1 (Phòng Sáng)
    ↓
Kiểm tra → Soi mô
    ↓
Đếm: Túi sạch vs Túi nhiễm
    ↓
Nhập vào hệ thống: "Mô Soi"
    ↓
Chu kỳ N (Phòng Cấy)
    ↓
Lấy "Mô Soi" làm "Mô Mẹ"
    ↓
Hệ thống tự động khấu trừ
```

---

## 📋 CÁC CHỨC NĂNG CHÍNH

### 1. QUẢN LÝ MÔ SOI

**Menu:** "Quản lý Mô Soi"

#### Tab 1: Nhập Mô Soi

**Mục đích:** Nhập kết quả kiểm tra từ Phòng Sáng

**Thông tin cần nhập:**
- 🌱 Tên giống
- 🔄 Chu kỳ trước (Nhân nhanh / Ra rễ / v.v.)
- 📅 Ngày kiểm tra (soi)
- 🔢 Tổng số túi ban đầu
- ❌ Số túi nhiễm
- ✅ Số cụm mỗi túi sạch

**Tự động tính:**
- Số túi sạch = Tổng - Nhiễm
- Tổng cụm sạch = Túi sạch × Cụm/túi
- Tỷ lệ sạch %
- Tỷ lệ nhiễm %

**Mã lô:** Tự động sinh ra dạng `MS-YYYYMMDD-XXX`

**Ví dụ:**
```
Tên giống: Đồng tiền đỏ
Chu kỳ trước: Nhân nhanh
Ngày soi: 02/01/2026
Tổng túi: 100
Túi nhiễm: 15
Cụm/túi: 5

→ Kết quả:
  Túi sạch: 85 túi
  Tổng cụm: 425 cụm
  Tỷ lệ sạch: 85%
  Tỷ lệ nhiễm: 15%
  Mã lô: MS-20260102-001
```

**Cảnh báo:**
- Tỷ lệ nhiễm > 20%: 🔴 Cảnh báo đỏ
- Tỷ lệ nhiễm 10-20%: ⚠️ Cảnh báo vàng

---

#### Tab 2: Danh sách Mô Soi

**Hiển thị:**
- Tất cả lô Mô Soi
- Thông tin: Mã lô, Giống, Chu kỳ, Ngày soi
- Số liệu: Túi ban đầu, Túi nhiễm, Túi sạch, Cụm/túi
- Tình trạng: Tổng cụm, Đã cấp, Còn lại
- Trạng thái: "Đang sử dụng" / "Đã kết thúc chu kỳ"

**Metrics tổng quan:**
- Lô đang sử dụng
- Tổng cụm còn lại
- Tổng cụm đã cấp
- Lô đã kết thúc

**Màu sắc:**
- 🟢 Xanh: Đang sử dụng, còn cụm
- 🟡 Vàng: Đang sử dụng, gần hết
- 🔴 Đỏ nhạt: Đã kết thúc chu kỳ

---

#### Tab 3: Báo cáo Sử dụng

**Thống kê theo giống:**
- Số lô
- Tổng cụm
- Đã cấp
- Còn lại
- Tỷ lệ nhiễm trung bình

**Biểu đồ:** Stacked bar chart (Đã cấp vs Còn lại)

---

### 2. ĐỐI SOÁT MÔ SOI

**Menu:** "Đối soát Mô Soi"

**Mục đích:** Check & Balance - Kiểm tra tổng Mô Soi có khớp với tổng Mô Mẹ đã cấy hay không

#### Bảng đối soát:

| Tên giống | Tổng cụm Mô Soi | Đã cấp (hệ thống) | Còn lại | Mô Mẹ đã cấy (nhật ký) | Chênh lệch | Trạng thái |
|-----------|----------------|-------------------|---------|------------------------|------------|-----------|
| Đồng tiền đỏ | 425 | 425 | 0 | 425 | 0 | ✅ KHỚP |
| Khoai lang tím | 300 | 200 | 100 | 200 | 0 | ⚠️ DƯ MÔ (100 cụm) |
| Cây xuất khẩu A | 150 | 150 | 0 | 180 | -30 | 🔴 BẤT THƯỜNG (Vượt 30 cụm) |

#### Trạng thái:

1. **✅ KHỚP:** 
   - Tổng Mô Mẹ đã cấp = Tổng Mô Soi đã cấp
   - Dữ liệu chính xác

2. **⚠️ DƯ MÔ:**
   - Còn Mô Soi chưa cấy hết
   - Gợi ý: Đẩy nhanh tiến độ hoặc hủy bỏ nếu để quá lâu

3. **🔴 BẤT THƯỜNG:**
   - Mô Mẹ đã cấp > Mô Soi có sẵn
   - KHÔNG thể xảy ra trong thực tế!
   - Nguyên nhân:
     - Nhân viên nhập nhật ký nhưng không chọn đúng lô Mô Soi
     - Lô Mô Soi chưa được nhập vào hệ thống
     - Dữ liệu nhập sai

#### Metrics tổng quan:
- ✅ Giống khớp
- ⚠️ Giống dư mô
- 🔴 Giống bất thường

---

### 3. LIÊN KẾT VỚI NHẬT KÝ CẤY

**Menu:** "Nhập liệu"

#### Quy trình:

1. **Chọn giống cây**
   - Hệ thống tự động tìm lô Mô Soi khả dụng cho giống đó

2. **Dropdown chọn lô Mô Soi**
   ```
   MS-20260102-001 | Nhân nhanh | Còn: 425 cụm (85 túi x 5 cụm)
   MS-20260103-002 | Ra rễ | Còn: 300 cụm (60 túi x 5 cụm)
   ```

3. **Hiển thị thông tin lô đã chọn:**
   - 📦 Mã lô
   - 🔄 Chu kỳ trước
   - ✅ Còn lại (cụm)
   - 📊 Tối đa (túi)

4. **Nhập số túi mẹ và số cụm/túi**
   - Ví dụ: 10 túi × 5 cụm = 50 cụm

5. **Khi bấm "Lưu":**
   - Hệ thống tự động khấu trừ 50 cụm từ lô Mô Soi
   - Cập nhật: Đã cấp +50, Còn lại -50
   - Lưu `ma_lo_mo_soi` vào nhật ký cấy
   - Hiển thị thông báo thành công

#### Cảnh báo:

**❌ Không có Mô Soi:**
```
🚫 KHÔNG CÓ MÔ SOI CHO GIỐNG: Đồng tiền đỏ

Nguyên nhân:
- Chưa nhập kết quả kiểm tra Mô Soi từ phòng sáng
- Mô Soi của giống này đã hết

Hành động:
1. Vào trang "Quản lý Mô Soi"
2. Nhập kết quả kiểm tra từ chu kỳ trước
3. Quay lại nhập nhật ký cấy

⚠️ KHÔNG THỂ NHẬP NHẬT KÝ nếu không có Mô Soi!
```

**⚠️ Không đủ cụm:**
```
⚠️ Mô soi Đồng tiền đỏ chỉ còn 30 cụm, không đủ 50 cụm

Hành động:
- Giảm số túi mẹ hoặc số cụm/túi
- Hoặc nhập thêm Mô Soi cho giống này
```

---

## 🔄 LOGIC TỰ ĐỘNG

### 1. Khấu trừ FIFO

- Khi nhập nhật ký cấy, hệ thống tự động:
  1. Tính số cụm cần dùng = Số túi mẹ × Số cụm/túi mẹ
  2. Kiểm tra lô Mô Soi còn đủ không
  3. Khấu trừ số cụm
  4. Cập nhật: `so_cum_da_cap` và `so_cum_con_lai`
  5. Lưu `ma_lo_mo_soi` vào nhật ký

### 2. Tự động đánh dấu hết chu kỳ

- Khi `so_cum_con_lai` = 0:
  - Trạng thái → "Đã kết thúc chu kỳ"
  - Hiển thị màu đỏ nhạt trong bảng
  - Không còn xuất hiện trong dropdown chọn lô

### 3. Đối soát tự động

- Dashboard "Đối soát Mô Soi" tự động:
  1. Tính tổng cụm Mô Soi từ bảng `mo_soi`
  2. Tính tổng cụm Mô Mẹ từ bảng `nhat_ky_cay`
  3. So sánh và phân loại trạng thái
  4. Hiển thị cảnh báo nếu bất thường

---

## 📊 DATABASE SCHEMA

### Bảng `mo_soi`:

```sql
CREATE TABLE mo_soi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ma_lo_mo_soi TEXT UNIQUE NOT NULL,
    ten_giong TEXT NOT NULL,
    chu_ky_truoc TEXT NOT NULL,
    ngay_soi TEXT NOT NULL,
    tuan_soi INTEGER NOT NULL,
    nam INTEGER NOT NULL,
    so_luong_ban_dau INTEGER NOT NULL,
    so_tui_nhiem INTEGER NOT NULL,
    so_tui_sach INTEGER NOT NULL,
    so_cum_moi_tui INTEGER NOT NULL,
    tong_cum_sach INTEGER NOT NULL,
    so_cum_da_cap INTEGER DEFAULT 0,
    so_cum_con_lai INTEGER NOT NULL,
    trang_thai TEXT NOT NULL DEFAULT 'Đang sử dụng',
    nguoi_soi TEXT NOT NULL,
    ma_nhan_vien TEXT NOT NULL,
    ghi_chu TEXT,
    ngay_tao TEXT NOT NULL,
    ngay_cap_nhat TEXT NOT NULL
);
```

### Bảng `nhat_ky_cay` (cột mới):

```sql
ALTER TABLE nhat_ky_cay ADD COLUMN ma_lo_mo_soi TEXT;
```

---

## 🎯 USE CASE

### Case 1: Nhập Mô Soi mới

```
1. Phòng Sáng hoàn thành chu kỳ "Nhân nhanh" cho "Đồng tiền đỏ"
2. Kiểm tra: 100 túi ban đầu, 15 túi nhiễm, 85 túi sạch, 5 cụm/túi
3. Vào "Quản lý Mô Soi" → Tab "Nhập Mô Soi"
4. Nhập thông tin
5. Hệ thống tính: 425 cụm sạch (85×5)
6. Lưu → Mã lô: MS-20260102-001
7. Trạng thái: "Đang sử dụng"
```

### Case 2: Nhập Nhật ký Cấy

```
1. Nhân viên vào "Nhập liệu"
2. Chọn giống: "Đồng tiền đỏ"
3. Hệ thống hiện dropdown:
   "MS-20260102-001 | Nhân nhanh | Còn: 425 cụm"
4. Chọn lô MS-20260102-001
5. Nhập: 10 túi mẹ, 5 cụm/túi → 50 cụm
6. Nhập các thông tin khác
7. Bấm "Lưu"
8. Hệ thống:
   - Khấu trừ 50 cụm từ MS-20260102-001
   - Cập nhật: Đã cấp = 50, Còn lại = 375
   - Lưu ma_lo_mo_soi vào nhật ký
9. Thông báo:
   "✅ Lưu thành công!
   🔬 Đã khấu trừ 50 cụm từ lô MS-20260102-001
   📊 Lô Mô Soi còn lại: 375 cụm"
```

### Case 3: Hết Mô Soi

```
1. Lô MS-20260102-001 còn 20 cụm
2. Nhân viên nhập nhật ký: 4 túi × 5 cụm = 20 cụm
3. Bấm "Lưu"
4. Hệ thống khấu trừ 20 cụm
5. Còn lại = 0
6. Tự động đánh dấu: "Đã kết thúc chu kỳ"
7. Lô không còn xuất hiện trong dropdown
```

### Case 4: Không đủ Mô Soi

```
1. Lô còn 20 cụm
2. Nhân viên nhập: 10 túi × 5 cụm = 50 cụm
3. Bấm "Lưu"
4. Hệ thống cảnh báo:
   "⚠️ Mô soi chỉ còn 20 cụm, không đủ 50 cụm"
5. KHÔNG LƯU nhật ký
6. Gợi ý giảm số túi hoặc nhập thêm Mô Soi
```

### Case 5: Đối soát phát hiện bất thường

```
1. Admin vào "Đối soát Mô Soi"
2. Hệ thống tính:
   - Tổng Mô Soi "Đồng tiền đỏ": 425 cụm
   - Đã cấp (hệ thống): 425 cụm
   - Mô Mẹ đã cấy (nhật ký): 450 cụm
   - Chênh lệch: -25 cụm
3. Trạng thái: "🔴 BẤT THƯỜNG (Vượt 25 cụm)"
4. Cảnh báo đỏ:
   "🚨 CẢNH BÁO NGHIÊM TRỌNG!
   Dữ liệu bất thường - cần kiểm tra lại!"
5. Admin kiểm tra:
   - Phát hiện 1 nhân viên nhập nhật ký không chọn lô Mô Soi
   - Sửa lại dữ liệu
   - Đối soát lại → ✅ KHỚP
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. BẮT BUỘC phải có Mô Soi trước khi nhập nhật ký
- Nếu không có Mô Soi cho giống đó, KHÔNG THỂ nhập nhật ký cấy

### 2. Quy trình ĐÚNG:
```
Phòng Sáng kiểm tra
    ↓
Nhập Mô Soi vào hệ thống
    ↓
Mới được nhập Nhật ký Cấy
```

### 3. Quy trình SAI (sẽ bị chặn):
```
Nhập Nhật ký Cấy trước
    ↓
❌ HỆ THỐNG CHẶN: "Không có Mô Soi!"
```

### 4. Đối soát thường xuyên:
- Admin nên vào "Đối soát Mô Soi" mỗi ngày
- Kiểm tra có bất thường không
- Xử lý ngay nếu phát hiện sai sót

### 5. Mô Soi còn dư:
- Nếu để quá lâu, chất lượng giảm
- Nên đẩy nhanh tiến độ cấy
- Hoặc hủy bỏ và nhập lô mới

---

## 🚀 TRIỂN KHAI

```powershell
cd D:\QUANLYLAB
git add app.py
git commit -m "Feature: Add Mo Soi Management System"
git push origin master
```

**Reboot Streamlit Cloud:**
1. Vào https://share.streamlit.io
2. Reboot app: QuanLyPhongLabGSH
3. Đợi 2-5 phút
4. Test: https://quanlyphonglabgsh-upgfgca3bsddruuap6qja2.streamlit.app/

---

**Green Straw Hat - Happiness Together 🌱**

**Phiên bản:** 2.1
**Ngày:** 02/01/2026
**Tính năng:** Quản lý Mô Soi hoàn chỉnh với Check & Balance

