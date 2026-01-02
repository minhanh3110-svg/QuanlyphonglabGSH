# 🔬 HƯỚNG DẪN QUẢN LÝ & PHÂN TÍCH NHIỄM

## Phiên bản: 2.4 - Infection Management & Analysis

---

## 📋 TỔNG QUAN

Trang **"Quản lý & Phân tích Nhiễm"** cung cấp công cụ phân tích chuyên sâu về tỷ lệ nhiễm với:
- 🔍 Bộ lọc dữ liệu linh hoạt
- 📊 Tính toán tỷ lệ sạch chính xác
- 📈 Biểu đồ so sánh trực quan
- 🎯 Cảnh báo tự động
- 📥 Xuất báo cáo Excel/CSV

---

## 🔍 BỘ LỌC DỮ LIỆU

### **4 Tiêu chí lọc:**

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Nhân viên  │  Giống cây  │  Lọc theo   │  Thời gian  │
│  [Dropdown] │  [Dropdown] │  [Dropdown] │  [Input]    │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

---

### **1. Lọc theo Nhân viên:**

```
Nhân viên
┌──────────────────────────┐
│ Tất cả                   │
│ Nguyễn Văn A (NVA001)    │
│ Trần Thị B (NVB002)      │
│ Lê Văn C (NVC003)        │
└──────────────────────────┘
```

**Chức năng:**
- Chọn "Tất cả": Xem tổng hợp tất cả nhân viên
- Chọn cụ thể: Xem chi tiết 1 nhân viên

---

### **2. Lọc theo Giống cây:**

```
Giống cây
┌──────────────────────────┐
│ Tất cả                   │
│ Đồng tiền đỏ             │
│ Đồng tiền vàng           │
│ Khoai lang tím           │
│ Cây xuất khẩu A          │
└──────────────────────────┘
```

**Chức năng:**
- Chọn "Tất cả": Xem tất cả giống
- Chọn cụ thể: Phân tích 1 giống

---

### **3. Lọc theo Thời gian:**

**3 Cách lọc:**

#### **A. Khoảng ngày:**
```
Lọc theo: [Khoảng ngày]

Từ ngày: [01/12/2025]
Đến ngày: [02/01/2026]
```

#### **B. Tuần cấy:**
```
Lọc theo: [Tuần cấy]

Tuần: [52]
```

#### **C. Tháng/Năm:**
```
Lọc theo: [Tháng/Năm]

Tháng: [1]  |  Năm: [2026]
```

---

## 📊 TÍNH TOÁN TỶ LỆ SẠCH

### **Công thức:**

```
Tổng túi làm = Tổng số túi con đã cấy

Túi sạch (Mã 3) = Số túi có mã cuối 3
Túi khuẩn (Mã 5) = Số túi có mã cuối 5 (Theo dõi)
Túi hủy (Mã 9) = Số túi có mã cuối 9 (Thất thoát)

Tỷ lệ sạch % = (Túi sạch / Tổng túi) × 100
Tỷ lệ khuẩn % = (Túi khuẩn / Tổng túi) × 100
Tỷ lệ hủy % = (Túi hủy / Tổng túi) × 100
```

---

### **Ví dụ:**

```
Nhân viên: Nguyễn Văn A
Tổng túi làm: 1,000 túi

Phân loại:
- Sạch (Mã 103): 920 túi
- Khuẩn nhẹ (Mã 105): 50 túi
- Nấm (Mã 209): 30 túi

Kết quả:
- Tỷ lệ sạch: 92.0%
- Tỷ lệ khuẩn: 5.0%
- Tỷ lệ hủy: 3.0%
```

---

## 📋 BẢNG TỔNG HỢP

### **Cấu trúc:**

| Mã NV | Nhân viên | Tổng túi làm | Túi sạch (Mã 3) | Túi khuẩn (Mã 5) | Túi hủy (Mã 9) | Tỷ lệ sạch % | Tỷ lệ khuẩn % | Tỷ lệ hủy % |
|-------|-----------|--------------|-----------------|------------------|----------------|--------------|---------------|-------------|
| NVA001 | Nguyễn Văn A | 1,000 | 920 | 50 | 30 | 92.0 | 5.0 | 3.0 |
| NVB002 | Trần Thị B | 800 | 650 | 100 | 50 | 81.3 | 12.5 | 6.3 |
| NVC003 | Lê Văn C | 1,200 | 1,140 | 40 | 20 | 95.0 | 3.3 | 1.7 |

---

### **Màu sắc Highlight:**

#### **🟢 Xanh (Xuất sắc):**
```
Tỷ lệ sạch >= 95%
→ Background: #d4edda
→ Text: #155724
→ Font-weight: Bold
```

#### **🟡 Vàng (Cần cải thiện):**
```
Tỷ lệ sạch < 85%
→ Background: #fff3cd
→ Font-weight: Bold
```

#### **🔴 Đỏ (Cảnh báo):**
```
Tỷ lệ hủy > 5%
→ Background: #f8d7da
→ Text: #721c24
→ Font-weight: Bold
```

---

## 📈 BIỂU ĐỒ SO SÁNH

### **Tab 1: So sánh Nhân viên**

**Biểu đồ cột nhóm (Grouped Bar Chart):**

```
       Tỷ lệ nhiễm theo Nhân viên
       
  100% ┤
       │
   80% ┤     █
       │  █  █     █
   60% ┤  █  █  █  █
       │  █  █  █  █
   40% ┤  █  █  █  █
       │  █  █  █  █
   20% ┤  █  █  █  █
       │  █  █  █  █
    0% └──┴──┴──┴──┴──
         NVA NVB NVC NVD
         
  Legend:
  █ Sạch (Xanh)
  █ Khuẩn (Cam)
  █ Hủy (Đỏ)
  
  ---- Ngưỡng cảnh báo 5% (Đường đỏ đứt)
```

**Đặc điểm:**
- 3 cột cho mỗi nhân viên
- Màu sắc phân biệt rõ ràng
- Đường cảnh báo 5% (đỏ đứt nét)
- Hover hiển thị giá trị chính xác

---

### **Tab 2: So sánh Giống cây**

**Biểu đồ cột nhóm:**

```
       Tỷ lệ nhiễm theo Giống cây
       
  100% ┤
       │
   80% ┤        █
       │  █     █     █
   60% ┤  █  █  █  █  █
       │  █  █  █  █  █
   40% ┤  █  █  █  █  █
       │  █  █  █  █  █
   20% ┤  █  █  █  █  █
       │  █  █  █  █  █
    0% └──┴──┴──┴──┴──┴──
         Đồng Khoai Xuất
         tiền  lang  khẩu
         
  ---- Ngưỡng cảnh báo 5%
```

**Bảng chi tiết:**

| Giống | Tổng túi | Tỷ lệ sạch % | Tỷ lệ khuẩn % | Tỷ lệ hủy % |
|-------|----------|--------------|---------------|-------------|
| Đồng tiền đỏ | 2,000 | 93.0 | 5.0 | 2.0 |
| Khoai lang tím | 1,500 | 88.0 | 8.0 | 4.0 |
| Cây xuất khẩu A | 1,000 | 95.0 | 3.0 | 2.0 |

---

### **Tab 3: Phân tích Nguyên nhân**

**Biểu đồ tròn (Pie Chart):**

```
     Phân bố Tổng thể
     
        ┌─────────────┐
        │             │
        │    92%      │ Sạch (Xanh)
        │             │
        │  5%   3%    │ Khuẩn (Cam)
        │             │ Hủy (Đỏ)
        └─────────────┘
```

**Phân tích tự động:**

#### **Nếu Tỷ lệ hủy > 10%:**
```
🔴 CẢNH BÁO NGHIÊM TRỌNG!

Tỷ lệ hủy trung bình: 12.5%

VƯỢT QUÁ ngưỡng cho phép (10%)

Nguyên nhân có thể:
- Môi trường nhiễm khuẩn
- Quy trình tiệt trùng kém
- Kỹ thuật cấy chưa đạt

Hành động:
- Kiểm tra ngay môi trường
- Đào tạo lại nhân viên
- Cải thiện quy trình
```

#### **Nếu Tỷ lệ hủy 5-10%:**
```
⚠️ CẦN CHÚ Ý!

Tỷ lệ hủy: 7.5%

Cần giảm xuống < 5%
```

#### **Nếu Tỷ lệ hủy < 5%:**
```
✅ TỐT!

Tỷ lệ hủy: 3.0%

Trong ngưỡng cho phép
```

#### **Nếu Tỷ lệ khuẩn > 10%:**
```
⚠️ Tỷ lệ khuẩn nhẹ cao: 12.0%

Cần theo dõi chặt để tránh lây lan
```

---

## 📥 XUẤT DỮ LIỆU

### **2 Loại báo cáo:**

#### **1. Báo cáo Nhân viên:**

```
[📥 Tải Báo cáo Nhân viên (CSV)]

File: bao_cao_nhiem_nhan_vien_20260102.csv

Nội dung:
Mã NV,Nhân viên,Tổng túi làm,Túi sạch (Mã 3),...
NVA001,Nguyễn Văn A,1000,920,50,30,92.0,5.0,3.0
NVB002,Trần Thị B,800,650,100,50,81.3,12.5,6.3
...
```

#### **2. Báo cáo Giống cây:**

```
[📥 Tải Báo cáo Giống cây (CSV)]

File: bao_cao_nhiem_giong_20260102.csv

Nội dung:
Giống,Tổng túi,Tỷ lệ sạch %,Tỷ lệ khuẩn %,Tỷ lệ hủy %
Đồng tiền đỏ,2000,93.0,5.0,2.0
Khoai lang tím,1500,88.0,8.0,4.0
...
```

---

## 💡 USE CASE

### **Case 1: Phân tích tổng thể tháng 1**

```
1. Admin vào "Quản lý & Phân tích Nhiễm"
2. Bộ lọc:
   - Nhân viên: Tất cả
   - Giống cây: Tất cả
   - Lọc theo: Tháng/Năm
   - Tháng: 1, Năm: 2026
3. Xem metrics tổng quan:
   - Tổng túi: 10,000
   - Tỷ lệ sạch TB: 91.5%
   - Tỷ lệ khuẩn TB: 6.0%
   - Tỷ lệ hủy TB: 2.5%
4. Xem bảng chi tiết → Phát hiện NVB002 có tỷ lệ hủy 6.3% (đỏ)
5. Xem biểu đồ → Xác nhận NVB002 cao nhất
6. Tải báo cáo CSV để lưu trữ
```

---

### **Case 2: Phân tích 1 nhân viên cụ thể**

```
1. Bộ lọc:
   - Nhân viên: Trần Thị B (NVB002)
   - Giống cây: Tất cả
   - Lọc theo: Khoảng ngày
   - Từ: 01/12/2025, Đến: 02/01/2026
2. Xem kết quả:
   - Tổng túi: 800
   - Tỷ lệ sạch: 81.3% (Vàng - Cần cải thiện)
   - Tỷ lệ hủy: 6.3% (Đỏ - Cảnh báo)
3. Tab "So sánh Giống cây":
   - Phát hiện "Khoai lang tím" có tỷ lệ hủy cao nhất (8.0%)
4. Kết luận:
   - NVB002 gặp vấn đề với giống "Khoai lang tím"
   - Cần đào tạo lại kỹ thuật cấy giống này
```

---

### **Case 3: Phân tích 1 giống cây**

```
1. Bộ lọc:
   - Nhân viên: Tất cả
   - Giống cây: Khoai lang tím
   - Lọc theo: Tuần cấy
   - Tuần: 52
2. Xem kết quả:
   - Tổng túi: 500
   - Tỷ lệ hủy TB: 7.0% (Cao!)
3. Tab "So sánh Nhân viên":
   - NVA001: 3.0% (Tốt)
   - NVB002: 8.0% (Cao)
   - NVC003: 2.0% (Tốt)
4. Kết luận:
   - Giống "Khoai lang tím" khó cấy
   - NVB002 cần hỗ trợ đặc biệt
```

---

## 🎯 NGƯỠNG CẢNH BÁO

### **Tỷ lệ Sạch:**

| Tỷ lệ | Đánh giá | Màu sắc | Hành động |
|-------|----------|---------|-----------|
| ≥ 95% | Xuất sắc | 🟢 Xanh | Duy trì |
| 85-95% | Tốt | Không màu | Tiếp tục |
| < 85% | Cần cải thiện | 🟡 Vàng | Kiểm tra |

---

### **Tỷ lệ Hủy:**

| Tỷ lệ | Đánh giá | Màu sắc | Hành động |
|-------|----------|---------|-----------|
| < 5% | Tốt | Không màu | Duy trì |
| 5-10% | Cần chú ý | ⚠️ Cảnh báo | Kiểm tra |
| > 10% | Nghiêm trọng | 🔴 Đỏ | Hành động ngay |

---

### **Tỷ lệ Khuẩn (Mã 5):**

| Tỷ lệ | Đánh giá | Hành động |
|-------|----------|-----------|
| < 5% | Tốt | Theo dõi bình thường |
| 5-10% | Cần chú ý | Tăng cường kiểm tra |
| > 10% | Cao | Cảnh báo lây lan |

---

## 🎨 GIAO DIỆN

### **Màu sắc Green Straw Hat:**

```css
Primary: #28a745 (Xanh lá)
Warning: #ff8c00 (Cam)
Danger: #8b0000 (Đỏ thẫm)
Success: #d4edda (Xanh nhạt)
Alert: #fff3cd (Vàng nhạt)
Error: #f8d7da (Đỏ nhạt)
```

---

### **Layout:**

```
┌─────────────────────────────────────────────┐
│ 🔬 Quản lý & Phân tích Nhiễm                │
│ Phân tích chuyên sâu tỷ lệ nhiễm...        │
├─────────────────────────────────────────────┤
│ 🔍 Bộ lọc dữ liệu                           │
│ [Nhân viên] [Giống] [Lọc theo] [Thời gian] │
├─────────────────────────────────────────────┤
│ 📊 Tổng hợp Tỷ lệ Sạch                      │
│ [Metrics: 4 cột]                            │
│ [Bảng chi tiết với highlight]               │
│ [Chú thích màu sắc]                         │
├─────────────────────────────────────────────┤
│ 📈 Biểu đồ So sánh                          │
│ [Tab 1] [Tab 2] [Tab 3]                    │
│ [Biểu đồ interactiv]                       │
├─────────────────────────────────────────────┤
│ 📥 Xuất dữ liệu                             │
│ [Download CSV NV] [Download CSV Giống]     │
└─────────────────────────────────────────────┘
```

---

## 📱 MOBILE-FRIENDLY

### **Responsive Design:**

```
Desktop (> 1024px):
- 4 cột bộ lọc
- Bảng full width
- Biểu đồ lớn

Tablet (768-1024px):
- 2 cột bộ lọc (2 hàng)
- Bảng scroll ngang
- Biểu đồ vừa

Mobile (< 768px):
- 1 cột bộ lọc (4 hàng)
- Bảng scroll ngang
- Biểu đồ nhỏ, touch-friendly
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### **1. Dữ liệu nguồn:**
- Lấy từ bảng `nhat_ky_cay`
- Phân loại theo mã tình trạng (3/5/9)
- Tính toán real-time

### **2. Mã 5 (Khuẩn nhẹ):**
- KHÔNG tính vào "hủy"
- Hiển thị riêng để theo dõi
- Có thể chuyển thành mã 9 sau này

### **3. Ngưỡng cảnh báo:**
- 5% là ngưỡng cảnh báo chuẩn
- Có thể điều chỉnh theo nhu cầu
- Hiển thị đường đỏ đứt nét trên biểu đồ

### **4. Xuất dữ liệu:**
- CSV format với UTF-8-sig (hỗ trợ tiếng Việt)
- Tên file tự động có ngày
- Lưu trữ hàng tháng

---

**Green Straw Hat - Happiness Together 🌱**

**Phiên bản:** 2.4
**Ngày:** 02/01/2026
**Tính năng:** Quản lý & Phân tích Nhiễm chuyên sâu

