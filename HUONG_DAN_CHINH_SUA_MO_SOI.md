# ✏️ HƯỚNG DẪN: CHỈNH SỬA MÔ SOI

## 🎯 MỤC ĐÍCH

Sau khi nhập Mô Soi, hệ thống tự động hiển thị danh sách bên dưới với khả năng chỉnh sửa nhanh.

**LỢI ÍCH:**
- ✅ Xem ngay kết quả vừa nhập
- ✅ Sửa lỗi nhanh chóng (nếu có)
- ✅ Không cần chuyển tab
- ✅ Giao diện thân thiện
- ✅ Tương tự trang "Nhập liệu" (UX nhất quán)

---

## 📋 GIAO DIỆN MỚI

### **1. Sau khi nhập Mô Soi:**

```
✅ ĐÃ LƯU MÔ SOI THÀNH CÔNG!

📦 Mã lô: MS20260102001
🌱 Giống: Đồng tiền đỏ
✅ Tổng cụm sạch: 450 cụm
📊 Tỷ lệ sạch: 90.0%

➡️ Lô này sẽ được dùng để cấp Mô Mẹ cho chu kỳ tiếp theo.

───────────────────────────────────────────────────

📋 DANH SÁCH MÔ SOI ĐÃ NHẬP

📊 Hiển thị 5 lô mô soi gần nhất

┌─────────────────────────────────────────────────────┐
│ 🔄 MS20260102001 - Đồng tiền đỏ (Nhân nhanh)        │
│    Ngày: 2026-01-02                        [✏️ Sửa] │
├─────────────────────────────────────────────────────┤
│ 📦 Thông tin Mô Soi:                                │
│ - Mã lô: MS20260102001                              │
│ - Giống: Đồng tiền đỏ | Chu kỳ trước: Nhân nhanh   │
│ - Ngày soi: 2026-01-02                              │
│ - Ban đầu: 100 túi | Nhiễm: 10 túi | Sạch: 90 túi  │
│ - Tỷ lệ sạch: 90.0%                                 │
│                                                     │
│ 🔢 Tình trạng sử dụng:                              │
│ - Tổng cụm sạch: 450 cụm                            │
│ - Đã cấp: 0 cụm (0.0%)                              │
│ - Còn lại: 450 cụm                                  │
│ - Trạng thái: Đang sử dụng                          │
│                                                     │
│ 👤 Người thực hiện:                                 │
│ - Tên: Admin | Mã: ADMIN                            │
│ - Ghi chú: Kết quả kiểm tra lô cấy ngày 01/01      │
└─────────────────────────────────────────────────────┘
```

---

### **2. Khi click "✏️ Sửa":**

```
┌─────────────────────────────────────────────────────┐
│ ✏️ Chỉnh sửa Mô Soi                                 │
├─────────────────────────────────────────────────────┤
│ 🔢 Cập nhật kết quả kiểm tra                        │
│                                                     │
│ ┌────────────┬────────────┬────────────────────┐   │
│ │ Tổng số túi│ Số túi nhiễm│ Số cụm/túi sạch   │   │
│ │ ban đầu    │             │                    │   │
│ │ [100     ↕]│ [10      ↕] │ [5             ↕]  │   │
│ └────────────┴────────────┴────────────────────┘   │
│                                                     │
│ 📊 Kết quả: 90 túi sạch × 5 cụm = 450 cụm sạch     │
│                                                     │
│ Ghi chú:                                            │
│ ┌───────────────────────────────────────────────┐   │
│ │ Kết quả kiểm tra lô cấy ngày 01/01           │   │
│ │                                               │   │
│ └───────────────────────────────────────────────┘   │
│                                                     │
│ ┌────────────────────┬───────────────────────────┐  │
│ │ [💾 Lưu thay đổi]  │ [❌ Hủy]                  │  │
│ └────────────────────┴───────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🎨 ICON TRẠNG THÁI

Hệ thống tự động hiển thị icon dựa trên tình trạng sử dụng:

| Icon | Trạng thái | Điều kiện |
|------|-----------|-----------|
| 🔄 | Đang sử dụng | Còn > 20% cụm |
| ⚠️ | Sắp hết | Đã dùng > 80% |
| ✅ | Đã kết thúc chu kỳ | Hệ thống đánh dấu |

---

## 🚀 USE CASE

### **Case 1: Nhập Mô Soi mới**

```
08:00 - Admin nhập kết quả kiểm tra
↓
Điền form:
  - Giống: Đồng tiền đỏ
  - Chu kỳ trước: Nhân nhanh
  - Ngày soi: 02/01/2026
  - Tổng túi ban đầu: 100
  - Túi nhiễm: 10
  - Cụm/túi sạch: 5
↓
Hệ thống tính:
  - Túi sạch: 90
  - Tổng cụm sạch: 450
  - Tỷ lệ sạch: 90%
↓
Click "💾 Lưu Mô Soi"
↓
✅ Thông báo thành công
↓
🎈 Balloons animation
↓
📋 Danh sách hiển thị ngay bên dưới
↓
Thấy lô vừa nhập ở đầu danh sách
```

---

### **Case 2: Phát hiện nhập sai ngay sau đó**

```
08:05 - Admin phát hiện nhập sai "Số túi nhiễm"
        (Thực tế là 8 túi, không phải 10 túi)
↓
Cuộn xuống phần "📋 Danh sách Mô Soi đã nhập"
↓
Tìm lô vừa nhập (MS20260102001)
↓
Click [✏️ Sửa]
↓
Form chỉnh sửa hiển thị
↓
Sửa: "Số túi nhiễm" từ 10 → 8
↓
Hệ thống tự động tính lại:
  - Túi sạch: 92 (thay vì 90)
  - Tổng cụm sạch: 460 (thay vì 450)
↓
Click "💾 Lưu thay đổi"
↓
✅ Thông báo: "Đã cập nhật Mô Soi thành công!"
↓
Trang refresh, hiển thị dữ liệu mới
```

---

### **Case 3: Admin kiểm tra lại lô cũ**

```
10:00 - Admin cần kiểm tra lại kết quả lô ngày hôm trước
↓
Cuộn xuống phần "📋 Danh sách Mô Soi đã nhập"
↓
Tìm lô cần kiểm tra (MS20260101001)
↓
Click vào expander để mở rộng
↓
Xem đầy đủ thông tin:
  - Số túi ban đầu, nhiễm, sạch
  - Tỷ lệ sạch
  - Tổng cụm, đã cấp, còn lại
  - Tỷ lệ sử dụng
  - Người soi, ghi chú
↓
Nếu cần sửa → Click [✏️ Sửa]
↓
Nếu không → Đóng expander
```

---

## 🔐 PHÂN QUYỀN

### **Admin:**
- ✅ Nhập Mô Soi mới
- ✅ Xem danh sách tất cả lô
- ✅ **Sửa bất kỳ lô nào**
- ✅ Xem báo cáo đối soát

### **Nhân viên:**
- ❌ Không có quyền truy cập trang này
- ℹ️ "Quản lý Mô Soi" chỉ dành cho Admin

---

## 📊 THÔNG TIN HIỂN THỊ

### **1. Thông tin Mô Soi:**
```
📦 Mã lô: MS20260102001
🌱 Giống: Đồng tiền đỏ
🔄 Chu kỳ trước: Nhân nhanh
📅 Ngày soi: 2026-01-02
📊 Kết quả kiểm tra:
   - Tổng túi ban đầu: 100
   - Túi nhiễm: 10
   - Túi sạch: 90
   - Tỷ lệ sạch: 90.0%
```

---

### **2. Tình trạng sử dụng:**
```
🔢 Số liệu:
   - Tổng cụm sạch: 450 cụm
   - Đã cấp cho nhân viên: 120 cụm
   - Còn lại trong kho: 330 cụm
   - Tỷ lệ đã dùng: 26.7%
   - Trạng thái: Đang sử dụng
```

---

### **3. Người thực hiện:**
```
👤 Thông tin:
   - Tên: Nguyễn Văn A
   - Mã nhân viên: NVA
   - Ghi chú: Kết quả kiểm tra lô cấy ngày 01/01
```

---

## ✏️ CHỨC NĂNG CHỈNH SỬA

### **CÓ THỂ SỬA:**
- ✅ Số túi ban đầu
- ✅ Số túi nhiễm
- ✅ Số cụm mỗi túi sạch
- ✅ Ghi chú

### **TỰ ĐỘNG TÍNH LẠI:**
- 🔄 Số túi sạch = Ban đầu - Nhiễm
- 🔄 Tổng cụm sạch = Túi sạch × Cụm/túi
- 🔄 Số cụm còn lại = Tổng cụm sạch - Đã cấp

### **KHÔNG THỂ SỬA:**
- ❌ Mã lô (tự động tạo)
- ❌ Tên giống (chọn khi nhập)
- ❌ Chu kỳ trước (chọn khi nhập)
- ❌ Ngày soi (chọn khi nhập)
- ❌ Số cụm đã cấp (tự động từ nhật ký cấy)
- ❌ Người soi (ghi nhận khi nhập)

---

## 🔢 LOGIC TÍNH TOÁN

### **Khi nhập mới:**

```python
# Input từ form:
so_luong_ban_dau = 100
so_tui_nhiem = 10
so_cum_moi_tui = 5

# Tính toán:
so_tui_sach = so_luong_ban_dau - so_tui_nhiem  # 90
tong_cum_sach = so_tui_sach * so_cum_moi_tui    # 450
so_cum_da_cap = 0                                # Chưa dùng
so_cum_con_lai = tong_cum_sach                   # 450
trang_thai = 'Đang sử dụng'
```

---

### **Khi chỉnh sửa:**

```python
# Input từ form edit:
edit_so_luong_ban_dau = 100
edit_so_tui_nhiem = 8  # Sửa từ 10 → 8
edit_so_cum_moi_tui = 5

# Tính toán lại:
edit_so_tui_sach = edit_so_luong_ban_dau - edit_so_tui_nhiem  # 92
edit_tong_cum_sach = edit_so_tui_sach * edit_so_cum_moi_tui    # 460

# GIỮ NGUYÊN số đã cấp (từ database):
so_cum_da_cap = 0  # (từ database, không thay đổi)

# Tính lại còn lại:
edit_so_cum_con_lai = edit_tong_cum_sach - so_cum_da_cap  # 460
```

---

### **Khi nhân viên cấy sử dụng Mô Soi:**

```python
# Nhân viên chọn lô mô soi trong form cấy:
ma_lo_mo_soi = "MS20260102001"
so_cum_can_dung = 50

# Hệ thống tự động khấu trừ:
UPDATE mo_soi
SET so_cum_da_cap = so_cum_da_cap + 50,     # 0 + 50 = 50
    so_cum_con_lai = so_cum_con_lai - 50    # 460 - 50 = 410
WHERE ma_lo_mo_soi = "MS20260102001"
```

---

## 📱 TỐI ƯU MOBILE

### **Layout responsive:**

```python
# Desktop: Info (3 phần) | Action (1 phần)
col_info, col_action = st.columns([3, 1])

# Mobile: Tự động stack thành 2 hàng
```

---

### **Expander:**

```python
# Mỗi lô là 1 expander riêng
with st.expander("🔄 MS20260102001 - Đồng tiền đỏ"):
    # Nội dung chi tiết
    # Click để mở/đóng
```

✅ **LỢI ÍCH:**
- Tiết kiệm không gian màn hình
- Dễ tìm kiếm lô cần xem
- Không bị quá tải thông tin

---

## ⚡ SO SÁNH TRƯỚC & SAU

### **TRƯỚC:**

```
❌ Sau khi nhập Mô Soi:
   - Chỉ có thông báo thành công
   - Muốn xem lại → Phải chuyển sang Tab 2
   - Muốn sửa → Không có chức năng
   - Phải xóa và nhập lại từ đầu
```

---

### **SAU:**

```
✅ Sau khi nhập Mô Soi:
   - Thông báo thành công
   - Hiển thị danh sách NGAY BÊN DƯỚI
   - Mỗi lô có nút [✏️ Sửa]
   - Click sửa → Form inline hiện ra
   - Lưu → Cập nhật ngay
   - UX mượt mà, tiết kiệm thời gian
```

---

## 🎯 LỢI ÍCH TỔNG THỂ

| Tính năng | Trước | Sau |
|-----------|-------|-----|
| Xem lại sau khi nhập | ❌ Phải chuyển tab | ✅ Hiển thị ngay |
| Sửa nếu sai | ❌ Không có | ✅ Click [Sửa] |
| Thời gian xử lý | ⏱️ Lâu | ⚡ Nhanh |
| Số bước thao tác | 📊 Nhiều | 📊 Ít |
| Trải nghiệm | ❌ Rời rạc | ✅ Liền mạch |
| Mobile-friendly | ❌ Khó dùng | ✅ Dễ dùng |

---

## 🔧 KỸ THUẬT

### **1. Hiển thị danh sách:**

```python
# Query 20 lô gần nhất
df_mo_soi = pd.read_sql_query('''
    SELECT * FROM mo_soi
    ORDER BY ngay_tao DESC
    LIMIT 20
''', conn)

# Loop và hiển thị từng lô
for idx, row in df_mo_soi.iterrows():
    with st.expander(f"{icon} {row['ma_lo_mo_soi']} - {row['ten_giong']}"):
        # Hiển thị thông tin chi tiết
        # Nút [✏️ Sửa]
```

---

### **2. Logic edit:**

```python
# Lưu trạng thái edit trong session_state
if st.button("✏️ Sửa", key=f"edit_mosoi_{row['id']}"):
    st.session_state[f'editing_mosoi_{row["id"]}'] = True
    st.rerun()

# Hiển thị form edit nếu trạng thái = True
if st.session_state.get(f'editing_mosoi_{row["id"]}', False):
    with st.form(f"form_edit_mosoi_{row['id']}"):
        # Form chỉnh sửa
        # Nút Lưu/Hủy
```

---

### **3. Update database:**

```python
if submitted_edit:
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        UPDATE mo_soi
        SET so_luong_ban_dau = ?, so_tui_nhiem = ?, 
            so_tui_sach = ?, so_cum_moi_tui = ?,
            tong_cum_sach = ?, so_cum_con_lai = ?,
            ghi_chu = ?, ngay_cap_nhat = ?
        WHERE id = ?
    ''', (
        edit_so_luong_ban_dau, edit_so_tui_nhiem, 
        edit_so_tui_sach, edit_so_cum_moi_tui,
        edit_tong_cum_sach, edit_so_cum_con_lai,
        edit_ghi_chu, datetime.now(), row['id']
    ))
    conn.commit()
    conn.close()
    st.success("✅ Đã cập nhật!")
    st.rerun()
```

---

## ✅ CHECKLIST TRIỂN KHAI

- [x] Thêm section "Danh sách Mô Soi đã nhập" sau form
- [x] Query 20 lô gần nhất từ database
- [x] Hiển thị mỗi lô trong expander riêng biệt
- [x] Tính toán và hiển thị icon trạng thái
- [x] Hiển thị thông tin đầy đủ (mô soi + sử dụng + người thực hiện)
- [x] Thêm nút [✏️ Sửa] (chỉ Admin)
- [x] Implement form chỉnh sửa inline
- [x] Logic tính toán lại khi edit
- [x] Update database khi save
- [x] Xử lý trạng thái session_state
- [x] Nút Lưu/Hủy
- [x] Thông báo thành công và refresh
- [x] Tối ưu layout cho mobile
- [x] Test chức năng edit
- [x] Test tính toán lại số liệu

---

## 📞 HỖ TRỢ

**Nếu không thấy danh sách:**
- ✅ Kiểm tra đã nhập ít nhất 1 lô Mô Soi chưa
- ✅ Kiểm tra database có bảng `mo_soi` không

**Nếu không sửa được:**
- ✅ Kiểm tra quyền: Chỉ Admin mới sửa được
- ✅ Kiểm tra `is_admin = True` trong session_state

**Nếu số liệu tính sai:**
- ✅ Kiểm tra công thức: `so_cum_con_lai = tong_cum_sach - so_cum_da_cap`
- ✅ Kiểm tra số cụm đã cấp không bị sửa

---

**🌱 Green Straw Hat - Happiness Together**

*Mô Soi giờ dễ quản lý và chỉnh sửa hơn bao giờ hết!*

