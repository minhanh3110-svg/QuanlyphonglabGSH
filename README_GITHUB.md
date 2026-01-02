# 🌱 Quản lý Lab Nuôi Cấy Mô

Ứng dụng quản lý phòng nuôi cấy mô thực vật chuyên nghiệp với đầy đủ tính năng: nhập liệu, in tem nhãn QR, báo cáo năng suất, quản lý phòng sáng, và dashboard quản trị.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Tính năng chính

### 📝 Quản lý nhật ký cấy
- Nhập liệu đầy đủ: Ngày cấy, nhân viên, giống cây, chu kỳ, môi trường, số túi, số cụm
- Tự động tính: Tổng số cây, thời gian làm việc, năng suất (cây/giờ)
- Tính tuần/tháng cấy tự động

### 🏷️ In tem nhãn với QR Code
- **Tự động tạo QR code** cho mỗi lô cấy
- **2 kích thước tem:** 35×22mm (lớn) và 25×15mm (nhỏ)
- **Tích hợp logo công ty** tự động
- **Quét QR để cập nhật** tình trạng lô nhanh chóng
- Xuất PDF in trực tiếp qua máy in tem nhiệt

### 📊 Báo cáo & Dashboard
- **Báo cáo năng suất** theo nhân viên/giống/thời gian
- **KPI nhiễm khuẩn** tự động tính toán
- **Cảnh báo đỏ** khi tỷ lệ nhiễm > 10%
- **Biểu đồ tương tác** (Plotly): So sánh năng suất, phân tích nhiễm khuẩn
- **Xuất Excel** báo cáo

### 💡 Quản lý phòng sáng
- **Tự động đồng bộ** dữ liệu từ nhật ký cấy
- **Quản lý vị trí** theo giàn/kệ
- **Cập nhật tình trạng nhiễm** chi tiết theo từng loại
- **Dự báo tuần xuất cây** tự động
- **Kiểm kê tổng hợp** toàn phòng sáng

### 🔐 Hệ thống phân quyền
- **Admin:** Xem tất cả dữ liệu, quản lý danh mục, dashboard đầy đủ
- **Nhân viên:** Chỉ xem dữ liệu cá nhân, nhập liệu, in tem

### 🎨 Tính năng khác
- Giao diện tiếng Việt 100%
- Responsive, hoạt động tốt trên mobile
- Logo công ty tích hợp
- Quản lý danh mục linh hoạt (giống cây, môi trường, nhân viên)

---

## 🚀 Triển khai

### 📋 Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (Python package manager)

### 💻 Chạy trên máy local

#### 1. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/QUANLYLAB.git
cd QUANLYLAB
```

#### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

#### 3. Chạy ứng dụng
```bash
streamlit run app.py
```

#### 4. Mở trình duyệt
Ứng dụng sẽ tự động mở tại: `http://localhost:8501`

**Tài khoản mặc định:**
- Tên đăng nhập: `admin`
- Mã nhân viên: `ADMIN001`

---

## ☁️ Deploy lên Streamlit Cloud (MIỄN PHÍ)

### Bước 1: Chuẩn bị
1. Tạo tài khoản GitHub (nếu chưa có): https://github.com
2. Tạo tài khoản Streamlit Cloud: https://share.streamlit.io

### Bước 2: Push code lên GitHub
```bash
# Khởi tạo git (nếu chưa có)
git init

# Thêm tất cả file
git add .

# Commit
git commit -m "Initial commit - Ứng dụng Quản lý Lab Nuôi Cấy"

# Kết nối với GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/QUANLYLAB.git

# Đẩy code lên GitHub
git push -u origin main
```

### Bước 3: Deploy trên Streamlit Cloud
1. Đăng nhập vào https://share.streamlit.io
2. Click **"New app"**
3. Chọn:
   - **Repository:** `YOUR_USERNAME/QUANLYLAB`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy"**
5. Đợi 2-3 phút → Ứng dụng sẽ online!

**URL ứng dụng:** `https://YOUR_APP_NAME.streamlit.app`

---

## 📁 Cấu trúc dự án

```
QUANLYLAB/
├── app.py                          # File ứng dụng chính
├── requirements.txt                 # Thư viện Python
├── data.db                          # Database SQLite (tự động tạo)
├── logo.png                         # Logo công ty (optional)
├── README.md                        # Hướng dẫn sử dụng
├── README_GITHUB.md                 # Hướng dẫn deploy GitHub
├── HUONG_DAN_LOGO.md               # Hướng dẫn thêm logo
├── HUONG_DAN_QR_TEM_NHAN.md        # Hướng dẫn in tem QR
├── HUONG_DAN_GIT.md                # Hướng dẫn Git chi tiết
├── .gitignore                       # File ignore Git
├── KHOI_DONG.bat                    # Script khởi động Windows
└── chay_ung_dung.bat                # Script cài đặt + chạy Windows
```

---

## 🎨 Thêm logo công ty

1. Chuẩn bị file logo:
   - Định dạng: **PNG** (nền trong suốt) hoặc JPG
   - Kích thước: Tối thiểu **500×500px**
   - Tỷ lệ: Hình vuông (1:1)

2. Đổi tên file thành: **`logo.png`**

3. Copy vào thư mục gốc dự án (cùng thư mục với `app.py`)

4. Khởi động lại ứng dụng

Logo sẽ tự động xuất hiện trên:
- ✅ Sidebar (menu bên trái)
- ✅ Tem nhãn 35×22mm
- ✅ Tem nhãn 25×15mm

**Chi tiết:** Xem file `HUONG_DAN_LOGO.md`

---

## 📖 Tài liệu

- 📘 [Hướng dẫn sử dụng QR Code và In Tem](HUONG_DAN_QR_TEM_NHAN.md)
- 🎨 [Hướng dẫn thêm Logo công ty](HUONG_DAN_LOGO.md)
- 🔧 [Hướng dẫn Git chi tiết](HUONG_DAN_GIT.md)

---

## 🛠️ Công nghệ sử dụng

- **Framework:** Streamlit 1.28+
- **Database:** SQLite
- **Data Processing:** Pandas
- **Charts:** Plotly
- **QR Code:** qrcode, Pillow
- **PDF Export:** reportlab, openpyxl

---

## 📊 Screenshots

### 🔐 Đăng nhập
![Login](https://via.placeholder.com/800x400?text=Login+Screen)

### 📝 Nhập liệu
![Data Entry](https://via.placeholder.com/800x400?text=Data+Entry)

### 🏷️ In tem nhãn
![Label Printing](https://via.placeholder.com/800x400?text=Label+Printing)

### 📊 Dashboard Admin
![Admin Dashboard](https://via.placeholder.com/800x400?text=Admin+Dashboard)

---

## 🔧 Cấu hình nâng cao

### Thay đổi URL cơ sở cho QR Code
Mở file `app.py`, tìm dòng:
```python
base_url = "http://localhost:8501"
```
Thay bằng URL thực tế khi deploy:
```python
base_url = "https://your-app-name.streamlit.app"
```

### Thay đổi kích thước logo trên tem
Trong `app.py`, tìm:
```python
# Tem lớn (35x22mm)
logo_size = int(height_px * 0.15)  # 15% chiều cao

# Tem nhỏ (25x15mm)
logo_size = int(height_px * 0.12)  # 12% chiều cao
```
Thay đổi tỷ lệ để điều chỉnh kích thước logo.

---

## 🐛 Xử lý lỗi thường gặp

### Lỗi: ModuleNotFoundError
**Giải pháp:** Cài đặt lại thư viện
```bash
pip install -r requirements.txt --upgrade
```

### Lỗi: Không hiển thị được QR Code
**Giải pháp:** Kiểm tra thư viện Pillow
```bash
pip uninstall Pillow
pip install Pillow
```

### Lỗi: Database locked
**Giải pháp:** Đóng tất cả kết nối đến `data.db`, khởi động lại ứng dụng

### Logo không hiển thị
**Giải pháp:** 
- Kiểm tra file `logo.png` có tồn tại không
- Kiểm tra tên file chính xác (chữ thường)
- Khởi động lại ứng dụng

---

## 🤝 Đóng góp

Contributions, issues và feature requests luôn được chào đón!

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

---

## 📝 License

Dự án này được phát hành dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

---

## 👨‍💻 Tác giả

**Lab Nuôi Cấy Mô Team**

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your.email@example.com

---

## 🙏 Lời cảm ơn

- [Streamlit](https://streamlit.io/) - Framework tuyệt vời để tạo web app Python
- [Plotly](https://plotly.com/) - Thư viện biểu đồ tương tác
- [qrcode](https://github.com/lincolnloop/python-qrcode) - Thư viện tạo mã QR

---

## 📈 Roadmap

- [ ] Thêm tính năng xuất báo cáo PDF
- [ ] Tích hợp email thông báo
- [ ] Thêm biểu đồ Gantt cho lịch trình xuất cây
- [ ] Mobile app (React Native)
- [ ] API RESTful
- [ ] Multi-language support (English)

---

## ⭐ Star History

Nếu dự án này hữu ích, hãy cho một ⭐ trên GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/QUANLYLAB&type=Date)](https://star-history.com/#YOUR_USERNAME/QUANLYLAB&Date)

---

**📞 Hỗ trợ:** Nếu gặp vấn đề, hãy tạo issue trên GitHub hoặc liên hệ qua email.

**🎉 Happy Coding!**

