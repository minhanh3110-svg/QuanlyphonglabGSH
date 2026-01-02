# 🔬 HỆ THỐNG PHÂN LOẠI NHIỄM THEO MÃ

## Phiên bản: 2.2 - Infection Classification System

---

## 📋 TỔNG QUAN

Hệ thống phân loại tình trạng nhiễm dựa trên **MÃ SỐ** để phân biệt rõ ràng giữa:
- Lô **SẠCH** (có thể sử dụng)
- Lô **KHUẨN NHẸ** (có thể theo dõi/cấy lại)
- Lô **NẶNG/HỦY** (thất thoát hoàn toàn)

---

## 🔢 DANH MỤC MÃ TÌNH TRẠNG

### **Mã cuối 3: SẠCH**

| Mã | Tên | Màu sắc | Icon | Ý nghĩa |
|----|-----|---------|------|---------|
| 103 | Sạch | Xanh lá (#28a745) | ✅ | Chất lượng tốt, sử dụng bình thường |

**Đặc điểm:**
- ✅ Lưu trong Phòng Sáng
- ✅ Có thể dùng làm Mô Mẹ
- ✅ Tính vào năng suất

---

### **Mã cuối 5: KHUẨN (Theo dõi)**

| Mã | Tên | Màu sắc | Icon | Ý nghĩa |
|----|-----|---------|------|---------|
| 105 | Khuẩn nhẹ | Vàng cam (#ff8c00) | ⚠️ | Nhiễm nhẹ, cần theo dõi |
| 205 | Khuẩn môi trường | Vàng cam (#ff8c00) | ⚠️ | Do môi trường |
| 305 | Khuẩn khác | Vàng cam (#ff8c00) | ⚠️ | Nguyên nhân khác |

**Đặc điểm:**
- ⚠️ Vẫn lưu trong Phòng Sáng
- ⚠️ **CÓ THỂ** dùng làm Mô Mẹ nhưng có cảnh báo
- ⚠️ Trạng thái: "Đang nuôi - Theo dõi khuẩn"
- 💡 Ưu tiên xử lý trước khi lây lan

---

### **Mã cuối 9: HỦY BỎ (Thất thoát)**

| Mã | Tên | Màu sắc | Icon | Ý nghĩa |
|----|-----|---------|------|---------|
| 109 | Khuẩn nặng | Đỏ thẫm (#8b0000) | 🔴 | Nhiễm nặng, hủy |
| 209 | Nấm | Đỏ thẫm (#8b0000) | 🔴 | Nấm, hủy |
| 309 | Hủy hoàn toàn | Đỏ thẫm (#8b0000) | 🔴 | Hủy hoàn toàn |

**Đặc điểm:**
- 🔴 **KHÔNG** lưu vào kho Phòng Sáng (trừ thẳng)
- 🔴 **KHÔNG** được dùng làm Mô Mẹ
- 🔴 Trạng thái: "Đã hủy"
- 📊 Tính vào tỷ lệ **THẤT THOÁT**

---

## 🎯 LOGIC PHÂN LOẠI

### Function: `phan_loai_tinh_trang(ma_tinh_trang)`

```python
ma_cuoi = ma_tinh_trang % 10

if ma_cuoi == 3:
    return 'sach', '#28a745', '✅'
elif ma_cuoi == 5:
    return 'khuan', '#ff8c00', '⚠️'
elif ma_cuoi == 9:
    return 'huy', '#8b0000', '🔴'
```

**Returns:** `(loai, color, icon)`
- `loai`: 'sach' | 'khuan' | 'huy'
- `color`: Mã màu hex
- `icon`: Emoji icon

---

## 📝 GIAO DIỆN NHẬP LIỆU

### **Dropdown Tình trạng:**

```
Tình trạng *
┌──────────────────────────────────────────┐
│ ✅ Sạch (Mã 103)                         │
│ ⚠️ Khuẩn nhẹ (Mã 105) - Theo dõi        │
│ ⚠️ Khuẩn môi trường (Mã 205) - Theo dõi │
│ ⚠️ Khuẩn khác (Mã 305) - Theo dõi       │
│ 🔴 Khuẩn nặng (Mã 109) - Hủy bỏ         │
│ 🔴 Nấm (Mã 209) - Hủy bỏ                │
│ 🔴 Hủy hoàn toàn (Mã 309) - Hủy bỏ      │
└──────────────────────────────────────────┘
```

---

### **Cảnh báo theo loại:**

#### **Mã cuối 3: SẠCH**

```
✅ Lô sạch (Mã cuối 3) - Chất lượng tốt
```

---

#### **Mã cuối 5: KHUẨN**

```
⚠️ CẢNH BÁO KHUẨN

Lô này có mã cuối 5 - Nhiễm khuẩn nhẹ
- Vẫn lưu trong Phòng Sáng
- Có thể sử dụng làm Mô Mẹ nhưng CẦN THEO DÕI
- Ưu tiên xử lý trước khi lây lan
```

---

#### **Mã cuối 9: HỦY BỎ**

```
🔴 HỦY BỎ

Lô này có mã cuối 9 - Nấm/Khuẩn nặng
- Sẽ bị TRỪ THẲNG khỏi kho Phòng Sáng
- Tính vào tỷ lệ THẤT THOÁT
- KHÔNG được dùng làm Mô Mẹ
```

---

## 💾 LOGIC LƯU DỮ LIỆU

### **1. Phân loại tình trạng:**

```python
ma_tinh_trang = get_ma_tinh_trang(tinh_trang)
loai, mau_sac, icon = phan_loai_tinh_trang(ma_tinh_trang)
```

---

### **2. Xử lý theo loại:**

#### **A. Mã cuối 3 (SẠCH):**

```python
tong_so_tui = so_tui_con
tong_so_cay = so_tui_sach * so_cum_tui_con
trang_thai = "Đang nuôi"
ghi_chu_them = ghi_chu
```

**→ Lưu vào Phòng Sáng bình thường**

---

#### **B. Mã cuối 5 (KHUẨN):**

```python
tong_so_tui = so_tui_con
tong_so_cay = so_tui_sach * so_cum_tui_con
trang_thai = "Đang nuôi - Theo dõi khuẩn"
ghi_chu_them = f"[CẢNH BÁO MÃ {ma_tinh_trang} - Khuẩn nhẹ] {ghi_chu}"
```

**→ Lưu vào Phòng Sáng với cảnh báo**

---

#### **C. Mã cuối 9 (HỦY):**

```python
tong_so_tui = 0  # TRỪ THẲNG
tong_so_cay = 0
trang_thai = "Đã hủy"
ghi_chu_them = f"[HỦY BỎ - Mã {ma_tinh_trang}] {ghi_chu}"
```

**→ KHÔNG lưu vào kho Phòng Sáng**

---

## 📊 THÔNG BÁO SAU KHI LƯU

### **Mã cuối 3: SẠCH**

```
✅ LƯU DỮ LIỆU THÀNH CÔNG!

📋 Lô sạch - Mã 103 (mã cuối 3)

📦 Đã tự động tạo bản ghi trong phòng sáng
🔬 Đã khấu trừ 50 cụm từ lô Mô Soi MS-20260102-001
📊 Lô Mô Soi còn lại: 375 cụm
```

---

### **Mã cuối 5: KHUẨN**

```
⚠️ ĐÃ LƯU - LÔ CẦN THEO DÕI!

📋 Lô này có Mã 105 (mã cuối 5) - Khuẩn nhẹ

📦 Đã lưu vào Phòng Sáng với trạng thái: Theo dõi khuẩn
✅ Có thể sử dụng làm Mô Mẹ nhưng CẦN KIỂM TRA KỸ
🔬 Đã khấu trừ 50 cụm từ lô Mô Soi MS-20260102-001
📊 Lô Mô Soi còn lại: 375 cụm

💡 Khuyến nghị: Ưu tiên xử lý trước khi lây lan
```

---

### **Mã cuối 9: HỦY BỎ**

```
🔴 ĐÃ LƯU - LÔ BỊ HỦY BỎ!

⚠️ Lô này có Mã 109 (mã cuối 9) - Khuẩn nặng

📋 Trạng thái: Đã hủy
❌ KHÔNG lưu vào kho Phòng Sáng (trừ thẳng)
📊 Tính vào tỷ lệ THẤT THOÁT
🔬 Đã khấu trừ 50 cụm từ lô Mô Soi MS-20260102-001
📊 Lô Mô Soi còn lại: 375 cụm

💡 Lưu ý: Cần kiểm tra nguyên nhân nhiễm để cải thiện quy trình
```

---

## 🎨 MÀU SẮC & ICON

### **Bảng màu:**

| Loại | Màu sắc | Hex | Sử dụng |
|------|---------|-----|---------|
| Sạch | Xanh lá | #28a745 | Nền, border, text |
| Khuẩn | Vàng cam | #ff8c00 | Cảnh báo, highlight |
| Hủy | Đỏ thẫm | #8b0000 | Error, warning |

### **Icon:**

| Loại | Icon | Ý nghĩa |
|------|------|---------|
| Sạch | ✅ | Chất lượng tốt |
| Khuẩn | ⚠️ | Cần theo dõi |
| Hủy | 🔴 | Thất thoát |

---

## 📈 BÁO CÁO & THỐNG KÊ

### **1. Tách biệt 2 loại nhiễm:**

#### **A. Tỷ lệ Khuẩn (Mã 5):**
- Nhiễm nhẹ, có thể xử lý
- Vẫn lưu trong phòng sáng
- Có thể sử dụng (với cảnh báo)

#### **B. Tỷ lệ Nấm/Hủy (Mã 9):**
- Thất thoát hoàn toàn
- Đã loại bỏ khỏi kho
- KHÔNG thể sử dụng

---

### **2. Biểu đồ Admin:**

**Biểu đồ 1: Tỷ lệ Khuẩn (có thể xử lý)**
```
Hiển thị:
- Số lô có mã cuối 5
- Phân bố theo loại khuẩn (Nhẹ, MT, Khác)
- Xu hướng theo thời gian
```

**Biểu đồ 2: Tỷ lệ Nấm (thất thoát)**
```
Hiển thị:
- Số lô có mã cuối 9
- Phân bố theo nguyên nhân (Nặng, Nấm, Hủy)
- Tỷ lệ % thất thoát
```

---

## 🏷️ TEM NHÃN

### **Đối với Mã 5 (Khuẩn):**

```
┌─────────────────────────────┐
│ [LOGO] Đồng tiền đỏ         │ ← Tên giống (Bold)
│ MS-20260102-001 | W02       │ ← Mã lô + Tuần
│ NVA | ⚠️ THEO DÕI KHUẨN      │ ← Mã NV + Cảnh báo
│                       [QR]   │ ← QR code
└─────────────────────────────┘
```

**Đặc điểm:**
- Dòng 3 thêm: "⚠️ THEO DÕI KHUẨN"
- Màu nền: Vàng nhạt
- Border: Vàng cam

---

### **Đối với Mã 9 (Hủy):**

```
🔴 KHÔNG IN TEM
(Lô đã hủy bỏ, không cần tem)
```

---

### **Đối với Mã 3 (Sạch):**

```
┌─────────────────────────────┐
│ [LOGO] Đồng tiền đỏ         │
│ MS-20260102-001 | W02       │
│ NVA                   [QR]  │
└─────────────────────────────┘
```

---

## 💡 USE CASE

### **Case 1: Lô Sạch (Mã 103)**

```
1. Nhân viên chọn: "✅ Sạch (Mã 103)"
2. Hệ thống hiển thị: "✅ Lô sạch (Mã cuối 3)"
3. Nhập các thông tin khác
4. Bấm "Lưu"
5. Hệ thống:
   - Lưu vào Phòng Sáng
   - Trạng thái: "Đang nuôi"
   - Có thể dùng làm Mô Mẹ
6. Thông báo: ✅ Màu xanh
```

---

### **Case 2: Lô Khuẩn nhẹ (Mã 105)**

```
1. Nhân viên chọn: "⚠️ Khuẩn nhẹ (Mã 105) - Theo dõi"
2. Hệ thống hiển thị cảnh báo vàng:
   "⚠️ CẢNH BÁO KHUẨN
   Lô này có mã cuối 5..."
3. Nhập thông tin
4. Bấm "Lưu"
5. Hệ thống:
   - Vẫn lưu vào Phòng Sáng
   - Trạng thái: "Đang nuôi - Theo dõi khuẩn"
   - Có thể dùng Mô Mẹ (với cảnh báo)
6. Thông báo: ⚠️ Màu vàng cam
7. Tem: In thêm dòng "⚠️ THEO DÕI KHUẨN"
```

---

### **Case 3: Lô Nấm (Mã 209)**

```
1. Nhân viên chọn: "🔴 Nấm (Mã 209) - Hủy bỏ"
2. Hệ thống hiển thị cảnh báo đỏ:
   "🔴 HỦY BỎ
   Lô này có mã cuối 9..."
3. Nhập thông tin
4. Bấm "Lưu"
5. Hệ thống:
   - KHÔNG lưu vào Phòng Sáng
   - Trạng thái: "Đã hủy"
   - Tính vào thất thoát
6. Thông báo: 🔴 Màu đỏ
7. Tem: KHÔNG in (đã hủy)
```

---

## 🔄 SO SÁNH HỆ THỐNG CŨ VS MỚI

### **Hệ thống CŨ:**

```
- Tình trạng: Chỉ là text (không có mã)
- Không phân biệt rõ loại nhiễm
- Tất cả đều lưu vào Phòng Sáng
- Báo cáo chung chung
- Khó kiểm soát chất lượng
```

---

### **Hệ thống MỚI:**

```
- Tình trạng: Có mã số (103, 105, 109...)
- Phân biệt rõ 3 loại: Sạch/Khuẩn/Hủy
- Mã 9 KHÔNG lưu vào Phòng Sáng
- Báo cáo tách biệt: Khuẩn vs Nấm
- Kiểm soát chất lượng tốt hơn
- Tem nhãn có cảnh báo rõ ràng
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### **1. Mã cuối quyết định tất cả:**

- Mã cuối **3**: Sạch
- Mã cuối **5**: Khuẩn (theo dõi)
- Mã cuối **9**: Hủy bỏ

### **2. Mã 9 = Thất thoát:**

- KHÔNG lưu vào Phòng Sáng
- KHÔNG được dùng làm Mô Mẹ
- Tính vào KPI thất thoát

### **3. Mã 5 = Cảnh báo:**

- Vẫn có thể dùng
- Nhưng cần theo dõi chặt
- Ưu tiên xử lý

### **4. Báo cáo tách biệt:**

- Tỷ lệ Khuẩn (Mã 5): Có thể xử lý
- Tỷ lệ Nấm (Mã 9): Thất thoát vĩnh viễn

---

**Green Straw Hat - Happiness Together 🌱**

**Phiên bản:** 2.2
**Ngày:** 02/01/2026
**Tính năng:** Hệ thống phân loại nhiễm theo mã

