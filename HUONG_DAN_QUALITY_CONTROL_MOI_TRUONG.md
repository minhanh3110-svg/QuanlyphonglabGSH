# 🎯 HƯỚNG DẪN TRIỂN KHAI QUALITY CONTROL MÔI TRƯỜNG

## ✅ ĐÃ HOÀN THÀNH (Commit: 1cfb97d)

### 1. Functions mới:
- ✅ `tinh_tuoi_moi_truong(ngay_do)` - Tính tuổi và mức cảnh báo
- ✅ `get_danh_sach_lo_moi_truong_co_canh_bao(ma_so)` - Lấy danh sách lô với cảnh báo
- ✅ `khau_tru_moi_truong_theo_lo(ma_lo, so_luong)` - Khấu trừ theo lô chọn

### 2. Database:
- ✅ Thêm cột `ma_lo_moi_truong_con` - Lưu mã lô đã sử dụng
- ✅ Thêm cột `canh_bao_moi_truong_qua_han` - Flag cảnh báo (0/1)
- ✅ Thêm cột `tuoi_moi_truong` - Số ngày tuổi môi trường
- ✅ Migration logic đã sẵn sàng

### 3. Mức cảnh báo:
```python
≤ 15 ngày: ✅ OK (Xanh #28a745)
16-20 ngày: ⚠️ CẦN ƯU TIÊN (Vàng #ffc107)
21-30 ngày: 🟠 SẮP QUÁ HẠN (Cam #ff8c00)
> 30 ngày: 🔴 QUÁ HẠN (Đỏ #dc3545)
```

---

## 🚧 CẦN TRIỂN KHAI TIẾP

### BƯỚC 1: Sửa Form Nhập Liệu

**File:** `app.py` - Tìm phần "Thông tin môi trường"

**Code cần thêm:**

```python
st.markdown("#### 🧪 Thông tin môi trường")

# ... Môi trường mẹ giữ nguyên ...

# ========== MÔI TRƯỜNG CON - CHỌN LÔ CỤ THỂ ==========
st.markdown("**Môi trường con (Chọn lô cụ thể):**")

# Lấy danh sách lô với cảnh báo
danh_sach_lo_con = get_danh_sach_lo_moi_truong_co_canh_bao(ma_so_moi_truong_con)

if len(danh_sach_lo_con) == 0:
    st.error("❌ Không có lô môi trường nào còn tồn kho!")
    st.stop()

# Tạo dropdown với cảnh báo màu sắc
lo_labels = [lo['label'] for lo in danh_sach_lo_con]
lo_chon_index = st.selectbox(
    "Chọn lô môi trường con *",
    options=range(len(danh_sach_lo_con)),
    format_func=lambda x: lo_labels[x],
    help="Lô đầu tiên (có 🌟) là gợi ý dùng trước (FIFO)"
)

lo_chon = danh_sach_lo_con[lo_chon_index]

# Hiển thị thông tin chi tiết lô đã chọn
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.metric("Mã lô", lo_chon['ma_lo'])
with col_info2:
    st.metric("Còn lại", f"{lo_chon['so_luong']} túi")
with col_info3:
    st.metric("Tuổi", f"{lo_chon['so_ngay']} ngày", 
              delta=lo_chon['muc_canh_bao'], 
              delta_color="inverse" if lo_chon['so_ngay'] > 20 else "normal")

# CẢNH BÁO NẾU QUÁ HẠN
if lo_chon['so_ngay'] > 30:
    st.error(f"""
    🔴 **CẢNH BÁO: MÔI TRƯỜNG QUÁ HẠN!**
    
    Lô {lo_chon['ma_lo']} đã {lo_chon['so_ngay']} ngày (> 30 ngày).
    
    **Rủi ro:**
    - Tỷ lệ nhiễm cao
    - Chất lượng môi trường giảm
    - Ảnh hưởng đến năng suất
    
    **Khuyến nghị:** Hủy bỏ hoặc kiểm tra kỹ trước khi sử dụng.
    """)
    
    # Checkbox xác nhận
    xac_nhan_qua_han = st.checkbox(
        "✅ Tôi hiểu rủi ro và vẫn muốn sử dụng lô môi trường này",
        key="xac_nhan_qua_han"
    )
    
    if not xac_nhan_qua_han:
        st.warning("⚠️ Vui lòng xác nhận để tiếp tục hoặc chọn lô khác")
        st.stop()

elif lo_chon['so_ngay'] > 20:
    st.warning(f"🟠 Lô này đã {lo_chon['so_ngay']} ngày. Nên kiểm tra trước khi sử dụng.")
elif lo_chon['so_ngay'] > 15:
    st.info(f"⚠️ Lô này đã {lo_chon['so_ngay']} ngày. Ưu tiên sử dụng sớm.")
```

---

### BƯỚC 2: Sửa Logic Lưu Dữ Liệu

**Tìm phần:** `if submitted:` trong form nhập liệu

**Thay đổi:**

```python
# TRƯỚC (Khấu trừ tự động FIFO):
success, message, danh_sach_lo = khau_tru_moi_truong_tu_kho(
    ma_so_moi_truong_con,
    so_tui_con
)

# SAU (Khấu trừ theo lô chọn):
success, message, thong_tin_lo = khau_tru_moi_truong_theo_lo(
    lo_chon['ma_lo'],
    so_tui_con
)

if not success:
    conn.rollback()
    conn.close()
    st.error(f"❌ {message}")
    st.stop()

# Lưu thông tin cảnh báo vào database
canh_bao_qua_han = 1 if thong_tin_lo['qua_han'] else 0
tuoi_moi_truong = thong_tin_lo['so_ngay']

c.execute('''
    INSERT INTO nhat_ky_cay (
        ..., ma_lo_moi_truong_con, canh_bao_moi_truong_qua_han, tuoi_moi_truong, ...
    ) VALUES (?, ?, ?, ?, ...)
''', (..., lo_chon['ma_lo'], canh_bao_qua_han, tuoi_moi_truong, ...))
```

---

### BƯỚC 3: Cập Nhật Trang Tồn Kho

**File:** `app.py` - Tab "Tồn kho" trong "Quản lý Kho Môi trường"

**Thêm cột tuổi và cảnh báo:**

```python
df_chi_tiet = pd.read_sql_query('''
    SELECT 
        ma_lo AS "Mã lô",
        ten_moi_truong AS "Loại",
        ngay_do AS "Ngày đổ",
        so_luong_ban_dau AS "Số lượng đổ",
        (so_luong_ban_dau - so_luong_con_lai) AS "Đã xuất",
        so_luong_con_lai AS "Còn lại",
        vi_tri_kho AS "Vị trí"
    FROM kho_moi_truong
    WHERE so_luong_ban_dau > 0
    ORDER BY ten_moi_truong, ngay_do ASC
''', conn)

# Tính tuổi và cảnh báo
df_chi_tiet['Tuổi (ngày)'] = df_chi_tiet['Ngày đổ'].apply(
    lambda x: (datetime.now() - datetime.strptime(x, "%Y-%m-%d")).days
)

df_chi_tiet['Cảnh báo'] = df_chi_tiet['Tuổi (ngày)'].apply(
    lambda x: "🔴 QUÁ HẠN" if x > 30 
         else "🟠 SẮP HẾT" if x > 20
         else "⚠️ ƯU TIÊN" if x > 15
         else "✅ OK"
)

# Highlight theo tuổi
def highlight_tuoi(row):
    tuoi = row['Tuổi (ngày)']
    if tuoi > 30:
        return ['background-color: #ffcccc'] * len(row)  # Đỏ nhạt
    elif tuoi > 20:
        return ['background-color: #ffe5cc'] * len(row)  # Cam nhạt
    elif tuoi > 15:
        return ['background-color: #ffffcc'] * len(row)  # Vàng nhạt
    return [''] * len(row)

styled_df = df_chi_tiet.style.apply(highlight_tuoi, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)
```

---

### BƯỚC 4: Thêm Dashboard Cảnh Báo

**Vị trí:** Trang chủ hoặc đầu trang "Quản lý Kho Môi trường"

```python
st.markdown("### ⚠️ Cảnh báo Môi trường Tồn kho Lâu ngày")

conn = sqlite3.connect('data.db')

# Query môi trường cần chú ý
df_canh_bao = pd.read_sql_query('''
    SELECT 
        ma_lo,
        ten_moi_truong,
        ngay_do,
        so_luong_con_lai,
        vi_tri_kho,
        CAST((julianday('now') - julianday(ngay_do)) AS INTEGER) AS tuoi_ngay
    FROM kho_moi_truong
    WHERE so_luong_con_lai > 0
      AND tuoi_ngay > 15
    ORDER BY tuoi_ngay DESC
''', conn)

conn.close()

if len(df_canh_bao) > 0:
    # Phân loại
    df_qua_han = df_canh_bao[df_canh_bao['tuoi_ngay'] > 30]
    df_sap_han = df_canh_bao[(df_canh_bao['tuoi_ngay'] > 20) & (df_canh_bao['tuoi_ngay'] <= 30)]
    df_uu_tien = df_canh_bao[(df_canh_bao['tuoi_ngay'] > 15) & (df_canh_bao['tuoi_ngay'] <= 20)]
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 Quá hạn (>30 ngày)", len(df_qua_han))
    with col2:
        st.metric("🟠 Sắp hết (20-30 ngày)", len(df_sap_han))
    with col3:
        st.metric("⚠️ Ưu tiên (15-20 ngày)", len(df_uu_tien))
    
    # Bảng chi tiết
    if len(df_qua_han) > 0:
        with st.expander("🔴 Danh sách Quá hạn - YÊU CẦU XỬ LÝ NGAY"):
            st.dataframe(df_qua_han, use_container_width=True, hide_index=True)
            st.error("⚠️ Khuyến nghị: Hủy bỏ hoặc kiểm tra kỹ trước khi sử dụng")
    
    if len(df_sap_han) > 0:
        with st.expander("🟠 Danh sách Sắp hết hạn"):
            st.dataframe(df_sap_han, use_container_width=True, hide_index=True)
    
    if len(df_uu_tien) > 0:
        with st.expander("⚠️ Danh sách Cần ưu tiên"):
            st.dataframe(df_uu_tien, use_container_width=True, hide_index=True)
else:
    st.success("✅ Tất cả môi trường đều trong thời hạn sử dụng tốt!")
```

---

### BƯỚC 5: Báo Cáo Admin

**Thêm vào trang "Báo cáo Năng suất" (Admin only):**

```python
if is_admin:
    st.markdown("---")
    st.markdown("### 📊 Báo cáo Sử dụng Môi trường Quá hạn")
    
    conn = sqlite3.connect('data.db')
    
    df_qua_han = pd.read_sql_query('''
        SELECT 
            nhan_vien AS "Nhân viên",
            COUNT(*) AS "Số lần dùng MT quá hạn",
            AVG(tuoi_moi_truong) AS "Tuổi TB (ngày)",
            MAX(tuoi_moi_truong) AS "Tuổi max (ngày)"
        FROM nhat_ky_cay
        WHERE canh_bao_moi_truong_qua_han = 1
        GROUP BY nhan_vien
        ORDER BY "Số lần dùng MT quá hạn" DESC
    ''', conn)
    
    conn.close()
    
    if len(df_qua_han) > 0:
        st.warning(f"⚠️ Có {len(df_qua_han)} nhân viên đã sử dụng môi trường quá hạn")
        st.dataframe(df_qua_han, use_container_width=True, hide_index=True)
        
        # Biểu đồ
        fig = px.bar(
            df_qua_han,
            x='Nhân viên',
            y='Số lần dùng MT quá hạn',
            title='Số lần sử dụng Môi trường Quá hạn theo Nhân viên',
            color='Số lần dùng MT quá hạn',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Khuyến nghị:** Đào tạo lại nhân viên về quy trình kiểm tra môi trường")
    else:
        st.success("✅ Không có nhân viên nào sử dụng môi trường quá hạn!")
```

---

## 📋 CHECKLIST TRIỂN KHAI

- [x] Thêm functions tính tuổi và cảnh báo
- [x] Thêm function khấu trừ theo lô chọn
- [x] Thêm cột database mới
- [x] Migration logic
- [ ] Sửa form nhập liệu - dropdown chọn lô
- [ ] Thêm cảnh báo màu sắc trong dropdown
- [ ] Thêm confirmation cho lô > 30 ngày
- [ ] Lưu thông tin cảnh báo vào database
- [ ] Cập nhật trang tồn kho với cột tuổi
- [ ] Thêm dashboard cảnh báo
- [ ] Thêm báo cáo admin

---

## 🎯 KẾT QUẢ MONG ĐỢI

### 1. Form Nhập Liệu:
```
Môi trường con:
┌────────────────────────────────────────────────────────┐
│ 🌟 ✅ MT-20260101-001 | 2026-01-01 (5 ngày) | Còn: 80 │ ← Gợi ý
│ ⚠️ MT-20260102-001 | 2026-01-02 (18 ngày) | Còn: 50   │
│ 🟠 MT-20251215-001 | 2025-12-15 (25 ngày) | Còn: 30   │
│ 🔴 MT-20251201-001 | 2025-12-01 (35 ngày) | Còn: 20   │ ← Cảnh báo
└────────────────────────────────────────────────────────┘

[Chọn lô đầu tiên]

Thông tin lô:
Mã lô: MT-20260101-001
Còn lại: 80 túi
Tuổi: 5 ngày (✅ OK)
```

### 2. Cảnh báo Quá hạn:
```
🔴 CẢNH BÁO: MÔI TRƯỜNG QUÁ HẠN!

Lô MT-20251201-001 đã 35 ngày (> 30 ngày).

Rủi ro:
- Tỷ lệ nhiễm cao
- Chất lượng môi trường giảm
- Ảnh hưởng đến năng suất

Khuyến nghị: Hủy bỏ hoặc kiểm tra kỹ.

☐ Tôi hiểu rủi ro và vẫn muốn sử dụng
```

### 3. Dashboard:
```
⚠️ Cảnh báo Môi trường Tồn kho Lâu ngày

┌──────────────┬──────────────┬──────────────┐
│ 🔴 Quá hạn   │ 🟠 Sắp hết   │ ⚠️ Ưu tiên   │
│   3 lô       │   5 lô       │   8 lô       │
└──────────────┴──────────────┴──────────────┘

▼ 🔴 Danh sách Quá hạn - YÊU CẦU XỬ LÝ NGAY
  MT-20251201-001 | MS821 | 35 ngày | 20 túi
  MT-20251205-002 | MS803 | 32 ngày | 15 túi
  ...
```

---

## 🚀 TRIỂN KHAI

```bash
# Sau khi code xong
cd D:\QUANLYLAB
git add app.py
git commit -m "Feature: Complete environment quality control system"
git push origin master

# Reboot Streamlit Cloud
```

---

## 📞 HỖ TRỢ

Nếu cần hỗ trợ triển khai:
1. Đọc kỹ từng bước
2. Test từng phần nhỏ
3. Kiểm tra syntax sau mỗi thay đổi
4. Commit thường xuyên

**Green Straw Hat - Happiness Together 🌱**

