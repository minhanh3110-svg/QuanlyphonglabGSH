# 🎨 HƯỚNG DẪN SỬ DỤNG LOGO GREEN STRAW HAT

## 📋 Thông tin logo

**Logo:** Green Straw Hat  
**Slogan:** Happiness Together  
**Màu sắc:** Xanh lá cây (#8BC34A) + Đỏ (#FF0000)  
**Đặc điểm:** Logo hình tròn yin-yang với mũ rơm  

---

## 📥 Cách lưu logo từ hình ảnh

### **Phương pháp 1: Lưu trực tiếp (Đơn giản)**

1. **Click chuột phải** vào hình logo
2. Chọn **"Save image as..."** hoặc **"Lưu hình ảnh dưới dạng..."**
3. **Đặt tên file:** `logo.png`
4. **Chọn thư mục:** `D:\QUANLYLAB\`
5. Nhấn **"Save"** hoặc **"Lưu"**

---

### **Phương pháp 2: Copy & Paste**

1. **Click chuột phải** vào hình logo → **"Copy image"**
2. Mở **Paint** (Windows)
3. **Ctrl+V** để paste
4. **File → Save As → PNG**
5. Lưu với tên: `logo.png` vào `D:\QUANLYLAB\`

---

### **Phương pháp 3: Screenshot & Crop**

1. **Windows + Shift + S** để chụp màn hình
2. Chọn vùng logo
3. Mở **Paint** → **Ctrl+V**
4. Crop chỉ lấy phần logo
5. **Save As PNG** → `logo.png`

---

## 🔧 Tối ưu logo (Optional)

Nếu logo quá lớn hoặc cần resize:

### **Sử dụng Paint:**
1. Mở `logo.png` bằng Paint
2. **Resize** → Nhập: **500 pixels** (width)
3. Check ✅ **"Maintain aspect ratio"**
4. **Save**

### **Sử dụng Online Tool:**
- https://www.iloveimg.com/resize-image
- Upload logo → Resize to **500×500px**
- Download

---

## ✅ Kiểm tra file logo

Sau khi lưu, kiểm tra:

```
D:\QUANLYLAB\
├── app.py              ✅
├── logo.png            ✅ ← File logo mới
├── requirements.txt    ✅
├── data.db
└── ...
```

### **Kiểm tra bằng lệnh:**

```powershell
cd D:\QUANLYLAB
dir logo.png
```

**Kết quả mong đợi:**
```
... logo.png
```

---

## 🚀 Khởi động lại ứng dụng

### **Cách 1: Dùng script tự động**

Double-click file: **`RELOAD_WITH_LOGO.bat`**

### **Cách 2: Thủ công**

1. Nếu app đang chạy: **Nhấn Ctrl+C** trong PowerShell
2. Chạy lại:
```powershell
cd D:\QUANLYLAB
python -m streamlit run app.py
```

3. **Reload trình duyệt:** Nhấn **Ctrl+R** hoặc **F5**

---

## 📐 Logo sẽ hiển thị ở đâu?

### **1. Trang đăng nhập**
```
┌────────────────────────────────────────────┐
│  [🎩]  🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱  [🎩]│
│         Green Straw Hat Logo               │
├────────────────────────────────────────────┤
│           🔐 Đăng nhập                     │
└────────────────────────────────────────────┘
```

### **2. Trang chính (Header)**
```
┌────────────────────────────────────────────┐
│  [🎩]  🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱  [🎩]│
└────────────────────────────────────────────┘
```

### **3. Sidebar**
```
┌──────────────┐
│   [🎩 LOGO]  │ ← Green Straw Hat
├──────────────┤
│ 👤 Nhân viên │
│ 🔑 Admin     │
└──────────────┘
```

### **4. Tem nhãn (In ấn)**
```
┌──────────────────┐
│[🎩]         [QR] │ ← Logo góc trái
│Đồng tiền đỏ [QR] │
│Lô #123      [QR] │
└──────────────────┘
```

---

## 🎨 Tùy chỉnh kích thước logo

Nếu logo quá to/nhỏ, chỉnh trong `app.py`:

### **Logo trang chủ:**
```python
logo_width = 150  # Đổi thành 120, 180, 200...
```

### **Logo sidebar:**
```python
logo_width = 200  # Đổi thành 180, 220, 250...
```

### **Logo tem nhãn 35×22mm:**
```python
logo_size = int(height_px * 0.15)  # Đổi 0.15 thành 0.12, 0.18...
```

### **Logo tem nhãn 25×15mm:**
```python
logo_size = int(height_px * 0.12)  # Đổi 0.12 thành 0.10, 0.15...
```

---

## 🔍 Xử lý sự cố

### ❌ **Logo không hiển thị**

**Kiểm tra:**
```powershell
cd D:\QUANLYLAB
dir logo.png
```

Nếu không thấy → Lưu lại logo

---

### ❌ **Logo bị méo**

**Nguyên nhân:** Logo không vuông (1:1)

**Giải pháp:**
1. Mở logo bằng Paint
2. Crop thành hình vuông
3. Resize về 500×500px
4. Save lại

---

### ❌ **Logo bị mờ**

**Nguyên nhân:** Độ phân giải thấp

**Giải pháp:**
- Tải logo độ phân giải cao hơn
- Hoặc dùng logo vector (SVG → PNG)
- Minimum: 500×500px
- Khuyến nghị: 1000×1000px

---

## 📊 Thông số logo khuyến nghị

| Thông số | Giá trị |
|----------|---------|
| **Định dạng** | PNG (nền trong suốt) |
| **Kích thước** | 500×500px đến 1000×1000px |
| **Tỷ lệ** | 1:1 (Hình vuông) |
| **Dung lượng** | < 1MB |
| **DPI** | 72-300 |
| **Color mode** | RGBA hoặc RGB |

---

## 🎯 Checklist

- [ ] Đã lưu hình logo từ trình duyệt
- [ ] File tên chính xác: `logo.png`
- [ ] File nằm trong: `D:\QUANLYLAB\`
- [ ] Logo kích thước >= 500×500px
- [ ] Đã khởi động lại ứng dụng
- [ ] Logo hiển thị đúng trên trang chủ
- [ ] Logo hiển thị đúng trên sidebar
- [ ] Logo in đúng trên tem nhãn

---

## 🎉 Kết quả

Sau khi hoàn thành:

✅ Logo Green Straw Hat xuất hiện ở trang chủ  
✅ Branding chuyên nghiệp "Happiness Together"  
✅ Logo hiển thị đẹp trên mọi thiết bị  
✅ Logo in rõ ràng trên tem nhãn  

---

## 📞 Lưu ý

- **Bản quyền:** Đảm bảo bạn có quyền sử dụng logo Green Straw Hat
- **Chất lượng:** Dùng logo độ phân giải cao nhất có thể
- **Backup:** Giữ file logo gốc để dùng sau này

---

**💚 Chúc bạn thành công với logo Green Straw Hat!**

