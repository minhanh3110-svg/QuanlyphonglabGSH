# 🎨 HƯỚNG DẪN TẠO VÀ SỬ DỤNG LOGO TRANG CHỦ

## 📋 Tổng quan

Logo công ty sẽ hiển thị ở **2 vị trí** trong ứng dụng:

1. **Trang chủ (Header):** Logo hiển thị 2 bên trái/phải của tiêu đề "QUẢN LÝ PHÒNG NUÔI CẤY MÔ"
2. **Sidebar:** Logo hiển thị ở đầu menu bên trái
3. **Tem nhãn:** Logo in trên tem 35×22mm và 25×15mm

---

## 🚀 Bước 1: Tạo Logo Mặc Định

Chúng tôi đã tạo sẵn một script để tạo logo mặc định đẹp mắt:

### Chạy script tạo logo:

```bash
python create_default_logo.py
```

### Kết quả:
- File `logo.png` được tạo tự động
- Kích thước: 500×500px
- Định dạng: PNG với nền trong suốt
- Thiết kế: Cây + chữ "LAB" + "Tissue Culture"

---

## 🎨 Bước 2: Tùy chỉnh Logo (Optional)

### Cách 1: Sử dụng logo mặc định
✅ Không cần làm gì thêm! Logo đã sẵn sàng.

### Cách 2: Thay thế bằng logo công ty thật

#### Yêu cầu file logo:

| Tiêu chí | Giá trị |
|----------|---------|
| **Định dạng** | PNG (khuyến nghị - nền trong suốt) hoặc JPG |
| **Kích thước** | Tối thiểu 500×500px, khuyến nghị 1000×1000px |
| **Tỷ lệ** | Hình vuông (1:1) hoặc gần vuông |
| **Dung lượng** | < 2MB |
| **Màu sắc** | Rõ ràng, tương phản cao |

#### Các bước:

1. **Chuẩn bị logo của bạn** (file PNG/JPG)

2. **Đổi tên file thành:** `logo.png`

3. **Copy vào thư mục dự án:**
   ```
   D:\QUANLYLAB\logo.png
   ```

4. **Khởi động lại ứng dụng:**
   ```bash
   python -m streamlit run app.py
   ```

---

## 📐 Vị trí hiển thị Logo

### 1. Trang chủ (Trước đăng nhập)

```
┌────────────────────────────────────────────────┐
│  [LOGO]  🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱  [LOGO]│
├────────────────────────────────────────────────┤
│                 🔐 Đăng nhập                   │
│                                                │
│  👤 Tên đăng nhập: [________]                 │
│  🔑 Mã nhân viên:  [________]                 │
│                                                │
│         [🚪 Đăng nhập]                         │
└────────────────────────────────────────────────┘
```

**Kích thước logo:** 150px × tự động (giữ tỷ lệ)

---

### 2. Trang chính (Sau đăng nhập)

```
┌────────────────────────────────────────────────┐
│  [LOGO]  🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱  [LOGO]│
├────────────────────────────────────────────────┤
│                                                │
│         (Nội dung ứng dụng)                   │
│                                                │
└────────────────────────────────────────────────┘
```

**Kích thước logo:** 120px × tự động (nhỏ hơn một chút)

---

### 3. Sidebar (Menu bên trái)

```
┌──────────────────┐
│                  │
│    [LOGO FULL]   │  ← Logo đầy đủ
│                  │
├──────────────────┤
│ 👤 Nguyễn Văn An │
│ Mã NV: NVA       │
│ 🔑 Quyền: Admin  │
├──────────────────┤
│ 📋 Chọn chức năng│
│ • Nhập liệu      │
│ • In tem nhãn    │
│ ...              │
└──────────────────┘
```

**Kích thước logo:** 200px × tự động (full width sidebar)

---

### 4. Tem nhãn

#### Tem lớn (35×22mm):
```
┌──────────────────────┐
│[Logo]           [QR] │  ← Logo 15% height
│Đồng tiền đỏ     [QR] │
│Lô #123 - T5     [QR] │
│NV: NVA               │
└──────────────────────┘
```

#### Tem nhỏ (25×15mm):
```
┌────────────────┐
│[L]        [QR] │  ← Logo 12% height
│Đồng tiền  [QR] │
│#123/T5    [QR] │
│NVA             │
└────────────────┘
```

---

## 💻 Responsive trên Mobile

### Trên màn hình nhỏ (< 768px):

```
┌──────────────────┐
│     [LOGO]       │  ← Logo giữa
│   QUẢN LÝ LAB    │  ← Text dưới
├──────────────────┤
│   🔐 Đăng nhập   │
└──────────────────┘
```

Logo tự động:
- Stack vertically (xếp dọc)
- Center alignment (căn giữa)
- Kích thước thu nhỏ (100px)

---

## 🎨 Tùy chỉnh nâng cao

### Thay đổi kích thước logo trang chủ

Mở file `app.py`, tìm dòng:

```python
logo_width = 150  # Trang đăng nhập
```

hoặc

```python
logo_width = 120  # Trang chính
```

Thay đổi con số (px):
- **Nhỏ hơn:** 100, 80, 60
- **Lớn hơn:** 180, 200, 250

---

### Thay đổi vị trí logo

#### Hiện tại: Logo 2 bên (trái + phải)

```python
col_logo, col_title, col_spacer = st.columns([1, 3, 1])
```

#### Đổi thành: Logo chỉ bên trái

```python
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image(logo_display, use_column_width=True)

with col_title:
    st.markdown('<div class="main-header">🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱</div>', unsafe_allow_html=True)
```

#### Đổi thành: Logo ở giữa (trên tiêu đề)

```python
# Hiển thị logo giữa
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo_display, use_column_width=True)

# Tiêu đề ở dưới
st.markdown('<div class="main-header">🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱</div>', unsafe_allow_html=True)
```

---

## 🖼️ Mẫu Logo gợi ý

### 1. Logo văn phòng chuyên nghiệp
- **Màu sắc:** Xanh lá + Trắng
- **Font:** Sans-serif, chữ in hoa
- **Icon:** Cây, lá, ống nghiệm

### 2. Logo hiện đại tối giản
- **Màu sắc:** Gradient xanh
- **Style:** Flat design, line art
- **Icon:** Biểu tượng DNA + cây

### 3. Logo truyền thống
- **Màu sắc:** Xanh đậm + Vàng gold
- **Style:** Classic, có viền
- **Icon:** Cây trong khung tròn

---

## 🛠️ Tools tạo logo online (Miễn phí)

### 1. **Canva** (Khuyến nghị)
- URL: https://www.canva.com
- Template: Search "lab logo" hoặc "science logo"
- Xuất: PNG với nền trong suốt

### 2. **Looka**
- URL: https://looka.com
- AI tự động tạo logo
- Free preview

### 3. **LogoMakr**
- URL: https://logomakr.com
- Đơn giản, nhanh
- Download miễn phí

### 4. **Hatchful by Shopify**
- URL: https://hatchful.shopify.com
- Nhiều template
- Không cần đăng ký

---

## 📝 Checklist

### ✅ Trước khi deploy:

- [ ] File logo tên `logo.png` đã có trong thư mục `D:\QUANLYLAB`
- [ ] Kích thước logo >= 500×500px
- [ ] Logo có nền trong suốt (PNG) hoặc nền trắng
- [ ] Logo rõ ràng, không bị vỡ
- [ ] Đã test trên local (`streamlit run app.py`)
- [ ] Logo hiển thị đúng ở trang chủ
- [ ] Logo hiển thị đúng ở sidebar
- [ ] Logo hiển thị đúng trên tem nhãn

### ✅ Sau khi deploy Streamlit Cloud:

- [ ] Push file `logo.png` lên GitHub
- [ ] Streamlit Cloud tự động rebuild
- [ ] Kiểm tra logo trên production
- [ ] Test trên mobile

---

## 🚨 Xử lý lỗi

### ❌ Logo không hiển thị

**Nguyên nhân 1:** File không tồn tại
```bash
# Kiểm tra
ls -la logo.png

# Tạo lại
python create_default_logo.py
```

**Nguyên nhân 2:** File bị lỗi
```python
# Test trong Python
from PIL import Image
img = Image.open('logo.png')
img.show()
```

**Nguyên nhân 3:** Chưa khởi động lại app
```bash
# Ctrl+C để dừng
# Chạy lại
streamlit run app.py
```

---

### ❌ Logo bị vỡ/mờ

**Giải pháp:** Tăng độ phân giải

```python
# Trong create_default_logo.py
size = 500  # ← Đổi thành 1000 hoặc 1500
```

---

### ❌ Logo quá to/quá nhỏ

**Giải pháp:** Điều chỉnh width trong code

```python
# File app.py
logo_width = 150  # ← Thay đổi con số này
```

---

## 🎉 Kết quả mong đợi

### Trang chủ với logo:

```
     [🌿]    🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱    [🌿]
    ═══════════════════════════════════════════════
              
              🔐 Đăng nhập hệ thống
    
    ───────────────────────────────────────────────
```

### Tính năng:
✅ Logo chuyên nghiệp  
✅ Branding rõ ràng  
✅ Tăng độ tin cậy  
✅ Dễ nhận diện  
✅ Responsive mobile  

---

## 📞 Hỗ trợ

Nếu gặp vấn đề:

1. Kiểm tra file `logo.png` có trong thư mục chưa
2. Kiểm tra kích thước file (< 2MB)
3. Thử mở file bằng ứng dụng xem ảnh
4. Chạy lại script tạo logo mặc định
5. Khởi động lại ứng dụng

---

**🎨 Chúc bạn có một logo đẹp!**

