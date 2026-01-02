# 🏷️ Hướng dẫn sử dụng tính năng Mã QR và In Tem Nhãn

## 📋 Tổng quan

Tính năng **Mã QR và In Tem Nhãn** giúp bạn:
- ✅ Tự động tạo mã QR duy nhất cho mỗi lô cấy
- ✅ Quét QR để truy cập nhanh thông tin lô
- ✅ In tem nhãn chuyên nghiệp với **2 kích thước linh hoạt**
- ✅ Theo dõi và quản lý lô cấy dễ dàng

---

## 🎯 HAI KÍCH THƯỚC TEM NHÃN

### 📏 Tem lớn 35×22mm (2 hàng nhãn trên cuộn)

**Đặc điểm:**
- ✅ Chữ to, dễ đọc (cỡ chữ 50pt, 35pt, 28pt)
- ✅ QR code lớn, dễ quét (75% chiều cao)
- ✅ Bố cục rộng rãi, chuyên nghiệp
- ✅ Phù hợp in bằng máy in tem 2 hàng

**Khi nào dùng:**
- 🌱 **Cây rễ xuất khẩu**
- 🌱 **Cây xuất khẩu A, B**
- 🌱 Các loại cây có tên chứa từ khóa: "xuất khẩu", "export"
- 🌱 Cần tem dễ đọc từ xa

**Nội dung hiển thị:**
```
┌────────────────────────────────┐
│ Đồng tiền đỏ         ║████████║│
│ Lô #123 - T1         ║████████║│  <- QR lớn
│ NV: Nguyễn Văn A     ║████████║│
└────────────────────────────────┘
```

---

### 📏 Tem nhỏ 25×15mm (3 hàng nhãn trên cuộn)

**Đặc điểm:**
- ✅ Tiết kiệm giấy (~40% so với tem lớn)
- ✅ Chữ vừa phải, vẫn đọc rõ (cỡ chữ 32pt, 24pt, 20pt)
- ✅ QR code compact nhưng đủ quét (70% chiều cao)
- ✅ Phù hợp in bằng máy in tem 3 hàng

**Khi nào dùng:**
- 🌿 **Cây thường** (Đồng tiền, Khoai lang, v.v.)
- 🌿 Các loại cây không cần tem quá lớn
- 🌿 Muốn tiết kiệm chi phí giấy in
- 🌿 In số lượng lớn hàng ngày

**Nội dung hiển thị:**
```
┌─────────────────────┐
│ Đồng tiền.. ║██████║│
│ #123/T1     ║██████║│  <- QR vừa
│ Nguyễn V.A  ║██████║│
└─────────────────────┘
```

---

## 🤖 TỰ ĐỘNG HÓA THÔNG MINH

### Hệ thống tự động phát hiện kích thước phù hợp

**Logic:**
```python
Nếu tên giống chứa:
  - "cây rễ xuất khẩu"
  - "xuất khẩu"
  - "cây xuất khẩu"
  - "cây a", "cây b"
  - "export"
→ Gợi ý: Tem LỚN 35×22mm

Ngược lại:
→ Gợi ý: Tem NHỎ 25×15mm
```

**Ưu điểm:**
- ✅ Không cần suy nghĩ, hệ thống tự gợi ý
- ✅ Vẫn có thể chọn thủ công nếu cần
- ✅ Tối ưu chi phí và chất lượng

---

## 🚀 Cách sử dụng

### 1️⃣ In tem ngay khi nhập liệu

**Bước 1:** Đăng nhập → Trang **"Nhập liệu"**

**Bước 2:** Điền đầy đủ thông tin form và nhấn **"💾 Lưu dữ liệu"**

**Bước 3:** Sau khi lưu thành công, cuộn xuống phần **"🏷️ In tem nhãn"**

**Bước 4:** Chọn kích thước tem:
- **"Tự động"** - Hệ thống gợi ý dựa trên loại cây
- **"35x22mm (2 hàng)"** - Tem lớn, chữ to
- **"25x15mm (3 hàng)"** - Tem nhỏ, tiết kiệm

**Bước 5:** Xem **Preview** tem nhãn bên phải

**Bước 6:** Nhấn **"📥 Tải tem nhãn (XXxYYmm) - PDF"**

---

### 2️⃣ In tem từ trang "Báo cáo Năng suất"

**Bước 1:** Vào trang **"Báo cáo Năng suất"**

**Bước 2:** Cuộn xuống phần **"🏷️ In tem nhãn"**

**Bước 3:** Chọn lô cần in từ dropdown

**Bước 4:** Chọn kích thước tem:
- **"Tự động"** - Có gợi ý bên cạnh
- **"35x22mm"** - Tem lớn
- **"25x15mm"** - Tem nhỏ

**Bước 5:** Xem preview tem và thông tin QR

**Bước 6:** Nhấn **"📥 Tải tem (XXxYYmm)"**

---

## 📱 Quét mã QR

(Không thay đổi - giữ nguyên như cũ)

---

## 🖨️ In tem nhãn

### Chuẩn bị

**Máy in hỗ trợ:**
- ✅ Máy in tem 2 hàng: Dùng cuộn 35×22mm
- ✅ Máy in tem 3 hàng: Dùng cuộn 25×15mm
- ✅ Xprinter XP-360B, XP-370B, XP-450B
- ✅ Brother QL-700, QL-800
- ✅ Zebra ZD410, ZD420

**Giấy tem cần:**
- 📦 Cuộn tem 35×22mm (2 hàng) - Cho cây xuất khẩu
- 📦 Cuộn tem 25×15mm (3 hàng) - Cho cây thường

---

### Bước in

**Bước 1:** Tải file PDF tem nhãn (đã đúng kích thước)

**Bước 2:** Mở file bằng:
- Adobe Acrobat Reader
- Trình duyệt (Chrome, Edge)

**Bước 3:** Nhấn **Ctrl+P** để in

**Bước 4:** Cài đặt máy in:
```
Máy in: [Chọn máy in tem của bạn]
Kích thước giấy:
  - Nếu file là 35x22mm → Chọn "35mm x 22mm"
  - Nếu file là 25x15mm → Chọn "25mm x 15mm"
Scale: 100% (Actual size)
Margins: None
```

**Bước 5:** Nhấn **Print**

✅ **Máy in sẽ tự động nhận diện đúng kích thước!**

---

## 💡 So sánh 2 loại tem

| Tiêu chí | Tem 35×22mm | Tem 25×15mm |
|----------|-------------|-------------|
| **Kích thước** | Lớn (2 hàng) | Nhỏ (3 hàng) |
| **Cỡ chữ** | To (50/35/28pt) | Vừa (32/24/20pt) |
| **QR code** | Lớn (75% cao) | Vừa (70% cao) |
| **Độ rõ** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Tiết kiệm** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Dùng cho** | Cây xuất khẩu | Cây thường |
| **Chi phí/tem** | ~500đ | ~300đ |
| **Số tem/cuộn** | ~300-500 | ~700-1000 |

---

## 🔧 Khắc phục sự cố

### ❌ Lỗi: "Máy in không nhận diện kích thước"

**Nguyên nhân:** Driver chưa có kích thước tùy chỉnh

**Giải pháp:**
1. Vào **Cài đặt máy in** → **Preferences**
2. Chọn tab **Page Setup** hoặc **Paper**
3. Thêm kích thước tùy chỉnh:
   - Tên: "Label 35x22"
   - Width: 35mm, Height: 22mm
   - Hoặc: "Label 25x15"
   - Width: 25mm, Height: 15mm
4. Lưu và thử in lại

---

### ❌ Lỗi: "Tem in ra bị nhỏ hoặc lớn không đúng"

**Nguyên nhân:** Scale không đúng 100%

**Giải pháp:**
1. Khi in, đảm bảo chọn:
   - **Scale: 100%** hoặc **Actual size**
   - **KHÔNG chọn**: "Fit to page", "Shrink to fit"
2. Margins: **None** hoặc **0**

---

### ❌ Lỗi: "Chữ bị mờ hoặc không rõ"

**Nguyên nhân:** DPI máy in thấp

**Giải pháp:**
1. Kiểm tra cài đặt chất lượng in:
   - Chọn **High Quality** hoặc **Best**
   - DPI: ≥ 300 (nếu có tùy chọn)
2. Kiểm tra mực/nước in còn đủ
3. Thử in thử 1 tem trước khi in hàng loạt

---

### ❌ Lỗi: "QR code không quét được"

**Nguyên nhân:** QR bị mờ hoặc nhỏ quá

**Giải pháp:**
1. Nếu dùng tem 25×15mm và QR bị mờ:
   - **Chuyển sang tem 35×22mm** (QR lớn hơn)
2. Tăng độ tương phản khi in:
   - Darkness: High
   - Density: Maximum

---

## 🎓 Mẹo sử dụng chuyên nghiệp

### 1. Phân loại cuộn tem

**Tủ tem A:**
- 📦 Cuộn 35×22mm → Dán nhãn "CÂY XUẤT KHẨU"
- Dùng cho: Cây rễ, cây xuất khẩu A/B

**Tủ tem B:**
- 📦 Cuộn 25×15mm → Dán nhãn "CÂY THƯỜNG"
- Dùng cho: Đồng tiền, Khoai lang, v.v.

---

### 2. Quy trình in hàng loạt

**Sáng:** In tem cho cây xuất khẩu (35×22mm)
1. Lắp cuộn 35×22mm vào máy
2. In tất cả tem cây xuất khẩu
3. Dán tem lên túi cây

**Chiều:** In tem cho cây thường (25×15mm)
1. Thay cuộn 25×15mm
2. In tất cả tem cây thường
3. Dán tem lên túi cây

**Lợi ích:**
- ✅ Không cần thay cuộn nhiều lần
- ✅ Tiết kiệm thời gian
- ✅ Giảm lãng phí giấy

---

### 3. Kiểm tra chất lượng định kỳ

**Mỗi tuần:**
1. In thử 1 tem 35×22mm → Quét QR
2. In thử 1 tem 25×15mm → Quét QR
3. Kiểm tra độ rõ chữ

**Nếu có vấn đề:**
- Vệ sinh đầu in
- Kiểm tra mực/nước in
- Hiệu chỉnh máy in

---

### 4. Lưu trữ tem PDF

**Cấu trúc thư mục:**
```
📁 Tem_Nhan/
  📁 2026/
    📁 Thang_01/
      📄 tem_nhan_lo_123_35_22.pdf
      📄 tem_nhan_lo_124_25_15.pdf
      📄 ...
```

**Tên file chuẩn:**
- `tem_nhan_lo_[ID]_[KichThuoc].pdf`
- Ví dụ: `tem_nhan_lo_123_35_22.pdf`

---

## 📊 Thống kê chi phí

### Chi phí 1 tháng (ví dụ)

**Giả sử:**
- Cây xuất khẩu: 100 lô/tháng → Tem 35×22mm
- Cây thường: 300 lô/tháng → Tem 25×15mm

**Tính toán:**
```
Tem 35×22mm: 100 tem × 500đ = 50,000đ
Tem 25×15mm: 300 tem × 300đ = 90,000đ
Tổng: 140,000đ/tháng
```

**So với tem 50×30mm cũ:**
```
400 tem × 600đ = 240,000đ/tháng
Tiết kiệm: 100,000đ/tháng (42%)
```

---

## 🎯 Kết luận

Hệ thống 2 kích thước tem nhãn giúp:
- ✅ **Linh hoạt**: Chọn kích thước phù hợp từng loại cây
- ✅ **Tiết kiệm**: Giảm 40% chi phí so với tem cố định
- ✅ **Tự động**: Hệ thống gợi ý thông minh
- ✅ **Chuyên nghiệp**: Tem đẹp, dễ đọc, dễ quét
- ✅ **Dễ sử dụng**: Preview trước khi in

**Khuyến nghị:**
- 🌱 Cây xuất khẩu, cây quan trọng → **Tem 35×22mm**
- 🌿 Cây thường, sản xuất hàng loạt → **Tem 25×15mm**

---

**Phát triển bởi:** AI Assistant  
**Phiên bản:** 3.1 (Với 2 kích thước tem linh hoạt)  
**Ngày cập nhật:** 02/01/2026


## 🚀 Cách sử dụng

### 1️⃣ Tạo mã QR và tem nhãn khi nhập liệu

**Bước 1:** Đăng nhập vào ứng dụng
- Tên đăng nhập: `admin` hoặc tài khoản nhân viên
- Mã nhân viên: `ADMIN001` hoặc mã của bạn

**Bước 2:** Vào trang **"Nhập liệu"**

**Bước 3:** Điền đầy đủ thông tin form:
- Ngày cấy
- Tên giống cây
- Chu kỳ
- Môi trường
- Số túi, số cụm
- Giờ bắt đầu, kết thúc
- Số Giàn/Kệ (nếu muốn)

**Bước 4:** Nhấn **"💾 Lưu dữ liệu"**

**Bước 5:** Sau khi lưu thành công, hệ thống sẽ tự động:
- ✅ Tạo mã QR duy nhất cho lô này
- ✅ Hiển thị preview tem nhãn
- ✅ Cho phép tải tem nhãn dưới dạng PDF

**Bước 6:** Nhấn **"📥 Tải tem nhãn (PDF)"** để tải file

---

### 2️⃣ In tem nhãn từ trang "Báo cáo Năng suất"

**Bước 1:** Vào trang **"Báo cáo Năng suất"**

**Bước 2:** Chọn bộ lọc (nếu cần):
- Từ ngày - Đến ngày
- Chu kỳ
- Nhân viên (nếu là Admin)

**Bước 3:** Cuộn xuống phần **"🏷️ In tem nhãn"**

**Bước 4:** Chọn lô cần in từ dropdown:
```
ID 123 - Đồng tiền đỏ - 02/01/2026
```

**Bước 5:** Xem preview tem nhãn và mã QR

**Bước 6:** Nhấn **"📥 Tải tem (PDF)"** để tải file

---

### 3️⃣ Quét mã QR để truy cập nhanh

#### 🔹 Sử dụng điện thoại/máy tính bảng:

**Bước 1:** Mở **Camera** trên điện thoại

**Bước 2:** Hướng camera vào **mã QR** trên tem nhãn

**Bước 3:** Nhấn vào thông báo **"Mở link"** xuất hiện

**Bước 4:** Trình duyệt sẽ tự động mở ứng dụng và:
- ✅ Chuyển đến trang **"Quản lý Phòng Sáng"**
- ✅ Tự động **mở expander** của lô đã quét
- ✅ Hiển thị thông báo: **"✅ Đã quét QR Code! Đang hiển thị lô ID: XXX"**

**Bước 5:** Cập nhật thông tin lô:
- Số Giàn/Kệ
- Số túi theo tình trạng (Sạch, Khuẩn nhẹ, Khuẩn nặng, Nấm, Khuẩn môi trường, Khác)
- Trạng thái (Đang nuôi, Đã xuất, Hủy)

**Bước 6:** Nhấn **"💾 Cập nhật"**

---

## 📱 Cấu trúc tem nhãn

Tem nhãn kích thước **50mm × 30mm** bao gồm:

```
┌─────────────────────────────────┐
│ 🌱 Đồng tiền đỏ          ║█████║│
│ 📅 02/01/2026            ║█████║│
│ 📆 Tuần 1                ║█████║│ <- Mã QR
│ 👤 Nguyễn Văn A          ║█████║│
│ 🔄 Nhân nhanh            ║█████║│
└─────────────────────────────────┘
```

**Thông tin trên tem:**
- 🌱 Tên giống cây
- 📅 Ngày cấy (dd/mm/yyyy)
- 📆 Tuần cấy
- 👤 Tên nhân viên
- 🔄 Chu kỳ
- 🔳 Mã QR (góc phải)

---

## 🖨️ In tem nhãn

### Phương pháp 1: In trực tiếp từ PDF

**Bước 1:** Tải file PDF tem nhãn

**Bước 2:** Mở file PDF bằng:
- Adobe Acrobat Reader
- Foxit Reader
- Trình duyệt (Chrome, Edge, Firefox)

**Bước 3:** Nhấn **Ctrl+P** hoặc **File → Print**

**Bước 4:** Chọn máy in:
- Máy in tem nhãn nhiệt (Xprinter, Brother, Zebra)
- Máy in laser/inkjet (nếu in lên giấy A4)

**Bước 5:** Cài đặt in:
- **Kích thước giấy:** Custom (50mm × 30mm)
- **Orientation:** Landscape (nếu cần)
- **Scale:** 100% (Actual size)

**Bước 6:** Nhấn **Print**

### Phương pháp 2: Sử dụng máy in tem nhiệt chuyên dụng

**Máy hỗ trợ:**
- ✅ Xprinter XP-360B, XP-370B
- ✅ Brother QL-700, QL-800
- ✅ Zebra ZD410, ZD420
- ✅ Dymo LabelWriter

**Cài đặt:**
1. Cài driver máy in từ nhà sản xuất
2. Chọn kích thước nhãn: **50mm × 30mm**
3. Đặt giấy tem vào máy
4. In từ file PDF

---

## 🔧 Khắc phục sự cố

### ❌ Lỗi: "Không tải được PDF"

**Nguyên nhân:** Thiếu thư viện `reportlab`

**Giải pháp:**
```bash
pip install reportlab
```

Hoặc chạy lại:
```bash
pip install -r requirements.txt
```

---

### ❌ Lỗi: "Mã QR không hiển thị"

**Nguyên nhân:** Thiếu thư viện `qrcode` hoặc `Pillow`

**Giải pháp:**
```bash
pip install qrcode Pillow
```

Hoặc chạy lại:
```bash
pip install -r requirements.txt
```

---

### ❌ Lỗi: "Quét QR không chuyển trang"

**Nguyên nhân:** Chưa đăng nhập

**Giải pháp:**
1. Đăng nhập vào ứng dụng trước
2. Sau đó mới quét QR code
3. Đảm bảo URL có dạng: `http://localhost:8501/?lo_id=123`

---

### ❌ Lỗi: "Tem nhãn in ra bị mờ"

**Nguyên nhân:** DPI thấp hoặc máy in không đúng cài đặt

**Giải pháp:**
1. Đảm bảo in ở **100% (Actual size)**
2. Không chọn **"Fit to page"** hoặc **"Shrink to fit"**
3. Kiểm tra cài đặt DPI của máy in (nên là 300 DPI trở lên)
4. Thử in trên giấy A4 để kiểm tra chất lượng trước

---

### ❌ Lỗi: "Font chữ không đẹp"

**Nguyên nhân:** Hệ thống không có font `arial.ttf`

**Giải pháp:**
- Trên Windows: Font Arial có sẵn, không cần làm gì
- Trên Linux:
  ```bash
  sudo apt-get install ttf-mscorefonts-installer
  ```
- Trên MacOS: Font Arial có sẵn

**Lưu ý:** Nếu không có font, ứng dụng sẽ dùng font mặc định (vẫn hoạt động bình thường)

---

## 💡 Mẹo sử dụng

### 1️⃣ In hàng loạt

**Cách 1:** In từng lô một từ trang "Báo cáo Năng suất"

**Cách 2:** In nhiều tem cùng lúc:
1. Lọc dữ liệu theo ngày
2. Chọn từng lô và tải PDF
3. Mở tất cả PDF và in cùng lúc

### 2️⃣ Lưu tem nhãn

- Tải PDF về máy
- Lưu vào thư mục có tên theo ngày: `Tem_02_01_2026`
- Dễ tìm lại khi cần in lại

### 3️⃣ Sử dụng QR code

**Tình huống:** Nhân viên đang ở nhà lưới, cần cập nhật tình trạng cây

**Giải pháp:**
1. Mang điện thoại/máy tính bảng vào nhà lưới
2. Quét QR trên tem nhãn
3. Cập nhật ngay trên ứng dụng
4. Không cần nhớ ID lô, không cần tìm kiếm thủ công

### 4️⃣ Kiểm tra trước khi in

- Xem preview tem trước khi in
- Kiểm tra thông tin đã chính xác chưa
- Thử in 1 tem để kiểm tra chất lượng
- Sau đó mới in hàng loạt

---

## 📊 Lưu ý quan trọng

### ⚠️ URL trong mã QR

**URL mặc định:** `http://localhost:8501/?lo_id=123`

**Lưu ý:**
- URL này chỉ hoạt động khi ứng dụng chạy trên máy local
- Nếu triển khai lên server, cần thay đổi `base_url` trong file `app.py`

**Cách thay đổi (cho Admin/Developer):**

Mở file `app.py`, tìm hàm `generate_qr_code`:

```python
def generate_qr_code(data_id):
    # Tạo URL với query parameter
    # Trong production, thay bằng URL thật của ứng dụng
    base_url = "http://localhost:8501"  # <- Thay đổi dòng này
    qr_data = f"{base_url}/?lo_id={data_id}"
    # ...
```

**Ví dụ thay đổi:**
```python
base_url = "https://quanlylab.yourdomain.com"
# Hoặc
base_url = "http://192.168.1.100:8501"  # IP trong mạng LAN
```

---

### ⚠️ Kích thước tem nhãn

**Mặc định:** 50mm × 30mm (tiêu chuẩn)

**Nếu muốn thay đổi:** Sửa trong hàm `create_label_image` ở file `app.py`:

```python
# Kích thước tem nhãn (mm -> pixels, 300 DPI)
width_mm, height_mm = 50, 30  # <- Thay đổi dòng này
```

**Kích thước phổ biến:**
- 50mm × 30mm (mặc định)
- 40mm × 25mm (nhỏ hơn)
- 60mm × 40mm (lớn hơn)

---

## 🎯 Kết luận

Tính năng **Mã QR và In Tem Nhãn** giúp:
- ✅ Tự động hóa quy trình ghi nhãn
- ✅ Truy xuất thông tin nhanh chóng
- ✅ Giảm sai sót khi nhập liệu thủ công
- ✅ Quản lý chuyên nghiệp hơn

**Bất kỳ thắc mắc nào, vui lòng liên hệ Admin!**

---

**Phát triển bởi:** AI Assistant  
**Phiên bản:** 3.0 (Với tính năng QR & Tem Nhãn)  
**Ngày cập nhật:** 02/01/2026

