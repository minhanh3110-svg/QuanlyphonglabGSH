# 📚 HƯỚNG DẪN ĐẨY CODE LÊN GITHUB

Hướng dẫn chi tiết từng bước để đẩy ứng dụng Quản lý Lab Nuôi Cấy lên GitHub và deploy lên Streamlit Cloud.

---

## 📋 Mục lục
1. [Chuẩn bị](#chuẩn-bị)
2. [Cài đặt Git](#cài-đặt-git)
3. [Tạo repository trên GitHub](#tạo-repository-trên-github)
4. [Đẩy code lên GitHub](#đẩy-code-lên-github)
5. [Deploy lên Streamlit Cloud](#deploy-lên-streamlit-cloud)
6. [Cập nhật code sau này](#cập-nhật-code-sau-này)
7. [Xử lý lỗi thường gặp](#xử-lý-lỗi-thường-gặp)

---

## 🎯 Chuẩn bị

### 1. Tạo tài khoản GitHub (nếu chưa có)

1. Truy cập: https://github.com
2. Click **"Sign up"**
3. Điền thông tin:
   - Email
   - Mật khẩu
   - Tên username (ví dụ: `labcaymo`)
4. Xác nhận email

### 2. Kiểm tra cấu trúc thư mục

Đảm bảo thư mục `QUANLYLAB` có đầy đủ các file:

```
D:\QUANLYLAB\
├── app.py                          ✅ Bắt buộc
├── requirements.txt                ✅ Bắt buộc
├── .gitignore                      ✅ Bắt buộc
├── README.md                       ✅ Khuyến nghị
├── README_GITHUB.md                ✅ Khuyến nghị
├── HUONG_DAN_LOGO.md              ✅ Khuyến nghị
├── HUONG_DAN_QR_TEM_NHAN.md       ✅ Khuyến nghị
├── HUONG_DAN_GIT.md               ✅ Khuyến nghị
├── data.db                         ⚠️ Optional (xóa nếu không muốn push)
├── logo.png                        ⚠️ Optional (nếu có logo)
├── KHOI_DONG.bat                   ⚠️ Optional
└── chay_ung_dung.bat               ⚠️ Optional
```

---

## 💻 Cài đặt Git

### Windows

#### Cách 1: Tải từ website chính thức
1. Truy cập: https://git-scm.com/download/win
2. Tải bản **64-bit Git for Windows Setup**
3. Chạy file cài đặt
4. Chọn tất cả tùy chọn mặc định
5. Click **"Next"** → **"Install"** → **"Finish"**

#### Cách 2: Dùng Chocolatey (nếu đã cài)
```powershell
choco install git -y
```

#### Cách 3: Dùng Winget (Windows 10/11)
```powershell
winget install --id Git.Git -e --source winget
```

### Kiểm tra cài đặt
Mở **PowerShell** hoặc **Command Prompt**, gõ:
```bash
git --version
```

Kết quả mong đợi:
```
git version 2.43.0.windows.1
```

---

## 🔧 Cấu hình Git lần đầu

Mở **PowerShell** hoặc **Command Prompt**, chạy:

```bash
# Cấu hình tên (hiển thị trên commit)
git config --global user.name "Tên của bạn"

# Cấu hình email (dùng email GitHub)
git config --global user.email "your.email@example.com"

# Kiểm tra cấu hình
git config --list
```

**Ví dụ:**
```bash
git config --global user.name "Nguyen Van An"
git config --global user.email "nguyenvanan@gmail.com"
```

---

## 🌐 Tạo repository trên GitHub

### Bước 1: Đăng nhập vào GitHub
Truy cập: https://github.com và đăng nhập

### Bước 2: Tạo repository mới
1. Click dấu **"+"** ở góc phải trên → **"New repository"**
2. Điền thông tin:
   - **Repository name:** `QUANLYLAB` (hoặc tên khác)
   - **Description:** `Ứng dụng Quản lý Lab Nuôi Cấy Mô`
   - **Public** hoặc **Private:** Chọn **Public** (để deploy Streamlit Cloud miễn phí)
   - ⚠️ **KHÔNG** check các ô:
     - Add a README file
     - Add .gitignore
     - Choose a license
3. Click **"Create repository"**

### Bước 3: Lưu lại URL repository
Sau khi tạo, bạn sẽ thấy URL dạng:
```
https://github.com/YOUR_USERNAME/QUANLYLAB.git
```

**Lưu lại URL này!**

---

## 🚀 Đẩy code lên GitHub

### Bước 1: Mở PowerShell tại thư mục dự án

**Cách 1:** Dùng File Explorer
1. Mở thư mục `D:\QUANLYLAB`
2. Nhấn `Shift + Right Click` vào vùng trống
3. Chọn **"Open PowerShell window here"** hoặc **"Open in Terminal"**

**Cách 2:** Dùng Command
```powershell
cd D:\QUANLYLAB
```

### Bước 2: Khởi tạo Git repository local

```bash
git init
```

Kết quả:
```
Initialized empty Git repository in D:/QUANLYLAB/.git/
```

### Bước 3: Thêm tất cả file vào staging area

```bash
git add .
```

**Giải thích:**
- `.` = thêm tất cả file
- File trong `.gitignore` sẽ tự động bị bỏ qua

### Bước 4: Commit (lưu snapshot)

```bash
git commit -m "Initial commit - Ứng dụng Quản lý Lab Nuôi Cấy"
```

Kết quả:
```
[main (root-commit) abc1234] Initial commit - Ứng dụng Quản lý Lab Nuôi Cấy
 15 files changed, 2500 insertions(+)
 create mode 100644 app.py
 create mode 100644 requirements.txt
 ...
```

### Bước 5: Đổi tên branch thành `main` (nếu cần)

```bash
git branch -M main
```

**Lý do:** GitHub mặc định dùng `main`, Git cũ dùng `master`

### Bước 6: Kết nối với GitHub repository

```bash
git remote add origin https://github.com/YOUR_USERNAME/QUANLYLAB.git
```

**Thay `YOUR_USERNAME` bằng username GitHub của bạn!**

**Ví dụ:**
```bash
git remote add origin https://github.com/labcaymo/QUANLYLAB.git
```

### Bước 7: Đẩy code lên GitHub

```bash
git push -u origin main
```

**Lần đầu sẽ yêu cầu đăng nhập:**
- **Username:** Tên đăng nhập GitHub
- **Password:** 
  - ⚠️ **KHÔNG** dùng mật khẩu thường
  - Phải dùng **Personal Access Token** (PAT)

#### Tạo Personal Access Token (PAT)

1. Vào GitHub → Click avatar → **Settings**
2. Cuối menu bên trái → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**
4. Điền:
   - **Note:** `QUANLYLAB App`
   - **Expiration:** `No expiration` hoặc `90 days`
   - **Select scopes:** Check ô **`repo`** (tất cả)
5. Click **"Generate token"**
6. **Copy token ngay** (chỉ hiện 1 lần!)
   ```
   ghp_ABcd1234EfGh5678IjKl9012MnOp3456Qr
   ```
7. Dùng token này làm **password** khi push

### Bước 8: Kiểm tra kết quả

Mở trình duyệt, truy cập:
```
https://github.com/YOUR_USERNAME/QUANLYLAB
```

Bạn sẽ thấy tất cả file đã được upload! 🎉

---

## ☁️ Deploy lên Streamlit Cloud

### Bước 1: Tạo tài khoản Streamlit Cloud

1. Truy cập: https://share.streamlit.io
2. Click **"Sign in"** → **"Continue with GitHub"**
3. Cho phép Streamlit truy cập GitHub

### Bước 2: Deploy app

1. Click **"New app"**
2. Chọn:
   - **Repository:** `YOUR_USERNAME/QUANLYLAB`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. **Advanced settings** (optional):
   - **Python version:** `3.9` hoặc `3.10`
4. Click **"Deploy!"**

### Bước 3: Đợi deploy xong

- Quá trình deploy mất **2-5 phút**
- Bạn sẽ thấy logs cài đặt thư viện
- Khi xong, app sẽ tự động chạy

### Bước 4: Lấy URL ứng dụng

URL dạng:
```
https://YOUR_USERNAME-quanlylab-app-xxxxx.streamlit.app
```

**Chia sẻ URL này để người khác truy cập!**

### Bước 5: Cập nhật URL trong code

1. Mở file `app.py`
2. Tìm dòng:
```python
base_url = "http://localhost:8501"
```
3. Thay bằng:
```python
base_url = "https://YOUR_USERNAME-quanlylab-app-xxxxx.streamlit.app"
```
4. Lưu file
5. Đẩy lại lên GitHub (xem bước tiếp theo)

---

## 🔄 Cập nhật code sau này

Khi bạn sửa code, muốn cập nhật lên GitHub:

### Bước 1: Kiểm tra thay đổi

```bash
git status
```

### Bước 2: Thêm file đã thay đổi

```bash
# Thêm tất cả file
git add .

# Hoặc thêm từng file cụ thể
git add app.py
git add requirements.txt
```

### Bước 3: Commit với message mô tả

```bash
git commit -m "Cập nhật tính năng XYZ"
```

**Ví dụ message tốt:**
```bash
git commit -m "Thêm tính năng xuất báo cáo PDF"
git commit -m "Sửa lỗi hiển thị logo trên tem nhỏ"
git commit -m "Cập nhật URL cho Streamlit Cloud"
```

### Bước 4: Đẩy lên GitHub

```bash
git push
```

### Bước 5: Streamlit Cloud tự động deploy lại

- Streamlit Cloud tự động phát hiện thay đổi
- Tự động rebuild và deploy (mất ~2 phút)
- Không cần làm gì thêm!

---

## 📝 Các lệnh Git thường dùng

### Kiểm tra trạng thái
```bash
git status
```

### Xem lịch sử commit
```bash
git log
git log --oneline  # Dạng ngắn gọn
```

### Xem thay đổi chưa commit
```bash
git diff
```

### Hoàn tác thay đổi chưa commit
```bash
git checkout -- app.py  # Hoàn tác 1 file
git checkout -- .       # Hoàn tác tất cả
```

### Xóa file khỏi Git (nhưng giữ trên máy)
```bash
git rm --cached data.db
git commit -m "Xóa database khỏi Git"
git push
```

### Tạo branch mới để thử nghiệm
```bash
git checkout -b feature/new-feature
# Làm việc trên branch mới
git add .
git commit -m "Thử nghiệm tính năng mới"
git push -u origin feature/new-feature
```

### Chuyển về branch main
```bash
git checkout main
```

### Merge branch vào main
```bash
git checkout main
git merge feature/new-feature
git push
```

---

## 🛠️ Xử lý lỗi thường gặp

### ❌ Lỗi: `fatal: not a git repository`

**Nguyên nhân:** Chưa chạy `git init`

**Giải pháp:**
```bash
cd D:\QUANLYLAB
git init
```

---

### ❌ Lỗi: `remote origin already exists`

**Nguyên nhân:** Đã kết nối với remote rồi

**Giải pháp 1:** Xóa và thêm lại
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/QUANLYLAB.git
```

**Giải pháp 2:** Kiểm tra remote hiện tại
```bash
git remote -v
```

---

### ❌ Lỗi: `failed to push some refs`

**Nguyên nhân:** GitHub có code mới hơn local

**Giải pháp:**
```bash
# Pull code mới về trước
git pull origin main --rebase

# Rồi push lại
git push
```

---

### ❌ Lỗi: `Support for password authentication was removed`

**Nguyên nhân:** GitHub không chấp nhận mật khẩu thường nữa

**Giải pháp:** Dùng Personal Access Token (xem hướng dẫn ở trên)

---

### ❌ Lỗi: `large files detected`

**Nguyên nhân:** File quá lớn (>100MB)

**Giải pháp:**
```bash
# Thêm file đó vào .gitignore
echo "data.db" >> .gitignore

# Xóa khỏi staging area
git rm --cached data.db

# Commit lại
git commit -m "Loại bỏ file lớn"
git push
```

---

### ❌ Không nhớ đã commit file nào

**Giải pháp:**
```bash
# Xem file trong commit gần nhất
git show --name-only

# Xem chi tiết thay đổi
git show
```

---

### ❌ Muốn hoàn tác commit gần nhất

**Giải pháp:**
```bash
# Hoàn tác nhưng giữ lại thay đổi
git reset --soft HEAD~1

# Hoàn tác và XÓA thay đổi (NGUY HIỂM!)
git reset --hard HEAD~1
```

---

## 🎯 Workflow chuẩn

### Workflow hàng ngày

```bash
# 1. Mở PowerShell tại thư mục dự án
cd D:\QUANLYLAB

# 2. Pull code mới nhất (nếu làm việc nhóm)
git pull

# 3. Sửa code...
# (code editor)

# 4. Kiểm tra thay đổi
git status

# 5. Thêm file
git add .

# 6. Commit
git commit -m "Mô tả ngắn gọn thay đổi"

# 7. Push lên GitHub
git push

# 8. Kiểm tra Streamlit Cloud tự động deploy
# (Mở URL app, đợi ~2 phút)
```

---

## 💡 Tips hữu ích

### 1. Alias cho lệnh dài
```bash
# Tạo shortcut
git config --global alias.st status
git config --global alias.co commit
git config --global alias.br branch

# Sử dụng
git st    # = git status
git co -m "message"  # = git commit -m "message"
```

### 2. Tránh push file nhạy cảm
Thêm vào `.gitignore`:
```
# Secrets
secrets.toml
*.env
*.key
*.pem
database_backup.db
```

### 3. Commit message chuẩn
```bash
# ✅ TỐT
git commit -m "Thêm tính năng xuất báo cáo PDF"
git commit -m "Sửa lỗi hiển thị QR code"
git commit -m "Cập nhật requirements.txt"

# ❌ KHÔNG TỐT
git commit -m "update"
git commit -m "fix bug"
git commit -m "asdfasdf"
```

### 4. Xem file đã thay đổi giữa 2 commit
```bash
git diff HEAD~1 HEAD --name-only
```

### 5. Tạo tag cho version
```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Release đầu tiên"
git push origin v1.0.0
```

---

## 📚 Tài liệu tham khảo

- **Git chính thức:** https://git-scm.com/doc
- **GitHub Docs:** https://docs.github.com
- **Streamlit Docs:** https://docs.streamlit.io
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf

---

## 🎓 Học thêm về Git

### Video tutorials (tiếng Việt)
- YouTube: "Git cơ bản cho người mới"
- YouTube: "GitHub từ con số 0"

### Khóa học online miễn phí
- https://learngitbranching.js.org (Interactive)
- https://www.codecademy.com/learn/learn-git

---

## 🚨 Lưu ý quan trọng

1. ⚠️ **KHÔNG** push file chứa mật khẩu, API key
2. ⚠️ **KHÔNG** push file database có dữ liệu thật (nếu nhạy cảm)
3. ✅ **LUÔN** kiểm tra `git status` trước khi commit
4. ✅ **LUÔN** viết commit message rõ ràng
5. ✅ **LUÔN** pull trước khi push (nếu làm nhóm)

---

## 🎉 Kết luận

Sau khi hoàn thành hướng dẫn này, bạn đã:

✅ Cài đặt và cấu hình Git  
✅ Tạo repository trên GitHub  
✅ Đẩy code lên GitHub  
✅ Deploy ứng dụng lên Streamlit Cloud  
✅ Biết cách cập nhật code sau này  

**🎊 Chúc mừng! Ứng dụng của bạn đã online!**

---

**📞 Cần hỗ trợ?** Tạo issue trên GitHub hoặc liên hệ qua email.

