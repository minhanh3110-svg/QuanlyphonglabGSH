# ☁️ HƯỚNG DẪN DEPLOY LÊN STREAMLIT CLOUD

Hướng dẫn chi tiết deploy ứng dụng Quản lý Lab Nuôi Cấy lên Streamlit Cloud **HOÀN TOÀN MIỄN PHÍ**.

---

## 🎯 Tại sao chọn Streamlit Cloud?

✅ **MIỄN PHÍ 100%** (không cần thẻ tín dụng)  
✅ **Tự động deploy** khi push code mới lên GitHub  
✅ **Unlimited apps** (không giới hạn số lượng app)  
✅ **SSL/HTTPS** tự động  
✅ **Tên miền đẹp:** `your-app.streamlit.app`  
✅ **Không cần cấu hình server**  
✅ **Resources:** 1GB RAM, 1 CPU core (đủ cho app này)  

---

## 📋 Yêu cầu trước khi deploy

### 1. Tài khoản GitHub
- Đã có tài khoản GitHub: https://github.com
- Code đã được push lên GitHub repository

### 2. File bắt buộc trong repository

```
YOUR_REPO/
├── app.py                ✅ File chính (bắt buộc)
├── requirements.txt      ✅ Danh sách thư viện (bắt buộc)
└── .gitignore           ✅ Loại trừ file không cần (khuyến nghị)
```

### 3. File `requirements.txt` phải chính xác

```txt
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
plotly>=5.17.0
qrcode>=7.4.2
Pillow>=10.0.0
reportlab>=4.0.0
```

---

## 🚀 Các bước deploy

### BƯỚC 1: Đăng nhập Streamlit Cloud

1. Truy cập: https://share.streamlit.io
2. Click **"Sign in"**
3. Chọn **"Continue with GitHub"**
4. Đăng nhập GitHub và cho phép Streamlit truy cập

**Lưu ý:** Lần đầu tiên GitHub sẽ hỏi bạn cho phép Streamlit truy cập repositories.

---

### BƯỚC 2: Tạo app mới

1. Sau khi đăng nhập, click **"New app"** (góc trên bên phải)

2. Điền thông tin:

   **a. Repository, branch, and file:**
   - **Repository:** Chọn `YOUR_USERNAME/QUANLYLAB` từ dropdown
   - **Branch:** `main` (mặc định)
   - **Main file path:** `app.py`

   **b. App URL (optional - tùy chỉnh):**
   - **App URL:** `quanlylab` hoặc tên khác
   - URL cuối cùng: `https://YOUR_USERNAME-quanlylab.streamlit.app`

3. Click **"Deploy!"** (nút màu đỏ)

---

### BƯỚC 3: Chờ deploy

**Quá trình deploy:**

1. **Installing Python packages** (~1-2 phút)
   - Cài đặt tất cả thư viện trong `requirements.txt`
   - Xem logs để theo dõi tiến trình

2. **Starting up** (~30 giây)
   - Khởi động ứng dụng
   - Chạy `app.py`

3. **Running** 🎉
   - Ứng dụng đã online!
   - Tự động mở trong tab mới

**Tổng thời gian:** ~2-5 phút

---

### BƯỚC 4: Kiểm tra app

1. URL ứng dụng: `https://YOUR_USERNAME-quanlylab.streamlit.app`
2. Thử đăng nhập:
   - Tên đăng nhập: `admin`
   - Mã nhân viên: `ADMIN001`
3. Kiểm tra các tính năng hoạt động

---

### BƯỚC 5: Cập nhật URL QR Code

⚠️ **Quan trọng:** Để QR Code hoạt động đúng, cần cập nhật URL trong code.

1. **Mở file `app.py`**

2. **Tìm dòng:**
```python
base_url = "http://localhost:8501"
```

3. **Thay bằng URL Streamlit Cloud:**
```python
base_url = "https://YOUR_USERNAME-quanlylab.streamlit.app"
```

**Ví dụ:**
```python
base_url = "https://labcaymo-quanlylab.streamlit.app"
```

4. **Lưu file và push lên GitHub:**
```bash
git add app.py
git commit -m "Cập nhật URL cho Streamlit Cloud"
git push
```

5. **Streamlit Cloud tự động deploy lại** (~2 phút)

---

## 🔧 Cấu hình nâng cao (Advanced settings)

Khi tạo app, click **"Advanced settings"** để tùy chỉnh:

### 1. Python version
```
Python 3.9  (khuyến nghị)
hoặc
Python 3.10
```

### 2. Secrets (biến môi trường)
Nếu cần lưu API key, mật khẩu:
```toml
# .streamlit/secrets.toml
[passwords]
admin_password = "your_secure_password"

[api_keys]
openai_key = "sk-xxxxxxxxxxxxx"
```

**Cách thêm secrets:**
1. Vào app đã deploy → **"Settings"** → **"Secrets"**
2. Paste nội dung secrets vào ô
3. Click **"Save"**

### 3. Resource limits (Mặc định)
- **Memory:** 1 GB RAM
- **CPU:** 1 vCPU

⚠️ **Không thể thay đổi** trong bản miễn phí.

---

## 📊 Quản lý app sau khi deploy

### Dashboard Streamlit Cloud

Truy cập: https://share.streamlit.io/

Tại đây bạn có thể:

#### 1. Xem logs
- **Menu app** → **"Logs"**
- Xem lỗi runtime, thông báo hệ thống

#### 2. Restart app
- **Menu app** → **"Reboot app"**
- Khởi động lại nếu app bị lỗi

#### 3. Xem analytics
- **Menu app** → **"Analytics"**
- Số lượng người truy cập
- Thời gian sử dụng

#### 4. Settings
- **Menu app** → **"Settings"**
- Đổi tên app
- Thêm secrets
- Xóa app

#### 5. Xóa app
- **Menu app** → **"Settings"** → **"Delete app"**
- Xác nhận xóa

---

## 🔄 Cập nhật app (Auto-deploy)

**Streamlit Cloud tự động deploy khi bạn push code mới!**

### Workflow cập nhật

```bash
# 1. Sửa code trên máy local
# (dùng editor của bạn)

# 2. Test trên local
streamlit run app.py

# 3. Commit và push
git add .
git commit -m "Thêm tính năng XYZ"
git push

# 4. Đợi 2-3 phút
# Streamlit Cloud tự động:
# - Phát hiện thay đổi
# - Pull code mới
# - Cài lại thư viện (nếu requirements.txt thay đổi)
# - Restart app

# 5. Kiểm tra app online
# (mở URL app trong trình duyệt)
```

### Theo dõi quá trình deploy

1. Vào https://share.streamlit.io
2. Click vào app đang deploy
3. Xem logs real-time:
   ```
   [Deploying...]
   Installing packages...
   Starting app...
   [Your app is live!]
   ```

---

## 🐛 Xử lý lỗi thường gặp

### ❌ Lỗi: `ModuleNotFoundError: No module named 'xxx'`

**Nguyên nhân:** Thiếu thư viện trong `requirements.txt`

**Giải pháp:**
1. Thêm thư viện vào `requirements.txt`:
```txt
streamlit>=1.28.0
pandas>=2.0.0
xxx>=1.0.0  # Thêm dòng này
```

2. Push lên GitHub:
```bash
git add requirements.txt
git commit -m "Thêm thư viện xxx"
git push
```

3. Streamlit Cloud tự động cài lại

---

### ❌ Lỗi: `This app has encountered an error`

**Nguyên nhân:** Lỗi trong code Python

**Giải pháp:**
1. Xem logs để tìm lỗi cụ thể:
   - Vào app → **"Manage app"** → **"Logs"**
2. Sửa lỗi trong code
3. Push lại lên GitHub

---

### ❌ Lỗi: `File "app.py" not found`

**Nguyên nhân:** Sai đường dẫn file

**Giải pháp:**
1. Vào Streamlit Cloud → **Settings** → **"Edit"**
2. Kiểm tra **Main file path:** phải là `app.py` (không có `/` ở đầu)
3. Click **"Save"**

---

### ❌ Lỗi: `App is taking longer than usual to load`

**Nguyên nhân:** App quá nặng hoặc cài nhiều thư viện

**Giải pháp:**
1. **Chờ thêm 2-3 phút** (lần đầu cài thư viện lâu)
2. **Tối ưu code:**
   - Dùng `@st.cache_data` cho hàm nặng
   - Giảm dữ liệu load ban đầu
3. **Tối ưu requirements.txt:**
   - Chỉ giữ thư viện thực sự cần dùng
   - Xóa thư viện không dùng

---

### ❌ Lỗi: `Memory limit exceeded`

**Nguyên nhân:** App dùng quá 1GB RAM

**Giải pháp:**
1. **Tối ưu code:**
   ```python
   # ❌ TỐN BỘ NHỚ
   df = pd.read_sql("SELECT * FROM big_table", conn)
   
   # ✅ TỐI ƯU
   df = pd.read_sql("SELECT * FROM big_table LIMIT 1000", conn)
   ```

2. **Xóa cache:**
   ```python
   @st.cache_data(max_entries=10)  # Giới hạn cache
   def load_data():
       return pd.read_csv('data.csv')
   ```

3. **Giảm dữ liệu trong database:**
   - Xóa dữ liệu cũ/test
   - Lưu chỉ dữ liệu cần thiết

---

### ❌ Lỗi: `Unable to connect to GitHub`

**Nguyên nhân:** Repository không public hoặc Streamlit không có quyền

**Giải pháp:**
1. **Đảm bảo repo là Public:**
   - Vào GitHub repo → **Settings** → **Danger Zone** → **Change visibility** → **Public**

2. **Cấp quyền cho Streamlit:**
   - Vào GitHub → **Settings** → **Applications** → **Streamlit** → **Grant access**

---

## 💰 Giới hạn bản miễn phí

### Streamlit Community Cloud (FREE)

| Tính năng | Giới hạn |
|-----------|---------|
| **Số lượng app** | Không giới hạn |
| **RAM** | 1 GB/app |
| **CPU** | 1 vCPU/app |
| **Storage** | 50 GB (tổng tất cả app) |
| **Băng thông** | Không giới hạn |
| **Concurrent users** | ~100-200 người |
| **Uptime** | 99.9% |
| **Custom domain** | ❌ Không (chỉ .streamlit.app) |
| **Private apps** | ❌ Không (tất cả đều public) |

### Nâng cấp (nếu cần)

**Streamlit for Teams** ($250/tháng):
- 5 GB RAM/app
- 4 vCPU/app
- Private apps
- Custom domains
- Priority support

**Không cần thiết** cho ứng dụng này!

---

## 🎯 Tối ưu hiệu suất

### 1. Cache dữ liệu

```python
@st.cache_data(ttl=3600)  # Cache 1 giờ
def load_data_from_db():
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query("SELECT * FROM nhat_ky_cay", conn)
    conn.close()
    return df

# Sử dụng
df = load_data_from_db()  # Chỉ query DB 1 lần/giờ
```

### 2. Lazy loading

```python
# ❌ TỐN TÀI NGUYÊN
df = pd.read_sql("SELECT * FROM nhat_ky_cay", conn)  # Load tất cả

# ✅ TỐI ƯU
if st.button("Xem dữ liệu"):
    df = pd.read_sql("SELECT * FROM nhat_ky_cay LIMIT 100", conn)
```

### 3. Giảm số lượng chart

```python
# Chỉ vẽ chart khi admin mở tab Dashboard
if is_admin:
    with st.expander("📊 Biểu đồ phân tích"):
        fig = px.bar(...)  # Chỉ vẽ khi expand
        st.plotly_chart(fig)
```

### 4. Tối ưu database

```python
# Thêm index cho query nhanh
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute("CREATE INDEX IF NOT EXISTS idx_ngay_cay ON nhat_ky_cay(ngay_cay)")
c.execute("CREATE INDEX IF NOT EXISTS idx_ma_nv ON nhat_ky_cay(ma_nhan_vien)")
conn.commit()
```

---

## 📱 Chia sẻ app

### URL công khai

```
https://YOUR_USERNAME-quanlylab.streamlit.app
```

**Ai cũng có thể truy cập URL này!**

### Nhúng vào website (iframe)

```html
<iframe src="https://YOUR_USERNAME-quanlylab.streamlit.app" 
        width="100%" 
        height="800px" 
        frameborder="0">
</iframe>
```

### Tạo QR Code cho app

1. Truy cập: https://www.qr-code-generator.com
2. Paste URL app
3. Download QR Code PNG
4. In ra hoặc gửi cho nhân viên

---

## 🔒 Bảo mật

### ⚠️ Lưu ý quan trọng

Bản miễn phí Streamlit Cloud:
- ❌ **App luôn PUBLIC** (ai cũng truy cập được)
- ❌ **Không có SSL riêng** (dùng chung .streamlit.app)
- ❌ **Không private** repository

### 🛡️ Cách bảo mật

#### 1. Đăng nhập bắt buộc
✅ **Đã làm:** App yêu cầu đăng nhập trước khi dùng

#### 2. Không lưu dữ liệu nhạy cảm
⚠️ **Tránh:** 
- Số điện thoại, CMND
- Địa chỉ chi tiết
- Thông tin tài chính

#### 3. Dùng secrets cho API key
```python
# Trong code
api_key = st.secrets["api_keys"]["openai_key"]

# Trên Streamlit Cloud: Settings → Secrets
[api_keys]
openai_key = "sk-xxxxx"
```

#### 4. Giới hạn IP (nếu cần)
```python
import streamlit as st

ALLOWED_IPS = ["192.168.1.100", "10.0.0.50"]
user_ip = st.experimental_get_query_params().get("client_ip", [""])[0]

if user_ip not in ALLOWED_IPS:
    st.error("❌ Bạn không có quyền truy cập từ IP này")
    st.stop()
```

---

## 📊 Monitoring

### 1. Google Analytics (optional)

Thêm vào `app.py`:
```python
import streamlit.components.v1 as components

# Google Analytics
ga_code = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
"""
components.html(ga_code, height=0)
```

### 2. Error logging

```python
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

try:
    # Your code
    pass
except Exception as e:
    logging.error(f"Error: {e}")
    st.error("Đã xảy ra lỗi, vui lòng thử lại")
```

---

## 🎉 Checklist Deploy thành công

### Trước khi deploy
- [ ] Code chạy tốt trên local
- [ ] File `requirements.txt` chính xác
- [ ] File `.gitignore` đã loại trừ file không cần
- [ ] Code đã push lên GitHub
- [ ] Repository là **Public**

### Sau khi deploy
- [ ] App mở được URL
- [ ] Đăng nhập thành công
- [ ] Các tính năng hoạt động
- [ ] QR Code được cập nhật URL mới
- [ ] Không có lỗi trong Logs
- [ ] Test trên mobile

---

## 📚 Tài liệu tham khảo

- **Streamlit Cloud Docs:** https://docs.streamlit.io/streamlit-community-cloud
- **Deployment Guide:** https://docs.streamlit.io/streamlit-community-cloud/get-started
- **Troubleshooting:** https://docs.streamlit.io/knowledge-base/deploy

---

## 🆘 Cần hỗ trợ?

### Community Forum
- https://discuss.streamlit.io

### GitHub Issues
- https://github.com/YOUR_USERNAME/QUANLYLAB/issues

### Email
- your.email@example.com

---

**🎊 Chúc mừng! App của bạn đã online 24/7 hoàn toàn miễn phí!**

