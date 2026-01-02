# 🌱 Ứng dụng Quản lý Lab Nuôi Cấy Mô Chuyên Nghiệp

Ứng dụng web quản lý phòng nuôi cấy mô được xây dựng bằng Python và Streamlit với đầy đủ tính năng quản lý, báo cáo, cảnh báo tự động, **mã QR và in tem nhãn**.

---

## ✨ TÍNH NĂNG CHÍNH

### 🆕 **TÍNH NĂNG MỚI: MÃ QR VÀ IN TEM NHÃN** ⭐
- 🏷️ **Tự động tạo mã QR duy nhất** cho mỗi lô cấy
- 📱 **Quét QR bằng điện thoại** để truy cập nhanh thông tin lô
- 🖨️ **In tem nhãn chuyên nghiệp** (50mm × 30mm) với:
  - Tên giống cây, Ngày cấy, Tuần cấy
  - Tên nhân viên, Chu kỳ
  - Mã QR ở góc phải
- 📥 **Xuất tem nhãn PDF** để in bằng máy in tem nhiệt (Xprinter, Brother, Zebra)
- 🔄 **Tự động navigate** đến đúng lô khi quét QR
- 📊 **Quản lý tem từ nhiều trang**: Nhập liệu, Báo cáo

👉 **[Xem hướng dẫn chi tiết](HUONG_DAN_QR_TEM_NHAN.md)**

### 1️⃣ **HỆ THỐNG ĐĂNG NHẬP & PHÂN QUYỀN**
- 🔑 **Tài khoản Admin**: Xem toàn bộ dữ liệu, quản lý nhân viên, quản lý danh mục
  - Tên đăng nhập: `admin`
  - Mã nhân viên: `ADMIN001`
- 👤 **Tài khoản Nhân viên**: Chỉ xem dữ liệu cá nhân
- 🔒 Bảo mật với session state

### 2️⃣ **QUẢN LÝ NHẬT KÝ CẤY**
📝 **Form nhập liệu đầy đủ:**
- **Thông tin cơ bản**: Ngày cấy, Tháng, Tuần (tự động tính)
- **Thông tin giống**: Tên giống (Dropdown + mục "Khác"), Chu kỳ (Nhân nhanh/Cấy giãn/Ra rễ/Nhân+Rễ)
- **Thông tin cấy**: 
  - Box cấy, Số Giàn/Kệ (có thể tùy chỉnh)
  - Môi trường mẹ/con (Dropdown từ danh mục)
  - Số túi mẹ/con, Số cụm/túi mẹ/con
- **Quản lý thời gian**: Giờ bắt đầu, Giờ kết thúc
- **Tình trạng**: Sạch, Khuẩn nhẹ, Khuẩn nặng, Nấm, Khuẩn môi trường, Khác

🤖 **Tự động tính toán:**
- ✅ Tổng số cây con = Số túi con × Số cụm/túi con
- ✅ Tổng giờ làm = Giờ kết thúc - Giờ bắt đầu
- ✅ Năng suất = Tổng số cây con ÷ Tổng giờ làm
- ✅ Tuần cấy, Tháng cấy từ ngày chọn

🔄 **Tự động đồng bộ**: Dữ liệu tự động chuyển sang Phòng Sáng khi lưu

### 3️⃣ **QUẢN LÝ PHÒNG SÁNG (INVENTORY)**
📦 **Quản lý chi tiết:**
- 🏷️ Vị trí: Số Giàn/Kệ (có thể nhập/sửa)
- 📊 Cập nhật số lượng theo 6 cột:
  - 🟢 Sạch
  - 🟡 Khuẩn nhẹ
  - 🔴 Khuẩn nặng
  - 🔴 Nấm
  - 🟠 Khuẩn môi trường
  - ⚪ Khác
- 📅 Dự báo Tuần xuất cây (tự động cộng thêm tuần theo chu kỳ)
- 🔄 Trạng thái: Đang nuôi, Đã xuất, Hủy

🤖 **Tự động tính toán:**
- ✅ Tổng số túi = Tổng các cột
- ✅ Tổng số cây = Số túi sạch × Số cụm/túi
- ✅ Tỷ lệ nhiễm = (Khuẩn nặng + Nấm) ÷ Tổng túi × 100%

🚨 **CẢNH BÁO ĐỎ RỰC** (Tính năng quan trọng):
- **Nếu Tỷ lệ nhiễm > 10%**: Hiển thị cảnh báo ĐỎ RỰC với animation pulse
- **Nếu Tỷ lệ nhiễm 5-10%**: Hiển thị cảnh báo VÀNG
- **Nếu Tỷ lệ nhiễm < 5%**: Hiển thị biểu tượng XANH (Tốt)
- Cảnh báo xuất hiện ở:
  - ✅ Tiêu đề expander của từng lô
  - ✅ Bên trong form chi tiết
  - ✅ Bảng tổng hợp (tô màu toàn bộ dòng)

### 4️⃣ **TỔNG HỢP PHÒNG SÁNG (CHỈ ADMIN)**
📈 **Thống kê tổng quan:**
- Tổng số túi
- Tổng số cây (sạch)
- Số giàn đang sử dụng
- Số loại giống

📋 **Bảng tổng hợp:**
- Tổng hợp theo Giàn/Kệ
- Cây sắp đến ngày xuất (7 ngày) với cảnh báo màu
- Bảng chi tiết với **Tỷ lệ nhiễm** và **Cảnh báo ĐỎ RỰC**

### 5️⃣ **BÁO CÁO NĂNG SUẤT & KPI**
📊 **Thống kê tổng quan:**
- Tổng số cây con, Tổng giờ làm, Năng suất TB
- Tổng số túi, **Tỷ lệ nhiễm tổng thể** (có màu cảnh báo)

📋 **Báo cáo chi tiết:**
- Báo cáo Tỷ lệ nhiễm theo Nhân viên (có màu cảnh báo)
- Báo cáo Năng suất theo Chu kỳ
- Bảng dữ liệu chi tiết (có màu theo Tình trạng)

📈 **Dashboard Admin** (Chỉ Admin):
1. **Biểu đồ so sánh năng suất** giữa các nhân viên
2. **Biểu đồ cột chồng** chi tiết các loại nhiễm của từng nhân viên
3. **Biểu đồ tròn phân tích nguyên nhân nhiễm**:
   - Khuẩn nặng + Nấm (Đỏ)
   - Khuẩn môi trường (Vàng)
   - Khác (Xám)
   - Sạch (Xanh)
4. **Bảng xếp hạng Nhân viên cấy sạch nhất** (tỷ lệ nhiễm thấp nhất)

💾 **Xuất báo cáo Excel** (Chỉ Admin)

### 6️⃣ **QUẢN LÝ DANH MỤC (CHỈ ADMIN)**
⚙️ **Quản lý không cần sửa code:**
- 🌿 **Tên giống**: Thêm/Xóa tên giống
- 🔄 **Chu kỳ**: Thêm/Xóa chu kỳ
- 🧪 **Môi trường**: Thêm/Xóa/Cập nhật hàng loạt môi trường (theo mã số và tên)

### 7️⃣ **QUẢN LÝ TÁI KHOẢN (CHỈ ADMIN)**
👥 **Quản lý nhân viên:**
- Thêm tài khoản nhân viên mới
- Xem danh sách tài khoản
- Xóa tài khoản (không thể xóa admin)

---

## 📋 Yêu cầu hệ thống

- Python 3.7 trở lên
- pip (trình quản lý gói Python)

---

## 🚀 Hướng dẫn cài đặt và chạy

### ⭐ Cách đơn giản nhất: Chạy bằng file .bat (Windows)

#### Lần đầu tiên cài đặt:
1. **Double-click vào file `chay_ung_dung.bat`**
   - File này sẽ tự động cài đặt thư viện và chạy ứng dụng

#### Khởi động lại ứng dụng (sau khi đã cài đặt):
1. **Double-click vào file `KHOI_DONG.bat`** 
   - File này chỉ khởi động ứng dụng (không cài đặt lại)
   - ⚡ **Cách nhanh nhất để chạy lại ứng dụng!**

💡 **Mẹo:** Bạn có thể tạo shortcut của file `KHOI_DONG.bat` trên Desktop để truy cập nhanh hơn:
- Right-click vào `KHOI_DONG.bat` → Chọn "Send to" → "Desktop (create shortcut)"

### Cách 2: Chạy thủ công

#### Bước 1: Cài đặt các thư viện cần thiết

Mở **Command Prompt** hoặc **PowerShell** trong thư mục chứa file `app.py` và chạy lệnh:

```bash
pip install -r requirements.txt
```

**Lưu ý:** Nếu gặp lỗi, thử dùng:
```bash
python -m pip install -r requirements.txt
```

#### Bước 2: Chạy ứng dụng

Chạy lệnh sau để khởi động ứng dụng:

```bash
streamlit run app.py
```

**Hoặc:**
```bash
python -m streamlit run app.py
```

#### Bước 3: Mở ứng dụng trong trình duyệt

Sau khi chạy lệnh, bạn sẽ thấy thông báo như sau:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Nếu trình duyệt không tự động mở:**
- Copy địa chỉ `http://localhost:8501` 
- Dán vào thanh địa chỉ trình duyệt (Chrome, Edge, Firefox...)
- Nhấn Enter

---

## 🎯 Hướng dẫn sử dụng

### 🔐 Đăng nhập
1. Sử dụng tài khoản mặc định:
   - **Tên đăng nhập**: `admin`
   - **Mã nhân viên**: `ADMIN001`
2. Hoặc tài khoản nhân viên do Admin tạo

### 📝 Nhập liệu
1. Chọn menu **"Nhập liệu"** trên sidebar
2. Điền đầy đủ thông tin vào form
3. Hệ thống tự động tính toán các giá trị
4. Nhấn **"💾 Lưu dữ liệu"**
5. ✅ Dữ liệu tự động chuyển sang Phòng Sáng

### ☀️ Quản lý Phòng Sáng
1. Chọn menu **"Quản lý Phòng Sáng"**
2. Sử dụng bộ lọc để tìm kiếm
3. Click vào expander để xem/sửa chi tiết
4. 🚨 Chú ý các lô có **CẢNH BÁO ĐỎ RỰC** (Tỷ lệ nhiễm > 10%)
5. Cập nhật số túi theo tình trạng
6. Nhấn **"💾 Cập nhật"**

### 📊 Xem báo cáo (Admin)
1. Chọn menu **"Báo cáo Năng suất"**
2. Chọn khoảng thời gian, chu kỳ, nhân viên
3. Xem các biểu đồ và bảng thống kê
4. Nhấn **"📥 Tải xuống Excel"** để xuất báo cáo

### 📈 Tổng hợp Phòng Sáng (Admin)
1. Chọn menu **"Tổng hợp Phòng Sáng"**
2. Xem thống kê tổng quan
3. Kiểm tra cây sắp đến ngày xuất
4. 🚨 Chú ý bảng chi tiết có **Cảnh báo ĐỎ RỰC**

### ⚙️ Quản lý danh mục (Admin)
1. Chọn menu **"Quản lý danh mục"**
2. Chọn tab: Tên giống / Chu kỳ / Môi trường
3. Thêm/Xóa các mục cần thiết
4. Với Môi trường: Có thể cập nhật hàng loạt

### 👥 Quản lý tài khoản (Admin)
1. Chọn menu **"Quản lý tài khoản"**
2. Thêm tài khoản nhân viên mới
3. Xem danh sách tài khoản
4. Xóa tài khoản (nếu cần)

---

## 🔧 Kiểm tra hệ thống (Nếu ứng dụng không chạy được)

Nếu ứng dụng không chạy được, hãy chạy file **`KIEM_TRA.bat`** để kiểm tra:
- Python đã được cài đặt chưa
- Các thư viện cần thiết đã được cài đặt chưa
- File app.py có tồn tại không

File này sẽ tự động phát hiện và hướng dẫn bạn sửa lỗi.

---

## ⚠️ Xử lý lỗi thường gặp

### Ứng dụng không chạy được / Không có phản hồi

**Bước 1:** Chạy file `KIEM_TRA.bat` để kiểm tra hệ thống

**Bước 2:** Kiểm tra các lỗi phổ biến:

#### Lỗi: "Python chua duoc cai dat"
- **Giải pháp:** 
  - Tải và cài đặt Python từ: https://www.python.org/downloads/
  - ⚠️ **Quan trọng:** Khi cài đặt, nhớ tick vào ô "Add Python to PATH"

#### Lỗi: "streamlit is not recognized" hoặc "Streamlit chua duoc cai dat"
- **Giải pháp:** 
  - Chạy lại file `chay_ung_dung.bat` (sẽ tự động cài đặt)
  - Hoặc chạy thủ công: `pip install streamlit pandas openpyxl plotly`

#### Lỗi: "No module named 'pandas'" hoặc thiếu thư viện khác
- **Giải pháp:** 
  - Chạy: `pip install -r requirements.txt`
  - Hoặc: `python -m pip install -r requirements.txt`

#### Link không mở được / Trình duyệt không tự động mở
- **Giải pháp:** 
  1. Xem trong cửa sổ terminal/command prompt có hiển thị "Local URL: http://localhost:8501" không
  2. Nếu có, copy link `http://localhost:8501` và dán vào trình duyệt (Chrome, Edge, Firefox...)
  3. Đảm bảo không có ứng dụng nào khác đang dùng cổng 8501
  4. Thử đóng tất cả cửa sổ terminal và chạy lại

#### Lỗi: "Port 8501 is already in use"
- **Giải pháp:**
  - Đóng tất cả cửa sổ terminal/PowerShell đang chạy
  - Hoặc tìm và đóng process đang dùng cổng 8501
  - Chạy lại ứng dụng

### Vẫn không được?
1. Chạy `KIEM_TRA.bat` và gửi kết quả
2. Mở PowerShell/Command Prompt, chạy `python -m streamlit run app.py` và gửi thông báo lỗi

---

## 📝 Lưu ý quan trọng

- ✅ Dữ liệu được lưu tự động trong file `data.db` (SQLite database)
- ✅ File `data.db` sẽ được tạo tự động khi chạy ứng dụng lần đầu tiên
- ✅ **KHÔNG XÓA** file `data.db` nếu không muốn mất dữ liệu
- ✅ Nên sao lưu file `data.db` định kỳ
- 🚨 **Chú ý Cảnh báo ĐỎ RỰC**: Lô hàng có tỷ lệ nhiễm > 10% cần xử lý ngay!

---

## 🎨 Giao diện

- ✅ Giao diện hiện đại, thân thiện
- ✅ Màu sắc rõ ràng: Xanh (Tốt), Vàng (Chú ý), Đỏ (Cảnh báo)
- ✅ Sidebar điều hướng tiện lợi
- ✅ Responsive, phù hợp mọi màn hình
- ✅ Animation cảnh báo ĐỎ RỰC thu hút sự chú ý

---

## 🔒 Bảo mật

- ✅ Hệ thống đăng nhập với session state
- ✅ Phân quyền rõ ràng: Admin / Nhân viên
- ✅ Mỗi nhân viên chỉ xem dữ liệu của mình
- ✅ Admin xem và quản lý toàn bộ hệ thống

---

## 🚀 Tính năng nổi bật

1. ✨ **Tự động đồng bộ** dữ liệu từ Nhật ký cấy → Phòng sáng
2. 🤖 **Tự động tính toán** tất cả các chỉ số (Năng suất, Tỷ lệ nhiễm, Tuần xuất...)
3. 🚨 **Cảnh báo ĐỎ RỰC** khi tỷ lệ nhiễm > 10% (Animation pulse)
4. 📊 **Dashboard chuyên nghiệp** với Plotly (Biểu đồ tương tác)
5. 📈 **Xếp hạng Nhân viên** dựa trên tỷ lệ nhiễm (KPI)
6. 💾 **Xuất Excel** báo cáo chi tiết
7. ⚙️ **Quản lý danh mục** không cần sửa code
8. 🔄 **Quản lý Phòng Sáng** với 6 cột tình trạng nhiễm
9. 📅 **Dự báo Tuần xuất cây** tự động
10. 🎨 **Giao diện đẹp** với gradient và màu sắc chuyên nghiệp
11. 🏷️ **Mã QR tự động** cho mỗi lô cấy (MỚI)
12. 📱 **Quét QR để truy cập nhanh** thông tin lô (MỚI)
13. 🖨️ **In tem nhãn chuyên nghiệp** dạng PDF (MỚI)

---

**Phát triển bởi:** AI Assistant  
**Công nghệ:** Python, Streamlit, SQLite, Pandas, Plotly, QRCode, Pillow, ReportLab  
**Phiên bản:** 3.0 (Với tính năng Mã QR và In Tem Nhãn)  
**Ngôn ngữ:** 100% Tiếng Việt

---

## 📚 Tài liệu bổ sung

- 📖 [Hướng dẫn sử dụng Mã QR và In Tem Nhãn](HUONG_DAN_QR_TEM_NHAN.md)
- 🎨 [Hướng dẫn Thêm Logo Công Ty](HUONG_DAN_LOGO.md)

