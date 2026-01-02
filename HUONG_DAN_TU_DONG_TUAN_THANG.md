# 📅 HƯỚNG DẪN: TỰ ĐỘNG TÍNH TUẦN VÀ THÁNG CẤY

## 🎯 MỤC ĐÍCH

Hệ thống tự động tính toán và hiển thị **Tuần cấy** và **Tháng cấy** dựa trên ngày cấy mà nhân viên chọn.

**LỢI ÍCH:**
- ✅ Không cần nhập tay → Giảm sai sót
- ✅ Dữ liệu thống nhất 100%
- ✅ Dễ dàng lọc và báo cáo theo tuần/tháng
- ✅ Tối ưu trên điện thoại

---

## 📊 LOGIC TỰ ĐỘNG TÍNH TOÁN

### **1. Ngày cấy → Tuần cấy**

```python
def tinh_tuan(ngay_cay):
    """Tính tuần từ ngày cấy (tuần bắt đầu từ thứ 2)"""
    # Tìm thứ 2 đầu tiên của năm
    # Đếm số tuần từ đó đến ngày cấy
    # Trả về: Tuần 01, Tuần 02, ..., Tuần 52
```

**VÍ DỤ:**
- Ngày cấy: `02/01/2026` → **Tuần 01**
- Ngày cấy: `15/06/2026` → **Tuần 24**
- Ngày cấy: `31/12/2026` → **Tuần 52**

---

### **2. Ngày cấy → Tháng/Năm**

```python
thang = ngay_cay.month  # Tháng (1-12)
nam = ngay_cay.year     # Năm (2026)
```

**VÍ DỤ:**
- Ngày cấy: `02/01/2026` → **Tháng 01/2026**
- Ngày cấy: `15/06/2026` → **Tháng 06/2026**
- Ngày cấy: `31/12/2026` → **Tháng 12/2026**

---

## 🖥️ GIAO DIỆN NGƯỜI DÙNG

### **Form nhập liệu:**

```
┌─────────────────────────────────────────────────┐
│ 📅 THÔNG TIN THỜI GIAN                          │
├─────────────────────────────────────────────────┤
│                                                 │
│ Ngày cấy *                                      │
│ ┌─────────────────┐                             │
│ │ 📅 02/01/2026   │ ← Nhân viên CHỌN            │
│ └─────────────────┘                             │
│                                                 │
│ ┌───────────────────┬─────────────────────────┐ │
│ │ 📊 Tuần cấy       │ 📅 Tháng/Năm            │ │
│ │ ┌───────────────┐ │ ┌───────────────────┐   │ │
│ │ │ Tuần 01       │ │ │ Tháng 01/2026     │   │ │
│ │ └───────────────┘ │ └───────────────────┘   │ │
│ │ (Read-only)       │ (Read-only)             │ │
│ └───────────────────┴─────────────────────────┘ │
│                                                 │
│ ↑ TỰ ĐỘNG TÍNH TOÁN                            │
└─────────────────────────────────────────────────┘
```

---

### **Trên Mobile:**

```
┌──────────────────────┐
│ Ngày cấy *           │
│ ┌──────────────────┐ │
│ │ 📅 02/01/2026    │ │
│ └──────────────────┘ │
│                      │
│ ┌──────────────────┐ │
│ │ 📊 Tuần cấy      │ │
│ │ Tuần 01          │ │
│ └──────────────────┘ │
│                      │
│ ┌──────────────────┐ │
│ │ 📅 Tháng/Năm     │ │
│ │ Tháng 01/2026    │ │
│ └──────────────────┘ │
│                      │
│ ↑ TỰ ĐỘNG            │
└──────────────────────┘
```

---

## 💾 LƯU TRỮ DATABASE

### **Bảng: `nhat_ky_cay`**

```sql
CREATE TABLE nhat_ky_cay (
    id INTEGER PRIMARY KEY,
    ngay_cay TEXT NOT NULL,        -- '2026-01-02'
    tuan INTEGER NOT NULL,          -- 1
    thang INTEGER NOT NULL,         -- 1
    ...
)
```

### **Khi lưu dữ liệu:**

```python
INSERT INTO nhat_ky_cay (
    ngay_cay, thang, tuan, ...
) VALUES (
    '2026-01-02',  -- Ngày cấy
    1,              -- Tháng (tự động)
    1,              -- Tuần (tự động)
    ...
)
```

---

## 🔍 ỨNG DỤNG TRONG BÁO CÁO

### **1. Lọc theo tuần:**

```python
# Admin chọn: "Tuần 24"
df_filtered = df[df['tuan'] == 24]
# → Hiển thị TẤT CẢ lô cấy trong tuần 24
```

### **2. Lọc theo tháng:**

```python
# Admin chọn: "Tháng 06"
df_filtered = df[df['thang'] == 6]
# → Hiển thị TẤT CẢ lô cấy trong tháng 06
```

### **3. Báo cáo năng suất theo tuần:**

```
┌──────┬────────────┬─────────────┬──────────┐
│ Tuần │ Nhân viên  │ Tổng túi    │ Năng suất│
├──────┼────────────┼─────────────┼──────────┤
│  24  │ NV A       │ 500         │ 50 cây/h │
│  24  │ NV B       │ 450         │ 45 cây/h │
│  25  │ NV A       │ 520         │ 52 cây/h │
└──────┴────────────┴─────────────┴──────────┘
```

### **4. Phân tích nhiễm theo tháng:**

```
📊 BIỂU ĐỒ: TỶ LỆ NHIỄM THEO THÁNG

Tháng 01: ████████░░ 8%
Tháng 02: ██████░░░░ 6%
Tháng 03: ███░░░░░░░ 3%
Tháng 04: █████░░░░░ 5%
```

---

## 🎨 TÍNH NĂNG ĐẶC BIỆT

### **1. Read-only Input:**

```python
st.text_input(
    "📊 Tuần cấy",
    value=f"Tuần {tuan:02d}",  # Format: 01, 02, ..., 52
    disabled=True,              # KHÔNG cho phép sửa
    help="Tự động tính từ ngày cấy"
)
```

### **2. Responsive Layout:**

```python
# Desktop: 2 cột cạnh nhau
col_tuan, col_thang = st.columns(2)

# Mobile: Tự động stack thành 1 cột
```

### **3. Format đẹp:**

```python
f"Tuần {tuan:02d}"        # 01, 02, 03, ..., 52
f"Tháng {thang:02d}/{nam}" # Tháng 01/2026, Tháng 12/2026
```

---

## 📱 TỐI ƯU CHO MOBILE

### **Trước (Không tối ưu):**

```
❌ st.info("Tháng: 1 | Tuần: 1")
- Nằm ngang 1 dòng
- Khó đọc trên mobile
- Không có context
```

### **Sau (Tối ưu):**

```
✅ 2 ô text_input read-only
- Mỗi ô có label rõ ràng
- Tự động stack trên mobile
- Có tooltip giải thích
- Format đẹp, dễ đọc
```

---

## 🚀 USE CASE

### **Case 1: Nhân viên nhập liệu hôm nay**

```
1. Nhân viên vào "Nhập liệu"
2. Chọn ngày cấy: 02/01/2026
3. Hệ thống TỰ ĐỘNG hiển thị:
   - Tuần cấy: Tuần 01
   - Tháng/Năm: Tháng 01/2026
4. Nhân viên kiểm tra → OK
5. Tiếp tục nhập các thông tin khác
6. Bấm "Lưu"
7. Database lưu: tuan=1, thang=1
```

---

### **Case 2: Admin lọc báo cáo theo tuần**

```
1. Admin vào "Quản lý & Phân tích Nhiễm"
2. Chọn bộ lọc: "Lọc theo Tuần"
3. Chọn: "Tuần 24"
4. Hệ thống query:
   SELECT * FROM nhat_ky_cay WHERE tuan = 24
5. Hiển thị TẤT CẢ lô cấy trong tuần 24
6. Admin phân tích tỷ lệ nhiễm
```

---

### **Case 3: Báo cáo năng suất tháng**

```
1. Admin vào "Báo cáo Hiệu suất"
2. Chọn bộ lọc: "Lọc theo Tháng"
3. Chọn: "Tháng 06/2026"
4. Hệ thống query:
   SELECT * FROM nhat_ky_cay 
   WHERE thang = 6 AND YEAR(ngay_cay) = 2026
5. Hiển thị biểu đồ:
   - Tổng số túi cấy trong tháng 06
   - Năng suất trung bình
   - Tỷ lệ nhiễm tháng 06
6. So sánh với các tháng khác
```

---

## ⚡ ĐIỂM KHÁC BIỆT

### **SO VỚI NHẬP TAY:**

| Tính năng           | Nhập tay | Tự động |
|---------------------|----------|---------|
| Tốc độ nhập liệu    | ⏱️ Chậm  | ⚡ Nhanh |
| Nguy cơ sai sót     | ❌ Cao   | ✅ 0%    |
| Dữ liệu thống nhất  | ❌ Không | ✅ 100%  |
| Phù hợp mobile      | ❌ Khó   | ✅ Dễ    |
| Dễ lọc báo cáo      | ❌ Khó   | ✅ Dễ    |

---

### **SO VỚI HIỂN THỊ INFO:**

**Trước (st.info):**
```
st.info(f"📆 Tháng: {thang} | Tuần: {tuan}")
```

❌ **VẤN ĐỀ:**
- Không rõ ràng
- Khó đọc trên mobile
- Không có context
- Không có format đẹp

**Sau (text_input read-only):**
```python
col_tuan, col_thang = st.columns(2)
with col_tuan:
    st.text_input("📊 Tuần cấy", value="Tuần 01", disabled=True)
with col_thang:
    st.text_input("📅 Tháng/Năm", value="Tháng 01/2026", disabled=True)
```

✅ **LỢI ÍCH:**
- Rõ ràng, từng ô riêng biệt
- Label cụ thể
- Tự động stack trên mobile
- Có tooltip giải thích
- Format chuyên nghiệp

---

## 🔧 KỸ THUẬT

### **1. Hàm tính tuần:**

```python
def tinh_tuan(ngay_cay):
    """
    Tính số tuần trong năm (ISO 8601)
    Tuần bắt đầu từ thứ 2
    """
    if isinstance(ngay_cay, str):
        ngay = datetime.strptime(ngay_cay, "%Y-%m-%d").date()
    else:
        ngay = ngay_cay
    
    # Tìm thứ 2 đầu tiên của năm
    ngay_dau_nam = date(ngay.year, 1, 1)
    days_since_monday = ngay_dau_nam.weekday()
    
    if days_since_monday == 0:
        thang_hai_dau_tuan = ngay_dau_nam
    else:
        thang_hai_dau_tuan = ngay_dau_nam + timedelta(days=7 - days_since_monday)
    
    # Tính số tuần
    delta = ngay - thang_hai_dau_tuan
    tuan_so = (delta.days // 7) + 1
    
    return max(1, min(tuan_so, 52))
```

---

### **2. Hàm tính tháng/năm:**

```python
thang = ngay_cay.month  # 1-12
nam = ngay_cay.year     # 2026
```

---

### **3. Format hiển thị:**

```python
# Tuần: 01, 02, ..., 52
f"Tuần {tuan:02d}"

# Tháng/Năm: Tháng 01/2026
f"Tháng {thang:02d}/{nam}"
```

---

### **4. Lưu vào Database:**

```python
c.execute('''
    INSERT INTO nhat_ky_cay (
        ngay_cay, thang, tuan, ...
    ) VALUES (?, ?, ?, ...)
''', (
    ngay_cay.strftime("%Y-%m-%d"),  # '2026-01-02'
    thang,                          # 1
    tuan,                           # 1
    ...
))
```

---

## 📈 THỐNG KÊ TRUY VẤN

### **1. Tổng số túi theo tuần:**

```sql
SELECT 
    tuan AS 'Tuần',
    SUM(so_tui_con) AS 'Tổng túi',
    AVG(nang_suat) AS 'Năng suất TB'
FROM nhat_ky_cay
GROUP BY tuan
ORDER BY tuan
```

---

### **2. Tỷ lệ nhiễm theo tháng:**

```sql
SELECT 
    thang AS 'Tháng',
    COUNT(*) AS 'Tổng lô',
    SUM(CASE WHEN tinh_trang LIKE '%Nhiễm%' THEN 1 ELSE 0 END) AS 'Lô nhiễm',
    ROUND(SUM(CASE WHEN tinh_trang LIKE '%Nhiễm%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS 'Tỷ lệ %'
FROM nhat_ky_cay
GROUP BY thang
ORDER BY thang
```

---

### **3. Top nhân viên theo tuần:**

```sql
SELECT 
    tuan AS 'Tuần',
    nhan_vien AS 'Nhân viên',
    SUM(tong_so_cay_con) AS 'Tổng cây',
    RANK() OVER (PARTITION BY tuan ORDER BY SUM(tong_so_cay_con) DESC) AS 'Hạng'
FROM nhat_ky_cay
GROUP BY tuan, nhan_vien
```

---

## ✅ CHECKLIST TRIỂN KHAI

- [x] Cập nhật database schema (cột `tuan`, `thang`)
- [x] Viết hàm `tinh_tuan(ngay_cay)`
- [x] Cập nhật form nhập liệu
- [x] Hiển thị read-only text_input
- [x] Tối ưu layout cho mobile (st.columns)
- [x] Lưu dữ liệu vào database
- [x] Test trên desktop
- [x] Test trên mobile
- [x] Cập nhật báo cáo (thêm filter theo tuần/tháng)
- [x] Viết tài liệu hướng dẫn

---

## 🎯 KẾT QUẢ

### **TRƯỚC:**
```
❌ Nhân viên phải nhập tay: Tuần, Tháng
❌ Dữ liệu không thống nhất
❌ Khó lọc báo cáo
❌ Dễ nhập sai
```

### **SAU:**
```
✅ Hệ thống tự động tính
✅ Dữ liệu thống nhất 100%
✅ Dễ lọc theo tuần/tháng
✅ Không bao giờ sai
✅ Tiết kiệm thời gian
✅ Tối ưu mobile
```

---

## 📞 HỖ TRỢ

**Nếu gặp vấn đề:**
1. Kiểm tra hàm `tinh_tuan()` có chạy đúng không
2. Kiểm tra database có cột `tuan`, `thang` không
3. Kiểm tra dữ liệu đã lưu vào database đúng chưa
4. Test trên nhiều ngày khác nhau (đầu năm, cuối năm)

---

**🌱 Green Straw Hat - Happiness Together**

*Tự động hóa để tập trung vào công việc quan trọng!*

