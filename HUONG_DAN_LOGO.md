# 🎨 HƯỚNG DẪN THÊM LOGO CÔNG TY

## 📋 Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Yêu cầu file logo](#yêu-cầu-file-logo)
3. [Cách thêm logo](#cách-thêm-logo)
4. [Vị trí hiển thị](#vị-trí-hiển-thị)
5. [Thay đổi logo](#thay-đổi-logo)
6. [Xử lý sự cố](#xử-lý-sự-cố)

---

## 🎯 Giới thiệu

Ứng dụng hỗ trợ hiển thị **logo công ty** ở 2 vị trí:

1. **Sidebar** (menu bên trái) - Xuất hiện trên mọi trang
2. **Tem nhãn** (góc trên trái) - In trên tem 35×22mm và 25×15mm

Logo sẽ tự động điều chỉnh kích thước phù hợp với từng vị trí.

---

## 📐 Yêu cầu file logo

### Định dạng file
✅ **Hỗ trợ:** PNG, JPG, JPEG  
✨ **Khuyến nghị:** PNG với nền trong suốt (transparent)

### Kích thước
- **Độ phân giải:** Tối thiểu 300×300 pixels
- **Khuyến nghị:** 500×500 pixels hoặc 1000×1000 pixels
- **Tỷ lệ:** Hình vuông hoặc gần vuông (1:1)

### Màu sắc
- **Nền trong suốt:** Tốt nhất (file PNG)
- **Nền trắng:** Được chấp nhận
- **Màu sắc:** Rõ ràng, tương phản cao

### Ví dụ logo tốt
```
✅ logo_500x500.png (nền trong suốt)
✅ logo_1000x1000.png (nền trong suốt)
✅ company_logo.png (nền trắng, viền rõ)
```

### Ví dụ logo không tốt
```
❌ logo_100x100.jpg (độ phân giải thấp)
❌ logo_wide_2000x500.png (quá dài)
❌ logo_blur.jpg (không rõ nét)
```

---

## 📂 Cách thêm logo

### Bước 1: Chuẩn bị file logo
1. Tạo/chọn file logo công ty theo yêu cầu trên
2. Đổi tên file thành: **`logo.png`** (hoặc `logo.jpg`)

### Bước 2: Copy vào thư mục dự án
```
D:\QUANLYLAB\
├── app.py
├── data.db
├── requirements.txt
├── logo.png          ← ĐẶT FILE LOGO VÀO ĐÂY
├── README.md
└── ...
```

**Lưu ý:** File logo phải nằm **cùng thư mục** với `app.py`

### Bước 3: Khởi động lại ứng dụng
```powershell
# Nhấn Ctrl+C để dừng ứng dụng (nếu đang chạy)
# Chạy lại:
python -m streamlit run app.py
```

### Bước 4: Kiểm tra kết quả
1. Mở trình duyệt
2. **Sidebar:** Logo xuất hiện ở trên cùng menu bên trái
3. **Tem nhãn:** Vào trang "In tem nhãn" → Xem preview tem

---

## 📍 Vị trí hiển thị

### 1️⃣ Sidebar (Menu bên trái)

```
┌─────────────────────────┐
│                         │
│     [LOGO CÔNG TY]      │ ← Logo ở đây (max 200px)
│                         │
├─────────────────────────┤
│ 🌱 Quản lý Lab Nuôi cấy │
├─────────────────────────┤
│ 👤 Nguyễn Văn An        │
│ 🔑 Mã NV: NVA           │
├─────────────────────────┤
│ 📋 Chọn chức năng       │
│ • Nhập liệu             │
│ • In tem nhãn           │
│ ...                     │
└─────────────────────────┘
```

**Đặc điểm:**
- Hiển thị ở **tất cả các trang**
- Tự động scale xuống **max 200px width**
- Giữ nguyên tỷ lệ khung hình

---

### 2️⃣ Tem nhãn 35×22mm (2 hàng)

```
┌────────────────────────────────┐
│ [Logo]                    [QR] │
│                           [QR] │ ← Logo góc trên trái (15% height)
│ Đồng tiền đỏ              [QR] │
│ #123/T5                        │
│ NV: NVA                        │
└────────────────────────────────┘
```

**Đặc điểm:**
- Logo chiếm **15% chiều cao tem**
- Đặt ở **góc trên trái**
- Không đè lên chữ và QR code

---

### 3️⃣ Tem nhãn 25×15mm (3 hàng)

```
┌────────────────────────┐
│ [L]              [QR]  │ ← Logo nhỏ (12% height)
│ Đồng tiền đỏ     [QR]  │
│ #123/T5          [QR]  │
│ NVA                    │
└────────────────────────┘
```

**Đặc điểm:**
- Logo chiếm **12% chiều cao tem** (nhỏ hơn)
- Đặt ở **góc trên trái**
- Tối ưu không gian cho tem nhỏ

---

## 🔄 Thay đổi logo

### Thay logo mới
1. Tắt ứng dụng (Ctrl+C)
2. **Xóa** file `logo.png` cũ
3. **Copy** file logo mới vào và đổi tên thành `logo.png`
4. Khởi động lại ứng dụng

### Thay đổi tên file logo
Nếu file logo của bạn có tên khác (ví dụ: `company_logo.png`):

**Cách 1: Đổi tên file** (Khuyến nghị)
```
company_logo.png  →  logo.png
```

**Cách 2: Sửa code**
1. Mở file `app.py`
2. Tìm dòng:
```python
LOGO_PATH = "logo.png"
```
3. Thay đổi thành:
```python
LOGO_PATH = "company_logo.png"
```
4. Lưu file và khởi động lại

---

## 🛠️ Xử lý sự cố

### ❌ Logo không hiển thị

**Nguyên nhân 1:** File logo không đúng vị trí
- ✅ **Giải pháp:** Kiểm tra file `logo.png` phải nằm cùng thư mục với `app.py`

**Nguyên nhân 2:** Tên file không đúng
- ✅ **Giải pháp:** Đảm bảo tên file là `logo.png` (chữ thường, không dấu, không khoảng trắng)

**Nguyên nhân 3:** Định dạng file không được hỗ trợ
- ✅ **Giải pháo:** Chuyển đổi sang PNG hoặc JPG

**Nguyên nhân 4:** File bị lỗi
- ✅ **Giải pháp:** Mở file bằng Paint hoặc Photoshop, export lại

---

### ❌ Logo bị mờ/vỡ

**Nguyên nhân:** Độ phân giải thấp
- ✅ **Giải pháp:** Sử dụng file logo có độ phân giải tối thiểu 300×300 pixels

---

### ❌ Logo quá lớn/quá nhỏ trên tem

**Nguyên nhân:** Tỷ lệ logo không phù hợp

**Giải pháp:** Chỉnh tỷ lệ logo trong code

1. Mở file `app.py`
2. Tìm dòng (cho tem 35×22mm):
```python
logo_size = int(height_px * 0.15)  # 15% chiều cao
```
3. Thay đổi con số `0.15` (15%):
   - Logo **to hơn**: `0.18` (18%) hoặc `0.20` (20%)
   - Logo **nhỏ hơn**: `0.12` (12%) hoặc `0.10` (10%)
4. Lưu và khởi động lại

**Lưu ý:** Làm tương tự cho tem 25×15mm (tìm `0.12`)

---

### ❌ Logo có nền đen/màu khi in tem

**Nguyên nhân:** File không có nền trong suốt

**Giải pháp:**
1. Mở file logo bằng Photoshop/GIMP
2. Xóa nền (làm trong suốt)
3. Export dạng PNG với "Transparency" enabled
4. Copy lại vào thư mục dự án

---

### ❌ Logo đè lên chữ/QR code

**Nguyên nhân:** Kích thước logo quá lớn

**Giải pháo:**
1. Giảm tỷ lệ logo (theo hướng dẫn trên)
2. Hoặc sử dụng logo nhỏ gọn hơn

---

## 💡 Lời khuyên

### Logo đẹp cho tem nhãn
✅ Sử dụng logo **icon** thay vì logo chữ dài  
✅ Nền **trong suốt** cho hiệu quả tốt nhất  
✅ Màu sắc **tương phản cao** (đen/trắng, xanh đậm/trắng)  
✅ Đơn giản, dễ nhận diện ở kích thước nhỏ  

### Logo đẹp cho sidebar
✅ Logo **full** (có thể có chữ)  
✅ Tỷ lệ **ngang** hoặc **vuông**  
✅ Độ phân giải cao (500×500 trở lên)  

---

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. ✅ File logo có tồn tại không?
2. ✅ Tên file có đúng không?
3. ✅ File có bị lỗi không? (thử mở bằng ứng dụng xem ảnh)
4. ✅ Đã khởi động lại ứng dụng chưa?

---

**🎉 Chúc bạn thành công!**

