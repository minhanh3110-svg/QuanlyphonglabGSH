# 🚀 HƯỚNG DẪN PUSH LÊN GITHUB

## ✅ ĐÃ HOÀN THÀNH
- [x] Khởi tạo Git repository
- [x] Sửa file `.gitignore`
- [x] Commit tất cả file

---

## 📋 BƯỚC TIẾP THEO

### **Bước 1: Tạo Repository trên GitHub**

1. Truy cập: https://github.com
2. Đăng nhập vào tài khoản của bạn
3. Click nút **"New"** (góc trên bên trái) hoặc **"+"** → **"New repository"**
4. Điền thông tin:
   - **Repository name**: `QuanLyPhongLabGSH` (hoặc tên khác)
   - **Description**: `Hệ thống quản lý phòng nuôi cấy mô với QR code và in tem nhãn`
   - **Public** hoặc **Private**: Tùy chọn
   - ⚠️ **KHÔNG** tick vào:
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
5. Click **"Create repository"**

---

### **Bước 2: Copy URL của Repository**

Sau khi tạo xong, GitHub sẽ hiển thị 1 trang với URL dạng:
```
https://github.com/USERNAME/QuanLyPhongLabGSH.git
```

**Copy URL này!** (Thay `USERNAME` bằng username GitHub của bạn)

---

### **Bước 3: Push Code lên GitHub**

Mở **PowerShell** hoặc **Terminal** và chạy các lệnh sau:

```powershell
# Di chuyển vào thư mục dự án
cd D:\QUANLYLAB

# Thêm remote repository (thay YOUR_GITHUB_URL bằng URL bạn vừa copy)
git remote add origin https://github.com/USERNAME/QuanLyPhongLabGSH.git

# Đổi tên branch thành main (nếu cần)
git branch -M main

# Push code lên GitHub
git push -u origin main
```

---

### **Bước 4: Nhập Username và Password**

Khi chạy lệnh `git push`, GitHub sẽ yêu cầu:

1. **Username**: Nhập username GitHub của bạn
2. **Password**: ⚠️ **KHÔNG phải mật khẩu bình thường!**
   - Cần tạo **Personal Access Token (PAT)**

#### **Cách tạo Personal Access Token:**

1. Truy cập: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Đặt tên: `QuanLyLab`
4. Chọn thời hạn: `No expiration` (hoặc tùy chọn)
5. Tick vào quyền: **`repo`** (toàn bộ quyền repo)
6. Click **"Generate token"**
7. **Copy token** (chỉ hiển thị 1 lần duy nhất!)
8. Dán token này vào ô **Password** khi Git yêu cầu

---

### **Bước 5: Xác nhận thành công**

Sau khi push thành công, bạn sẽ thấy:
```
Enumerating objects: 20, done.
Counting objects: 100% (20/20), done.
Writing objects: 100% (20/20), done.
Total 20 (delta 0), reused 0 (delta 0)
To https://github.com/USERNAME/QuanLyPhongLabGSH.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **HOÀN THÀNH!** Code đã được push lên GitHub!

---

## 🔧 LỆNH NHANH (Copy & Paste)

```powershell
cd D:\QUANLYLAB
git remote add origin https://github.com/USERNAME/QuanLyPhongLabGSH.git
git branch -M main
git push -u origin main
```

**⚠️ Nhớ thay `USERNAME` và `QuanLyPhongLabGSH` bằng thông tin của bạn!**

---

## 🆘 XỬ LÝ LỖI THƯỜNG GẶP

### **Lỗi 1: remote origin already exists**
```powershell
git remote remove origin
git remote add origin https://github.com/USERNAME/QuanLyPhongLabGSH.git
```

### **Lỗi 2: Authentication failed**
- Tạo lại Personal Access Token (xem hướng dẫn ở Bước 4)
- Hoặc dùng GitHub Desktop: https://desktop.github.com

### **Lỗi 3: Updates were rejected**
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 📱 TRIỂN KHAI LÊN STREAMLIT CLOUD

Sau khi push lên GitHub, bạn có thể triển khai miễn phí:

1. Truy cập: https://share.streamlit.io
2. Đăng nhập bằng GitHub
3. Click **"New app"**
4. Chọn:
   - Repository: `QuanLyPhongLabGSH`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **"Deploy"**

⏱️ Đợi 2-5 phút → App sẽ chạy online!

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, hãy:
1. Kiểm tra file `HUONG_DAN_GIT.md`
2. Kiểm tra file `DEPLOY_STREAMLIT_CLOUD.md`
3. Hoặc hỏi tôi!

---

**🎉 Chúc bạn thành công!**

