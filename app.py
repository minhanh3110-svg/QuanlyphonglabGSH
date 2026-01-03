import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import io
import plotly.express as px
import plotly.graph_objects as go
from calendar import monthrange
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import base64
import os

# ========== CẤU HÌNH LOGO ==========
# Đặt tên file logo vào thư mục gốc của dự án
# Hỗ trợ các định dạng: PNG, JPG, JPEG
LOGO_PATH = "logo.png"  # Thay đổi tên file này nếu cần

# Cấu hình trang - TỐI ƯU CHO MOBILE
st.set_page_config(
    page_title="Quản lý Phòng Nuôi Cấy Mô",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"  # Thu gọn sidebar mặc định để dễ dùng trên mobile
)

# CSS tùy chỉnh - TỐI ƯU CHO MOBILE
st.markdown("""
    <style>
    /* ========== HEADER ========== */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2d5016;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #a8e063 0%, #56ab2f 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* ========== BUTTONS - TỐI ƯU MOBILE ========== */
    .stButton>button {
        background-color: #56ab2f;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        width: 100%;
        min-height: 48px; /* Kích thước tối thiểu cho mobile */
        touch-action: manipulation; /* Tắt double-tap zoom */
    }
    .stButton>button:hover {
        background-color: #2d5016;
    }
    
    /* ========== FORM INPUTS - TỐI ƯU MOBILE ========== */
    /* Input fields lớn hơn, dễ chạm */
    .stTextInput input, 
    .stNumberInput input,
    .stSelectbox select,
    .stTextArea textarea {
        font-size: 16px !important; /* Tránh auto-zoom trên iOS */
        padding: 0.75rem !important;
        min-height: 48px !important;
        border-radius: 8px !important;
    }
    
    /* Date/Time input */
    .stDateInput input,
    .stTimeInput input {
        font-size: 16px !important;
        padding: 0.75rem !important;
        min-height: 48px !important;
    }
    
    /* Selectbox dropdown */
    div[data-baseweb="select"] > div {
        font-size: 16px !important;
        min-height: 48px !important;
        padding: 0.5rem !important;
    }
    
    /* Number input buttons */
    button[data-baseweb="button-arrow"] {
        width: 40px !important;
        height: 40px !important;
    }
    
    /* ========== CẢNH BÁO ĐỎ RỰC ========== */
    div[data-testid="stAlert"][data-baseweb="notification"]:has(> div > div:first-child:contains("CẢNH BÁO ĐỎ RỰC")) {
        background-color: #dc3545 !important;
        border: 3px solid #a71d2a !important;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    /* Cảnh báo chú ý vàng */
    div[data-testid="stAlert"][data-baseweb="notification"]:has(> div > div:first-child:contains("Chú ý")) {
        background-color: #ffc107 !important;
        border: 2px solid #ff9800 !important;
    }
    
    /* ========== RESPONSIVE TABLE ========== */
    /* Bảng cuộn ngang trên mobile */
    .stDataFrame {
        overflow-x: auto !important;
    }
    
    /* ========== MOBILE RESPONSIVE ========== */
    @media (max-width: 768px) {
        /* Header nhỏ hơn trên mobile */
        .main-header {
            font-size: 1.5rem;
            padding: 0.75rem 0;
            margin-bottom: 1rem;
        }
        
        /* Sidebar thu gọn mặc định */
        section[data-testid="stSidebar"] {
            width: 0px;
        }
        
        /* Button full width, dễ bấm */
        .stButton>button {
            padding: 1rem;
            font-size: 1.1rem;
            min-height: 56px;
        }
        
        /* Form submit button nổi bật */
        .stFormSubmitButton>button {
            background-color: #56ab2f !important;
            font-size: 1.2rem !important;
            padding: 1.2rem !important;
            min-height: 60px !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            font-weight: bold !important;
        }
        
        /* Input fields lớn hơn trên mobile */
        .stTextInput input, 
        .stNumberInput input,
        .stSelectbox select,
        .stTextArea textarea,
        .stDateInput input,
        .stTimeInput input {
            font-size: 18px !important;
            padding: 1rem !important;
            min-height: 56px !important;
        }
        
        /* Dropdown lớn hơn */
        div[data-baseweb="select"] > div {
            font-size: 18px !important;
            min-height: 56px !important;
        }
        
        /* Label lớn hơn, dễ đọc */
        label {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Expander dễ bấm hơn */
        .streamlit-expanderHeader {
            font-size: 1.1rem !important;
            padding: 1rem !important;
            min-height: 56px !important;
        }
        
        /* Tab dễ chọn hơn */
        button[data-baseweb="tab"] {
            font-size: 1rem !important;
            padding: 1rem !important;
            min-height: 52px !important;
        }
        
        /* Metric cards stack vertically */
        div[data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        /* Chart full width */
        .js-plotly-plot {
            width: 100% !important;
        }
        
        /* Download button lớn hơn */
        .stDownloadButton>button {
            padding: 1rem !important;
            font-size: 1.1rem !important;
            min-height: 56px !important;
        }
        
        /* Spacing tốt hơn giữa các elements */
        .element-container {
            margin-bottom: 1rem !important;
        }
        
        /* Success/Error message dễ đọc hơn */
        .stAlert {
            font-size: 1rem !important;
            padding: 1rem !important;
        }
    }
    
    /* ========== TABLET (768px - 1024px) ========== */
    @media (min-width: 768px) and (max-width: 1024px) {
        .main-header {
            font-size: 2rem;
        }
        
        .stButton>button {
            min-height: 52px;
            font-size: 1.05rem;
        }
        
        .stTextInput input,
        .stNumberInput input {
            font-size: 17px !important;
            min-height: 52px !important;
        }
    }
    
    /* ========== PREVENT ZOOM ON IOS ========== */
    @supports (-webkit-touch-callout: none) {
        input, select, textarea {
            font-size: 16px !important; /* iOS không zoom nếu >= 16px */
        }
    }
    
    /* ========== TOUCH TARGETS ========== */
    /* Đảm bảo mọi element có thể click có kích thước tối thiểu 44x44px (Apple HIG) */
    button, a, input[type="checkbox"], input[type="radio"] {
        min-width: 44px;
        min-height: 44px;
        touch-action: manipulation;
    }
    </style>
""", unsafe_allow_html=True)

# ========== KHỞI TẠO DATABASE ==========
def check_table_structure(conn, table_name):
    """Kiểm tra cấu trúc bảng có đúng không"""
    try:
        c = conn.cursor()
        c.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in c.fetchall()]
        return columns
    except:
        return []

def migrate_database():
    """Migrate database từ cấu trúc cũ sang mới"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Kiểm tra và migrate bảng nhat_ky_cay
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nhat_ky_cay'")
    table_exists = c.fetchone() is not None
    
    if table_exists:
        columns = check_table_structure(conn, 'nhat_ky_cay')
        
        # Thêm cột ma_qr nếu chưa có
        if 'ma_qr' not in columns:
            try:
                c.execute("ALTER TABLE nhat_ky_cay ADD COLUMN ma_qr TEXT UNIQUE")
                conn.commit()
            except:
                pass
        
        # Thêm cột ma_lo_moi_truong_con nếu chưa có
        if 'ma_lo_moi_truong_con' not in columns:
            try:
                c.execute("ALTER TABLE nhat_ky_cay ADD COLUMN ma_lo_moi_truong_con TEXT")
                conn.commit()
            except:
                pass
        
        # Thêm cột canh_bao_moi_truong_qua_han nếu chưa có
        if 'canh_bao_moi_truong_qua_han' not in columns:
            try:
                c.execute("ALTER TABLE nhat_ky_cay ADD COLUMN canh_bao_moi_truong_qua_han INTEGER DEFAULT 0")
                conn.commit()
            except:
                pass
        
        # Thêm cột tuoi_moi_truong nếu chưa có
        if 'tuoi_moi_truong' not in columns:
            try:
                c.execute("ALTER TABLE nhat_ky_cay ADD COLUMN tuoi_moi_truong INTEGER")
                conn.commit()
            except:
                pass
        
        # Thêm cột ma_lo_mo_soi nếu chưa có
        if 'ma_lo_mo_soi' not in columns:
            try:
                c.execute("ALTER TABLE nhat_ky_cay ADD COLUMN ma_lo_mo_soi TEXT")
                conn.commit()
            except:
                pass
        
        # Thêm cột ma_tinh_trang nếu chưa có (mã số 3 chữ số)
        if 'ma_tinh_trang' not in columns:
            try:
                c.execute("ALTER TABLE nhat_ky_cay ADD COLUMN ma_tinh_trang INTEGER DEFAULT 301")
                conn.commit()
            except:
                pass
        
        # Nếu không có cột ngay_cay hoặc ma_so_moi_truong_me, đây là cấu trúc cũ
        if 'ngay_cay' not in columns or 'ma_so_moi_truong_me' not in columns:
            # Backup dữ liệu cũ nếu có
            try:
                c.execute("SELECT COUNT(*) FROM nhat_ky_cay")
                count = c.fetchone()[0]
                if count > 0:
                    c.execute('''
                        CREATE TABLE IF NOT EXISTS nhat_ky_cay_backup_old AS 
                        SELECT * FROM nhat_ky_cay
                    ''')
                    conn.commit()
            except:
                pass
            
            # Xóa bảng cũ và tạo lại với cấu trúc mới
            c.execute("DROP TABLE IF EXISTS nhat_ky_cay")
            conn.commit()
    
    # Kiểm tra và migrate bảng danh_muc_moi_truong
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='danh_muc_moi_truong'")
    mt_table_exists = c.fetchone() is not None
    
    if mt_table_exists:
        columns = check_table_structure(conn, 'danh_muc_moi_truong')
        
        # Nếu không có cột ma_so, đây là cấu trúc cũ
        if 'ma_so' not in columns:
            # Backup dữ liệu cũ
            try:
                c.execute("SELECT COUNT(*) FROM danh_muc_moi_truong")
                count = c.fetchone()[0]
                if count > 0:
                    c.execute('''
                        CREATE TABLE IF NOT EXISTS danh_muc_moi_truong_backup_old AS 
                        SELECT * FROM danh_muc_moi_truong
                    ''')
                    conn.commit()
            except:
                pass
            
            # Xóa bảng cũ và tạo lại với cấu trúc mới
            c.execute("DROP TABLE IF EXISTS danh_muc_moi_truong")
            conn.commit()
    
    # Kiểm tra và tạo bảng phòng sáng nếu chưa có
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quan_ly_phong_sang'")
    ps_table_exists = c.fetchone() is not None
    
    if not ps_table_exists:
        # Tạo bảng phòng sáng mới
        c.execute('''
            CREATE TABLE IF NOT EXISTS quan_ly_phong_sang (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_nhat_ky_cay INTEGER NOT NULL,
                ngay_cay TEXT NOT NULL,
                nhan_vien TEXT NOT NULL,
                ma_nhan_vien TEXT NOT NULL,
                ten_giong TEXT NOT NULL,
                chu_ky TEXT NOT NULL,
                so_gian_ke TEXT NOT NULL,
                trang_thai TEXT NOT NULL DEFAULT 'Đang nuôi',
                so_tui_sach INTEGER DEFAULT 0,
                so_tui_khuan_nhe INTEGER DEFAULT 0,
                so_tui_khuan_nang INTEGER DEFAULT 0,
                so_tui_nam INTEGER DEFAULT 0,
                so_tui_khuan_moi_truong INTEGER DEFAULT 0,
                so_tui_khac INTEGER DEFAULT 0,
                tong_so_tui INTEGER DEFAULT 0,
                tong_so_cay INTEGER DEFAULT 0,
                tuan_xuat_cay INTEGER,
                ngay_xuat_cay TEXT,
                ghi_chu TEXT,
                ngay_tao TEXT NOT NULL,
                ngay_cap_nhat TEXT NOT NULL
            )
        ''')
        conn.commit()
    
    conn.close()

def init_database():
    """Tạo các bảng trong database nếu chưa tồn tại"""
    # Migrate database trước
    migrate_database()
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Bảng tài khoản đăng nhập
    c.execute('''
        CREATE TABLE IF NOT EXISTS tai_khoan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ten_dang_nhap TEXT UNIQUE NOT NULL,
            ma_nhan_vien TEXT UNIQUE NOT NULL,
            ten_nhan_vien TEXT NOT NULL,
            quyen_han TEXT NOT NULL DEFAULT 'nhan_vien',
            ngay_tao TEXT NOT NULL
        )
    ''')
    
    # Bảng nhật ký cấy (cấu trúc mới)
    c.execute('''
        CREATE TABLE IF NOT EXISTS nhat_ky_cay (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ngay_cay TEXT NOT NULL,
            thang INTEGER NOT NULL,
            tuan INTEGER NOT NULL,
            nhan_vien TEXT NOT NULL,
            ma_nhan_vien TEXT NOT NULL,
            ten_giong TEXT NOT NULL,
            chu_ky TEXT NOT NULL,
            tinh_trang TEXT NOT NULL,
            box_cay INTEGER NOT NULL,
            ma_so_moi_truong_me INTEGER NOT NULL,
            ma_so_moi_truong_con INTEGER NOT NULL,
            so_tui_me INTEGER NOT NULL,
            so_cum_tui_me INTEGER NOT NULL,
            so_tui_con INTEGER NOT NULL,
            so_cum_tui_con INTEGER NOT NULL,
            tong_so_cay_con INTEGER NOT NULL,
            gio_bat_dau TEXT NOT NULL,
            gio_ket_thuc TEXT NOT NULL,
            tong_gio_lam REAL NOT NULL,
            nang_suat REAL NOT NULL,
            ghi_chu TEXT,
            ma_qr TEXT UNIQUE,
            ngay_tao TEXT NOT NULL
        )
    ''')
    
    # Bảng danh mục tên giống
    c.execute('''
        CREATE TABLE IF NOT EXISTS danh_muc_ten_giong (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ten_giong TEXT UNIQUE NOT NULL,
            ngay_tao TEXT NOT NULL
        )
    ''')
    
    # Bảng danh mục chu kỳ
    c.execute('''
        CREATE TABLE IF NOT EXISTS danh_muc_chu_ky (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chu_ky TEXT UNIQUE NOT NULL,
            ngay_tao TEXT NOT NULL
        )
    ''')
    
    # Bảng danh mục Mã tình trạng - CHỈ LƯU MÃ SỐ
    c.execute('''
        CREATE TABLE IF NOT EXISTS danh_muc_ma_tinh_trang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_so INTEGER UNIQUE NOT NULL,
            ngay_tao TEXT NOT NULL
        )
    ''')
    
    # Bảng danh mục Giàn/Kệ (Phòng sáng)
    c.execute('''
        CREATE TABLE IF NOT EXISTS danh_muc_gian_ke (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            so_gian_ke TEXT NOT NULL UNIQUE,
            ghi_chu TEXT,
            ngay_tao TEXT
        )
    ''')
    
    # Bảng danh mục Vị trí Kho môi trường
    c.execute('''
        CREATE TABLE IF NOT EXISTS danh_muc_vi_tri_kho (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vi_tri_kho TEXT NOT NULL UNIQUE,
            ghi_chu TEXT,
            ngay_tao TEXT
        )
    ''')
    
    # Bảng Kho Môi trường
    c.execute('''
        CREATE TABLE IF NOT EXISTS kho_moi_truong (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_lo TEXT UNIQUE NOT NULL,
            ma_so_moi_truong INTEGER NOT NULL,
            ten_moi_truong TEXT NOT NULL,
            ngay_do TEXT NOT NULL,
            tuan_do INTEGER NOT NULL,
            nam INTEGER NOT NULL,
            so_luong_ban_dau INTEGER NOT NULL,
            so_luong_con_lai INTEGER NOT NULL,
            vi_tri_kho TEXT NOT NULL,
            nguoi_do TEXT,
            ghi_chu TEXT,
            ngay_tao TEXT NOT NULL,
            FOREIGN KEY (ma_so_moi_truong) REFERENCES danh_muc_moi_truong(ma_so)
        )
    ''')
    
    # Bảng Quản lý Mô Soi (kết quả chu kỳ trước từ phòng sáng)
    c.execute('''
        CREATE TABLE IF NOT EXISTS mo_soi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_lo_mo_soi TEXT UNIQUE NOT NULL,
            ten_giong TEXT NOT NULL,
            chu_ky_truoc TEXT NOT NULL,
            ngay_soi TEXT NOT NULL,
            tuan_soi INTEGER NOT NULL,
            nam INTEGER NOT NULL,
            so_luong_ban_dau INTEGER NOT NULL,
            so_tui_nhiem INTEGER NOT NULL,
            so_tui_sach INTEGER NOT NULL,
            so_cum_moi_tui INTEGER NOT NULL,
            tong_cum_sach INTEGER NOT NULL,
            so_cum_da_cap INTEGER DEFAULT 0,
            so_cum_con_lai INTEGER NOT NULL,
            trang_thai TEXT NOT NULL DEFAULT 'Đang sử dụng',
            nguoi_soi TEXT NOT NULL,
            ma_nhan_vien TEXT NOT NULL,
            ghi_chu TEXT,
            ngay_tao TEXT NOT NULL,
            ngay_cap_nhat TEXT NOT NULL
        )
    ''')
    
    # Bảng danh mục môi trường (có mã số)
    c.execute('''
        CREATE TABLE IF NOT EXISTS danh_muc_moi_truong (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_so INTEGER UNIQUE NOT NULL,
            ten_moi_truong TEXT NOT NULL,
            ngay_tao TEXT NOT NULL
        )
    ''')
    
    # Bảng quản lý phòng sáng
    c.execute('''
        CREATE TABLE IF NOT EXISTS quan_ly_phong_sang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_nhat_ky_cay INTEGER NOT NULL,
            ngay_cay TEXT NOT NULL,
            nhan_vien TEXT NOT NULL,
            ma_nhan_vien TEXT NOT NULL,
            ten_giong TEXT NOT NULL,
            chu_ky TEXT NOT NULL,
            so_gian_ke TEXT NOT NULL,
            trang_thai TEXT NOT NULL DEFAULT 'Đang nuôi',
            so_tui_sach INTEGER DEFAULT 0,
            so_tui_khuan_nhe INTEGER DEFAULT 0,
            so_tui_khuan_nang INTEGER DEFAULT 0,
            so_tui_nam INTEGER DEFAULT 0,
            so_tui_khuan_moi_truong INTEGER DEFAULT 0,
            so_tui_khac INTEGER DEFAULT 0,
            tong_so_tui INTEGER DEFAULT 0,
            tong_so_cay INTEGER DEFAULT 0,
            tuan_xuat_cay INTEGER,
            ngay_xuat_cay TEXT,
            ghi_chu TEXT,
            ngay_tao TEXT NOT NULL,
            ngay_cap_nhat TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    
    # Thêm tài khoản admin mặc định
    c.execute('SELECT COUNT(*) FROM tai_khoan WHERE ten_dang_nhap = ?', ('admin',))
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO tai_khoan (ten_dang_nhap, ma_nhan_vien, ten_nhan_vien, quyen_han, ngay_tao)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'ADMIN001', 'Quản trị viên', 'admin', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    # Thêm danh mục tên giống mẫu
    c.execute('SELECT COUNT(*) FROM danh_muc_ten_giong')
    if c.fetchone()[0] == 0:
        ten_giong_mau = [
            "Đồng tiền đỏ", "Đồng tiền vàng", "Khoai lang tím",
            "Cây xuất khẩu A", "Cây xuất khẩu B"
        ]
        for tg in ten_giong_mau:
            c.execute('''
                INSERT OR IGNORE INTO danh_muc_ten_giong (ten_giong, ngay_tao)
                VALUES (?, ?)
            ''', (tg, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    # Thêm danh mục chu kỳ mẫu
    c.execute('SELECT COUNT(*) FROM danh_muc_chu_ky')
    if c.fetchone()[0] == 0:
        chu_ky_mau = ["Nhân nhanh", "Cấy giãn", "Ra rễ", "Nhân + Ra rễ"]
        for ck in chu_ky_mau:
            c.execute('''
                INSERT OR IGNORE INTO danh_muc_chu_ky (chu_ky, ngay_tao)
                VALUES (?, ?)
            ''', (ck, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    # Thêm danh mục môi trường mẫu (với mã số)
    c.execute('SELECT COUNT(*) FROM danh_muc_moi_truong')
    if c.fetchone()[0] == 0:
        moi_truong_mau = [
            (1, "MS"),
            (2, "MS + BAP"),
            (3, "MS + NAA"),
            (4, "MS + IBA"),
            (5, "Khác")
        ]
        for ma_so, ten_mt in moi_truong_mau:
            c.execute('''
                INSERT OR IGNORE INTO danh_muc_moi_truong (ma_so, ten_moi_truong, ngay_tao)
                VALUES (?, ?, ?)
            ''', (ma_so, ten_mt, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()

# Khởi tạo database
init_database()

# ========== HÀM HỖ TRỢ ==========
def tinh_tuan(ngay_cay):
    """Tính tuần từ ngày cấy (tuần bắt đầu từ thứ 2)"""
    if isinstance(ngay_cay, str):
        ngay = datetime.strptime(ngay_cay, "%Y-%m-%d").date()
    else:
        ngay = ngay_cay if isinstance(ngay_cay, date) else ngay_cay.date()
    
    # Tìm thứ 2 đầu tiên của năm
    ngay_dau_nam = date(ngay.year, 1, 1)
    days_since_monday = ngay_dau_nam.weekday()
    
    # Nếu ngày đầu năm không phải thứ 2, tìm thứ 2 đầu tiên
    if days_since_monday == 0:
        thang_hai_dau_tuan = ngay_dau_nam
    else:
        thang_hai_dau_tuan = ngay_dau_nam + timedelta(days=7 - days_since_monday)
    
    # Tính số tuần
    if ngay < thang_hai_dau_tuan:
        # Nếu ngày trước thứ 2 đầu tiên, tính tuần của năm trước
        ngay_dau_nam_truoc = date(ngay.year - 1, 1, 1)
        days_since_monday_truoc = ngay_dau_nam_truoc.weekday()
        if days_since_monday_truoc == 0:
            thang_hai_dau_tuan = ngay_dau_nam_truoc
        else:
            thang_hai_dau_tuan = ngay_dau_nam_truoc + timedelta(days=7 - days_since_monday_truoc)
    
    so_ngay = (ngay - thang_hai_dau_tuan).days
    tuan = (so_ngay // 7) + 1
    return max(1, tuan)

def tinh_tong_gio_lam(gio_bat_dau, gio_ket_thuc):
    """Tính tổng giờ làm việc"""
    try:
        gio_bd = datetime.strptime(gio_bat_dau, "%H:%M")
        gio_kt = datetime.strptime(gio_ket_thuc, "%H:%M")
        if gio_kt < gio_bd:
            # Nếu giờ kết thúc nhỏ hơn giờ bắt đầu, có thể là qua ngày
            gio_kt = gio_kt + timedelta(days=1)
        diff = gio_kt - gio_bd
        return diff.total_seconds() / 3600.0
    except:
        return 0.0

def tinh_tuan_xuat_cay(ngay_cay, chu_ky):
    """Tính tuần xuất cây dựa trên chu kỳ"""
    try:
        if isinstance(ngay_cay, str):
            ngay = datetime.strptime(ngay_cay, "%Y-%m-%d").date()
        else:
            ngay = ngay_cay if isinstance(ngay_cay, date) else ngay_cay.date()
        
        # Xác định số tuần dựa trên chu kỳ
        if "Nhân" in chu_ky and "Ra rễ" in chu_ky:
            so_tuan = 8  # Nhân + Ra rễ: 8 tuần
        elif "Nhân" in chu_ky:
            so_tuan = 6  # Nhân nhanh: 6 tuần
        elif "Ra rễ" in chu_ky:
            so_tuan = 4  # Ra rễ: 4 tuần
        elif "Giãn" in chu_ky:
            so_tuan = 3  # Cấy giãn: 3 tuần
        else:
            so_tuan = 4  # Mặc định: 4 tuần
        
        # Tính ngày xuất cây
        ngay_xuat = ngay + timedelta(weeks=so_tuan)
        
        # Tính tuần xuất cây
        tuan_xuat = tinh_tuan(ngay_xuat)
        
        return tuan_xuat, ngay_xuat.strftime("%Y-%m-%d")
    except:
        return None, None

def get_danh_sach_ten_giong():
    """Lấy danh sách tên giống từ database"""
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query('SELECT ten_giong FROM danh_muc_ten_giong ORDER BY ten_giong', conn)
    conn.close()
    return df['ten_giong'].tolist()

def get_danh_sach_chu_ky():
    """Lấy danh sách chu kỳ từ database"""
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query('SELECT chu_ky FROM danh_muc_chu_ky ORDER BY chu_ky', conn)
    conn.close()
    return df['chu_ky'].tolist()

def get_danh_sach_ma_tinh_trang():
    """
    Lấy danh sách mã tình trạng từ database
    Returns: list of integers [301, 305, 209, ...]
    """
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query('SELECT ma_so FROM danh_muc_ma_tinh_trang ORDER BY ma_so', conn)
    conn.close()
    
    if len(df) == 0:
        return []
    return df['ma_so'].tolist()

def get_danh_sach_gian_ke():
    """Lấy danh sách giàn/kệ từ database"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT so_gian_ke FROM danh_muc_gian_ke ORDER BY so_gian_ke')
    result = [row[0] for row in c.fetchall()]
    conn.close()
    return result

def get_danh_sach_vi_tri_kho():
    """Lấy danh sách vị trí kho môi trường từ database"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT vi_tri_kho FROM danh_muc_vi_tri_kho ORDER BY vi_tri_kho')
    result = [row[0] for row in c.fetchall()]
    conn.close()
    return result

def tao_ma_lo_moi_truong():
    """Tạo mã lô môi trường tự động theo format: MT-YYYYMMDD-XXX"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    ngay_hom_nay = datetime.now().strftime("%Y%m%d")
    
    # Đếm số lô đã tạo trong ngày
    c.execute('''
        SELECT COUNT(*) FROM kho_moi_truong 
        WHERE ma_lo LIKE ?
    ''', (f'MT-{ngay_hom_nay}-%',))
    count = c.fetchone()[0]
    conn.close()
    
    # Tạo mã mới
    so_thu_tu = count + 1
    ma_lo = f"MT-{ngay_hom_nay}-{so_thu_tu:03d}"
    return ma_lo

def tinh_tuoi_moi_truong(ngay_do):
    """
    Tính số ngày đã trôi qua kể từ ngày đổ môi trường
    Returns: (so_ngay: int, muc_canh_bao: str, icon: str, mau: str)
    """
    try:
        ngay_do_dt = datetime.strptime(ngay_do, "%Y-%m-%d")
        ngay_hien_tai = datetime.now()
        so_ngay = (ngay_hien_tai - ngay_do_dt).days
        
        # Xác định mức cảnh báo
        if so_ngay <= 15:
            return so_ngay, "OK", "✅", "#28a745"  # Xanh
        elif so_ngay <= 20:
            return so_ngay, "CẦN ƯU TIÊN", "⚠️", "#ffc107"  # Vàng
        elif so_ngay <= 30:
            return so_ngay, "SẮP QUÁ HẠN", "🟠", "#ff8c00"  # Cam
        else:
            return so_ngay, "QUÁ HẠN", "🔴", "#dc3545"  # Đỏ
    except:
        return 0, "ERROR", "❓", "#6c757d"

def get_danh_sach_lo_moi_truong_co_canh_bao(ma_so_moi_truong):
    """
    Lấy danh sách lô môi trường còn hàng với thông tin cảnh báo tuổi
    Returns: list of dict với thông tin lô + cảnh báo
    """
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT id, ma_lo, so_luong_con_lai, ngay_do, vi_tri_kho, nguoi_do
        FROM kho_moi_truong
        WHERE ma_so_moi_truong = ? AND so_luong_con_lai > 0
        ORDER BY ngay_do ASC
    ''', (ma_so_moi_truong,))
    
    rows = c.fetchall()
    conn.close()
    
    danh_sach_lo = []
    for row in rows:
        lo_id, ma_lo, so_luong, ngay_do, vi_tri, nguoi_do = row
        so_ngay, muc_canh_bao, icon, mau = tinh_tuoi_moi_truong(ngay_do)
        
        # Xác định gợi ý
        goi_y = ""
        if len(danh_sach_lo) == 0:  # Lô đầu tiên (cũ nhất)
            goi_y = " 🌟 GỢI Ý DÙNG TRƯỚC"
        
        danh_sach_lo.append({
            'id': lo_id,
            'ma_lo': ma_lo,
            'so_luong': so_luong,
            'ngay_do': ngay_do,
            'so_ngay': so_ngay,
            'muc_canh_bao': muc_canh_bao,
            'icon': icon,
            'mau': mau,
            'vi_tri': vi_tri,
            'nguoi_do': nguoi_do if nguoi_do else "N/A",
            'goi_y': goi_y,
            'label': f"{icon} {ma_lo} | {ngay_do} ({so_ngay} ngày) | Còn: {so_luong} túi | {muc_canh_bao}{goi_y}"
        })
    
    return danh_sach_lo

def khau_tru_moi_truong_theo_lo(ma_lo_chon, so_luong_can_dung):
    """
    Khấu trừ môi trường từ lô cụ thể do người dùng chọn
    Returns: (success: bool, message: str, thong_tin_lo: dict)
    """
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Lấy thông tin lô được chọn
    c.execute('''
        SELECT id, ma_lo, so_luong_con_lai, ngay_do, ma_so_moi_truong
        FROM kho_moi_truong
        WHERE ma_lo = ?
    ''', (ma_lo_chon,))
    
    row = c.fetchone()
    
    if not row:
        conn.close()
        return False, f"⚠️ Không tìm thấy lô {ma_lo_chon}!", {}
    
    lo_id, ma_lo, so_luong_con_lai, ngay_do, ma_so_moi_truong = row
    
    # Kiểm tra đủ số lượng không
    if so_luong_con_lai < so_luong_can_dung:
        conn.close()
        return False, f"⚠️ Lô {ma_lo} không đủ! Còn: {so_luong_con_lai}, Cần: {so_luong_can_dung}", {}
    
    # Khấu trừ
    so_luong_moi = so_luong_con_lai - so_luong_can_dung
    c.execute('''
        UPDATE kho_moi_truong
        SET so_luong_con_lai = ?
        WHERE id = ?
    ''', (so_luong_moi, lo_id))
    
    conn.commit()
    conn.close()
    
    # Tính tuổi môi trường
    so_ngay, muc_canh_bao, icon, mau = tinh_tuoi_moi_truong(ngay_do)
    
    thong_tin_lo = {
        'ma_lo': ma_lo,
        'so_luong_tru': so_luong_can_dung,
        'ngay_do': ngay_do,
        'so_ngay': so_ngay,
        'muc_canh_bao': muc_canh_bao,
        'qua_han': so_ngay > 30
    }
    
    message = f"✅ Đã khấu trừ {so_luong_can_dung} túi từ lô {ma_lo} ({so_ngay} ngày)"
    return True, message, thong_tin_lo

def khau_tru_moi_truong_tu_kho(ma_so_moi_truong, so_luong_can_dung):
    """
    Khấu trừ môi trường từ kho theo nguyên tắc FIFO
    Returns: (success: bool, message: str, danh_sach_lo_su_dung: list)
    """
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Lấy danh sách lô môi trường còn hàng, sắp xếp theo ngày đổ (FIFO)
    c.execute('''
        SELECT id, ma_lo, so_luong_con_lai, ngay_do 
        FROM kho_moi_truong 
        WHERE ma_so_moi_truong = ? AND so_luong_con_lai > 0
        ORDER BY ngay_do ASC
    ''', (ma_so_moi_truong,))
    
    danh_sach_lo = c.fetchall()
    
    if not danh_sach_lo:
        conn.close()
        return False, f"⚠️ Không tìm thấy lô môi trường mã {ma_so_moi_truong} trong kho!", []
    
    # Tính tổng số lượng còn lại
    tong_ton_kho = sum([lo[2] for lo in danh_sach_lo])
    
    if tong_ton_kho < so_luong_can_dung:
        conn.close()
        return False, f"⚠️ Kho không đủ! Cần: {so_luong_can_dung} túi, Còn: {tong_ton_kho} túi", []
    
    # Thực hiện khấu trừ FIFO
    so_luong_con_thieu = so_luong_can_dung
    danh_sach_lo_su_dung = []
    
    for lo in danh_sach_lo:
        if so_luong_con_thieu <= 0:
            break
        
        lo_id, ma_lo, so_luong_con_lai, ngay_do = lo
        
        if so_luong_con_lai >= so_luong_con_thieu:
            # Lô này đủ để trừ hết
            so_luong_tru = so_luong_con_thieu
            so_luong_moi = so_luong_con_lai - so_luong_tru
            so_luong_con_thieu = 0
        else:
            # Lô này không đủ, trừ hết và chuyển lô tiếp theo
            so_luong_tru = so_luong_con_lai
            so_luong_moi = 0
            so_luong_con_thieu -= so_luong_tru
        
        # Cập nhật số lượng còn lại
        c.execute('''
            UPDATE kho_moi_truong 
            SET so_luong_con_lai = ? 
            WHERE id = ?
        ''', (so_luong_moi, lo_id))
        
        danh_sach_lo_su_dung.append({
            'ma_lo': ma_lo,
            'so_luong_tru': so_luong_tru,
            'ngay_do': ngay_do
        })
    
    conn.commit()
    conn.close()
    
    message = f"✅ Đã khấu trừ {so_luong_can_dung} túi từ {len(danh_sach_lo_su_dung)} lô"
    return True, message, danh_sach_lo_su_dung

def kiem_tra_moi_truong_qua_han():
    """
    Kiểm tra các lô môi trường quá hạn (>= 30 ngày)
    Returns: (so_lo_qua_han: int, danh_sach_lo: list)
    """
    conn = sqlite3.connect('data.db')
    
    df = pd.read_sql_query('''
        SELECT 
            ma_lo,
            ten_moi_truong,
            ngay_do,
            so_luong_con_lai,
            vi_tri_kho,
            nguoi_do,
            CAST((julianday('now') - julianday(ngay_do)) AS INTEGER) AS tuoi_ngay
        FROM kho_moi_truong
        WHERE so_luong_con_lai > 0
          AND tuoi_ngay >= 30
        ORDER BY tuoi_ngay DESC
    ''', conn)
    
    conn.close()
    
    return len(df), df.to_dict('records') if len(df) > 0 else []

def cap_nhat_trang_thai_lo_moi_truong(ma_lo, trang_thai):
    """
    Cập nhật trạng thái lô môi trường (đã xử lý hoặc hủy)
    trang_thai: 'da_xu_ly' hoặc 'huy_bo'
    """
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    if trang_thai == 'huy_bo':
        # Set số lượng còn lại = 0
        c.execute('''
            UPDATE kho_moi_truong
            SET so_luong_con_lai = 0,
                ghi_chu = CASE 
                    WHEN ghi_chu IS NULL THEN '[HỦY BỎ: Quá hạn 30 ngày]'
                    ELSE ghi_chu || ' [HỦY BỎ: Quá hạn 30 ngày]'
                END
            WHERE ma_lo = ?
        ''', (ma_lo,))
    elif trang_thai == 'da_xu_ly':
        # Thêm ghi chú đã kiểm tra
        c.execute('''
            UPDATE kho_moi_truong
            SET ghi_chu = CASE 
                    WHEN ghi_chu IS NULL THEN '[ĐÃ KIỂM TRA: Vẫn sử dụng được]'
                    ELSE ghi_chu || ' [ĐÃ KIỂM TRA: Vẫn sử dụng được]'
                END
            WHERE ma_lo = ?
        ''', (ma_lo,))
    
    conn.commit()
    conn.close()

def get_danh_sach_moi_truong():
    """Lấy danh sách môi trường từ database (trả về dict: mã số -> tên)"""
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query('SELECT ma_so, ten_moi_truong FROM danh_muc_moi_truong ORDER BY ma_so', conn)
    conn.close()
    return df.set_index('ma_so')['ten_moi_truong'].to_dict()

def get_ten_moi_truong(ma_so):
    """Lấy tên môi trường từ mã số"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT ten_moi_truong FROM danh_muc_moi_truong WHERE ma_so = ?', (ma_so,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else f"Mã {ma_so}"

# ========== DANH MỤC TÌNH TRẠNG VỚI MÃ ==========

def get_danh_muc_tinh_trang():
    """
    Trả về danh mục tình trạng với mã số
    Mã cuối 3: Sạch
    Mã cuối 5: Khuẩn (có thể theo dõi/cấy lại)
    Mã cuối 9: Nấm/Khuẩn nặng (Hủy bỏ)
    
    Returns: dict {mã: tên}
    """
    return {
        103: "Sạch",
        105: "Khuẩn nhẹ",
        205: "Khuẩn môi trường",
        305: "Khuẩn khác",
        109: "Khuẩn nặng",
        209: "Nấm",
        309: "Hủy hoàn toàn"
    }

def get_ten_tinh_trang(ma_tinh_trang):
    """Lấy tên tình trạng từ mã"""
    danh_muc = get_danh_muc_tinh_trang()
    return danh_muc.get(ma_tinh_trang, f"Mã {ma_tinh_trang}")

def get_ma_tinh_trang(ten_tinh_trang):
    """Lấy mã tình trạng từ tên"""
    danh_muc = get_danh_muc_tinh_trang()
    # Đảo ngược dict
    reverse_dict = {v: k for k, v in danh_muc.items()}
    return reverse_dict.get(ten_tinh_trang, None)

def phan_loai_tinh_trang(ma_tinh_trang):
    """
    Phân loại tình trạng theo mã cuối
    Returns: ('sach' | 'khuan' | 'huy', color, icon)
    """
    if ma_tinh_trang is None:
        return 'unknown', '#808080', '❓'
    
    ma_cuoi = ma_tinh_trang % 10
    
    if ma_cuoi == 3:
        # Sạch
        return 'sach', '#28a745', '✅'
    elif ma_cuoi == 5:
        # Khuẩn - có thể theo dõi
        return 'khuan', '#ff8c00', '⚠️'
    elif ma_cuoi == 9:
        # Nấm/Hủy - thất thoát
        return 'huy', '#8b0000', '🔴'
    else:
        return 'unknown', '#808080', '❓'

def get_mau_sac_tinh_trang(ma_tinh_trang):
    """Lấy màu sắc theo tình trạng"""
    loai, color, icon = phan_loai_tinh_trang(ma_tinh_trang)
    return color

def get_icon_tinh_trang(ma_tinh_trang):
    """Lấy icon theo tình trạng"""
    loai, color, icon = phan_loai_tinh_trang(ma_tinh_trang)
    return icon

# ========== FUNCTIONS CHO QUẢN LÝ MÔ SOI ==========

def tao_ma_lo_mo_soi():
    """Tạo mã lô mô soi tự động: MS-YYYYMMDD-XXX"""
    today = date.today().strftime("%Y%m%d")
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM mo_soi WHERE ma_lo_mo_soi LIKE ?", (f"MS-{today}-%",))
    count = c.fetchone()[0]
    conn.close()
    return f"MS-{today}-{count+1:03d}"

def get_danh_sach_mo_soi_kha_dung(ten_giong=None):
    """
    Lấy danh sách mô soi khả dụng (còn cụm chưa cấy)
    Nếu có ten_giong, chỉ lấy lô của giống đó
    Returns: List of dicts
    """
    conn = sqlite3.connect('data.db')
    
    if ten_giong:
        query = '''
            SELECT 
                ma_lo_mo_soi,
                ten_giong,
                chu_ky_truoc,
                ngay_soi,
                tong_cum_sach,
                so_cum_da_cap,
                so_cum_con_lai,
                so_cum_moi_tui,
                trang_thai
            FROM mo_soi
            WHERE so_cum_con_lai > 0
              AND trang_thai = 'Đang sử dụng'
              AND ten_giong = ?
            ORDER BY ngay_soi ASC
        '''
        df = pd.read_sql_query(query, conn, params=(ten_giong,))
    else:
        query = '''
            SELECT 
                ma_lo_mo_soi,
                ten_giong,
                chu_ky_truoc,
                ngay_soi,
                tong_cum_sach,
                so_cum_da_cap,
                so_cum_con_lai,
                so_cum_moi_tui,
                trang_thai
            FROM mo_soi
            WHERE so_cum_con_lai > 0
              AND trang_thai = 'Đang sử dụng'
            ORDER BY ngay_soi ASC
        '''
        df = pd.read_sql_query(query, conn)
    
    conn.close()
    return df.to_dict('records') if len(df) > 0 else []

def khau_tru_mo_soi(ma_lo_mo_soi, so_cum_can_dung):
    """
    Khấu trừ số cụm mô soi khi được dùng làm mô mẹ
    Returns: (success: bool, message: str, so_cum_con_lai: int)
    """
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Lấy thông tin lô mô soi
    c.execute('''
        SELECT so_cum_con_lai, so_cum_da_cap, ten_giong 
        FROM mo_soi 
        WHERE ma_lo_mo_soi = ?
    ''', (ma_lo_mo_soi,))
    
    result = c.fetchone()
    
    if not result:
        conn.close()
        return False, "❌ Không tìm thấy lô mô soi", 0
    
    so_cum_con_lai, so_cum_da_cap, ten_giong = result
    
    if so_cum_con_lai < so_cum_can_dung:
        conn.close()
        return False, f"⚠️ Mô soi {ten_giong} chỉ còn {so_cum_con_lai} cụm, không đủ {so_cum_can_dung} cụm", so_cum_con_lai
    
    # Khấu trừ
    so_cum_con_lai_moi = so_cum_con_lai - so_cum_can_dung
    so_cum_da_cap_moi = so_cum_da_cap + so_cum_can_dung
    
    # Nếu hết mô soi, đánh dấu "Đã kết thúc chu kỳ"
    trang_thai_moi = 'Đã kết thúc chu kỳ' if so_cum_con_lai_moi == 0 else 'Đang sử dụng'
    
    c.execute('''
        UPDATE mo_soi
        SET so_cum_da_cap = ?,
            so_cum_con_lai = ?,
            trang_thai = ?,
            ngay_cap_nhat = ?
        WHERE ma_lo_mo_soi = ?
    ''', (so_cum_da_cap_moi, so_cum_con_lai_moi, trang_thai_moi, 
          datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ma_lo_mo_soi))
    
    conn.commit()
    conn.close()
    
    return True, f"✅ Đã khấu trừ {so_cum_can_dung} cụm từ lô {ma_lo_mo_soi}", so_cum_con_lai_moi

def get_bao_cao_doi_soat_mo_soi():
    """
    Tạo báo cáo đối soát: Mô Soi vs Mô Mẹ đã cấy
    Returns: DataFrame với cột:
        - ten_giong
        - tong_cum_mo_soi (từ bảng mo_soi)
        - tong_cum_da_cap (đã dùng làm mô mẹ)
        - tong_cum_con_lai (chưa dùng)
        - trang_thai (OK / DƯ MÔ / BẤT THƯỜNG)
    """
    conn = sqlite3.connect('data.db')
    
    # Lấy tổng mô soi theo giống
    df_mo_soi = pd.read_sql_query('''
        SELECT 
            ten_giong,
            SUM(tong_cum_sach) AS tong_cum_mo_soi,
            SUM(so_cum_da_cap) AS tong_cum_da_cap,
            SUM(so_cum_con_lai) AS tong_cum_con_lai
        FROM mo_soi
        GROUP BY ten_giong
    ''', conn)
    
    # Lấy tổng mô mẹ đã cấy (từ nhật ký)
    df_nhat_ky = pd.read_sql_query('''
        SELECT 
            ten_giong,
            SUM(so_tui_me * so_cum_tui_me) AS tong_cum_me_da_cay
        FROM nhat_ky_cay
        WHERE ma_lo_mo_soi IS NOT NULL
        GROUP BY ten_giong
    ''', conn)
    
    conn.close()
    
    # Merge 2 bảng
    if len(df_mo_soi) == 0:
        return pd.DataFrame(columns=['ten_giong', 'tong_cum_mo_soi', 'tong_cum_da_cap', 
                                     'tong_cum_con_lai', 'tong_cum_me_da_cay', 'chenh_lech', 'trang_thai'])
    
    df = df_mo_soi.merge(df_nhat_ky, on='ten_giong', how='left')
    df['tong_cum_me_da_cay'] = df['tong_cum_me_da_cay'].fillna(0).astype(int)
    
    # Tính chênh lệch và trạng thái
    df['chenh_lech'] = df['tong_cum_da_cap'] - df['tong_cum_me_da_cay']
    
    def xac_dinh_trang_thai(row):
        if row['chenh_lech'] == 0:
            return '✅ KHỚP'
        elif row['chenh_lech'] > 0:
            return f"⚠️ DƯ MÔ ({row['chenh_lech']} cụm)"
        else:
            return f"🔴 BẤT THƯỜNG (Vượt {abs(row['chenh_lech'])} cụm)"
    
    df['trang_thai'] = df.apply(xac_dinh_trang_thai, axis=1)
    
    return df

# ========== HÀM TẠO MÃ QR VÀ TEM NHÃN ==========
def load_logo():
    """
    Load logo công ty từ file.
    Trả về: PIL Image object hoặc None nếu không tìm thấy.
    """
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH)
            # Convert sang RGBA để hỗ trợ transparency
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')
            return logo
        except Exception as e:
            print(f"Lỗi khi load logo: {e}")
            return None
    return None

def generate_qr_code(data_id):
    """Tạo mã QR cho một lô cấy"""
    # Tạo URL với query parameter
    # Trong production, thay bằng URL thật của ứng dụng
    base_url = "http://localhost:8501"
    qr_data = f"{base_url}/?lo_id={data_id}"
    
    # Tạo QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Tạo hình ảnh QR và convert sang PIL Image RGB
    qr_img = qr.make_image(fill_color="black", back_color="white")
    # Convert sang RGB để tương thích với Streamlit
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')
    
    return qr_img, qr_data

def detect_label_size(ten_giong):
    """Tự động phát hiện kích thước tem phù hợp dựa trên loại cây"""
    # Danh sách các cây xuất khẩu/cây rễ cần tem lớn
    cay_can_tem_lon = [
        "cây rễ xuất khẩu", "xuất khẩu", "cây xuất khẩu",
        "cây a", "cây b", "export"
    ]
    
    ten_giong_lower = ten_giong.lower()
    for keyword in cay_can_tem_lon:
        if keyword in ten_giong_lower:
            return "35x22"  # Tem lớn 2 hàng
    
    return "25x15"  # Tem nhỏ 3 hàng (mặc định)

def create_label_image_35x22(data):
    """Tạo tem nhãn 35mm x 22mm (2 hàng nhãn trên cuộn) - Tem LỚN"""
    # Kích thước tem
    width_mm, height_mm = 35, 22
    dpi = 300
    width_px = int(width_mm / 25.4 * dpi)
    height_px = int(height_mm / 25.4 * dpi)
    
    # Tạo ảnh trắng
    img = Image.new('RGB', (width_px, height_px), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load font
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 50)   # Tên giống (Bold)
        font_medium = ImageFont.truetype("arial.ttf", 35)    # Thông tin khác
        font_small = ImageFont.truetype("arial.ttf", 30)     # Mã nhân viên
    except:
        try:
            font_large = ImageFont.truetype("arial.ttf", 50)
            font_medium = ImageFont.truetype("arial.ttf", 35)
            font_small = ImageFont.truetype("arial.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # ========== THÊM LOGO (GÓC TRÊN TRÁI) ==========
    logo = load_logo()
    logo_height = 0
    if logo:
        # Logo chiếm 15% chiều cao tem
        logo_size = int(height_px * 0.15)
        logo_resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Đặt logo ở góc trên trái
        logo_x = 10
        logo_y = 10
        
        # Paste logo (hỗ trợ transparency)
        if logo_resized.mode == 'RGBA':
            img.paste(logo_resized, (logo_x, logo_y), logo_resized)
        else:
            img.paste(logo_resized, (logo_x, logo_y))
        
        logo_height = logo_size + 5  # Thêm khoảng cách sau logo
    
    # Tạo QR code
    qr_img, _ = generate_qr_code(data['id'])
    qr_size = int(height_px * 0.75)  # QR chiếm 75% chiều cao
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Vị trí QR ở bên phải
    qr_x = width_px - qr_size - 15
    qr_y = (height_px - qr_size) // 2
    img.paste(qr_img, (qr_x, qr_y))
    
    # Vẽ đường viền
    draw.rectangle([(0, 0), (width_px-1, height_px-1)], outline='black', width=3)
    
    # Vẽ text bên trái (bắt đầu từ dưới logo)
    text_x = 15
    y_offset = max(25 + logo_height, 25)  # Bắt đầu sau logo hoặc vị trí mặc định
    line_height = 42
    
    # Dòng 1: Tên giống (Bold, lớn)
    ten_giong = data['ten_giong']
    if len(ten_giong) > 18:
        ten_giong = ten_giong[:18] + "..."
    draw.text((text_x, y_offset), ten_giong, fill='black', font=font_large)
    y_offset += line_height + 5
    
    # Dòng 2: Mã lô / Tuần cấy
    ma_lo_text = f"Lô #{data['id']} - T{data['tuan']}"
    draw.text((text_x, y_offset), ma_lo_text, fill='black', font=font_medium)
    y_offset += line_height
    
    # Dòng 3: Mã nhân viên (thay vì tên)
    ma_nv = data.get('ma_nhan_vien', 'N/A')
    draw.text((text_x, y_offset), f"NV: {ma_nv}", fill='black', font=font_small)
    
    return img

def create_label_image_25x15(data):
    """Tạo tem nhãn 25mm x 15mm (3 hàng nhãn trên cuộn) - Tem NHỎ - Tối ưu hóa"""
    # Kích thước tem
    width_mm, height_mm = 25, 15
    dpi = 300
    width_px = int(width_mm / 25.4 * dpi)
    height_px = int(height_mm / 25.4 * dpi)
    
    # Tạo ảnh trắng
    img = Image.new('RGB', (width_px, height_px), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load font (tối ưu cho tem nhỏ)
    try:
        font_title_bold = ImageFont.truetype("arialbd.ttf", 34)  # Tên giống (Bold)
        font_info = ImageFont.truetype("arial.ttf", 26)          # Mã lô/Tuần
        font_small = ImageFont.truetype("arial.ttf", 24)         # Mã NV
    except:
        try:
            font_title_bold = ImageFont.truetype("arial.ttf", 34)
            font_info = ImageFont.truetype("arial.ttf", 26)
            font_small = ImageFont.truetype("arial.ttf", 24)
        except:
            font_title_bold = ImageFont.load_default()
            font_info = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # ========== THÊM LOGO (GÓC TRÊN TRÁI, NHỎ HƠN) ==========
    logo = load_logo()
    logo_height = 0
    if logo:
        # Logo chiếm 12% chiều cao tem (nhỏ hơn cho tem nhỏ)
        logo_size = int(height_px * 0.12)
        logo_resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Đặt logo ở góc trên trái
        logo_x = 6
        logo_y = 6
        
        # Paste logo (hỗ trợ transparency)
        if logo_resized.mode == 'RGBA':
            img.paste(logo_resized, (logo_x, logo_y), logo_resized)
        else:
            img.paste(logo_resized, (logo_x, logo_y))
        
        logo_height = logo_size + 3  # Thêm khoảng cách sau logo
    
    # Tạo QR code (TĂNG kích thước lên tối đa - 80% chiều cao)
    qr_img, _ = generate_qr_code(data['id'])
    qr_size = int(height_px * 0.85)  # QR chiếm 85% chiều cao (tăng từ 70%)
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Vị trí QR ở góc phải (giảm margin)
    qr_x = width_px - qr_size - 5  # Margin chỉ 5px
    qr_y = (height_px - qr_size) // 2
    img.paste(qr_img, (qr_x, qr_y))
    
    # Vẽ đường viền mỏng
    draw.rectangle([(0, 0), (width_px-1, height_px-1)], outline='black', width=2)
    
    # Vẽ text bên trái (tối ưu không gian, bắt đầu từ dưới logo)
    text_x = 8  # Margin trái nhỏ
    text_width = qr_x - 12  # Chiều rộng vùng text
    y_offset = max(12 + logo_height, 12)  # Bắt đầu sau logo hoặc vị trí mặc định
    line_height = 28  # Khoảng cách dòng compact
    
    # Hàng 1: Tên giống (BOLD, rút gọn thông minh)
    ten_giong = data['ten_giong']
    if len(ten_giong) > 11:
        ten_giong = ten_giong[:11] + ".."
    draw.text((text_x, y_offset), ten_giong, fill='black', font=font_title_bold)
    y_offset += line_height
    
    # Hàng 2: Mã lô + Tuần cấy (compact)
    ma_lo_text = f"#{data['id']}/T{data['tuan']}"
    draw.text((text_x, y_offset), ma_lo_text, fill='black', font=font_info)
    y_offset += line_height
    
    # Hàng 3: Mã nhân viên (CHỈ mã, không có prefix "NV:")
    ma_nv = data.get('ma_nhan_vien', 'N/A')
    # Rút gọn mã nếu quá dài
    if len(ma_nv) > 10:
        ma_nv = ma_nv[:10]
    draw.text((text_x, y_offset), ma_nv, fill='black', font=font_small)
    
    return img

def create_label_image(data, size="auto"):
    """
    Tạo hình ảnh tem nhãn với kích thước tự động hoặc chỉ định
    
    Args:
        data: Dictionary chứa thông tin lô cấy
        size: "auto" (tự động), "35x22" (tem lớn), "25x15" (tem nhỏ)
    """
    if size == "auto":
        size = detect_label_size(data['ten_giong'])
    
    if size == "35x22":
        return create_label_image_35x22(data)
    else:  # "25x15"
        return create_label_image_25x15(data)

def image_to_base64(img):
    """Chuyển đổi PIL Image sang base64 để hiển thị trong Streamlit"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def create_label_pdf(data, size="auto"):
    """Tạo file PDF chứa tem nhãn đúng kích thước"""
    buffer = io.BytesIO()
    
    # Xác định kích thước
    if size == "auto":
        size = detect_label_size(data['ten_giong'])
    
    # Tạo tem nhãn
    label_img = create_label_image(data, size)
    
    # Chuyển đổi PIL Image sang định dạng có thể dùng cho reportlab
    img_buffer = io.BytesIO()
    label_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Kích thước tem theo mm -> points (1 inch = 25.4 mm = 72 points)
    if size == "35x22":
        label_width_mm, label_height_mm = 35, 22
    else:  # "25x15"
        label_width_mm, label_height_mm = 25, 15
    
    label_width_pt = label_width_mm / 25.4 * 72
    label_height_pt = label_height_mm / 25.4 * 72
    
    # Tạo PDF với kích thước chính xác bằng kích thước tem
    # Điều này giúp máy in tem nhiệt tự động nhận diện đúng
    c = canvas.Canvas(buffer, pagesize=(label_width_pt, label_height_pt))
    
    # Vẽ tem (full page, không có margin)
    c.drawImage(ImageReader(img_buffer), 0, 0, width=label_width_pt, height=label_height_pt)
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer, size

# ========== QUẢN LÝ SESSION ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# ========== XỬ LÝ QUERY PARAMETER (QR CODE SCANNING) ==========
# Kiểm tra xem có query parameter lo_id không (từ QR code)
query_params = st.query_params
if 'lo_id' in query_params and st.session_state.logged_in:
    st.session_state.scan_lo_id = query_params['lo_id']
    st.session_state.auto_navigate = True
else:
    if 'scan_lo_id' not in st.session_state:
        st.session_state.scan_lo_id = None
    if 'auto_navigate' not in st.session_state:
        st.session_state.auto_navigate = False

# ========== TRANG ĐĂNG NHẬP ==========
if not st.session_state.logged_in:
    # ========== HEADER VỚI LOGO ==========
    # Hiển thị logo công ty ở trang chủ (nếu có)
    logo = load_logo()
    if logo:
        col_logo, col_title, col_spacer = st.columns([1, 3, 1])
        
        with col_logo:
            # Logo bên trái
            logo_display = logo.copy()
            logo_width = 150
            logo_height = int(logo_display.height * (logo_width / logo_display.width))
            logo_display = logo_display.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Convert sang RGB để hiển thị
            if logo_display.mode == 'RGBA':
                bg = Image.new('RGB', logo_display.size, (255, 255, 255))
                bg.paste(logo_display, mask=logo_display.split()[3])
                logo_display = bg
            
            st.image(logo_display, use_column_width=True)
        
        with col_title:
            st.markdown('<div class="main-header">🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱</div>', unsafe_allow_html=True)
        
        with col_spacer:
            # Logo bên phải (đối xứng)
            st.image(logo_display, use_column_width=True)
    else:
        # Không có logo, chỉ hiển thị header
        st.markdown('<div class="main-header">🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱</div>', unsafe_allow_html=True)
    
    st.header("🔐 Đăng nhập")
    st.markdown("---")
    
    with st.form("form_dang_nhap"):
        ten_dang_nhap = st.text_input("👤 Tên đăng nhập", placeholder="Nhập tên đăng nhập...")
        ma_nhan_vien = st.text_input("🔑 Mã nhân viên", placeholder="Nhập mã nhân viên...", type="password")
        
        submitted = st.form_submit_button("🚪 Đăng nhập", use_container_width=True)
        
        if submitted:
            if ten_dang_nhap.strip() and ma_nhan_vien.strip():
                conn = sqlite3.connect('data.db')
                c = conn.cursor()
                c.execute('''
                    SELECT ten_dang_nhap, ma_nhan_vien, ten_nhan_vien, quyen_han 
                    FROM tai_khoan 
                    WHERE ten_dang_nhap = ? AND ma_nhan_vien = ?
                ''', (ten_dang_nhap.strip(), ma_nhan_vien.strip()))
                
                result = c.fetchone()
                conn.close()
                
                if result:
                    st.session_state.logged_in = True
                    st.session_state.user_info = {
                        'ten_dang_nhap': result[0],
                        'ma_nhan_vien': result[1],
                        'ten_nhan_vien': result[2],
                        'quyen_han': result[3]
                    }
                    st.success(f"✅ Đăng nhập thành công! Chào mừng {result[2]}")
                    st.rerun()
                else:
                    st.error("❌ Tên đăng nhập hoặc mã nhân viên không đúng!")
            else:
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin!")
    
    st.markdown("---")
    st.info("💡 **Tài khoản mặc định:** Tên đăng nhập: `admin`, Mã nhân viên: `ADMIN001`")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Thông tin")
    st.sidebar.info(
        """
        **Ứng dụng Quản lý Phòng Nuôi Cấy Mô**
        
        📌 Vui lòng đăng nhập để sử dụng
        
        👤 Nhân viên: Chỉ xem dữ liệu cá nhân
        
        🔑 Admin: Xem tất cả dữ liệu và biểu đồ
        """
    )

# ========== ỨNG DỤNG CHÍNH (SAU KHI ĐĂNG NHẬP) ==========
else:
    user_info = st.session_state.user_info
    is_admin = user_info['quyen_han'] == 'admin'
    
    # Header với logo
    # ========== HEADER VỚI LOGO ==========
    logo = load_logo()
    if logo:
        col_logo_main, col_title_main, col_spacer_main = st.columns([1, 3, 1])
        
        with col_logo_main:
            # Logo bên trái
            logo_display = logo.copy()
            logo_width = 120
            logo_height = int(logo_display.height * (logo_width / logo_display.width))
            logo_display = logo_display.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Convert sang RGB để hiển thị
            if logo_display.mode == 'RGBA':
                bg = Image.new('RGB', logo_display.size, (255, 255, 255))
                bg.paste(logo_display, mask=logo_display.split()[3])
                logo_display = bg
            
            st.image(logo_display, use_column_width=True)
        
        with col_title_main:
            st.markdown('<div class="main-header">🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱</div>', unsafe_allow_html=True)
        
        with col_spacer_main:
            # Logo bên phải (đối xứng)
            st.image(logo_display, use_column_width=True)
    else:
        # Không có logo, chỉ hiển thị header
        st.markdown('<div class="main-header">🌱 QUẢN LÝ PHÒNG NUÔI CẤY MÔ 🌱</div>', unsafe_allow_html=True)
    
    # Sidebar với thông tin người dùng
    # ========== HIỂN THỊ LOGO CÔNG TY ==========
    logo = load_logo()
    if logo:
        # Resize logo để vừa với sidebar (max width 200px)
        logo_display = logo.copy()
        logo_width = 200
        logo_height = int(logo_display.height * (logo_width / logo_display.width))
        logo_display = logo_display.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        
        # Convert sang RGB để hiển thị
        if logo_display.mode == 'RGBA':
            # Tạo background trắng cho logo có alpha
            bg = Image.new('RGB', logo_display.size, (255, 255, 255))
            bg.paste(logo_display, mask=logo_display.split()[3])  # 3 is the alpha channel
            logo_display = bg
        
        # Hiển thị logo
        st.sidebar.image(logo_display, use_column_width=True)
        st.sidebar.markdown("---")
    
    st.sidebar.markdown(f"### 👤 {user_info['ten_nhan_vien']}")
    st.sidebar.markdown(f"**Mã NV:** {user_info['ma_nhan_vien']}")
    if is_admin:
        st.sidebar.success("🔑 Quyền: Admin")
    else:
        st.sidebar.info("👤 Quyền: Nhân viên")
    
    if st.sidebar.button("🚪 Đăng xuất"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # ========== THÔNG BÁO THÔNG MINH CHO ADMIN ==========
    if is_admin:
        so_lo_qua_han, danh_sach_qua_han = kiem_tra_moi_truong_qua_han()
        
        if so_lo_qua_han > 0:
            # Hiển thị cảnh báo trong sidebar
            st.sidebar.error(f"""
            🚨 **CẢNH BÁO KHẨN CẤP**
            
            Có **{so_lo_qua_han} lô** môi trường 
            đã quá 30 ngày!
            
            ⚠️ Vui lòng kiểm tra và xử lý ngay
            """)
            
            # Nút quick access
            if st.sidebar.button("🔍 Xem chi tiết & Xử lý", use_container_width=True, type="primary"):
                st.session_state['show_urgent_tasks'] = True
            
            # Toast notification (hiện 1 lần khi load)
            if 'toast_shown' not in st.session_state:
                st.toast(f"🚨 CẢNH BÁO: {so_lo_qua_han} lô môi trường quá hạn!", icon="🚨")
                st.session_state['toast_shown'] = True
        else:
            # Reset toast flag khi không còn cảnh báo
            if 'toast_shown' in st.session_state:
                del st.session_state['toast_shown']
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Thông tin")
    st.sidebar.info(
        f"""
        **Phiên bản:** 2.0
        **Người dùng:** {user_info['ten_nhan_vien']}
        **Quyền:** {'Quản trị viên' if is_admin else 'Nhân viên'}
        """
    )
    
    # Menu
    if is_admin:
        menu = st.sidebar.selectbox(
            "📋 Chọn chức năng",
            ["Nhập liệu", "In tem nhãn", "Báo cáo Năng suất", "Quản lý & Phân tích Nhiễm", "Quản lý Phòng Sáng", "Tổng hợp Phòng Sáng", "Quản lý Mô Soi", "Đối soát Mô Soi", "Quản lý Kho Môi trường", "Quản lý danh mục", "Quản lý tài khoản"]
        )
    else:
        # NHÂN VIÊN: Nhập liệu + Xem báo cáo cá nhân
        menu = st.sidebar.selectbox(
            "📋 Chọn chức năng",
            ["Nhập liệu", "Báo cáo Cá nhân"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.info("""
        **👤 Quyền Nhân viên:**
        
        Bạn có thể:
        - ✅ Nhập nhật ký cấy
        - ✅ Sửa nhật ký **TRONG NGÀY**
        - ✅ Xem báo cáo cá nhân
        
        ⚠️ **Lưu ý:**
        - Chỉ sửa được nhật ký **HÔM NAY**
        - Nhật ký ngày cũ → Liên hệ Admin
        
        💡 Không có quyền quản lý hệ thống.
        """)
    
    # ========== DASHBOARD VIỆC CẦN LÀM GẤP (ADMIN) ==========
    if is_admin and st.session_state.get('show_urgent_tasks', False):
        st.markdown("---")
        st.markdown("# 🚨 VIỆC CẦN XỬ LÝ GẤP")
        
        so_lo_qua_han, danh_sach_qua_han = kiem_tra_moi_truong_qua_han()
        
        if so_lo_qua_han > 0:
            st.error(f"""
            ### ⚠️ CÓ {so_lo_qua_han} LÔ MÔI TRƯỜNG QUÁ HẠN (≥ 30 NGÀY)
            
            **Hành động cần thực hiện:**
            - Kiểm tra chất lượng môi trường
            - Quyết định: Tiếp tục sử dụng hoặc Hủy bỏ
            - Cập nhật trạng thái để không hiện cảnh báo nữa
            """)
            
            # Hiển thị từng lô với action buttons
            for lo in danh_sach_qua_han:
                with st.expander(f"🔴 {lo['ma_lo']} - {lo['ten_moi_truong']} ({lo['tuoi_ngay']} ngày)", expanded=True):
                    col_info, col_action = st.columns([2, 1])
                    
                    with col_info:
                        st.markdown(f"""
                        **Thông tin lô:**
                        - 📦 **Mã lô:** {lo['ma_lo']}
                        - 🧪 **Loại:** {lo['ten_moi_truong']}
                        - 📅 **Ngày đổ:** {lo['ngay_do']}
                        - ⏰ **Tuổi:** {lo['tuoi_ngay']} ngày
                        - 📊 **Còn lại:** {lo['so_luong_con_lai']} túi
                        - 📍 **Vị trí:** {lo['vi_tri_kho']}
                        - 👤 **Người đổ:** {lo['nguoi_do'] if lo['nguoi_do'] else 'N/A'}
                        
                        **⚠️ RỦI RO:**
                        - Tỷ lệ nhiễm cao
                        - Chất lượng môi trường giảm
                        - Ảnh hưởng đến năng suất cấy
                        """)
                    
                    with col_action:
                        st.markdown("### Hành động:")
                        
                        if st.button("✅ Đã kiểm tra - Vẫn dùng được", 
                                   key=f"keep_{lo['ma_lo']}", 
                                   use_container_width=True,
                                   type="secondary"):
                            cap_nhat_trang_thai_lo_moi_truong(lo['ma_lo'], 'da_xu_ly')
                            st.success("✅ Đã ghi nhận: Lô vẫn sử dụng được")
                            st.rerun()
                        
                        if st.button("🗑️ HỦY BỎ lô này", 
                                   key=f"delete_{lo['ma_lo']}", 
                                   use_container_width=True,
                                   type="primary"):
                            cap_nhat_trang_thai_lo_moi_truong(lo['ma_lo'], 'huy_bo')
                            st.success("✅ Đã hủy bỏ lô môi trường")
                            st.rerun()
            
            # Nút đóng
            st.markdown("---")
            if st.button("✖️ Đóng danh sách việc cần làm", use_container_width=True):
                st.session_state['show_urgent_tasks'] = False
                st.rerun()
        else:
            st.success("✅ Không có lô môi trường nào cần xử lý gấp!")
            if st.button("✖️ Đóng", use_container_width=True):
                st.session_state['show_urgent_tasks'] = False
                st.rerun()
        
        st.markdown("---")
    
    # ========== TRANG BÁO CÁO CÁ NHÂN (NHÂN VIÊN) ==========
    if menu == "Báo cáo Cá nhân":
        st.header(f"📊 Báo cáo Cá nhân - {user_info['ten_nhan_vien']}")
        st.markdown(f"**Mã nhân viên:** {user_info['ma_nhan_vien']}")
        st.markdown("---")
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📝 Nhật ký của tôi", "📈 Năng suất", "🔬 Tỷ lệ nhiễm"])
        
        # Tab 1: Nhật ký cá nhân
        with tab1:
            st.subheader("📝 Nhật ký cấy của tôi")
            
            conn = sqlite3.connect('data.db')
            
            # Lọc theo ngày
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                ngay_bat_dau = st.date_input(
                    "Từ ngày",
                    value=date.today() - timedelta(days=30)
                )
            with col_filter2:
                ngay_ket_thuc = st.date_input(
                    "Đến ngày",
                    value=date.today()
                )
            
            query = '''
                SELECT 
                    id, ngay_cay, ten_giong, chu_ky, tinh_trang,
                    so_tui_me, so_cum_tui_me, so_tui_con, so_cum_tui_con,
                    tong_so_cay_con, gio_bat_dau, gio_ket_thuc,
                    tong_gio_lam, nang_suat, ghi_chu
                FROM nhat_ky_cay
                WHERE ma_nhan_vien = ?
                  AND ngay_cay BETWEEN ? AND ?
                ORDER BY ngay_cay DESC, id DESC
            '''
            
            df = pd.read_sql_query(
                query, conn,
                params=(user_info['ma_nhan_vien'], 
                       ngay_bat_dau.strftime('%Y-%m-%d'),
                       ngay_ket_thuc.strftime('%Y-%m-%d'))
            )
            conn.close()
            
            if len(df) > 0:
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Tổng lô cấy", len(df))
                with col2:
                    st.metric("Tổng cây con", f"{df['tong_so_cay_con'].sum():,}")
                with col3:
                    st.metric("Tổng giờ làm", f"{df['tong_gio_lam'].sum():.1f}h")
                with col4:
                    st.metric("Năng suất TB", f"{df['nang_suat'].mean():.1f}")
                
                st.markdown("---")
                
                # Hiển thị bảng
                df_display = df.rename(columns={
                    'id': 'ID',
                    'ngay_cay': 'Ngày cấy',
                    'ten_giong': 'Giống',
                    'chu_ky': 'Chu kỳ',
                    'tinh_trang': 'Tình trạng',
                    'so_tui_me': 'Túi mẹ',
                    'so_cum_tui_me': 'Cụm/Túi mẹ',
                    'so_tui_con': 'Túi con',
                    'so_cum_tui_con': 'Cụm/Túi con',
                    'tong_so_cay_con': 'Tổng cây',
                    'gio_bat_dau': 'Giờ BĐ',
                    'gio_ket_thuc': 'Giờ KT',
                    'tong_gio_lam': 'Giờ làm',
                    'nang_suat': 'Năng suất',
                    'ghi_chu': 'Ghi chú'
                })
                
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                # Download
                st.download_button(
                    "📥 Tải xuống Excel",
                    data=df_display.to_csv(index=False).encode('utf-8-sig'),
                    file_name=f"nhat_ky_{user_info['ma_nhan_vien']}_{date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("ℹ️ Không có dữ liệu trong khoảng thời gian này.")
        
        # Tab 2: Năng suất
        with tab2:
            st.subheader("📈 Báo cáo Năng suất")
            
            conn = sqlite3.connect('data.db')
            
            # Lọc theo tháng
            col1, col2 = st.columns(2)
            with col1:
                thang_filter = st.selectbox(
                    "Chọn tháng",
                    options=list(range(1, 13)),
                    index=date.today().month - 1
                )
            with col2:
                nam_filter = st.number_input(
                    "Năm",
                    min_value=2020,
                    max_value=2030,
                    value=date.today().year
                )
            
            query = '''
                SELECT 
                    ten_giong,
                    chu_ky,
                    COUNT(*) AS so_lo,
                    SUM(so_tui_con) AS tong_tui,
                    SUM(tong_so_cay_con) AS tong_cay,
                    SUM(tong_gio_lam) AS tong_gio,
                    AVG(nang_suat) AS nang_suat_tb
                FROM nhat_ky_cay
                WHERE ma_nhan_vien = ?
                  AND thang = ?
                  AND strftime('%Y', ngay_cay) = ?
                GROUP BY ten_giong, chu_ky
                ORDER BY tong_cay DESC
            '''
            
            df_nang_suat = pd.read_sql_query(
                query, conn,
                params=(user_info['ma_nhan_vien'], thang_filter, str(nam_filter))
            )
            conn.close()
            
            if len(df_nang_suat) > 0:
                # Tổng hợp
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tổng cây cấy", f"{df_nang_suat['tong_cay'].sum():,}")
                with col2:
                    st.metric("Tổng giờ làm", f"{df_nang_suat['tong_gio'].sum():.1f}h")
                with col3:
                    st.metric("Năng suất TB", f"{df_nang_suat['nang_suat_tb'].mean():.1f}")
                
                st.markdown("---")
                
                # Biểu đồ
                import plotly.express as px
                
                fig = px.bar(
                    df_nang_suat,
                    x='ten_giong',
                    y='tong_cay',
                    color='chu_ky',
                    title=f"Năng suất tháng {thang_filter}/{nam_filter}",
                    labels={'tong_cay': 'Tổng cây', 'ten_giong': 'Giống'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Bảng chi tiết
                st.markdown("#### Chi tiết theo giống")
                df_display = df_nang_suat.rename(columns={
                    'ten_giong': 'Giống',
                    'chu_ky': 'Chu kỳ',
                    'so_lo': 'Số lô',
                    'tong_tui': 'Tổng túi',
                    'tong_cay': 'Tổng cây',
                    'tong_gio': 'Tổng giờ',
                    'nang_suat_tb': 'Năng suất TB'
                })
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            else:
                st.info(f"ℹ️ Không có dữ liệu tháng {thang_filter}/{nam_filter}.")
        
        # Tab 3: Tỷ lệ nhiễm
        with tab3:
            st.subheader("🔬 Tỷ lệ Nhiễm")
            
            conn = sqlite3.connect('data.db')
            
            # Lọc theo khoảng thời gian
            col1, col2 = st.columns(2)
            with col1:
                ngay_bd = st.date_input(
                    "Từ ngày",
                    value=date.today() - timedelta(days=30),
                    key="nhiem_tu_ngay"
                )
            with col2:
                ngay_kt = st.date_input(
                    "Đến ngày",
                    value=date.today(),
                    key="nhiem_den_ngay"
                )
            
            query = '''
                SELECT 
                    tinh_trang,
                    COUNT(*) AS so_lo,
                    SUM(so_tui_con) AS tong_tui
                FROM nhat_ky_cay
                WHERE ma_nhan_vien = ?
                  AND ngay_cay BETWEEN ? AND ?
                GROUP BY tinh_trang
            '''
            
            df_nhiem = pd.read_sql_query(
                query, conn,
                params=(user_info['ma_nhan_vien'],
                       ngay_bd.strftime('%Y-%m-%d'),
                       ngay_kt.strftime('%Y-%m-%d'))
            )
            conn.close()
            
            if len(df_nhiem) > 0:
                # Tính tổng
                tong_tui = df_nhiem['tong_tui'].sum()
                tui_sach = df_nhiem[df_nhiem['tinh_trang'] == 'Sạch']['tong_tui'].sum() if 'Sạch' in df_nhiem['tinh_trang'].values else 0
                
                # Phân loại theo mã
                tui_khuan = 0  # Mã 5
                tui_huy = 0    # Mã 9
                
                for _, row in df_nhiem.iterrows():
                    ma = get_ma_tinh_trang(row['tinh_trang'])
                    if ma:
                        loai, _, _ = phan_loai_tinh_trang(ma)
                        if loai == 'khuan':
                            tui_khuan += row['tong_tui']
                        elif loai == 'huy':
                            tui_huy += row['tong_tui']
                
                ty_le_sach = (tui_sach / tong_tui * 100) if tong_tui > 0 else 0
                ty_le_khuan = (tui_khuan / tong_tui * 100) if tong_tui > 0 else 0
                ty_le_huy = (tui_huy / tong_tui * 100) if tong_tui > 0 else 0
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Tổng túi", f"{tong_tui:,}")
                with col2:
                    st.metric("✅ Sạch", f"{ty_le_sach:.1f}%", delta=None, delta_color="normal")
                with col3:
                    st.metric("⚠️ Khuẩn (Mã 5)", f"{ty_le_khuan:.1f}%", delta=None, delta_color="off")
                with col4:
                    st.metric("🔴 Hủy (Mã 9)", f"{ty_le_huy:.1f}%", delta=None, delta_color="inverse")
                
                # Đánh giá
                if ty_le_huy > 15:
                    st.error(f"""
                    🔴 **CẢNH BÁO CAO!**
                    
                    Tỷ lệ hủy bỏ của bạn là **{ty_le_huy:.1f}%** (cao hơn mức cho phép 15%)
                    
                    **Nguyên nhân có thể:**
                    - Môi trường không đảm bảo
                    - Kỹ thuật cấy chưa tốt
                    - Thiết bị tiệt trùng kém
                    
                    💡 **Khuyến nghị:** Cần cải thiện quy trình ngay
                    """)
                elif ty_le_huy > 10:
                    st.warning(f"""
                    ⚠️ **CẦN CHÚ Ý!**
                    
                    Tỷ lệ hủy bỏ của bạn là **{ty_le_huy:.1f}%** (cần giảm xuống < 10%)
                    
                    💡 **Khuyến nghị:** Kiểm tra lại quy trình
                    """)
                elif ty_le_sach >= 85:
                    st.success(f"""
                    ✅ **RẤT TỐT!**
                    
                    Tỷ lệ sạch của bạn là **{ty_le_sach:.1f}%** - Xuất sắc!
                    
                    🎉 Tiếp tục duy trì chất lượng này!
                    """)
                else:
                    st.info(f"""
                    📊 **BÌN THƯỜNG**
                    
                    Tỷ lệ sạch: **{ty_le_sach:.1f}%**
                    
                    💡 Cố gắng đạt mức > 85%
                    """)
                
                st.markdown("---")
                
                # Biểu đồ tròn
                import plotly.graph_objects as go
                
                fig = go.Figure(data=[go.Pie(
                    labels=['Sạch', 'Khuẩn (Mã 5)', 'Hủy (Mã 9)'],
                    values=[tui_sach, tui_khuan, tui_huy],
                    marker=dict(colors=['#28a745', '#ff8c00', '#8b0000'])
                )])
                
                fig.update_layout(title="Phân bố tình trạng")
                st.plotly_chart(fig, use_container_width=True)
                
                # Bảng chi tiết
                st.markdown("#### Chi tiết theo tình trạng")
                df_display = df_nhiem.rename(columns={
                    'tinh_trang': 'Tình trạng',
                    'so_lo': 'Số lô',
                    'tong_tui': 'Tổng túi'
                })
                df_display['Tỷ lệ %'] = (df_display['Tổng túi'] / tong_tui * 100).round(1)
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ Không có dữ liệu trong khoảng thời gian này.")
    
    # ========== TRANG NHẬP LIỆU (ADMIN + NHÂN VIÊN) ==========
    elif menu == "Nhập liệu":
        st.header("📝 Nhập liệu mới")
        st.markdown("---")
        
        # Lấy danh sách từ database
        danh_sach_ten_giong = get_danh_sach_ten_giong()
        danh_sach_chu_ky = get_danh_sach_chu_ky()
        danh_sach_moi_truong = get_danh_sach_moi_truong()  # Dict: mã số -> tên
        
        # Danh mục tình trạng với mã
        dict_tinh_trang = get_danh_muc_tinh_trang()
        danh_sach_tinh_trang = list(dict_tinh_trang.values())  # Danh sách tên để hiển thị
        
        if len(danh_sach_ten_giong) == 0 or len(danh_sach_chu_ky) == 0 or len(danh_sach_moi_truong) == 0:
            st.warning("⚠️ Vui lòng cập nhật danh mục ở trang 'Quản lý danh mục' trước khi nhập liệu.")
        else:
            with st.form("form_nhap_lieu", clear_on_submit=True):
                # TỐI ƯU MOBILE: Chỉ dùng 1 cột trên mobile, 2 cột trên desktop
                # Streamlit tự động responsive với st.columns()
                
                st.markdown("#### 📅 Thông tin thời gian")
                ngay_cay = st.date_input(
                    "Ngày cấy *",
                    value=date.today()
                )
                
                # Lấy năm từ ngày cấy
                nam = ngay_cay.year
                
                # NHẬP TAY Tuần và Tháng
                col_tuan, col_thang = st.columns(2)
                with col_tuan:
                    tuan = st.selectbox(
                        "📊 Tuần cấy *",
                        options=list(range(1, 53)),
                        index=tinh_tuan(ngay_cay) - 1,  # Gợi ý tuần hiện tại
                        help="Chọn tuần cấy (1-52)"
                    )
                with col_thang:
                    thang = st.selectbox(
                        "📅 Tháng cấy *",
                        options=list(range(1, 13)),
                        index=ngay_cay.month - 1,  # Gợi ý tháng hiện tại
                        help="Chọn tháng cấy (1-12)"
                    )
                
                st.markdown("---")
                st.markdown("#### 🌿 Thông tin giống")
                ten_giong = st.selectbox(
                    "Tên giống *",
                    options=danh_sach_ten_giong,
                    index=0,
                    help="Chọn loại giống cây"
                )
                
                chu_ky = st.selectbox(
                    "Chu kỳ *",
                    options=danh_sach_chu_ky,
                    index=0,
                    help="Chọn chu kỳ cấy"
                )
                
                # THAY ĐỔI: Tình trạng đơn giản chỉ 2 lựa chọn
                col_tinh_trang, col_ma = st.columns(2)
                
                with col_tinh_trang:
                    tinh_trang = st.selectbox(
                        "Tình trạng *",
                        options=["Sạch", "Khuẩn"],
                        index=0,
                        help="Chọn tình trạng: Sạch hoặc Khuẩn"
                    )
                
                with col_ma:
                    # Dropdown đơn giản - chỉ hiển thị mã số
                    danh_sach_ma = get_danh_sach_ma_tinh_trang()
                    
                    if len(danh_sach_ma) == 0:
                        st.warning("⚠️ Chưa có mã tình trạng. Vui lòng thêm ở 'Quản lý danh mục'!")
                        ma_tinh_trang = 301  # Fallback
                    else:
                        ma_tinh_trang = st.selectbox(
                            "Mã tình trạng *",
                            options=danh_sach_ma,
                            index=0,
                            help="Chọn mã tình trạng"
                        )
                
                box_cay = st.number_input(
                    "Box cấy *",
                    min_value=1,
                    value=1,
                    step=1,
                    help="Số lượng box cấy"
                )
                
                st.markdown("---")
                st.markdown("#### 📝 Ghi chú & Giàn cây")
                
                ghi_chu = st.text_area(
                    "Ghi chú",
                    placeholder="Nhập ghi chú nếu có...",
                    height=80,
                    help="Thông tin bổ sung"
                )
                
                # Lấy danh sách giàn/kệ từ database
                danh_sach_gian_ke = get_danh_sach_gian_ke()
                
                if len(danh_sach_gian_ke) > 0:
                    so_gian_ke = st.selectbox(
                        "Số Giàn/Kệ *",
                        options=danh_sach_gian_ke,
                        help="Chọn giàn/kệ từ danh sách (Quản lý tại 'Quản lý danh mục')"
                    )
                else:
                    st.warning("⚠️ Chưa có giàn/kệ nào. Vui lòng thêm tại 'Quản lý danh mục' → 'Giàn/Kệ Phòng Sáng'")
                    so_gian_ke = st.text_input(
                        "Số Giàn/Kệ (tạm thời) *",
                        placeholder="Ví dụ: Giàn A1, Kệ B2...",
                        value=f"Giàn {box_cay}",
                        help="Nhập tạm - Nên thêm vào danh mục để dễ quản lý"
                    )
                
                st.markdown("---")
                st.markdown("#### 🧪 Thông tin môi trường")
                
                # Tạo danh sách tên môi trường để chọn (sắp xếp theo tên)
                danh_sach_ten_moi_truong = sorted([ten_mt for ten_mt in danh_sach_moi_truong.values()])
                
                # Tạo dict ngược: tên -> mã số
                dict_ten_to_ma = {ten_mt: ma_so for ma_so, ten_mt in danh_sach_moi_truong.items()}
                
                moi_truong_me = st.selectbox(
                    "Môi trường mẹ *",
                    options=danh_sach_ten_moi_truong,
                    index=0 if len(danh_sach_ten_moi_truong) > 0 else None,
                    help="Chọn môi trường mẹ từ danh sách"
                )
                
                # Lấy mã số từ tên môi trường đã chọn
                ma_so_moi_truong_me = dict_ten_to_ma.get(moi_truong_me, None)
                
                moi_truong_con = st.selectbox(
                    "Môi trường con *",
                    options=danh_sach_ten_moi_truong,
                    index=0 if len(danh_sach_ten_moi_truong) > 0 else None,
                    help="Chọn môi trường con từ danh sách"
                )
                
                # Lấy mã số từ tên môi trường đã chọn
                ma_so_moi_truong_con = dict_ten_to_ma.get(moi_truong_con, None)
                
                st.markdown("---")
                st.markdown("#### ⏰ Thời gian làm việc cho giống này")
                st.caption("(Vui lòng chọn hoặc nhập tay giờ thực tế - chính xác đến từng phút)")
                
                col_time1, col_time2 = st.columns(2)
                
                with col_time1:
                    gio_bat_dau = st.time_input(
                        "⏰ Giờ bắt đầu *",
                        value=None,
                        help="Chọn hoặc nhập tay giờ bắt đầu (chính xác đến phút). Ví dụ: 08:23",
                        key="gio_bd_time_input",
                        step=60  # Bước nhảy 60 giây = 1 phút
                    )
                
                with col_time2:
                    gio_ket_thuc = st.time_input(
                        "⏰ Giờ kết thúc *",
                        value=None,
                        help="Chọn hoặc nhập tay giờ kết thúc (chính xác đến phút). Ví dụ: 12:47",
                        key="gio_kt_time_input",
                        step=60  # Bước nhảy 60 giây = 1 phút
                    )
                
                # Biến kiểm tra thời gian hợp lệ
                thoi_gian_hop_le = False
                
                # Validation và tính toán
                if gio_bat_dau is not None and gio_ket_thuc is not None:
                    # Kiểm tra giờ kết thúc > giờ bắt đầu
                    if gio_ket_thuc <= gio_bat_dau:
                        st.error("⚠️ Giờ kết thúc phải lớn hơn giờ bắt đầu")
                        thoi_gian_hop_le = False
                    else:
                        # Tính tổng giờ làm chính xác đến từng phút
                        # Chuyển đổi time object sang string để dùng hàm tinh_tong_gio_lam
                        gio_bat_dau_str = gio_bat_dau.strftime("%H:%M")
                        gio_ket_thuc_str = gio_ket_thuc.strftime("%H:%M")
                        tong_gio_temp = tinh_tong_gio_lam(gio_bat_dau_str, gio_ket_thuc_str)
                        
                        if tong_gio_temp > 0:
                            # Tính số phút chính xác
                            tong_phut = int(tong_gio_temp * 60)
                            st.success(f"✅ Thời gian làm việc: **{tong_gio_temp:.2f} giờ** ({tong_phut} phút)")
                            thoi_gian_hop_le = True
                        else:
                            st.error("⚠️ Thời gian làm việc không hợp lệ")
                            thoi_gian_hop_le = False
                            
                elif gio_bat_dau is not None or gio_ket_thuc is not None:
                    # Chỉ nhập 1 trong 2
                    st.warning("⚠️ Vui lòng nhập đầy đủ cả giờ bắt đầu và giờ kết thúc")
                    thoi_gian_hop_le = False
                else:
                    # Chưa nhập gì
                    st.info("💡 Vui lòng chọn hoặc nhập tay thời gian bắt đầu và kết thúc (click vào ô để nhập)")
                    thoi_gian_hop_le = False
                
                # Nếu không hợp lệ, set giá trị mặc định để tránh lỗi (sẽ không cho submit)
                if not thoi_gian_hop_le:
                    gio_bat_dau = datetime.now().time()
                    gio_ket_thuc = datetime.now().time()
                
                st.markdown("---")
                st.markdown("#### 🔬 Nguồn gốc Mô Mẹ")
                
                # Lấy danh sách lô mô soi khả dụng cho giống này
                danh_sach_lo_mo_soi = get_danh_sach_mo_soi_kha_dung(ten_giong)
                
                if len(danh_sach_lo_mo_soi) > 0:
                    # Tạo options cho dropdown
                    lo_options = {}
                    for lo in danh_sach_lo_mo_soi:
                        label = f"{lo['ma_lo_mo_soi']} | {lo['chu_ky_truoc']} | Còn: {lo['so_cum_con_lai']} cụm ({lo['so_cum_con_lai'] // lo['so_cum_moi_tui']} túi x {lo['so_cum_moi_tui']} cụm)"
                        lo_options[label] = lo['ma_lo_mo_soi']
                    
                    # Hiển thị dropdown chọn lô
                    lo_selected_label = st.selectbox(
                        "Chọn lô Mô Soi *",
                        options=list(lo_options.keys()),
                        help="Chọn lô mô soi để lấy mô mẹ. Hệ thống sẽ tự động khấu trừ."
                    )
                    ma_lo_mo_soi = lo_options[lo_selected_label]
                    
                    # Lấy thông tin lô đã chọn
                    lo_info = [lo for lo in danh_sach_lo_mo_soi if lo['ma_lo_mo_soi'] == ma_lo_mo_soi][0]
                    
                    # Hiển thị thông tin lô
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📦 Mã lô", lo_info['ma_lo_mo_soi'])
                    with col2:
                        st.metric("🔄 Chu kỳ trước", lo_info['chu_ky_truoc'])
                    with col3:
                        st.metric("✅ Còn lại", f"{lo_info['so_cum_con_lai']} cụm")
                    with col4:
                        so_tui_toi_da = lo_info['so_cum_con_lai'] // lo_info['so_cum_moi_tui']
                        st.metric("📊 Tối đa", f"~{so_tui_toi_da} túi")
                    
                    st.success(f"✅ Đã chọn lô **{ma_lo_mo_soi}** - Hệ thống sẽ tự động khấu trừ khi lưu nhật ký")
                else:
                    st.error(f"""
                    🚫 **KHÔNG CÓ MÔ SOI CHO GIỐNG: {ten_giong}**
                    
                    **Nguyên nhân:**
                    - Chưa nhập kết quả kiểm tra Mô Soi từ phòng sáng
                    - Mô Soi của giống này đã hết
                    
                    **Hành động:**
                    1. Vào trang "Quản lý Mô Soi"
                    2. Nhập kết quả kiểm tra từ chu kỳ trước
                    3. Quay lại nhập nhật ký cấy
                    
                    ⚠️ **KHÔNG THỂ NHẬP NHẬT KÝ** nếu không có Mô Soi!
                    """)
                    ma_lo_mo_soi = None
                
                st.markdown("---")
                st.markdown("#### 👨‍🌾 Thông tin túi mẹ")
                
                so_tui_me = st.number_input(
                    "Số túi mẹ *",
                    min_value=1,
                    value=1,
                    step=1,
                    help="Số lượng túi mẹ sử dụng từ lô mô soi"
                )
                
                so_cum_tui_me = st.number_input(
                    "Số cụm/túi mẹ *",
                    min_value=1,
                    value=1,
                    step=1,
                    help="Số cụm trên mỗi túi mẹ"
                )
                
                st.markdown("---")
                st.markdown("#### 🌱 Thông tin túi con")
                
                so_tui_con = st.number_input(
                    "Số túi con *",
                    min_value=1,
                    value=1,
                    step=1,
                    help="Số lượng túi con đã cấy"
                )
                
                so_cum_tui_con = st.number_input(
                    "Số cụm/túi con *",
                    min_value=1,
                    value=1,
                    step=1,
                    help="Số cụm trên mỗi túi con"
                )
                
                st.markdown("---")
                st.markdown("#### 📝 Ghi chú")
                ghi_chu = st.text_area(
                    "Ghi chú",
                    placeholder="Nhập ghi chú nếu có...",
                    height=100,
                    help="Thông tin bổ sung"
                )
                
                # Tính toán năng suất
                tong_so_cay_con = so_tui_con * so_cum_tui_con
                
                # Tính tổng giờ làm chính xác
                if thoi_gian_hop_le:
                    tong_gio_lam = tinh_tong_gio_lam(
                        gio_bat_dau.strftime("%H:%M"),
                        gio_ket_thuc.strftime("%H:%M")
                    )
                else:
                    tong_gio_lam = 0
                
                nang_suat = tong_so_cay_con / tong_gio_lam if tong_gio_lam > 0 else 0
                
                st.markdown("---")
                st.markdown("#### 📈 Kết quả tính toán tự động")
                col_metric1, col_metric2, col_metric3 = st.columns(3)
                
                with col_metric1:
                    st.metric("Tổng số cây con", f"{tong_so_cay_con:,}")
                
                with col_metric2:
                    st.metric("Tổng giờ làm", f"{tong_gio_lam:.2f} giờ")
                
                with col_metric3:
                    st.metric("Năng suất", f"{nang_suat:.2f} cây/giờ")
                
                st.markdown("---")
                
                # Nút submit với kiểm tra validation
                if not thoi_gian_hop_le:
                    st.warning("⚠️ Cần nhập đầy đủ thời gian hợp lệ trước khi lưu")
                
                submitted = st.form_submit_button("💾 LƯU DỮ LIỆU", use_container_width=True, type="primary")
                
                if submitted:
                    # Kiểm tra thời gian hợp lệ trước khi lưu
                    if not thoi_gian_hop_le:
                        st.error("❌ Không thể lưu! Vui lòng nhập đầy đủ thông tin thời gian hợp lệ (Giờ bắt đầu và Giờ kết thúc)")
                        st.stop()
                    
                    # Kiểm tra có chọn lô mô soi không
                    if ma_lo_mo_soi is None:
                        st.error(f"""
                        ❌ **KHÔNG THỂ LƯU NHẬT KÝ!**
                        
                        **Lý do:** Không có Mô Soi cho giống **{ten_giong}**
                        
                        **Hành động:**
                        1. Vào trang "Quản lý Mô Soi"
                        2. Nhập kết quả kiểm tra từ chu kỳ trước
                        3. Quay lại nhập nhật ký cấy
                        """)
                        st.stop()
                    
                    # Tính số cụm mô mẹ cần khấu trừ
                    so_cum_mo_me_can_dung = so_tui_me * so_cum_tui_me
                    
                    # Khấu trừ mô soi
                    success, message, so_cum_con_lai_sau_khau_tru = khau_tru_mo_soi(ma_lo_mo_soi, so_cum_mo_me_can_dung)
                    
                    if not success:
                        st.error(f"""
                        ❌ **KHÔNG THỂ KHẤU TRỪ MÔ SOI!**
                        
                        {message}
                        
                        **Hành động:**
                        - Giảm số túi mẹ hoặc số cụm/túi
                        - Hoặc nhập thêm Mô Soi cho giống này
                        """)
                        st.stop()
                    
                    ngay_tao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    conn = sqlite3.connect('data.db')
                    c = conn.cursor()
                    # Kiểm tra mã số môi trường có hợp lệ không
                    if ma_so_moi_truong_me is None or ma_so_moi_truong_con is None:
                        st.error("❌ Môi trường không hợp lệ! Vui lòng kiểm tra lại.")
                    else:
                        # Tạo mã QR duy nhất (dùng timestamp để đảm bảo unique)
                        ma_qr_unique = f"QR_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                        
                        c.execute('''
                            INSERT INTO nhat_ky_cay (
                                ngay_cay, thang, tuan, nhan_vien, ma_nhan_vien, ten_giong, chu_ky, tinh_trang, ma_tinh_trang,
                                box_cay, ma_so_moi_truong_me, ma_so_moi_truong_con,
                                so_tui_me, so_cum_tui_me, so_tui_con, so_cum_tui_con,
                                tong_so_cay_con, gio_bat_dau, gio_ket_thuc, tong_gio_lam, nang_suat, ghi_chu, ma_qr, ma_lo_mo_soi, ngay_tao
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            ngay_cay.strftime("%Y-%m-%d"), thang, tuan,
                            user_info['ten_nhan_vien'], user_info['ma_nhan_vien'],
                            ten_giong, chu_ky, tinh_trang, ma_tinh_trang, box_cay,
                            ma_so_moi_truong_me, ma_so_moi_truong_con,
                            so_tui_me, so_cum_tui_me, so_tui_con, so_cum_tui_con,
                            tong_so_cay_con,
                            gio_bat_dau.strftime("%H:%M"), gio_ket_thuc.strftime("%H:%M"),
                            tong_gio_lam, nang_suat, ghi_chu, ma_qr_unique, ma_lo_mo_soi, ngay_tao
                        ))
                        
                        # Lấy ID vừa tạo
                        id_nhat_ky = c.lastrowid
                        
                        # Xử lý số giàn/kệ - sử dụng giá trị từ form hoặc mặc định
                        if not so_gian_ke.strip():
                            so_gian_ke_value = f"Giàn {box_cay}"
                        else:
                            so_gian_ke_value = so_gian_ke.strip()
                        
                        # Tính tuần xuất cây
                        tuan_xuat, ngay_xuat = tinh_tuan_xuat_cay(ngay_cay, chu_ky)
                        
                        # Tự động tạo bản ghi trong phòng sáng
                        # Phân loại theo mã tình trạng (giờ đã có biến ma_tinh_trang từ form)
                        loai_tinh_trang, mau_sac, icon = phan_loai_tinh_trang(ma_tinh_trang)
                        
                        # Khởi tạo số túi dựa trên tình trạng
                        if tinh_trang == "Sạch":
                            so_tui_sach = so_tui_con
                            so_tui_khuan_nhe = 0
                            so_tui_khuan_nang = 0
                            so_tui_nam = 0
                            so_tui_khuan_moi_truong = 0
                            so_tui_khac = 0
                        else:  # Khuẩn
                            so_tui_sach = 0
                            # Phân loại dựa trên mã
                            if ma_tinh_trang % 10 == 9:  # Mã cuối 9: Hủy
                                so_tui_khuan_nang = so_tui_con
                                so_tui_khuan_nhe = 0
                                so_tui_nam = 0
                                so_tui_khuan_moi_truong = 0
                                so_tui_khac = 0
                            elif ma_tinh_trang % 10 == 5:  # Mã cuối 5: Khuẩn nhẹ
                                so_tui_khuan_nhe = so_tui_con
                                so_tui_khuan_nang = 0
                                so_tui_nam = 0
                                so_tui_khuan_moi_truong = 0
                                so_tui_khac = 0
                            else:  # Các mã khác
                                so_tui_khuan_nhe = so_tui_con
                                so_tui_khuan_nang = 0
                                so_tui_nam = 0
                                so_tui_khuan_moi_truong = 0
                                so_tui_khac = 0
                        
                        # LOGIC MÃ 9: HỦY BỎ - KHÔNG LƯU VÀO PHÒNG SÁNG
                        if loai_tinh_trang == 'huy':
                            # Mã cuối 9: Hủy bỏ, không tạo bản ghi phòng sáng
                            tong_so_tui = 0  # Trừ thẳng khỏi kho
                            tong_so_cay = 0
                            trang_thai_phong_sang = "Đã hủy"
                            ghi_chu_them = f"[HỦY BỎ - Mã {ma_tinh_trang}] " + (ghi_chu if ghi_chu else "")
                        else:
                            # Mã cuối 3 (sạch) hoặc 5 (khuẩn - theo dõi): Lưu vào phòng sáng bình thường
                            tong_so_tui = so_tui_con
                            tong_so_cay = so_tui_sach * so_cum_tui_con  # Chỉ tính cây sạch
                            
                            if loai_tinh_trang == 'khuan':
                                trang_thai_phong_sang = "Đang nuôi - Theo dõi khuẩn"
                                ghi_chu_them = f"[CẢNH BÁO MÃ {ma_tinh_trang} - Khuẩn] " + (ghi_chu if ghi_chu else "")
                            else:
                                trang_thai_phong_sang = "Đang nuôi"
                                ghi_chu_them = ghi_chu
                        
                        c.execute('''
                            INSERT INTO quan_ly_phong_sang (
                                id_nhat_ky_cay, ngay_cay, nhan_vien, ma_nhan_vien, ten_giong, chu_ky,
                                so_gian_ke, trang_thai,
                                so_tui_sach, so_tui_khuan_nhe, so_tui_khuan_nang, so_tui_nam,
                                so_tui_khuan_moi_truong, so_tui_khac,
                                tong_so_tui, tong_so_cay, tuan_xuat_cay, ngay_xuat_cay,
                                ghi_chu, ngay_tao, ngay_cap_nhat
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            id_nhat_ky, ngay_cay.strftime("%Y-%m-%d"),
                            user_info['ten_nhan_vien'], user_info['ma_nhan_vien'],
                            ten_giong, chu_ky, so_gian_ke_value, trang_thai_phong_sang,
                            so_tui_sach, so_tui_khuan_nhe, so_tui_khuan_nang, so_tui_nam,
                            so_tui_khuan_moi_truong, so_tui_khac,
                            tong_so_tui, tong_so_cay, tuan_xuat, ngay_xuat,
                            ghi_chu_them, ngay_tao, ngay_tao
                        ))
                        
                        conn.commit()
                        
                        # ========== KHẤU TRỪ MÔI TRƯỜNG TỰ ĐỘNG (FIFO) ==========
                        # Khấu trừ môi trường con (số lượng = số túi con)
                        success, message, danh_sach_lo = khau_tru_moi_truong_tu_kho(
                            ma_so_moi_truong_con,
                            so_tui_con
                        )
                        
                        if not success:
                            # Nếu không đủ môi trường, rollback và thông báo
                            conn.rollback()
                            conn.close()
                            st.error(f"❌ {message}")
                            st.warning("⚠️ Không thể lưu nhật ký cấy. Vui lòng nhập thêm môi trường vào kho!")
                            st.info("💡 Vào 'Quản lý Kho Môi trường' → 'Nhập kho' để thêm môi trường mới")
                            st.stop()
                        
                        conn.close()
                        
                        # Hiển thị thông tin khấu trừ theo loại tình trạng
                        if loai_tinh_trang == 'huy':
                            st.error(f"""
                            🔴 **ĐÃ LƯU - LÔ BỊ HỦY BỎ!**
                            
                            ⚠️ **Lô này có Mã {ma_tinh_trang_luu} (mã cuối 9) - {tinh_trang}**
                            
                            📋 Trạng thái: **Đã hủy**
                            ❌ **KHÔNG** lưu vào kho Phòng Sáng (trừ thẳng)
                            📊 Tính vào tỷ lệ **THẤT THOÁT**
                            🔬 Đã khấu trừ {so_cum_mo_me_can_dung} cụm từ lô Mô Soi **{ma_lo_mo_soi}**
                            📊 Lô Mô Soi còn lại: **{so_cum_con_lai_sau_khau_tru} cụm**
                            
                            💡 **Lưu ý:** Cần kiểm tra nguyên nhân nhiễm để cải thiện quy trình
                            """)
                        elif loai_tinh_trang == 'khuan':
                            st.warning(f"""
                            ⚠️ **ĐÃ LƯU - LÔ CẦN THEO DÕI!**
                            
                            📋 **Lô này có Mã {ma_tinh_trang_luu} (mã cuối 5) - {tinh_trang}**
                            
                            📦 Đã lưu vào Phòng Sáng với trạng thái: **Theo dõi khuẩn**
                            ✅ Có thể sử dụng làm Mô Mẹ nhưng **cần kiểm tra kỹ**
                            🔬 Đã khấu trừ {so_cum_mo_me_can_dung} cụm từ lô Mô Soi **{ma_lo_mo_soi}**
                            📊 Lô Mô Soi còn lại: **{so_cum_con_lai_sau_khau_tru} cụm**
                            
                            💡 **Khuyến nghị:** Ưu tiên xử lý trước khi lây lan
                            """)
                        else:  # sach
                            st.success(f"""
                            ✅ **LƯU DỮ LIỆU THÀNH CÔNG!**
                            
                            📋 **Lô sạch - Mã {ma_tinh_trang_luu} (mã cuối 3)**
                            
                            📦 Đã tự động tạo bản ghi trong phòng sáng
                            🔬 Đã khấu trừ {so_cum_mo_me_can_dung} cụm từ lô Mô Soi **{ma_lo_mo_soi}**
                            📊 Lô Mô Soi còn lại: **{so_cum_con_lai_sau_khau_tru} cụm**
                            """)
                        
                        # Chi tiết môi trường đã xuất
                        with st.expander("📦 Chi tiết xuất môi trường từ kho (FIFO)"):
                            st.success(message)
                            for lo in danh_sach_lo:
                                st.text(f"• Lô {lo['ma_lo']} (Ngày đổ: {lo['ngay_do']}): -{lo['so_luong_tru']} túi")
                        
                        st.markdown("---")
                        st.markdown("### 🏷️ In tem nhãn")
                        
                        # Tạo dữ liệu tem nhãn
                        label_data = {
                            'id': id_nhat_ky,
                            'ten_giong': ten_giong,
                            'ngay_cay': ngay_cay.strftime("%d/%m/%Y"),
                            'tuan': tuan,
                            'nhan_vien': user_info['ten_nhan_vien'],
                            'ma_nhan_vien': user_info['ma_nhan_vien'],  # Thêm mã nhân viên
                            'chu_ky': chu_ky
                        }
                        
                        # Tự động phát hiện kích thước phù hợp
                        recommended_size = detect_label_size(ten_giong)
                        
                        col_size, col_preview = st.columns([1, 3])
                        
                        with col_size:
                            st.markdown("#### Chọn kích thước tem")
                            
                            # Radio button chọn kích thước
                            size_option = st.radio(
                                "Kích thước:",
                                options=["Tự động", "35x22mm (2 hàng)", "25x15mm (3 hàng)"],
                                index=0,
                                key=f"size_option_{id_nhat_ky}"
                            )
                            
                            # Chuyển đổi lựa chọn
                            if size_option == "Tự động":
                                selected_size = "auto"
                                st.info(f"💡 Gợi ý: {recommended_size}mm")
                            elif size_option == "35x22mm (2 hàng)":
                                selected_size = "35x22"
                            else:
                                selected_size = "25x15"
                            
                            # Thông tin kích thước
                            if selected_size == "auto":
                                display_size = recommended_size
                            else:
                                display_size = selected_size
                            
                            if display_size == "35x22":
                                st.success("✅ Tem lớn (2 hàng)\n- Chữ to, dễ đọc\n- Dùng cho cây xuất khẩu")
                            else:
                                st.success("✅ Tem nhỏ (3 hàng)\n- Tiết kiệm giấy\n- Dùng cho cây thường")
                        
                        with col_preview:
                            st.markdown("#### Preview tem nhãn")
                            
                            # Tạo và hiển thị preview tem
                            label_img = create_label_image(label_data, selected_size)
                            st.image(label_img, caption=f"Tem nhãn lô {id_nhat_ky} ({display_size}mm)", width=400)
                        
                        # Nút tải PDF (full width)
                        pdf_buffer, actual_size = create_label_pdf(label_data, selected_size)
                        st.download_button(
                            label=f"📥 Tải tem nhãn ({actual_size}mm) - PDF",
                            data=pdf_buffer,
                            file_name=f"tem_nhan_lo_{id_nhat_ky}_{actual_size.replace('x', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
        
        # ========== HIỂN THỊ NHẬT KÝ ĐÃ NHẬP HÔM NAY ==========
        st.markdown("---")
        st.markdown("---")
        st.header("📋 Nhật ký đã nhập hôm nay")
        
        conn = sqlite3.connect('data.db')
        
        # Query nhật ký hôm nay của nhân viên (hoặc tất cả nếu admin)
        if is_admin:
            df_today = pd.read_sql_query('''
                SELECT 
                    id, ngay_cay, nhan_vien, ten_giong, chu_ky, tinh_trang,
                    so_tui_me, so_cum_tui_me, so_tui_con, so_cum_tui_con,
                    tong_so_cay_con, gio_bat_dau, gio_ket_thuc, tong_gio_lam,
                    nang_suat, ghi_chu, box_cay,
                    ma_so_moi_truong_me, ma_so_moi_truong_con
                FROM nhat_ky_cay
                WHERE DATE(ngay_cay) = DATE('now')
                ORDER BY ngay_tao DESC
                LIMIT 20
            ''', conn)
        else:
            df_today = pd.read_sql_query('''
                SELECT 
                    id, ngay_cay, nhan_vien, ten_giong, chu_ky, tinh_trang,
                    so_tui_me, so_cum_tui_me, so_tui_con, so_cum_tui_con,
                    tong_so_cay_con, gio_bat_dau, gio_ket_thuc, tong_gio_lam,
                    nang_suat, ghi_chu, box_cay,
                    ma_so_moi_truong_me, ma_so_moi_truong_con
                FROM nhat_ky_cay
                WHERE DATE(ngay_cay) = DATE('now')
                  AND ma_nhan_vien = ?
                ORDER BY ngay_tao DESC
                LIMIT 20
            ''', conn, params=(user_info['ma_nhan_vien'],))
        
        conn.close()
        
        if len(df_today) > 0:
            st.info(f"📊 Hiển thị **{len(df_today)}** bản ghi gần nhất hôm nay")
            
            # Hiển thị từng bản ghi với form chỉnh sửa
            for idx, row in df_today.iterrows():
                with st.expander(f"🌱 Lô #{row['id']} - {row['ten_giong']} - {row['nhan_vien']} - {row['gio_bat_dau']}"):
                    # Hiển thị thông tin hiện tại
                    col_info, col_action = st.columns([3, 1])
                    
                    with col_info:
                        st.markdown(f"""
                        **Thông tin cơ bản:**
                        - 🌿 **Giống**: {row['ten_giong']} | **Chu kỳ**: {row['chu_ky']} | **Tình trạng**: {row['tinh_trang']}
                        - 📦 **Box**: {row['box_cay']} | **Giờ**: {row['gio_bat_dau']} - {row['gio_ket_thuc']} ({row['tong_gio_lam']:.2f}h)
                        - 👨‍🌾 **Túi mẹ**: {row['so_tui_me']} x {row['so_cum_tui_me']} cụm
                        - 🌱 **Túi con**: {row['so_tui_con']} x {row['so_cum_tui_con']} cụm = **{row['tong_so_cay_con']} cây**
                        - 📈 **Năng suất**: {row['nang_suat']:.2f} cây/giờ
                        - 📝 **Ghi chú**: {row['ghi_chu'] if row['ghi_chu'] else '_Không có_'}
                        """)
                    
                    with col_action:
                        # Kiểm tra quyền sửa
                        ngay_cay_record = pd.to_datetime(row['ngay_cay']).date()
                        ngay_hom_nay = date.today()
                        
                        # Admin: Sửa được mọi lúc
                        # Nhân viên: Chỉ sửa được nhật ký HÔM NAY
                        co_the_sua = is_admin or (ngay_cay_record == ngay_hom_nay)
                        
                        if co_the_sua:
                            if st.button("✏️ Sửa", key=f"edit_{row['id']}", use_container_width=True):
                                st.session_state[f'editing_{row["id"]}'] = True
                                st.rerun()
                        else:
                            st.warning("""
                            🔒 **Không thể sửa**
                            
                            Nhật ký ngày cũ
                            
                            → Liên hệ Admin
                            """)
                    
                    # Form chỉnh sửa (chỉ hiển thị khi click "Sửa")
                    if st.session_state.get(f'editing_{row["id"]}', False):
                        st.markdown("---")
                        st.markdown("### ✏️ Chỉnh sửa thông tin")
                        
                        with st.form(f"form_edit_{row['id']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                edit_ten_giong = st.selectbox(
                                    "Tên giống",
                                    options=danh_sach_ten_giong,
                                    index=danh_sach_ten_giong.index(row['ten_giong']) if row['ten_giong'] in danh_sach_ten_giong else 0,
                                    key=f"edit_giong_{row['id']}"
                                )
                                
                                edit_chu_ky = st.selectbox(
                                    "Chu kỳ",
                                    options=danh_sach_chu_ky,
                                    index=danh_sach_chu_ky.index(row['chu_ky']) if row['chu_ky'] in danh_sach_chu_ky else 0,
                                    key=f"edit_chu_ky_{row['id']}"
                                )
                                
                                edit_tinh_trang = st.selectbox(
                                    "Tình trạng",
                                    options=danh_sach_tinh_trang,
                                    index=danh_sach_tinh_trang.index(row['tinh_trang']) if row['tinh_trang'] in danh_sach_tinh_trang else 0,
                                    key=f"edit_tinh_trang_{row['id']}"
                                )
                            
                            with col2:
                                edit_so_tui_con = st.number_input(
                                    "Số túi con",
                                    min_value=1,
                                    value=int(row['so_tui_con']),
                                    key=f"edit_tui_con_{row['id']}"
                                )
                                
                                edit_so_cum_tui_con = st.number_input(
                                    "Số cụm/túi con",
                                    min_value=1,
                                    value=int(row['so_cum_tui_con']),
                                    key=f"edit_cum_con_{row['id']}"
                                )
                                
                                edit_ghi_chu = st.text_area(
                                    "Ghi chú",
                                    value=row['ghi_chu'] if row['ghi_chu'] else "",
                                    key=f"edit_ghi_chu_{row['id']}",
                                    height=80
                                )
                            
                            col_submit, col_cancel = st.columns(2)
                            
                            with col_submit:
                                submitted_edit = st.form_submit_button("💾 Lưu thay đổi", use_container_width=True, type="primary")
                            
                            with col_cancel:
                                cancelled = st.form_submit_button("❌ Hủy", use_container_width=True)
                            
                            if submitted_edit:
                                # Tính lại giá trị
                                edit_tong_cay = edit_so_tui_con * edit_so_cum_tui_con
                                edit_nang_suat = edit_tong_cay / row['tong_gio_lam'] if row['tong_gio_lam'] > 0 else 0
                                
                                # Cập nhật database
                                conn = sqlite3.connect('data.db')
                                c = conn.cursor()
                                c.execute('''
                                    UPDATE nhat_ky_cay
                                    SET ten_giong = ?, chu_ky = ?, tinh_trang = ?,
                                        so_tui_con = ?, so_cum_tui_con = ?,
                                        tong_so_cay_con = ?, nang_suat = ?, ghi_chu = ?
                                    WHERE id = ?
                                ''', (
                                    edit_ten_giong, edit_chu_ky, edit_tinh_trang,
                                    edit_so_tui_con, edit_so_cum_tui_con,
                                    edit_tong_cay, edit_nang_suat, edit_ghi_chu,
                                    row['id']
                                ))
                                
                                # Cập nhật phòng sáng tương ứng
                                c.execute('''
                                    UPDATE quan_ly_phong_sang
                                    SET ten_giong = ?, chu_ky = ?
                                    WHERE id_nhat_ky_cay = ?
                                ''', (edit_ten_giong, edit_chu_ky, row['id']))
                                
                                conn.commit()
                                conn.close()
                                
                                # Xóa trạng thái editing
                                st.session_state[f'editing_{row["id"]}'] = False
                                st.success("✅ Đã cập nhật thành công!")
                                st.rerun()
                            
                            if cancelled:
                                st.session_state[f'editing_{row["id"]}'] = False
                                st.rerun()
        else:
            st.info("ℹ️ Chưa có nhật ký nào hôm nay. Hãy bắt đầu nhập liệu!")
    
    # ========== TRANG IN TEM NHÃN (CHỈ ADMIN) ==========
    elif menu == "In tem nhãn" and is_admin:
        st.header("🏷️ In Tem Nhãn")
        st.markdown("---")
        
        st.info("💡 Chọn lô cấy để xem preview và in tem nhãn với kích thước phù hợp")
        
        # Kết nối database và lấy dữ liệu
        conn = sqlite3.connect('data.db')
        
        if is_admin:
            query = 'SELECT * FROM nhat_ky_cay ORDER BY ngay_cay DESC, id DESC'
            df = pd.read_sql_query(query, conn)
        else:
            query = 'SELECT * FROM nhat_ky_cay WHERE ma_nhan_vien = ? ORDER BY ngay_cay DESC, id DESC'
            df = pd.read_sql_query(query, conn, params=(user_info['ma_nhan_vien'],))
        
        conn.close()
        
        if len(df) > 0:
            df['ngay_cay'] = pd.to_datetime(df['ngay_cay'])
            
            # ========== BỘ LỌC ==========
            st.subheader("🔍 Bộ lọc dữ liệu")
            
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                ngay_bat_dau_label = st.date_input(
                    "📅 Từ ngày",
                    value=df['ngay_cay'].min().date() if len(df) > 0 else date.today(),
                    key="ngay_bd_label"
                )
                ngay_ket_thuc_label = st.date_input(
                    "📅 Đến ngày",
                    value=df['ngay_cay'].max().date() if len(df) > 0 else date.today(),
                    key="ngay_kt_label"
                )
            
            with col_filter2:
                danh_sach_giong_label = ["Tất cả"] + sorted(df['ten_giong'].unique().tolist())
                giong_filter_label = st.selectbox(
                    "🌿 Lọc theo giống",
                    options=danh_sach_giong_label,
                    index=0,
                    key="filter_giong_label"
                )
            
            with col_filter3:
                if is_admin:
                    danh_sach_nv_label = ["Tất cả"] + sorted(df['nhan_vien'].unique().tolist())
                    nhan_vien_filter_label = st.selectbox(
                        "👤 Lọc theo nhân viên",
                        options=danh_sach_nv_label,
                        index=0,
                        key="filter_nv_label"
                    )
                else:
                    st.info(f"👤 Nhân viên: {user_info['ten_nhan_vien']}")
                    nhan_vien_filter_label = user_info['ten_nhan_vien']
            
            # Áp dụng bộ lọc
            df_filtered_label = df.copy()
            df_filtered_label = df_filtered_label[
                (df_filtered_label['ngay_cay'].dt.date >= ngay_bat_dau_label) & 
                (df_filtered_label['ngay_cay'].dt.date <= ngay_ket_thuc_label)
            ]
            
            if giong_filter_label != "Tất cả":
                df_filtered_label = df_filtered_label[df_filtered_label['ten_giong'] == giong_filter_label]
            
            if is_admin and nhan_vien_filter_label != "Tất cả":
                df_filtered_label = df_filtered_label[df_filtered_label['nhan_vien'] == nhan_vien_filter_label]
            
            st.markdown("---")
            
            if len(df_filtered_label) > 0:
                # Hiển thị số lượng lô
                st.success(f"📦 Tìm thấy **{len(df_filtered_label)} lô** phù hợp với bộ lọc")
                
                st.markdown("---")
                
                # ========== CHỌN LÔ VÀ IN TEM ==========
                st.subheader("📋 Chọn lô và xem preview tem")
                
                # Dropdown để chọn lô
                df_for_label = df_filtered_label[['id', 'ten_giong', 'ngay_cay', 'tuan', 'nhan_vien', 'ma_nhan_vien', 'chu_ky']].copy()
                df_for_label['label_text'] = df_for_label.apply(
                    lambda row: f"ID {row['id']} - {row['ten_giong']} - {row['ngay_cay'].strftime('%d/%m/%Y')} - {row['nhan_vien']}", 
                    axis=1
                )
                
                col_select_label, col_size_label = st.columns([2, 1])
                
                with col_select_label:
                    selected_label = st.selectbox(
                        "Chọn lô cần in tem",
                        options=df_for_label['label_text'].tolist(),
                        key="select_label_main"
                    )
                
                if selected_label:
                    # Lấy thông tin lô đã chọn
                    selected_id = int(selected_label.split(' - ')[0].replace('ID ', ''))
                    selected_row = df_for_label[df_for_label['id'] == selected_id].iloc[0]
                    
                    # Tạo dữ liệu tem
                    label_data = {
                        'id': selected_row['id'],
                        'ten_giong': selected_row['ten_giong'],
                        'ngay_cay': selected_row['ngay_cay'].strftime('%d/%m/%Y'),
                        'tuan': selected_row['tuan'],
                        'nhan_vien': selected_row['nhan_vien'],
                        'ma_nhan_vien': selected_row['ma_nhan_vien'],
                        'chu_ky': selected_row['chu_ky']
                    }
                    
                    # Tự động phát hiện kích thước
                    recommended_size = detect_label_size(selected_row['ten_giong'])
                    
                    with col_size_label:
                        st.markdown("#### Kích thước tem")
                        
                        # Radio button chọn kích thước
                        size_option_main = st.radio(
                            "Chọn:",
                            options=["Tự động", "35x22mm (Lớn)", "25x15mm (Nhỏ)"],
                            index=0,
                            key="size_option_main"
                        )
                        
                        if size_option_main == "Tự động":
                            selected_size = "auto"
                            st.caption(f"💡 Gợi ý: {recommended_size}")
                        elif size_option_main == "35x22mm (Lớn)":
                            selected_size = "35x22"
                        else:
                            selected_size = "25x15"
                    
                    st.markdown("---")
                    
                    # Hiển thị thông tin lô
                    col_info_label, col_preview_label = st.columns([1, 2])
                    
                    with col_info_label:
                        st.markdown("#### 📄 Thông tin lô")
                        st.write(f"**ID:** {selected_row['id']}")
                        st.write(f"**Tên giống:** {selected_row['ten_giong']}")
                        st.write(f"**Ngày cấy:** {selected_row['ngay_cay'].strftime('%d/%m/%Y')}")
                        st.write(f"**Tuần:** {selected_row['tuan']}")
                        st.write(f"**Nhân viên:** {selected_row['nhan_vien']}")
                        st.write(f"**Mã NV:** {selected_row['ma_nhan_vien']}")
                        st.write(f"**Chu kỳ:** {selected_row['chu_ky']}")
                        
                        st.markdown("---")
                        
                        # Xác định kích thước hiển thị
                        if selected_size == "auto":
                            display_size = recommended_size
                        else:
                            display_size = selected_size
                        
                        if display_size == "35x22":
                            st.success("✅ **Tem lớn (35×22mm)**\n- 2 hàng nhãn\n- Chữ to, QR lớn\n- Dùng cho cây xuất khẩu")
                        else:
                            st.info("✅ **Tem nhỏ (25×15mm)**\n- 3 hàng nhãn\n- Tiết kiệm giấy\n- QR tối ưu 85%")
                        
                        st.markdown("---")
                        
                        # Hiển thị QR code riêng
                        st.markdown("#### 📱 Mã QR")
                        qr_img, qr_url = generate_qr_code(selected_row['id'])
                        st.image(qr_img, caption="Quét để truy cập lô", width=180)
                        st.caption(f"**URL:** `{qr_url}`")
                    
                    with col_preview_label:
                        st.markdown("#### 🔍 Preview Tem Nhãn")
                        
                        # Tạo và hiển thị preview tem
                        label_img = create_label_image(label_data, selected_size)
                        st.image(label_img, caption=f"Tem nhãn lô {selected_row['id']} ({display_size}mm)", use_column_width=True)
                        
                        st.markdown("---")
                        
                        # Nút tải PDF (full width)
                        pdf_buffer, actual_size = create_label_pdf(label_data, selected_size)
                        st.download_button(
                            label=f"📥 TẢI TEM NHÃN ({actual_size}mm) - PDF",
                            data=pdf_buffer,
                            file_name=f"tem_nhan_lo_{selected_row['id']}_{actual_size.replace('x', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary",
                            key="download_label_main"
                        )
                        
                        st.caption("💡 Mở file PDF và in bằng máy in tem nhiệt")
            else:
                st.warning("⚠️ Không có lô nào phù hợp với bộ lọc đã chọn.")
        else:
            st.info("ℹ️ Chưa có dữ liệu. Vui lòng nhập liệu ở trang 'Nhập liệu' trước.")
    
    # ========== TRANG QUẢN LÝ & PHÂN TÍCH NHIỄM (CHỈ ADMIN) ==========
    elif menu == "Quản lý & Phân tích Nhiễm" and is_admin:
        st.header("🔬 Quản lý & Phân tích Nhiễm")
        st.markdown("**Phân tích chuyên sâu tỷ lệ nhiễm theo nhân viên, giống cây và thời gian**")
        st.markdown("---")
        
        conn = sqlite3.connect('data.db')
        
        # ========== BỘ LỌC DỮ LIỆU ==========
        st.subheader("🔍 Bộ lọc dữ liệu")
        
        col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
        
        with col_filter1:
            # Lọc theo nhân viên
            df_nhan_vien = pd.read_sql_query('SELECT DISTINCT ma_nhan_vien, ten_nhan_vien FROM tai_khoan ORDER BY ten_nhan_vien', conn)
            nhan_vien_options = ['Tất cả'] + [f"{row['ten_nhan_vien']} ({row['ma_nhan_vien']})" for _, row in df_nhan_vien.iterrows()]
            nhan_vien_filter = st.selectbox("Nhân viên", options=nhan_vien_options)
            
            if nhan_vien_filter != 'Tất cả':
                ma_nv_filter = nhan_vien_filter.split('(')[1].strip(')')
            else:
                ma_nv_filter = None
        
        with col_filter2:
            # Lọc theo giống
            df_giong = pd.read_sql_query('SELECT DISTINCT ten_giong FROM danh_muc_ten_giong ORDER BY ten_giong', conn)
            giong_options = ['Tất cả'] + df_giong['ten_giong'].tolist()
            giong_filter = st.selectbox("Giống cây", options=giong_options)
        
        with col_filter3:
            # Lọc theo loại thời gian
            loai_thoi_gian = st.selectbox(
                "Lọc theo",
                options=["Khoảng ngày", "Tuần cấy", "Tháng/Năm"]
            )
        
        with col_filter4:
            # Tùy chọn thời gian
            if loai_thoi_gian == "Khoảng ngày":
                ngay_bd = st.date_input("Từ ngày", value=date.today() - timedelta(days=30))
                ngay_kt = st.date_input("Đến ngày", value=date.today())
                where_time = f"ngay_cay BETWEEN '{ngay_bd.strftime('%Y-%m-%d')}' AND '{ngay_kt.strftime('%Y-%m-%d')}'"
            elif loai_thoi_gian == "Tuần cấy":
                tuan_filter = st.number_input("Tuần", min_value=1, max_value=53, value=date.today().isocalendar()[1])
                where_time = f"tuan = {tuan_filter}"
            else:  # Tháng/Năm
                thang_filter = st.selectbox("Tháng", options=list(range(1, 13)), index=date.today().month - 1)
                nam_filter = st.number_input("Năm", min_value=2020, max_value=2030, value=date.today().year)
                where_time = f"thang = {thang_filter} AND strftime('%Y', ngay_cay) = '{nam_filter}'"
        
        # Build WHERE clause
        where_clauses = [where_time]
        if ma_nv_filter:
            where_clauses.append(f"nhat_ky_cay.ma_nhan_vien = '{ma_nv_filter}'")
        if giong_filter != 'Tất cả':
            where_clauses.append(f"nhat_ky_cay.ten_giong = '{giong_filter}'")
        
        where_sql = " AND ".join(where_clauses)
        
        st.markdown("---")
        
        # ========== TÍNH TOÁN TỶ LỆ SẠCH ==========
        st.subheader("📊 Tổng hợp Tỷ lệ Sạch")
        
        # Query dữ liệu nhật ký cấy
        query_nhat_ky = f'''
            SELECT 
                nhat_ky_cay.ma_nhan_vien,
                nhat_ky_cay.nhan_vien,
                nhat_ky_cay.ten_giong,
                nhat_ky_cay.tinh_trang,
                nhat_ky_cay.so_tui_con,
                nhat_ky_cay.id
            FROM nhat_ky_cay
            WHERE {where_sql}
        '''
        
        df_nhat_ky = pd.read_sql_query(query_nhat_ky, conn)
        
        if len(df_nhat_ky) > 0:
            # Phân loại theo mã tình trạng
            df_nhat_ky['ma_tinh_trang'] = df_nhat_ky['tinh_trang'].apply(lambda x: get_ma_tinh_trang(x))
            df_nhat_ky['loai_tinh_trang'] = df_nhat_ky['ma_tinh_trang'].apply(
                lambda x: phan_loai_tinh_trang(x)[0] if x else 'unknown'
            )
            
            # Tính toán theo nhân viên
            summary_data = []
            
            for (ma_nv, ten_nv), group in df_nhat_ky.groupby(['ma_nhan_vien', 'nhan_vien']):
                tong_tui = group['so_tui_con'].sum()
                
                # Phân loại
                tui_sach = group[group['loai_tinh_trang'] == 'sach']['so_tui_con'].sum()
                tui_khuan = group[group['loai_tinh_trang'] == 'khuan']['so_tui_con'].sum()
                tui_huy = group[group['loai_tinh_trang'] == 'huy']['so_tui_con'].sum()
                
                # Tính tỷ lệ
                ty_le_sach = (tui_sach / tong_tui * 100) if tong_tui > 0 else 0
                ty_le_khuan = (tui_khuan / tong_tui * 100) if tong_tui > 0 else 0
                ty_le_huy = (tui_huy / tong_tui * 100) if tong_tui > 0 else 0
                
                summary_data.append({
                    'Mã NV': ma_nv,
                    'Nhân viên': ten_nv,
                    'Tổng túi làm': tong_tui,
                    'Túi sạch (Mã 3)': tui_sach,
                    'Túi khuẩn (Mã 5)': tui_khuan,
                    'Túi hủy (Mã 9)': tui_huy,
                    'Tỷ lệ sạch %': round(ty_le_sach, 1),
                    'Tỷ lệ khuẩn %': round(ty_le_khuan, 1),
                    'Tỷ lệ hủy %': round(ty_le_huy, 1)
                })
            
            df_summary = pd.DataFrame(summary_data)
            
            # Metrics tổng quan
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Tổng túi", f"{df_summary['Tổng túi làm'].sum():,}")
            with col2:
                ty_le_sach_tb = (df_summary['Túi sạch (Mã 3)'].sum() / df_summary['Tổng túi làm'].sum() * 100) if df_summary['Tổng túi làm'].sum() > 0 else 0
                st.metric("Tỷ lệ sạch TB", f"{ty_le_sach_tb:.1f}%")
            with col3:
                ty_le_khuan_tb = (df_summary['Túi khuẩn (Mã 5)'].sum() / df_summary['Tổng túi làm'].sum() * 100) if df_summary['Tổng túi làm'].sum() > 0 else 0
                st.metric("Tỷ lệ khuẩn TB", f"{ty_le_khuan_tb:.1f}%")
            with col4:
                ty_le_huy_tb = (df_summary['Túi hủy (Mã 9)'].sum() / df_summary['Tổng túi làm'].sum() * 100) if df_summary['Tổng túi làm'].sum() > 0 else 0
                st.metric("Tỷ lệ hủy TB", f"{ty_le_huy_tb:.1f}%")
            
            st.markdown("---")
            
            # Bảng chi tiết với highlight
            st.markdown("#### 📋 Bảng chi tiết theo nhân viên")
            
            def highlight_ty_le(row):
                styles = [''] * len(row)
                # Highlight tỷ lệ hủy > 5%
                if row['Tỷ lệ hủy %'] > 5:
                    styles[-1] = 'background-color: #f8d7da; font-weight: bold; color: #721c24'
                # Highlight tỷ lệ sạch < 85%
                if row['Tỷ lệ sạch %'] < 85:
                    styles[-3] = 'background-color: #fff3cd; font-weight: bold'
                # Highlight tỷ lệ sạch >= 95%
                elif row['Tỷ lệ sạch %'] >= 95:
                    styles[-3] = 'background-color: #d4edda; font-weight: bold; color: #155724'
                return styles
            
            styled_df = df_summary.style.apply(highlight_ty_le, axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # Chú thích
            st.info("""
            **Chú thích màu sắc:**
            - 🟢 **Xanh:** Tỷ lệ sạch ≥ 95% (Xuất sắc)
            - 🟡 **Vàng:** Tỷ lệ sạch < 85% (Cần cải thiện)
            - 🔴 **Đỏ:** Tỷ lệ hủy > 5% (Cảnh báo)
            """)
            
            st.markdown("---")
            
            # ========== BIỂU ĐỒ SO SÁNH ==========
            st.subheader("📈 Biểu đồ So sánh")
            
            tab1, tab2, tab3 = st.tabs(["So sánh Nhân viên", "So sánh Giống cây", "Phân tích Nguyên nhân"])
            
            # Tab 1: So sánh nhân viên
            with tab1:
                import plotly.graph_objects as go
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Sạch (Mã 3)',
                    x=df_summary['Nhân viên'],
                    y=df_summary['Tỷ lệ sạch %'],
                    marker_color='#28a745'
                ))
                
                fig.add_trace(go.Bar(
                    name='Khuẩn (Mã 5)',
                    x=df_summary['Nhân viên'],
                    y=df_summary['Tỷ lệ khuẩn %'],
                    marker_color='#ff8c00'
                ))
                
                fig.add_trace(go.Bar(
                    name='Hủy (Mã 9)',
                    x=df_summary['Nhân viên'],
                    y=df_summary['Tỷ lệ hủy %'],
                    marker_color='#8b0000'
                ))
                
                fig.update_layout(
                    title="Tỷ lệ nhiễm theo Nhân viên",
                    xaxis_title="Nhân viên",
                    yaxis_title="Tỷ lệ (%)",
                    barmode='group',
                    height=500
                )
                
                # Thêm đường cảnh báo 5%
                fig.add_hline(y=5, line_dash="dash", line_color="red", 
                             annotation_text="Ngưỡng cảnh báo 5%")
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Tab 2: So sánh giống cây
            with tab2:
                # Tính toán theo giống
                summary_giong = []
                
                for giong, group in df_nhat_ky.groupby('ten_giong'):
                    tong_tui = group['so_tui_con'].sum()
                    tui_sach = group[group['loai_tinh_trang'] == 'sach']['so_tui_con'].sum()
                    tui_khuan = group[group['loai_tinh_trang'] == 'khuan']['so_tui_con'].sum()
                    tui_huy = group[group['loai_tinh_trang'] == 'huy']['so_tui_con'].sum()
                    
                    ty_le_sach = (tui_sach / tong_tui * 100) if tong_tui > 0 else 0
                    ty_le_khuan = (tui_khuan / tong_tui * 100) if tong_tui > 0 else 0
                    ty_le_huy = (tui_huy / tong_tui * 100) if tong_tui > 0 else 0
                    
                    summary_giong.append({
                        'Giống': giong,
                        'Tổng túi': tong_tui,
                        'Tỷ lệ sạch %': round(ty_le_sach, 1),
                        'Tỷ lệ khuẩn %': round(ty_le_khuan, 1),
                        'Tỷ lệ hủy %': round(ty_le_huy, 1)
                    })
                
                df_giong_summary = pd.DataFrame(summary_giong)
                
                fig2 = go.Figure()
                
                fig2.add_trace(go.Bar(
                    name='Sạch (Mã 3)',
                    x=df_giong_summary['Giống'],
                    y=df_giong_summary['Tỷ lệ sạch %'],
                    marker_color='#28a745'
                ))
                
                fig2.add_trace(go.Bar(
                    name='Khuẩn (Mã 5)',
                    x=df_giong_summary['Giống'],
                    y=df_giong_summary['Tỷ lệ khuẩn %'],
                    marker_color='#ff8c00'
                ))
                
                fig2.add_trace(go.Bar(
                    name='Hủy (Mã 9)',
                    x=df_giong_summary['Giống'],
                    y=df_giong_summary['Tỷ lệ hủy %'],
                    marker_color='#8b0000'
                ))
                
                fig2.update_layout(
                    title="Tỷ lệ nhiễm theo Giống cây",
                    xaxis_title="Giống cây",
                    yaxis_title="Tỷ lệ (%)",
                    barmode='group',
                    height=500
                )
                
                fig2.add_hline(y=5, line_dash="dash", line_color="red",
                              annotation_text="Ngưỡng cảnh báo 5%")
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Bảng chi tiết giống
                st.markdown("#### Chi tiết theo giống")
                st.dataframe(df_giong_summary, use_container_width=True, hide_index=True)
            
            # Tab 3: Phân tích nguyên nhân
            with tab3:
                st.markdown("#### 🔍 Phân tích Nguyên nhân Nhiễm")
                
                # Biểu đồ tròn tổng thể
                col1, col2 = st.columns(2)
                
                with col1:
                    tong_sach = df_summary['Túi sạch (Mã 3)'].sum()
                    tong_khuan = df_summary['Túi khuẩn (Mã 5)'].sum()
                    tong_huy = df_summary['Túi hủy (Mã 9)'].sum()
                    
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=['Sạch (Mã 3)', 'Khuẩn (Mã 5)', 'Hủy (Mã 9)'],
                        values=[tong_sach, tong_khuan, tong_huy],
                        marker=dict(colors=['#28a745', '#ff8c00', '#8b0000']),
                        hole=0.3
                    )])
                    
                    fig_pie.update_layout(
                        title="Phân bố Tổng thể",
                        height=400
                    )
                    
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    st.markdown("**Phân tích:**")
                    
                    if ty_le_huy_tb > 10:
                        st.error(f"""
                        🔴 **CẢNH BÁO NGHIÊM TRỌNG!**
                        
                        Tỷ lệ hủy trung bình: **{ty_le_huy_tb:.1f}%**
                        
                        **Vượt quá ngưỡng cho phép (10%)**
                        
                        **Nguyên nhân có thể:**
                        - Môi trường nhiễm khuẩn
                        - Quy trình tiệt trùng kém
                        - Kỹ thuật cấy chưa đạt
                        
                        **Hành động:**
                        - Kiểm tra ngay môi trường
                        - Đào tạo lại nhân viên
                        - Cải thiện quy trình
                        """)
                    elif ty_le_huy_tb > 5:
                        st.warning(f"""
                        ⚠️ **CẦN CHÚ Ý!**
                        
                        Tỷ lệ hủy: **{ty_le_huy_tb:.1f}%**
                        
                        Cần giảm xuống < 5%
                        """)
                    else:
                        st.success(f"""
                        ✅ **TỐT!**
                        
                        Tỷ lệ hủy: **{ty_le_huy_tb:.1f}%**
                        
                        Trong ngưỡng cho phép
                        """)
                    
                    if ty_le_khuan_tb > 10:
                        st.warning(f"""
                        ⚠️ **Tỷ lệ khuẩn nhẹ cao: {ty_le_khuan_tb:.1f}%**
                        
                        Cần theo dõi chặt để tránh lây lan
                        """)
            
            st.markdown("---")
            
            # ========== XUẤT DỮ LIỆU ==========
            st.subheader("📥 Xuất dữ liệu")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Xuất tổng hợp nhân viên
                csv_nv = df_summary.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    "📥 Tải Báo cáo Nhân viên (CSV)",
                    data=csv_nv,
                    file_name=f"bao_cao_nhiem_nhan_vien_{date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Xuất chi tiết giống
                if len(df_giong_summary) > 0:
                    csv_giong = df_giong_summary.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        "📥 Tải Báo cáo Giống cây (CSV)",
                        data=csv_giong,
                        file_name=f"bao_cao_nhiem_giong_{date.today().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
        else:
            st.info("ℹ️ Không có dữ liệu phù hợp với bộ lọc đã chọn.")
        
        conn.close()
    
    # ========== TRANG BÁO CÁO NĂNG SUẤT (CHỈ ADMIN) ==========
    elif menu == "Báo cáo Năng suất" and is_admin:
        st.header("📊 Báo cáo Năng suất")
        st.markdown("---")
        
        # Kết nối database và lấy dữ liệu
        conn = sqlite3.connect('data.db')
        
        if is_admin:
            # Admin xem tất cả
            query = 'SELECT * FROM nhat_ky_cay ORDER BY ngay_cay DESC, id DESC'
        else:
            # Nhân viên chỉ xem dữ liệu của mình
            query = 'SELECT * FROM nhat_ky_cay WHERE ma_nhan_vien = ? ORDER BY ngay_cay DESC, id DESC'
        
        if is_admin:
            df = pd.read_sql_query(query, conn)
        else:
            df = pd.read_sql_query(query, conn, params=(user_info['ma_nhan_vien'],))
        
        conn.close()
        
        if len(df) > 0:
            df['ngay_cay'] = pd.to_datetime(df['ngay_cay'])
            
            # ========== BỘ LỌC ==========
            st.subheader("🔍 Bộ lọc dữ liệu")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                ngay_bat_dau = st.date_input(
                    "📅 Từ ngày",
                    value=df['ngay_cay'].min().date() if len(df) > 0 else date.today(),
                    key="ngay_bd"
                )
                ngay_ket_thuc = st.date_input(
                    "📅 Đến ngày",
                    value=df['ngay_cay'].max().date() if len(df) > 0 else date.today(),
                    key="ngay_kt"
                )
            
            with col2:
                danh_sach_chu_ky_filter = ["Tất cả"] + sorted(df['chu_ky'].unique().tolist())
                chu_ky_filter = st.selectbox(
                    "🔄 Lọc theo chu kỳ",
                    options=danh_sach_chu_ky_filter,
                    index=0,
                    key="filter_chu_ky"
                )
            
            with col3:
                if is_admin:
                    danh_sach_nv_filter = ["Tất cả"] + sorted(df['nhan_vien'].unique().tolist())
                    nhan_vien_filter = st.selectbox(
                        "👤 Lọc theo nhân viên",
                        options=danh_sach_nv_filter,
                        index=0,
                        key="filter_nv"
                    )
                else:
                    st.info(f"👤 Nhân viên: {user_info['ten_nhan_vien']}")
                    nhan_vien_filter = user_info['ten_nhan_vien']
            
            # Áp dụng bộ lọc
            df_filtered = df.copy()
            df_filtered = df_filtered[
                (df_filtered['ngay_cay'].dt.date >= ngay_bat_dau) & 
                (df_filtered['ngay_cay'].dt.date <= ngay_ket_thuc)
            ]
            
            if chu_ky_filter != "Tất cả":
                df_filtered = df_filtered[df_filtered['chu_ky'] == chu_ky_filter]
            
            if is_admin and nhan_vien_filter != "Tất cả":
                df_filtered = df_filtered[df_filtered['nhan_vien'] == nhan_vien_filter]
            
            st.markdown("---")
            
            # ========== THỐNG KÊ TỔNG QUAN ==========
            st.subheader("📈 Thống kê tổng quan")
            
            # Tính tỷ lệ nhiễm (dựa trên số túi con, không phải số box)
            tong_tui_lam = df_filtered['so_tui_con'].sum()
            tong_tui_khuan_nang = df_filtered[df_filtered['tinh_trang'] == 'Khuẩn nặng']['so_tui_con'].sum()
            tong_tui_nam = df_filtered[df_filtered['tinh_trang'] == 'Nấm']['so_tui_con'].sum()
            ty_le_nhiem = ((tong_tui_khuan_nang + tong_tui_nam) / tong_tui_lam * 100) if tong_tui_lam > 0 else 0
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Tổng số cây con", f"{int(df_filtered['tong_so_cay_con'].sum()):,}")
            
            with col2:
                st.metric("Tổng giờ làm", f"{df_filtered['tong_gio_lam'].sum():.2f}")
            
            with col3:
                nang_suat_tb = df_filtered['nang_suat'].mean() if len(df_filtered) > 0 else 0
                st.metric("Năng suất TB", f"{nang_suat_tb:.2f} cây/giờ")
            
            with col4:
                st.metric("Tổng số túi", f"{tong_tui_lam:,}")
            
            with col5:
                # Màu sắc theo tỷ lệ nhiễm
                if ty_le_nhiem < 5:
                    delta_color = "normal"
                elif ty_le_nhiem < 10:
                    delta_color = "off"
                else:
                    delta_color = "inverse"
                st.metric("Tỷ lệ nhiễm", f"{ty_le_nhiem:.2f}%", delta=f"{(int(tong_tui_khuan_nang) + int(tong_tui_nam)):,} túi", delta_color=delta_color)
            
            st.markdown("---")
            
            # ========== BÁO CÁO TỶ LỆ NHIỄM ==========
            st.subheader("📊 Báo cáo Tỷ lệ nhiễm theo Nhân viên")
            
            if len(df_filtered) > 0:
                # Tính tỷ lệ nhiễm cho từng nhân viên (dựa trên số túi con)
                df_ty_le_nhiem = df_filtered.groupby('nhan_vien').agg({
                    'so_tui_con': 'sum'  # Tổng số túi con
                }).reset_index()
                df_ty_le_nhiem.columns = ['Nhân viên', 'Tổng số túi']
                
                # Tính số túi nhiễm (Khuẩn nặng + Nấm) cho mỗi nhân viên
                df_nhiem = df_filtered[df_filtered['tinh_trang'].isin(['Khuẩn nặng', 'Nấm'])].groupby('nhan_vien').agg({
                    'so_tui_con': 'sum'
                }).reset_index()
                df_nhiem.columns = ['Nhân viên', 'Số túi nhiễm']
                
                df_ty_le_nhiem = df_ty_le_nhiem.merge(df_nhiem, on='Nhân viên', how='left')
                df_ty_le_nhiem['Số túi nhiễm'] = df_ty_le_nhiem['Số túi nhiễm'].fillna(0).astype(int)
                df_ty_le_nhiem['Tỷ lệ nhiễm (%)'] = (df_ty_le_nhiem['Số túi nhiễm'] / df_ty_le_nhiem['Tổng số túi'] * 100).round(2)
                df_ty_le_nhiem = df_ty_le_nhiem.sort_values('Tỷ lệ nhiễm (%)', ascending=True)
                
                st.dataframe(
                    df_ty_le_nhiem,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("---")
            
            # ========== BÁO CÁO THEO CHU KỲ ==========
            st.subheader("📊 Báo cáo năng suất theo chu kỳ")
            
            if len(df_filtered) > 0:
                # Nhóm theo chu kỳ
                df_chu_ky = df_filtered.groupby('chu_ky').agg({
                    'tong_so_cay_con': 'sum',
                    'tong_gio_lam': 'sum',
                    'nang_suat': 'mean'
                }).reset_index()
                
                df_chu_ky['nang_suat_tong'] = df_chu_ky['tong_so_cay_con'] / df_chu_ky['tong_gio_lam']
                df_chu_ky.columns = ['Chu kỳ', 'Tổng số cây con', 'Tổng giờ làm', 'Năng suất TB', 'Năng suất tổng']
                df_chu_ky = df_chu_ky.sort_values('Năng suất tổng', ascending=False)
                
                st.dataframe(
                    df_chu_ky,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("---")
                
                # ========== BIỂU ĐỒ (CHỈ ADMIN) ==========
                if is_admin:
                    st.subheader("📊 Dashboard Quản trị - Phân tích Chất lượng")
                    
                    # 1. Biểu đồ cột chồng: Chi tiết các loại nhiễm của từng nhân viên
                    st.markdown("#### 📊 Biểu đồ chi tiết các loại nhiễm theo Nhân viên")
                    
                    # Tính tổng số túi con theo từng loại tình trạng cho mỗi nhân viên
                    df_chi_tiet_nhiem = df_filtered.groupby(['nhan_vien', 'tinh_trang']).agg({
                        'so_tui_con': 'sum'
                    }).reset_index()
                    df_chi_tiet_nhiem.columns = ['nhan_vien', 'tinh_trang', 'Số túi']
                    df_pivot = df_chi_tiet_nhiem.pivot(index='nhan_vien', columns='tinh_trang', values='Số túi').fillna(0)
                    
                    # Sắp xếp theo thứ tự mong muốn
                    tinh_trang_order = ['Sạch', 'Khuẩn nhẹ', 'Khuẩn nặng', 'Nấm', 'Khuẩn môi trường', 'Khác']
                    df_pivot = df_pivot.reindex(columns=[t for t in tinh_trang_order if t in df_pivot.columns], fill_value=0)
                    
                    # Màu sắc
                    colors_map = {
                        'Sạch': '#28a745',  # Xanh lá
                        'Khuẩn nhẹ': '#ffc107',  # Vàng
                        'Khuẩn nặng': '#dc3545',  # Đỏ
                        'Nấm': '#dc3545',  # Đỏ
                        'Khuẩn môi trường': '#ffc107',  # Vàng
                        'Khác': '#6c757d'  # Xám
                    }
                    
                    fig_stacked = go.Figure()
                    for tinh_trang in df_pivot.columns:
                        fig_stacked.add_trace(go.Bar(
                            name=tinh_trang,
                            x=df_pivot.index,
                            y=df_pivot[tinh_trang],
                            marker_color=colors_map.get(tinh_trang, '#6c757d')
                        ))
                    
                    fig_stacked.update_layout(
                        barmode='stack',
                        title='📊 Chi tiết các loại nhiễm của từng nhân viên',
                        xaxis_title='Nhân viên',
                        yaxis_title='Số túi',
                        height=500,
                        xaxis_tickangle=-45,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    
                    st.plotly_chart(fig_stacked, use_container_width=True)
                    
                    st.markdown("---")
                    
                    # 2. Biểu đồ tròn: Phân tích nguyên nhân nhiễm
                    st.markdown("#### 🥧 Phân tích nguyên nhân nhiễm")
                    
                    tong_khuan_nang_nam = df_filtered[df_filtered['tinh_trang'].isin(['Khuẩn nặng', 'Nấm'])]['so_tui_con'].sum()
                    tong_khuan_moi_truong = df_filtered[df_filtered['tinh_trang'] == 'Khuẩn môi trường']['so_tui_con'].sum()
                    tong_khac = df_filtered[df_filtered['tinh_trang'] == 'Khác']['so_tui_con'].sum()
                    tong_sach = df_filtered[df_filtered['tinh_trang'] == 'Sạch']['so_tui_con'].sum()
                    
                    labels_pie = ['Khuẩn nặng + Nấm', 'Khuẩn môi trường', 'Khác', 'Sạch']
                    values_pie = [tong_khuan_nang_nam, tong_khuan_moi_truong, tong_khac, tong_sach]
                    colors_pie = ['#dc3545', '#ffc107', '#6c757d', '#28a745']
                    
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=labels_pie,
                        values=values_pie,
                        marker=dict(colors=colors_pie),
                        hole=0.3
                    )])
                    
                    fig_pie.update_layout(
                        title='🥧 Phân tích nguyên nhân nhiễm',
                        height=500
                    )
                    
                    st.plotly_chart(fig_pie, use_container_width=True)
                    
                    st.markdown("---")
                    
                    # 3. Bảng xếp hạng: Nhân viên cấy sạch nhất
                    st.markdown("#### 🏆 Bảng xếp hạng: Nhân viên cấy sạch nhất")
                    
                    # Tính tỷ lệ nhiễm cho từng nhân viên (đã tính ở trên)
                    df_xep_hang = df_ty_le_nhiem.copy()
                    df_xep_hang['Xếp hạng'] = range(1, len(df_xep_hang) + 1)
                    df_xep_hang = df_xep_hang[['Xếp hạng', 'Nhân viên', 'Tổng số túi', 'Số túi nhiễm', 'Tỷ lệ nhiễm (%)']]
                    
                    # Tô màu theo tỷ lệ nhiễm
                    def highlight_row(row):
                        if row['Tỷ lệ nhiễm (%)'] < 5:
                            return ['background-color: #d4edda'] * len(row)  # Xanh nhạt
                        elif row['Tỷ lệ nhiễm (%)'] < 10:
                            return ['background-color: #fff3cd'] * len(row)  # Vàng nhạt
                        else:
                            return ['background-color: #f8d7da'] * len(row)  # Đỏ nhạt
                    
                    st.dataframe(
                        df_xep_hang.style.apply(highlight_row, axis=1),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    st.markdown("---")
                    
                    # 4. Biểu đồ so sánh năng suất (giữ nguyên)
                    st.markdown("#### 📊 Biểu đồ so sánh năng suất giữa các nhân viên")
                    
                    # Tính năng suất trung bình của mỗi nhân viên
                    df_nhan_vien = df_filtered.groupby('nhan_vien').agg({
                        'tong_so_cay_con': 'sum',
                        'tong_gio_lam': 'sum',
                        'nang_suat': 'mean'
                    }).reset_index()
                    
                    df_nhan_vien['nang_suat_tong'] = df_nhan_vien['tong_so_cay_con'] / df_nhan_vien['tong_gio_lam']
                    df_nhan_vien = df_nhan_vien.sort_values('nang_suat_tong', ascending=False)
                    
                    # Vẽ biểu đồ cột
                    fig = px.bar(
                        df_nhan_vien,
                        x='nhan_vien',
                        y='nang_suat_tong',
                        title='📊 So sánh năng suất giữa các nhân viên (cây/giờ)',
                        labels={'nhan_vien': 'Nhân viên', 'nang_suat_tong': 'Năng suất (cây/giờ)'},
                        color='nang_suat_tong',
                        color_continuous_scale='Greens'
                    )
                    fig.update_layout(
                        xaxis_tickangle=-45,
                        height=500,
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig.update_traces(marker_line_color='#2d5016', marker_line_width=1.5)
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                
                # ========== BẢNG DỮ LIỆU CHI TIẾT ==========
                st.subheader("📋 Bảng dữ liệu chi tiết")
                
                # Join với bảng danh mục môi trường để lấy tên
                conn = sqlite3.connect('data.db')
                df_mt = pd.read_sql_query('SELECT ma_so, ten_moi_truong FROM danh_muc_moi_truong', conn)
                conn.close()
                
                df_display = df_filtered[[
                    'ngay_cay', 'nhan_vien', 'ten_giong', 'chu_ky', 'tinh_trang',
                    'ma_so_moi_truong_me', 'ma_so_moi_truong_con',
                    'tong_so_cay_con', 'tong_gio_lam', 'nang_suat'
                ]].copy()
                
                # Merge để lấy tên môi trường
                df_display = df_display.merge(
                    df_mt, left_on='ma_so_moi_truong_me', right_on='ma_so', how='left'
                ).rename(columns={'ten_moi_truong': 'moi_truong_me'})
                df_display = df_display.merge(
                    df_mt, left_on='ma_so_moi_truong_con', right_on='ma_so', how='left'
                ).rename(columns={'ten_moi_truong': 'moi_truong_con'})
                
                df_display = df_display[[
                    'ngay_cay', 'nhan_vien', 'ten_giong', 'chu_ky', 'tinh_trang',
                    'moi_truong_me', 'moi_truong_con',
                    'tong_so_cay_con', 'tong_gio_lam', 'nang_suat'
                ]]
                
                df_display.columns = [
                    'Ngày cấy', 'Nhân viên', 'Tên giống', 'Chu kỳ', 'Tình trạng',
                    'Môi trường mẹ', 'Môi trường con',
                    'Tổng số cây con', 'Tổng giờ làm', 'Năng suất (cây/giờ)'
                ]
                
                df_display['Ngày cấy'] = df_display['Ngày cấy'].dt.strftime("%d/%m/%Y")
                df_display['Tổng giờ làm'] = df_display['Tổng giờ làm'].round(2)
                df_display['Năng suất (cây/giờ)'] = df_display['Năng suất (cây/giờ)'].round(2)
                
                # Tô màu cột Tình trạng
                def color_tinh_trang(val):
                    if val == 'Sạch':
                        return 'background-color: #d4edda; color: #155724'  # Xanh lá
                    elif val in ['Khuẩn nặng', 'Nấm']:
                        return 'background-color: #f8d7da; color: #721c24'  # Đỏ
                    elif val == 'Khuẩn môi trường':
                        return 'background-color: #fff3cd; color: #856404'  # Vàng
                    elif val == 'Khuẩn nhẹ':
                        return 'background-color: #ffeaa7; color: #856404'  # Vàng nhạt
                    else:
                        return ''
                
                styled_df = df_display.style.applymap(color_tinh_trang, subset=['Tình trạng'])
                
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # ========== IN TEM NHÃN CHO CÁC LÔ ==========
                st.markdown("---")
                st.subheader("🏷️ In tem nhãn")
                st.info("Chọn một lô để xem và in tem nhãn với kích thước phù hợp")
                
                # Dropdown để chọn lô
                df_for_label = df_filtered[['id', 'ten_giong', 'ngay_cay', 'tuan', 'nhan_vien', 'ma_nhan_vien', 'chu_ky']].copy()
                df_for_label['label_text'] = df_for_label.apply(
                    lambda row: f"ID {row['id']} - {row['ten_giong']} - {row['ngay_cay'].strftime('%d/%m/%Y')}", 
                    axis=1
                )
                
                col_select, col_size_choice = st.columns([2, 1])
                
                with col_select:
                    selected_label = st.selectbox(
                        "Chọn lô cần in tem",
                        options=df_for_label['label_text'].tolist(),
                        key="select_label_report"
                    )
                
                if selected_label:
                    # Lấy thông tin lô đã chọn
                    selected_id = int(selected_label.split(' - ')[0].replace('ID ', ''))
                    selected_row = df_for_label[df_for_label['id'] == selected_id].iloc[0]
                    
                    # Tạo dữ liệu tem
                    label_data = {
                        'id': selected_row['id'],
                        'ten_giong': selected_row['ten_giong'],
                        'ngay_cay': selected_row['ngay_cay'].strftime('%d/%m/%Y'),
                        'tuan': selected_row['tuan'],
                        'nhan_vien': selected_row['nhan_vien'],
                        'ma_nhan_vien': selected_row['ma_nhan_vien'],  # Đã có trong df_for_label
                        'chu_ky': selected_row['chu_ky']
                    }
                    
                    # Tự động phát hiện kích thước
                    recommended_size = detect_label_size(selected_row['ten_giong'])
                    
                    with col_size_choice:
                        # Radio button chọn kích thước
                        size_option_report = st.radio(
                            "Kích thước tem:",
                            options=["Tự động", "35x22mm", "25x15mm"],
                            index=0,
                            key="size_option_report"
                        )
                        
                        if size_option_report == "Tự động":
                            selected_size = "auto"
                            st.caption(f"💡 Gợi ý: {recommended_size}")
                        elif size_option_report == "35x22mm":
                            selected_size = "35x22"
                        else:
                            selected_size = "25x15"
                    
                    col_preview, col_qr_info = st.columns([2, 1])
                    
                    with col_preview:
                        # Tạo và hiển thị tem
                        label_img = create_label_image(label_data, selected_size)
                        
                        # Xác định kích thước hiển thị
                        if selected_size == "auto":
                            display_size = recommended_size
                        else:
                            display_size = selected_size
                        
                        st.image(label_img, caption=f"Tem nhãn lô {selected_row['id']} ({display_size}mm)", width=450)
                        
                        # Thông tin kích thước
                        if display_size == "35x22":
                            st.success("✅ **Tem lớn (35×22mm - 2 hàng)**\n- Chữ to, dễ đọc\n- Phù hợp: Cây xuất khẩu, cây rễ")
                        else:
                            st.info("✅ **Tem nhỏ (25×15mm - 3 hàng)**\n- Tiết kiệm giấy\n- Phù hợp: Cây thường")
                    
                    with col_qr_info:
                        st.markdown("#### 📱 Thông tin QR")
                        
                        # Hiển thị QR code riêng
                        qr_img, qr_url = generate_qr_code(selected_row['id'])
                        st.image(qr_img, caption="Mã QR", width=200)
                        st.caption(f"**URL:** {qr_url}")
                        
                        # Nút tải PDF
                        st.markdown("---")
                        pdf_buffer, actual_size = create_label_pdf(label_data, selected_size)
                        st.download_button(
                            label=f"📥 Tải tem ({actual_size}mm)",
                            data=pdf_buffer,
                            file_name=f"tem_nhan_lo_{selected_row['id']}_{actual_size.replace('x', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key="download_label_report"
                        )
                
                # ========== XUẤT EXCEL ==========
                st.markdown("---")
                
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_filtered.to_excel(writer, sheet_name='Báo cáo', index=False)
                
                output.seek(0)
                
                st.download_button(
                    label="📥 Tải về Excel",
                    data=output.getvalue(),
                    file_name=f"Bao_cao_nang_suat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Không có dữ liệu phù hợp với bộ lọc đã chọn.")
        else:
            st.info("ℹ️ Chưa có dữ liệu. Vui lòng nhập liệu ở tab 'Nhập liệu'.")
    
    # ========== TRANG QUẢN LÝ PHÒNG SÁNG (CHỈ ADMIN) ==========
    elif menu == "Quản lý Phòng Sáng" and is_admin:
        st.header("☀️ Quản lý Phòng Sáng")
        st.markdown("---")
        
        # Xử lý khi quét QR code
        if st.session_state.auto_navigate and st.session_state.scan_lo_id:
            st.success(f"✅ Đã quét QR Code! Đang hiển thị lô ID: {st.session_state.scan_lo_id}")
            st.info("💡 Bạn có thể cuộn xuống để cập nhật thông tin lô này.")
            # Reset auto_navigate để không hiển thị thông báo lần sau
            st.session_state.auto_navigate = False
        
        # Lấy dữ liệu phòng sáng
        conn = sqlite3.connect('data.db')
        
        if is_admin:
            query = 'SELECT * FROM quan_ly_phong_sang ORDER BY ngay_cay DESC, id DESC'
            df_ps = pd.read_sql_query(query, conn)
        else:
            query = 'SELECT * FROM quan_ly_phong_sang WHERE ma_nhan_vien = ? ORDER BY ngay_cay DESC, id DESC'
            df_ps = pd.read_sql_query(query, conn, params=(user_info['ma_nhan_vien'],))
        
        conn.close()
        
        if len(df_ps) > 0:
            df_ps['ngay_cay'] = pd.to_datetime(df_ps['ngay_cay'])
            if 'ngay_xuat_cay' in df_ps.columns:
                df_ps['ngay_xuat_cay'] = pd.to_datetime(df_ps['ngay_xuat_cay'], errors='coerce')
            
            # Bộ lọc
            st.subheader("🔍 Bộ lọc dữ liệu")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                ngay_bd_ps = st.date_input(
                    "📅 Từ ngày",
                    value=df_ps['ngay_cay'].min().date() if len(df_ps) > 0 else date.today(),
                    key="ngay_bd_ps"
                )
                ngay_kt_ps = st.date_input(
                    "📅 Đến ngày",
                    value=df_ps['ngay_cay'].max().date() if len(df_ps) > 0 else date.today(),
                    key="ngay_kt_ps"
                )
            
            with col2:
                danh_sach_giong_ps = ["Tất cả"] + sorted(df_ps['ten_giong'].unique().tolist())
                giong_filter_ps = st.selectbox("🌿 Lọc theo giống", options=danh_sach_giong_ps, index=0, key="filter_giong_ps")
            
            with col3:
                danh_sach_trang_thai = ["Tất cả", "Đang nuôi", "Đã xuất", "Hủy"]
                trang_thai_filter = st.selectbox("📊 Lọc theo trạng thái", options=danh_sach_trang_thai, index=0, key="filter_trang_thai")
            
            # Áp dụng bộ lọc
            df_ps_filtered = df_ps.copy()
            df_ps_filtered = df_ps_filtered[
                (df_ps_filtered['ngay_cay'].dt.date >= ngay_bd_ps) & 
                (df_ps_filtered['ngay_cay'].dt.date <= ngay_kt_ps)
            ]
            
            if giong_filter_ps != "Tất cả":
                df_ps_filtered = df_ps_filtered[df_ps_filtered['ten_giong'] == giong_filter_ps]
            
            if trang_thai_filter != "Tất cả":
                df_ps_filtered = df_ps_filtered[df_ps_filtered['trang_thai'] == trang_thai_filter]
            
            st.markdown("---")
            
            # Bảng dữ liệu với khả năng chỉnh sửa
            st.subheader("📋 Danh sách cây trong phòng sáng")
            
            if len(df_ps_filtered) > 0:
                # Hiển thị bảng với các cột tình trạng nằm ngang
                for idx, row in df_ps_filtered.iterrows():
                    # Tính tỷ lệ nhiễm cho lô này
                    tong_tui_lo = row['tong_so_tui']
                    tui_nhiem_lo = row['so_tui_khuan_nang'] + row['so_tui_nam']
                    ty_le_nhiem_lo = (tui_nhiem_lo / tong_tui_lo * 100) if tong_tui_lo > 0 else 0
                    
                    # Xác định màu cảnh báo
                    if ty_le_nhiem_lo > 10:
                        canh_bao_icon = "🔴 CẢNH BÁO"
                        canh_bao_color = "red"
                    elif ty_le_nhiem_lo > 5:
                        canh_bao_icon = "🟡 Chú ý"
                        canh_bao_color = "orange"
                    else:
                        canh_bao_icon = "🟢 Tốt"
                        canh_bao_color = "green"
                    
                    expander_title = f"{canh_bao_icon} | {row['ten_giong']} - {row['so_gian_ke']} | Ngày cấy: {row['ngay_cay'].strftime('%d/%m/%Y') if isinstance(row['ngay_cay'], pd.Timestamp) else row['ngay_cay']} | Tỷ lệ nhiễm: {ty_le_nhiem_lo:.1f}%"
                    
                    # CRITICAL FIX TRIỆT ĐỂ: Kiểm tra lô được quét - đảm bảo 100% boolean
                    is_scanned_batch = False
                    try:
                        if hasattr(st.session_state, 'scan_lo_id') and st.session_state.scan_lo_id is not None:
                            is_scanned_batch = (str(row['id_nhat_ky_cay']) == str(st.session_state.scan_lo_id))
                            # Force boolean
                            is_scanned_batch = True if is_scanned_batch else False
                    except Exception:
                        is_scanned_batch = False
                    
                    # Chắc chắn 100% expanded là boolean (không dùng bool() nữa)
                    expander_is_expanded = True if is_scanned_batch == True else False
                    
                    with st.expander(expander_title, expanded=expander_is_expanded):
                        # Hiển thị cảnh báo nếu tỷ lệ > 10%
                        if ty_le_nhiem_lo > 10:
                            st.error(f"🚨 **CẢNH BÁO ĐỎ RỰC**: Lô này có tỷ lệ nhiễm **{ty_le_nhiem_lo:.2f}%** (> 10%)! Cần kiểm tra ngay!")
                        elif ty_le_nhiem_lo > 5:
                            st.warning(f"⚠️ **Chú ý**: Lô này có tỷ lệ nhiễm **{ty_le_nhiem_lo:.2f}%**. Theo dõi chặt chẽ!")
                        
                        col_info, col_edit = st.columns([2, 1])
                        
                        with col_info:
                            st.markdown(f"**Nhân viên:** {row['nhan_vien']}")
                            st.markdown(f"**Chu kỳ:** {row['chu_ky']}")
                            st.markdown(f"**Trạng thái:** {row['trang_thai']}")
                            if pd.notna(row.get('ngay_xuat_cay')):
                                st.markdown(f"**Dự kiến xuất:** Tuần {row['tuan_xuat_cay']} ({row['ngay_xuat_cay'].strftime('%d/%m/%Y') if isinstance(row['ngay_xuat_cay'], pd.Timestamp) else row['ngay_xuat_cay']})")
                        
                        with col_edit:
                            with st.form(f"form_edit_{row['id']}", clear_on_submit=False):
                                so_gian_ke_new = st.text_input("Số Giàn/Kệ", value=row['so_gian_ke'], key=f"gian_{row['id']}")
                                
                                st.markdown("**Cập nhật số túi theo tình trạng:**")
                                col_tui1, col_tui2 = st.columns(2)
                                
                                with col_tui1:
                                    so_tui_sach = st.number_input("Sạch", min_value=0, value=int(row['so_tui_sach']), key=f"sach_{row['id']}")
                                    so_tui_khuan_nhe = st.number_input("Khuẩn nhẹ", min_value=0, value=int(row['so_tui_khuan_nhe']), key=f"knhe_{row['id']}")
                                    so_tui_khuan_nang = st.number_input("Khuẩn nặng", min_value=0, value=int(row['so_tui_khuan_nang']), key=f"knang_{row['id']}")
                                
                                with col_tui2:
                                    so_tui_nam = st.number_input("Nấm", min_value=0, value=int(row['so_tui_nam']), key=f"nam_{row['id']}")
                                    so_tui_khuan_mt = st.number_input("Khuẩn môi trường", min_value=0, value=int(row['so_tui_khuan_moi_truong']), key=f"kmt_{row['id']}")
                                    so_tui_khac = st.number_input("Khác", min_value=0, value=int(row['so_tui_khac']), key=f"khac_{row['id']}")
                                
                                trang_thai_new = st.selectbox("Trạng thái", ["Đang nuôi", "Đã xuất", "Hủy"], 
                                                             index=["Đang nuôi", "Đã xuất", "Hủy"].index(row['trang_thai']) if row['trang_thai'] in ["Đang nuôi", "Đã xuất", "Hủy"] else 0,
                                                             key=f"trangthai_{row['id']}")
                                
                                # Tính toán tự động
                                tong_so_tui = so_tui_sach + so_tui_khuan_nhe + so_tui_khuan_nang + so_tui_nam + so_tui_khuan_mt + so_tui_khac
                                
                                # Lấy số cụm/túi từ bản ghi gốc
                                conn_temp = sqlite3.connect('data.db')
                                c_temp = conn_temp.cursor()
                                c_temp.execute('SELECT so_cum_tui_con FROM nhat_ky_cay WHERE id = ?', (int(row['id_nhat_ky_cay']),))
                                result = c_temp.fetchone()
                                so_cum_tui_con = result[0] if result else 1
                                conn_temp.close()
                                
                                tong_so_cay = so_tui_sach * so_cum_tui_con
                                
                                st.info(f"📊 Tổng túi: {tong_so_tui} | Tổng cây (sạch): {tong_so_cay}")
                                
                                if st.form_submit_button("💾 Cập nhật", use_container_width=True):
                                    ngay_cap_nhat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    
                                    conn = sqlite3.connect('data.db')
                                    c = conn.cursor()
                                    c.execute('''
                                        UPDATE quan_ly_phong_sang SET
                                            so_gian_ke = ?,
                                            trang_thai = ?,
                                            so_tui_sach = ?,
                                            so_tui_khuan_nhe = ?,
                                            so_tui_khuan_nang = ?,
                                            so_tui_nam = ?,
                                            so_tui_khuan_moi_truong = ?,
                                            so_tui_khac = ?,
                                            tong_so_tui = ?,
                                            tong_so_cay = ?,
                                            ngay_cap_nhat = ?
                                        WHERE id = ?
                                    ''', (
                                        so_gian_ke_new, trang_thai_new,
                                        so_tui_sach, so_tui_khuan_nhe, so_tui_khuan_nang,
                                        so_tui_nam, so_tui_khuan_mt, so_tui_khac,
                                        tong_so_tui, tong_so_cay, ngay_cap_nhat, row['id']
                                    ))
                                    conn.commit()
                                    conn.close()
                                    
                                    st.success("✅ Cập nhật thành công!")
                                    st.rerun()
            else:
                st.warning("⚠️ Không có dữ liệu phù hợp với bộ lọc.")
        else:
            st.info("ℹ️ Chưa có dữ liệu trong phòng sáng. Dữ liệu sẽ tự động được tạo khi bạn nhập liệu ở trang 'Nhập liệu'.")
    
    # ========== TRANG TỔNG HỢP PHÒNG SÁNG (CHỈ ADMIN) ==========
    elif menu == "Tổng hợp Phòng Sáng" and is_admin:
        st.header("📊 Tổng hợp Phòng Sáng")
        st.markdown("---")
        
        conn = sqlite3.connect('data.db')
        df_ps = pd.read_sql_query('SELECT * FROM quan_ly_phong_sang WHERE trang_thai = "Đang nuôi" ORDER BY so_gian_ke, ten_giong', conn)
        conn.close()
        
        if len(df_ps) > 0:
            # Thống kê tổng quan
            st.subheader("📈 Thống kê tổng quan")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Tổng số túi", f"{int(df_ps['tong_so_tui'].sum()):,}")
            
            with col2:
                st.metric("Tổng số cây (sạch)", f"{int(df_ps['tong_so_cay'].sum()):,}")
            
            with col3:
                st.metric("Số giàn đang sử dụng", f"{df_ps['so_gian_ke'].nunique():,}")
            
            with col4:
                # Đếm số loại giống
                st.metric("Số loại giống", f"{df_ps['ten_giong'].nunique():,}")
            
            st.markdown("---")
            
            # Tổng hợp theo giàn
            st.subheader("📋 Tổng hợp theo Giàn/Kệ")
            
            df_gian = df_ps.groupby('so_gian_ke').agg({
                'tong_so_tui': 'sum',
                'tong_so_cay': 'sum',
                'ten_giong': lambda x: ', '.join(x.unique())
            }).reset_index()
            df_gian.columns = ['Giàn/Kệ', 'Tổng số túi', 'Tổng số cây', 'Loại giống']
            
            st.dataframe(df_gian, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Cây sắp đến ngày xuất
            st.subheader("🌱 Cây sắp đến ngày xuất vườn")
            
            today = date.today()
            df_ps['ngay_xuat_cay'] = pd.to_datetime(df_ps['ngay_xuat_cay'], errors='coerce')
            df_sap_xuat = df_ps[df_ps['ngay_xuat_cay'].notna()].copy()
            df_sap_xuat['so_ngay_con_lai'] = (df_sap_xuat['ngay_xuat_cay'].dt.date - today).apply(lambda x: x.days)
            df_sap_xuat = df_sap_xuat[df_sap_xuat['so_ngay_con_lai'] >= 0].sort_values('so_ngay_con_lai')
            
            if len(df_sap_xuat) > 0:
                df_display_xuat = df_sap_xuat[[
                    'ten_giong', 'so_gian_ke', 'chu_ky', 'tong_so_tui', 'tong_so_cay',
                    'ngay_xuat_cay', 'tuan_xuat_cay'
                ]].copy()
                df_display_xuat['ngay_xuat_cay'] = df_display_xuat['ngay_xuat_cay'].dt.strftime("%d/%m/%Y")
                df_display_xuat['so_ngay_con_lai'] = df_sap_xuat['so_ngay_con_lai']
                df_display_xuat.columns = [
                    'Tên giống', 'Giàn/Kệ', 'Chu kỳ', 'Tổng túi', 'Tổng cây',
                    'Ngày xuất dự kiến', 'Tuần xuất', 'Số ngày còn lại'
                ]
                
                # Tô màu theo số ngày còn lại
                def highlight_ngay(row):
                    if row['Số ngày còn lại'] <= 7:
                        return ['background-color: #f8d7da'] * len(row)  # Đỏ nhạt - sắp xuất
                    elif row['Số ngày còn lại'] <= 14:
                        return ['background-color: #fff3cd'] * len(row)  # Vàng nhạt
                    else:
                        return [''] * len(row)
                
                st.dataframe(
                    df_display_xuat.style.apply(highlight_ngay, axis=1),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("ℹ️ Không có cây nào sắp đến ngày xuất.")
            
            st.markdown("---")
            
            # Bảng chi tiết tất cả
            st.subheader("📋 Bảng chi tiết tất cả cây trong phòng sáng")
            
            # Tính tỷ lệ nhiễm cho từng lô
            df_ps_with_rate = df_ps.copy()
            df_ps_with_rate['Túi nhiễm'] = df_ps_with_rate['so_tui_khuan_nang'] + df_ps_with_rate['so_tui_nam']
            df_ps_with_rate['Tỷ lệ nhiễm (%)'] = (df_ps_with_rate['Túi nhiễm'] / df_ps_with_rate['tong_so_tui'] * 100).round(2)
            df_ps_with_rate['Tỷ lệ nhiễm (%)'] = df_ps_with_rate['Tỷ lệ nhiễm (%)'].fillna(0)
            
            df_display_all = df_ps_with_rate[[
                'ten_giong', 'so_gian_ke', 'chu_ky', 'trang_thai',
                'so_tui_sach', 'so_tui_khuan_nhe', 'so_tui_khuan_nang',
                'so_tui_nam', 'so_tui_khuan_moi_truong', 'so_tui_khac',
                'tong_so_tui', 'tong_so_cay', 'Tỷ lệ nhiễm (%)', 'ngay_xuat_cay', 'tuan_xuat_cay'
            ]].copy()
            
            df_display_all['ngay_xuat_cay'] = df_display_all['ngay_xuat_cay'].dt.strftime("%d/%m/%Y") if 'ngay_xuat_cay' in df_display_all.columns else None
            df_display_all.columns = [
                'Tên giống', 'Giàn/Kệ', 'Chu kỳ', 'Trạng thái',
                'Sạch', 'Khuẩn nhẹ', 'Khuẩn nặng', 'Nấm', 'Khuẩn MT', 'Khác',
                'Tổng túi', 'Tổng cây', 'Tỷ lệ nhiễm (%)', 'Ngày xuất', 'Tuần xuất'
            ]
            
            # Tô màu theo tỷ lệ nhiễm
            def highlight_ty_le_nhiem(row):
                ty_le = row['Tỷ lệ nhiễm (%)']
                if ty_le > 10:
                    return ['background-color: #dc3545; color: white; font-weight: bold'] * len(row)  # ĐỎ RỰC
                elif ty_le > 5:
                    return ['background-color: #ffc107; color: black'] * len(row)  # Vàng
                else:
                    return [''] * len(row)
            
            styled_df_all = df_display_all.style.apply(highlight_ty_le_nhiem, axis=1)
            
            # Thống kê số lô cảnh báo
            so_lo_canh_bao = len(df_ps_with_rate[df_ps_with_rate['Tỷ lệ nhiễm (%)'] > 10])
            so_lo_chu_y = len(df_ps_with_rate[(df_ps_with_rate['Tỷ lệ nhiễm (%)'] > 5) & (df_ps_with_rate['Tỷ lệ nhiễm (%)'] <= 10)])
            
            if so_lo_canh_bao > 0:
                st.error(f"🚨 **CÓ {so_lo_canh_bao} LÔ CẢNH BÁO ĐỎ** (Tỷ lệ nhiễm > 10%)! Cần xử lý ngay!")
            if so_lo_chu_y > 0:
                st.warning(f"⚠️ Có {so_lo_chu_y} lô cần chú ý (Tỷ lệ nhiễm 5-10%)")
            
            st.dataframe(styled_df_all, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Chưa có dữ liệu trong phòng sáng.")
    
    # ========== TRANG QUẢN LÝ MÔ SOI (CHỈ ADMIN) ==========
    elif menu == "Quản lý Mô Soi" and is_admin:
        st.header("🔬 Quản lý Mô Soi")
        st.markdown("**Mô Soi** là kết quả kiểm tra từ chu kỳ trước (Phòng Sáng) - nguồn cung cấp Mô Mẹ cho chu kỳ tiếp theo")
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📝 Nhập Mô Soi", "📊 Danh sách Mô Soi", "📈 Báo cáo Sử dụng"])
        
        # Tab 1: Nhập Mô Soi mới
        with tab1:
            st.subheader("📝 Nhập kết quả kiểm tra Mô Soi từ Phòng Sáng")
            st.info("""
            **Quy trình:**
            1. **Chọn lô cấy** từ Phòng Sáng (đã nhập trước đó)
            2. Hệ thống tự động điền thông tin: Giống, Chu kỳ, Ngày/Tuần/Tháng cấy, Nhân viên, Số túi
            3. Admin chỉ cần nhập: **Số túi nhiễm** và **Số cụm/túi sạch**
            """)
            
            # Query danh sách lô từ Phòng Sáng (chưa được kiểm tra thành Mô Soi)
            conn = sqlite3.connect('data.db')
            df_phong_sang = pd.read_sql_query('''
                SELECT DISTINCT
                    ps.id,
                    ps.id_nhat_ky_cay,
                    ps.ten_giong,
                    ps.chu_ky,
                    ps.ngay_cay,
                    ps.nhan_vien,
                    ps.ma_nhan_vien,
                    nk.tuan AS tuan_cay,
                    nk.thang AS thang_cay,
                    ps.tong_so_tui,
                    ps.so_tui_sach,
                    (ps.so_tui_khuan_nhe + ps.so_tui_khuan_nang + ps.so_tui_khuan_moi_truong) AS so_tui_khuan,
                    (ps.so_tui_nam) AS so_tui_huy,
                    ps.trang_thai
                FROM quan_ly_phong_sang ps
                LEFT JOIN nhat_ky_cay nk ON ps.id_nhat_ky_cay = nk.id
                WHERE ps.id_nhat_ky_cay NOT IN (
                    SELECT id_nhat_ky_cay FROM mo_soi WHERE id_nhat_ky_cay IS NOT NULL
                )
                ORDER BY ps.ngay_cay DESC
                LIMIT 100
            ''', conn)
            conn.close()
            
            if len(df_phong_sang) == 0:
                st.warning("""
                ⚠️ **Không có lô nào từ Phòng Sáng để kiểm tra.**
                
                Vui lòng:
                1. Nhập Nhật ký cấy trước
                2. Đợi lô cấy chuyển sang Phòng Sáng
                3. Quay lại đây để nhập kết quả kiểm tra Mô Soi
                """)
            else:
                # Tạo dictionary để map
                dict_phong_sang = {}
                danh_sach_lua_chon = []
                danh_sach_hien_thi = []  # Label ngắn gọn
                
                for idx, row in df_phong_sang.iterrows():
                    # Label đầy đủ (để map)
                    label_full = f"{row['ten_giong']} - {row['chu_ky']} - Ngày: {row['ngay_cay']} - NV: {row['nhan_vien']} ({row['tong_so_tui']} túi)"
                    # Label ngắn gọn (hiển thị dropdown)
                    label_short = f"🌱 {row['ten_giong']} - 📅 {row['ngay_cay']} ({row['tong_so_tui']} túi)"
                    
                    danh_sach_lua_chon.append(label_full)
                    danh_sach_hien_thi.append(label_short)
                    dict_phong_sang[label_short] = row
                
                # DROPDOWN RA NGOÀI FORM để tương tác động
                st.markdown("#### 🎯 Chọn lô cấy từ Phòng Sáng")
                
                # Tùy chọn: Dropdown hoặc Radio (dễ bấm hơn trên mobile)
                chon_kieu = st.radio(
                    "Cách chọn lô:",
                    ["📋 Dropdown (gọn)", "🔘 Danh sách (dễ bấm)"],
                    horizontal=True,
                    help="Chọn 'Danh sách' nếu dùng điện thoại"
                )
                
                if chon_kieu == "📋 Dropdown (gọn)":
                    lo_chon = st.selectbox(
                        "Chọn lô cần kiểm tra *",
                        options=danh_sach_hien_thi,
                        help="Chọn lô cấy đã hoàn thành chu kỳ trong Phòng Sáng",
                        key="lo_chon_mosoi_dropdown"
                    )
                else:
                    # Radio buttons - dễ bấm hơn trên mobile
                    lo_chon = st.radio(
                        "Chọn lô cần kiểm tra *",
                        options=danh_sach_hien_thi,
                        help="Bấm vào lô cần kiểm tra",
                        key="lo_chon_mosoi_radio"
                    )
                
                # Lấy thông tin lô đã chọn
                if lo_chon:
                    thong_tin_lo = dict_phong_sang[lo_chon]
                    
                    st.markdown("---")
                    st.markdown("#### 📋 Thông tin lô đã chọn (Tự động từ Phòng Sáng)")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.info(f"""
                        **🌱 Giống:** {thong_tin_lo['ten_giong']}
                        
                        **🔄 Chu kỳ:** {thong_tin_lo['chu_ky']}
                        """)
                    with col2:
                        st.info(f"""
                        **📅 Ngày cấy:** {thong_tin_lo['ngay_cay']}
                        
                        **📊 Tuần {thong_tin_lo['tuan_cay']} / Tháng {thong_tin_lo['thang_cay']}**
                        """)
                    with col3:
                        st.info(f"""
                        **👤 Nhân viên:** {thong_tin_lo['nhan_vien']}
                        
                        **📦 Tổng túi:** {int(thong_tin_lo['tong_so_tui'])} túi
                        """)
                    
                    # Hiển thị chi tiết tình trạng từ phòng sáng
                    with st.expander("📊 Chi tiết tình trạng từ Phòng Sáng"):
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("✅ Túi sạch", f"{int(thong_tin_lo['so_tui_sach'])} túi")
                        with col_b:
                            st.metric("⚠️ Túi khuẩn", f"{int(thong_tin_lo['so_tui_khuan'])} túi")
                        with col_c:
                            st.metric("❌ Túi hủy (Nấm)", f"{int(thong_tin_lo['so_tui_huy'])} túi")
                    
                    st.markdown("---")
                    st.markdown("---")
                    
                    # FORM BẮT ĐẦU TỪ ĐÂY (sau khi đã chọn lô)
                    with st.form("form_nhap_mo_soi", clear_on_submit=False):
                        st.markdown("#### 📅 Thông tin kiểm tra")
                        ngay_soi = st.date_input(
                            "Ngày kiểm tra (soi) *",
                            value=date.today(),
                            help="Ngày thực hiện kiểm tra mô soi"
                        )
                    
                        st.markdown("---")
                        st.markdown("#### 🔢 Kết quả kiểm tra (Admin nhập)")
                    
                        # Số túi ban đầu tự động = tổng số túi từ phòng sáng
                        so_luong_ban_dau = int(thong_tin_lo['tong_so_tui'])
                    
                        col1, col2 = st.columns(2)
                        with col1:
                            so_tui_nhiem = st.number_input(
                                "Số túi nhiễm (Nấm + Khuẩn nặng) *",
                                min_value=0,
                                max_value=so_luong_ban_dau,
                                value=int(thong_tin_lo['so_tui_khuan'] + thong_tin_lo['so_tui_huy']) if (thong_tin_lo['so_tui_khuan'] + thong_tin_lo['so_tui_huy']) > 0 else 0,
                                step=1,
                                help="Tổng túi bị nấm, khuẩn nặng (không dùng được)"
                            )
                    
                        with col2:
                            so_cum_moi_tui = st.number_input(
                                "Số cụm mỗi túi sạch *",
                                min_value=1,
                                value=5,
                                step=1,
                                help="Số cụm trung bình trong mỗi túi sạch"
                            )
                    
                        # Tính toán tự động
                        so_tui_sach = so_luong_ban_dau - so_tui_nhiem
                        tong_cum_sach = so_tui_sach * so_cum_moi_tui
                    
                        st.markdown("---")
                        st.markdown("#### 📊 Kết quả tự động tính")
                    
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Túi sạch", f"{so_tui_sach} túi")
                        with col2:
                            st.metric("Tổng cụm sạch", f"{tong_cum_sach} cụm")
                        with col3:
                            ty_le_sach = (so_tui_sach / so_luong_ban_dau * 100) if so_luong_ban_dau > 0 else 0
                            st.metric("Tỷ lệ sạch", f"{ty_le_sach:.1f}%")
                        with col4:
                            ty_le_nhiem = (so_tui_nhiem / so_luong_ban_dau * 100) if so_luong_ban_dau > 0 else 0
                            st.metric("Tỷ lệ nhiễm", f"{ty_le_nhiem:.1f}%")
                    
                        if ty_le_nhiem > 20:
                            st.error(f"🔴 **CẢNH BÁO:** Tỷ lệ nhiễm cao ({ty_le_nhiem:.1f}%)! Cần kiểm tra quy trình.")
                        elif ty_le_nhiem > 10:
                            st.warning(f"⚠️ Tỷ lệ nhiễm hơi cao ({ty_le_nhiem:.1f}%), cần lưu ý.")
                    
                        st.markdown("---")
                        st.markdown("#### 👤 Người thực hiện kiểm tra")
                    
                        col1, col2 = st.columns(2)
                        with col1:
                            nguoi_soi = st.text_input(
                                "Tên nhân viên soi *",
                                value=user_info['ten_nhan_vien'],
                                help="Người thực hiện kiểm tra"
                            )
                        with col2:
                            ma_nhan_vien_soi = st.text_input(
                                "Mã nhân viên *",
                                value=user_info['ma_nhan_vien'],
                                help="Mã nhân viên"
                            )
                    
                        ghi_chu = st.text_area(
                            "Ghi chú",
                            placeholder="Ví dụ: Kết quả kiểm tra lô cấy ngày 01/01/2026...",
                            help="Thông tin bổ sung"
                        )
                    
                        submitted = st.form_submit_button("💾 Lưu Mô Soi", use_container_width=True, type="primary")
                    
                        if submitted:
                            if so_tui_sach <= 0:
                                st.error("❌ Số túi sạch phải > 0. Vui lòng kiểm tra lại!")
                            else:
                                # Lấy thông tin từ lô đã chọn
                                ten_giong = thong_tin_lo['ten_giong']
                                chu_ky_truoc = thong_tin_lo['chu_ky']
                                id_nhat_ky_cay = int(thong_tin_lo['id_nhat_ky_cay'])
                            
                                # Tạo mã lô mô soi
                                ma_lo_mo_soi = tao_ma_lo_mo_soi()
                                tuan_soi = int(ngay_soi.strftime('%U'))
                                nam = ngay_soi.year
                            
                                # Lưu vào database
                                conn = sqlite3.connect('data.db')
                                c = conn.cursor()
                            
                                # Thêm cột id_nhat_ky_cay nếu chưa có
                                try:
                                    c.execute("ALTER TABLE mo_soi ADD COLUMN id_nhat_ky_cay INTEGER")
                                    conn.commit()
                                except:
                                    pass
                            
                                c.execute('''
                                    INSERT INTO mo_soi (
                                        ma_lo_mo_soi, ten_giong, chu_ky_truoc, ngay_soi, tuan_soi, nam,
                                        so_luong_ban_dau, so_tui_nhiem, so_tui_sach, so_cum_moi_tui,
                                        tong_cum_sach, so_cum_da_cap, so_cum_con_lai, trang_thai,
                                        nguoi_soi, ma_nhan_vien, ghi_chu, ngay_tao, ngay_cap_nhat,
                                        id_nhat_ky_cay
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (
                                    ma_lo_mo_soi, ten_giong, chu_ky_truoc, ngay_soi.strftime('%Y-%m-%d'), 
                                    tuan_soi, nam, so_luong_ban_dau, so_tui_nhiem, so_tui_sach, 
                                    so_cum_moi_tui, tong_cum_sach, 0, tong_cum_sach, 'Đang sử dụng',
                                    nguoi_soi, ma_nhan_vien_soi, ghi_chu,
                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    id_nhat_ky_cay
                                ))
                                conn.commit()
                                conn.close()
                            
                                st.success(f"""
                                ✅ **ĐÃ LƯU MÔ SOI THÀNH CÔNG!**
                            
                                📦 **Mã lô:** {ma_lo_mo_soi}
                                🌱 **Giống:** {ten_giong} - **Chu kỳ:** {chu_ky_truoc}
                                📅 **Ngày cấy:** {thong_tin_lo['ngay_cay']} - **NV cấy:** {thong_tin_lo['nhan_vien']}
                                📊 **Tổng túi:** {so_luong_ban_dau} → **Nhiễm:** {so_tui_nhiem} → **Sạch:** {so_tui_sach}
                                ✅ **Tổng cụm sạch:** {tong_cum_sach} cụm
                                📈 **Tỷ lệ sạch:** {ty_le_sach:.1f}%
                            
                                ➡️ Lô này sẽ được dùng để cấp Mô Mẹ cho chu kỳ tiếp theo.
                                """)
                                st.balloons()
                            st.rerun()
                
                # ===== HIỂN THỊ DANH SÁCH MÔ SOI ĐÃ NHẬP =====
                st.markdown("---")
                st.markdown("---")
                st.header("📋 Danh sách Mô Soi đã nhập")
            
            conn = sqlite3.connect('data.db')
            
            # Query danh sách mô soi gần đây (20 bản ghi)
            df_mo_soi = pd.read_sql_query('''
                SELECT 
                    id, ma_lo_mo_soi, ten_giong, chu_ky_truoc, ngay_soi,
                    so_luong_ban_dau, so_tui_nhiem, so_tui_sach, so_cum_moi_tui,
                    tong_cum_sach, so_cum_da_cap, so_cum_con_lai, trang_thai,
                    nguoi_soi, ma_nhan_vien, ghi_chu
                FROM mo_soi
                ORDER BY ngay_tao DESC
                LIMIT 20
            ''', conn)
            conn.close()
            
            if len(df_mo_soi) > 0:
                st.info(f"📊 Hiển thị {len(df_mo_soi)} lô mô soi gần nhất")
                
                for idx, row in df_mo_soi.iterrows():
                    # Tính tỷ lệ
                    ty_le_sach = (row['so_tui_sach'] / row['so_luong_ban_dau'] * 100) if row['so_luong_ban_dau'] > 0 else 0
                    ty_le_da_cap = (row['so_cum_da_cap'] / row['tong_cum_sach'] * 100) if row['tong_cum_sach'] > 0 else 0
                    
                    # Icon trạng thái
                    if row['trang_thai'] == 'Đã kết thúc chu kỳ':
                        icon_status = "✅"
                        color_status = "green"
                    elif ty_le_da_cap > 80:
                        icon_status = "⚠️"
                        color_status = "orange"
                    else:
                        icon_status = "🔄"
                        color_status = "blue"
                    
                    with st.expander(f"{icon_status} **{row['ma_lo_mo_soi']}** - {row['ten_giong']} ({row['chu_ky_truoc']}) - Ngày: {row['ngay_soi']}"):
                        col_info, col_action = st.columns([3, 1])
                        
                        with col_info:
                            st.markdown(f"""
                            **📦 Thông tin Mô Soi:**
                            - 🔖 **Mã lô:** {row['ma_lo_mo_soi']}
                            - 🌱 **Giống:** {row['ten_giong']} | **Chu kỳ trước:** {row['chu_ky_truoc']}
                            - 📅 **Ngày soi:** {row['ngay_soi']}
                            - 📊 **Ban đầu:** {row['so_luong_ban_dau']} túi | **Nhiễm:** {row['so_tui_nhiem']} túi | **Sạch:** {row['so_tui_sach']} túi
                            - 🎯 **Tỷ lệ sạch:** {ty_le_sach:.1f}%
                            
                            **🔢 Tình trạng sử dụng:**
                            - ✅ **Tổng cụm sạch:** {row['tong_cum_sach']} cụm
                            - 📤 **Đã cấp:** {row['so_cum_da_cap']} cụm ({ty_le_da_cap:.1f}%)
                            - 📦 **Còn lại:** {row['so_cum_con_lai']} cụm
                            - 🏷️ **Trạng thái:** {row['trang_thai']}
                            
                            **👤 Người thực hiện:**
                            - **Tên:** {row['nguoi_soi']} | **Mã:** {row['ma_nhan_vien']}
                            - 📝 **Ghi chú:** {row['ghi_chu'] if row['ghi_chu'] else '_Không có_'}
                            """)
                        
                        with col_action:
                            # Chỉ Admin mới sửa được
                            if is_admin:
                                if st.button("✏️ Sửa", key=f"edit_mosoi_{row['id']}", use_container_width=True):
                                    st.session_state[f'editing_mosoi_{row["id"]}'] = True
                                    st.rerun()
                            else:
                                st.info("🔒 Chỉ Admin")
                        
                        # Form chỉnh sửa (chỉ hiển thị khi click "Sửa")
                        if st.session_state.get(f'editing_mosoi_{row["id"]}', False):
                            st.markdown("---")
                            st.markdown("### ✏️ Chỉnh sửa Mô Soi")
                            
                            with st.form(f"form_edit_mosoi_{row['id']}"):
                                st.markdown("#### 🔢 Cập nhật kết quả kiểm tra")
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    edit_so_luong_ban_dau = st.number_input(
                                        "Tổng số túi ban đầu",
                                        min_value=1,
                                        value=int(row['so_luong_ban_dau']),
                                        key=f"edit_ban_dau_{row['id']}"
                                    )
                                with col2:
                                    edit_so_tui_nhiem = st.number_input(
                                        "Số túi nhiễm",
                                        min_value=0,
                                        value=int(row['so_tui_nhiem']),
                                        key=f"edit_nhiem_{row['id']}"
                                    )
                                with col3:
                                    edit_so_cum_moi_tui = st.number_input(
                                        "Số cụm/túi sạch",
                                        min_value=1,
                                        value=int(row['so_cum_moi_tui']),
                                        key=f"edit_cum_{row['id']}"
                                    )
                                
                                # Tính toán lại
                                edit_so_tui_sach = edit_so_luong_ban_dau - edit_so_tui_nhiem
                                edit_tong_cum_sach = edit_so_tui_sach * edit_so_cum_moi_tui
                                
                                st.info(f"📊 **Kết quả:** {edit_so_tui_sach} túi sạch × {edit_so_cum_moi_tui} cụm = **{edit_tong_cum_sach} cụm sạch**")
                                
                                edit_ghi_chu = st.text_area(
                                    "Ghi chú",
                                    value=row['ghi_chu'] if row['ghi_chu'] else "",
                                    key=f"edit_ghi_chu_mosoi_{row['id']}",
                                    height=80
                                )
                                
                                col_submit, col_cancel = st.columns(2)
                                
                                with col_submit:
                                    submitted_edit = st.form_submit_button("💾 Lưu thay đổi", use_container_width=True, type="primary")
                                
                                with col_cancel:
                                    cancelled = st.form_submit_button("❌ Hủy", use_container_width=True)
                                
                                if submitted_edit:
                                    if edit_so_tui_sach <= 0:
                                        st.error("❌ Số túi sạch phải > 0!")
                                    else:
                                        # Tính lại số cụm còn lại (giữ nguyên số đã cấp)
                                        edit_so_cum_con_lai = edit_tong_cum_sach - row['so_cum_da_cap']
                                        
                                        # Cập nhật database
                                        conn = sqlite3.connect('data.db')
                                        c = conn.cursor()
                                        c.execute('''
                                            UPDATE mo_soi
                                            SET so_luong_ban_dau = ?, so_tui_nhiem = ?, so_tui_sach = ?,
                                                so_cum_moi_tui = ?, tong_cum_sach = ?, so_cum_con_lai = ?,
                                                ghi_chu = ?, ngay_cap_nhat = ?
                                            WHERE id = ?
                                        ''', (
                                            edit_so_luong_ban_dau, edit_so_tui_nhiem, edit_so_tui_sach,
                                            edit_so_cum_moi_tui, edit_tong_cum_sach, edit_so_cum_con_lai,
                                            edit_ghi_chu, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                            row['id']
                                        ))
                                        conn.commit()
                                        conn.close()
                                        
                                        # Xóa trạng thái editing
                                        st.session_state[f'editing_mosoi_{row["id"]}'] = False
                                        st.success("✅ Đã cập nhật Mô Soi thành công!")
                                        st.rerun()
                                
                                if cancelled:
                                    st.session_state[f'editing_mosoi_{row["id"]}'] = False
                                    st.rerun()
            else:
                st.info("ℹ️ Chưa có dữ liệu Mô Soi. Vui lòng nhập lô đầu tiên.")
        
        # Tab 2: Danh sách Mô Soi
        with tab2:
            st.subheader("📊 Danh sách Mô Soi hiện có")
            
            conn = sqlite3.connect('data.db')
            df = pd.read_sql_query('''
                SELECT 
                    ma_lo_mo_soi AS 'Mã lô',
                    ten_giong AS 'Tên giống',
                    chu_ky_truoc AS 'Chu kỳ trước',
                    ngay_soi AS 'Ngày soi',
                    so_luong_ban_dau AS 'Túi ban đầu',
                    so_tui_nhiem AS 'Túi nhiễm',
                    so_tui_sach AS 'Túi sạch',
                    so_cum_moi_tui AS 'Cụm/túi',
                    tong_cum_sach AS 'Tổng cụm',
                    so_cum_da_cap AS 'Đã cấp',
                    so_cum_con_lai AS 'Còn lại',
                    trang_thai AS 'Trạng thái',
                    nguoi_soi AS 'Người soi'
                FROM mo_soi
                ORDER BY ngay_soi DESC
            ''', conn)
            conn.close()
            
            if len(df) > 0:
                # Metrics tổng quan
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    tong_lo_dang_su_dung = len(df[df['Trạng thái'] == 'Đang sử dụng'])
                    st.metric("Lô đang sử dụng", tong_lo_dang_su_dung)
                with col2:
                    tong_cum_con_lai = df[df['Trạng thái'] == 'Đang sử dụng']['Còn lại'].sum()
                    st.metric("Tổng cụm còn lại", f"{tong_cum_con_lai:,}")
                with col3:
                    tong_cum_da_cap = df['Đã cấp'].sum()
                    st.metric("Tổng cụm đã cấp", f"{tong_cum_da_cap:,}")
                with col4:
                    lo_ket_thuc = len(df[df['Trạng thái'] == 'Đã kết thúc chu kỳ'])
                    st.metric("Lô đã kết thúc", lo_ket_thuc)
                
                st.markdown("---")
                
                # Styling cho bảng
                def highlight_trang_thai(row):
                    if row['Trạng thái'] == 'Đang sử dụng':
                        if row['Còn lại'] > 0:
                            return ['background-color: #d4edda'] * len(row)  # Xanh lá
                        else:
                            return ['background-color: #fff3cd'] * len(row)  # Vàng
                    elif row['Trạng thái'] == 'Đã kết thúc chu kỳ':
                        return ['background-color: #f8d7da'] * len(row)  # Đỏ nhạt
                    return [''] * len(row)
                
                styled_df = df.style.apply(highlight_trang_thai, axis=1)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
                # Download
                st.download_button(
                    "📥 Tải xuống Excel",
                    data=df.to_csv(index=False).encode('utf-8-sig'),
                    file_name=f"mo_soi_{date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("ℹ️ Chưa có dữ liệu mô soi. Vui lòng nhập ở tab 'Nhập Mô Soi'.")
        
        # Tab 3: Báo cáo sử dụng
        with tab3:
            st.subheader("📈 Báo cáo Sử dụng Mô Soi")
            
            conn = sqlite3.connect('data.db')
            
            # Thống kê theo giống
            df_stats = pd.read_sql_query('''
                SELECT 
                    ten_giong,
                    COUNT(*) AS so_lo,
                    SUM(tong_cum_sach) AS tong_cum,
                    SUM(so_cum_da_cap) AS da_cap,
                    SUM(so_cum_con_lai) AS con_lai,
                    ROUND(AVG(CAST(so_tui_nhiem AS FLOAT) / so_luong_ban_dau * 100), 1) AS ty_le_nhiem_tb
                FROM mo_soi
                GROUP BY ten_giong
                ORDER BY tong_cum DESC
            ''', conn)
            
            conn.close()
            
            if len(df_stats) > 0:
                st.markdown("#### 📊 Thống kê theo giống")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Bar chart
                    import plotly.graph_objects as go
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name='Đã cấp',
                        x=df_stats['ten_giong'],
                        y=df_stats['da_cap'],
                        marker_color='#28a745'
                    ))
                    fig.add_trace(go.Bar(
                        name='Còn lại',
                        x=df_stats['ten_giong'],
                        y=df_stats['con_lai'],
                        marker_color='#ffc107'
                    ))
                    
                    fig.update_layout(
                        title="Mô Soi: Đã cấp vs Còn lại",
                        xaxis_title="Tên giống",
                        yaxis_title="Số cụm",
                        barmode='stack',
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("**Chi tiết:**")
                    st.dataframe(df_stats, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ Chưa có dữ liệu để thống kê.")
    
    # ========== TRANG ĐỐI SOÁT MÔ SOI (CHỈ ADMIN) ==========
    elif menu == "Đối soát Mô Soi" and is_admin:
        st.header("🔍 Đối soát Mô Soi vs Mô Mẹ đã cấy")
        st.markdown("**Check & Balance:** Kiểm tra tổng Mô Soi có khớp với tổng Mô Mẹ đã cấy hay không")
        st.markdown("---")
        
        df_doi_soat = get_bao_cao_doi_soat_mo_soi()
        
        if len(df_doi_soat) > 0:
            # Metrics tổng quan
            col1, col2, col3 = st.columns(3)
            
            with col1:
                tong_khop = len(df_doi_soat[df_doi_soat['trang_thai'].str.contains('KHỚP')])
                st.metric("✅ Giống khớp", tong_khop, help="Mô soi = Mô mẹ đã cấy")
            
            with col2:
                tong_du = len(df_doi_soat[df_doi_soat['trang_thai'].str.contains('DƯ MÔ')])
                st.metric("⚠️ Giống dư mô", tong_du, help="Còn mô soi chưa cấy")
            
            with col3:
                tong_bat_thuong = len(df_doi_soat[df_doi_soat['trang_thai'].str.contains('BẤT THƯỜNG')])
                st.metric("🔴 Giống bất thường", tong_bat_thuong, help="Mô mẹ đã cấy > Mô soi!")
            
            st.markdown("---")
            
            # Hiển thị bảng đối soát
            st.markdown("### 📋 Bảng đối soát chi tiết")
            
            df_display = df_doi_soat.rename(columns={
                'ten_giong': 'Tên giống',
                'tong_cum_mo_soi': 'Tổng cụm Mô Soi',
                'tong_cum_da_cap': 'Đã cấp (theo hệ thống)',
                'tong_cum_con_lai': 'Còn lại',
                'tong_cum_me_da_cay': 'Mô Mẹ đã cấy (theo nhật ký)',
                'chenh_lech': 'Chênh lệch',
                'trang_thai': 'Trạng thái'
            })
            
            # Styling
            def highlight_doi_soat(row):
                if '🔴 BẤT THƯỜNG' in str(row['Trạng thái']):
                    return ['background-color: #f8d7da; font-weight: bold'] * len(row)
                elif '⚠️ DƯ MÔ' in str(row['Trạng thái']):
                    return ['background-color: #fff3cd'] * len(row)
                elif '✅ KHỚP' in str(row['Trạng thái']):
                    return ['background-color: #d4edda'] * len(row)
                return [''] * len(row)
            
            styled_df = df_display.style.apply(highlight_doi_soat, axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # Cảnh báo nếu có bất thường
            if tong_bat_thuong > 0:
                st.error(f"""
                🚨 **CẢNH BÁO NGHIÊM TRỌNG!**
                
                Có {tong_bat_thuong} giống có dữ liệu bất thường:
                - Tổng Mô Mẹ đã cấy > Tổng Mô Soi có sẵn
                - Điều này không thể xảy ra trong thực tế!
                
                **Nguyên nhân có thể:**
                1. Nhân viên nhập nhật ký nhưng không chọn đúng lô Mô Soi
                2. Lô Mô Soi chưa được nhập vào hệ thống
                3. Dữ liệu nhập sai
                
                **Hành động:**
                - Kiểm tra lại nhật ký cấy của từng nhân viên
                - Xác nhận lại số liệu với phòng sáng
                """)
            
            if tong_du > 0:
                st.warning(f"""
                ⚠️ **LƯU Ý:**
                
                Có {tong_du} giống còn dư Mô Soi chưa cấy hết.
                
                **Gợi ý:**
                - Đẩy nhanh tiến độ cấy
                - Kiểm tra chất lượng mô soi còn lại
                - Cân nhắc hủy bỏ nếu để quá lâu
                """)
            
            # Download
            st.download_button(
                "📥 Tải báo cáo đối soát",
                data=df_display.to_csv(index=False).encode('utf-8-sig'),
                file_name=f"doi_soat_mo_soi_{date.today().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("""
            ℹ️ **Chưa có dữ liệu để đối soát**
            
            Để sử dụng tính năng này:
            1. Nhập dữ liệu Mô Soi ở trang "Quản lý Mô Soi"
            2. Liên kết Mô Soi với nhật ký cấy (chọn lô Mô Soi khi nhập nhật ký)
            3. Hệ thống sẽ tự động đối soát
            """)
    
    # ========== TRANG QUẢN LÝ KHO MÔI TRƯỜNG (CHỈ ADMIN) ==========
    elif menu == "Quản lý Kho Môi trường" and is_admin:
        st.header("🧪 Quản lý Kho Môi trường")
        st.markdown("Nhập kho môi trường mới và theo dõi tồn kho")
        st.markdown("---")
        
        # Tabs: Nhập kho | Tồn kho | Lịch sử xuất
        tab_nhap, tab_ton, tab_lich_su = st.tabs(["📥 Nhập kho", "📊 Tồn kho", "📜 Lịch sử xuất"])
        
        # ========== TAB 1: NHẬP KHO MÔI TRƯỜNG ==========
        with tab_nhap:
            st.subheader("📥 Nhập môi trường mới vào kho")
            
            danh_sach_moi_truong = get_danh_sach_moi_truong()
            danh_sach_vi_tri_kho = get_danh_sach_vi_tri_kho()
            
            if len(danh_sach_moi_truong) == 0:
                st.warning("⚠️ Chưa có môi trường trong danh mục. Vui lòng thêm tại 'Quản lý danh mục' → 'Môi trường'")
            elif len(danh_sach_vi_tri_kho) == 0:
                st.info("💡 Chưa có vị trí kho. Thêm ngay bên dưới hoặc tại 'Quản lý danh mục'")
                
                # Form thêm nhanh vị trí kho
                with st.expander("➕ Thêm nhanh vị trí kho"):
                    with st.form("form_them_nhanh_vi_tri_kho", clear_on_submit=True):
                        vi_tri_kho_moi = st.text_input(
                            "Vị trí kho *",
                            placeholder="VD: Kho A1, Kệ môi trường tầng 1",
                            help="Nhập vị trí lưu trữ môi trường"
                        )
                        submitted = st.form_submit_button("➕ Thêm", use_container_width=True)
                        
                        if submitted and vi_tri_kho_moi.strip():
                            conn = sqlite3.connect('data.db')
                            c = conn.cursor()
                            try:
                                c.execute('''
                                    INSERT INTO danh_muc_vi_tri_kho (vi_tri_kho, ngay_tao)
                                    VALUES (?, ?)
                                ''', (vi_tri_kho_moi.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                conn.commit()
                                st.success(f"✅ Đã thêm vị trí kho: {vi_tri_kho_moi}")
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error(f"❌ Vị trí kho '{vi_tri_kho_moi}' đã tồn tại!")
                            finally:
                                conn.close()
            
            # Form nhập kho môi trường (TỐI ƯU MOBILE)
            if len(danh_sach_moi_truong) > 0:
                with st.form("form_nhap_kho_moi_truong", clear_on_submit=True):
                    st.markdown("#### 📝 Thông tin lô môi trường")
                    
                    # Tự động tạo mã lô
                    ma_lo_moi = tao_ma_lo_moi_truong()
                    st.info(f"🏷️ Mã lô tự động: **{ma_lo_moi}**")
                    
                    # Chọn loại môi trường
                    dict_ten_to_ma = {v: k for k, v in danh_sach_moi_truong.items()}
                    ten_moi_truong_chon = st.selectbox(
                        "Loại môi trường *",
                        options=list(danh_sach_moi_truong.values()),
                        help="Chọn loại môi trường đã đổ"
                    )
                    ma_so_moi_truong = dict_ten_to_ma[ten_moi_truong_chon]
                    
                    # Ngày đổ
                    ngay_do = st.date_input(
                        "Ngày đổ môi trường *",
                        value=date.today(),
                        help="Ngày thực hiện đổ môi trường"
                    )
                    
                    # Tự động tính tuần và năm
                    tuan_do = tinh_tuan(ngay_do)
                    nam = ngay_do.year
                    st.info(f"📆 Tuần: {tuan_do} | Năm: {nam}")
                    
                    # Số lượng
                    so_luong = st.number_input(
                        "Số lượng túi/hộp đã đổ *",
                        min_value=1,
                        value=100,
                        step=10,
                        help="Tổng số túi hoặc hộp môi trường đã đổ"
                    )
                    
                    # Vị trí kho
                    if len(danh_sach_vi_tri_kho) > 0:
                        vi_tri_kho = st.selectbox(
                            "Vị trí lưu trữ *",
                            options=danh_sach_vi_tri_kho,
                            help="Chọn vị trí kho lưu trữ"
                        )
                    else:
                        vi_tri_kho = st.text_input(
                            "Vị trí lưu trữ (tạm thời) *",
                            placeholder="VD: Kho A1",
                            help="Nên thêm vào danh mục để dễ quản lý"
                        )
                    
                    # Người đổ
                    nguoi_do = st.text_input(
                        "Người thực hiện",
                        value=st.session_state.user_info['ten_nhan_vien'] if not is_admin else "",
                        placeholder="VD: Nguyễn Văn A",
                        help="Tên người đổ môi trường"
                    )
                    
                    # Ghi chú
                    ghi_chu = st.text_area(
                        "Ghi chú",
                        placeholder="VD: Lô môi trường tốt, màu sắc đạt chuẩn",
                        help="Thông tin bổ sung về lô môi trường"
                    )
                    
                    # Nút submit
                    submitted = st.form_submit_button("💾 Lưu vào kho", use_container_width=True, type="primary")
                    
                    if submitted:
                        if vi_tri_kho.strip():
                            conn = sqlite3.connect('data.db')
                            c = conn.cursor()
                            try:
                                c.execute('''
                                    INSERT INTO kho_moi_truong (
                                        ma_lo, ma_so_moi_truong, ten_moi_truong,
                                        ngay_do, tuan_do, nam,
                                        so_luong_ban_dau, so_luong_con_lai,
                                        vi_tri_kho, nguoi_do, ghi_chu, ngay_tao
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (
                                    ma_lo_moi,
                                    ma_so_moi_truong,
                                    ten_moi_truong_chon,
                                    ngay_do.strftime("%Y-%m-%d"),
                                    tuan_do,
                                    nam,
                                    so_luong,
                                    so_luong,  # Ban đầu còn lại = số lượng đổ
                                    vi_tri_kho.strip(),
                                    nguoi_do.strip() if nguoi_do.strip() else None,
                                    ghi_chu.strip() if ghi_chu.strip() else None,
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                ))
                                conn.commit()
                                st.success(f"✅ Đã nhập kho thành công! Mã lô: {ma_lo_moi}")
                                st.balloons()
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error(f"❌ Mã lô '{ma_lo_moi}' đã tồn tại!")
                            except Exception as e:
                                st.error(f"❌ Lỗi: {str(e)}")
                            finally:
                                conn.close()
                        else:
                            st.warning("⚠️ Vui lòng nhập vị trí kho!")
        
        # ========== TAB 2: TỒN KHO ==========
        with tab_ton:
            st.subheader("📊 Báo cáo Tồn kho Môi trường")
            
            conn = sqlite3.connect('data.db')
            
            # Tổng hợp tồn kho theo loại
            df_ton_kho = pd.read_sql_query('''
                SELECT 
                    ten_moi_truong AS "Loại môi trường",
                    SUM(so_luong_con_lai) AS "Tổng tồn",
                    COUNT(*) AS "Số lô",
                    GROUP_CONCAT(DISTINCT vi_tri_kho) AS "Vị trí"
                FROM kho_moi_truong
                WHERE so_luong_con_lai > 0
                GROUP BY ma_so_moi_truong, ten_moi_truong
                ORDER BY "Tổng tồn" DESC
            ''', conn)
            
            if len(df_ton_kho) > 0:
                st.markdown("#### 📦 Tổng tồn kho theo loại")
                st.dataframe(df_ton_kho, use_container_width=True, hide_index=True)
                
                # Biểu đồ
                fig = px.bar(
                    df_ton_kho,
                    x="Loại môi trường",
                    y="Tổng tồn",
                    title="Biểu đồ Tồn kho Môi trường",
                    color="Tổng tồn",
                    color_continuous_scale="Greens"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                st.markdown("#### 📋 Chi tiết từng lô")
                
                # Chi tiết từng lô
                df_chi_tiet = pd.read_sql_query('''
                    SELECT 
                        ma_lo AS "Mã lô",
                        ten_moi_truong AS "Loại",
                        ngay_do AS "Ngày đổ",
                        tuan_do AS "Tuần",
                        so_luong_ban_dau AS "Số lượng đổ",
                        so_luong_con_lai AS "Còn lại",
                        ROUND(CAST(so_luong_con_lai AS FLOAT) / so_luong_ban_dau * 100, 1) AS "% Còn",
                        vi_tri_kho AS "Vị trí",
                        nguoi_do AS "Người đổ"
                    FROM kho_moi_truong
                    WHERE so_luong_con_lai > 0
                    ORDER BY ngay_do ASC
                ''', conn)
                
                # Tính số tuần đã lưu kho
                df_chi_tiet['Tuần lưu'] = df_chi_tiet['Ngày đổ'].apply(
                    lambda x: (datetime.now() - datetime.strptime(x, "%Y-%m-%d")).days // 7
                )
                
                # Highlight môi trường cũ (> 8 tuần)
                def highlight_old(row):
                    if row['Tuần lưu'] > 8:
                        return ['background-color: #fff3cd'] * len(row)
                    elif row['% Còn'] < 20:
                        return ['background-color: #f8d7da'] * len(row)
                    return [''] * len(row)
                
                styled_df = df_chi_tiet.style.apply(highlight_old, axis=1)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
                # Cảnh báo
                df_canh_bao = df_chi_tiet[df_chi_tiet['Tuần lưu'] > 8]
                if len(df_canh_bao) > 0:
                    st.warning(f"⚠️ **{len(df_canh_bao)} lô đã lưu kho quá lâu (> 8 tuần)**. Nên sử dụng sớm để đảm bảo chất lượng!")
                
                df_sap_het = df_chi_tiet[df_chi_tiet['% Còn'] < 20]
                if len(df_sap_het) > 0:
                    st.info(f"💡 **{len(df_sap_het)} lô sắp hết** (< 20% còn lại). Cần đổ thêm!")
            else:
                st.info("ℹ️ Chưa có môi trường trong kho. Hãy nhập kho tại tab 'Nhập kho'.")
            
            conn.close()
        
        # ========== TAB 3: LỊCH SỬ XUẤT & ĐỐI CHIẾU ==========
        with tab_lich_su:
            st.subheader("📜 Lịch sử Xuất môi trường & Đối chiếu")
            
            conn = sqlite3.connect('data.db')
            
            # ========== PHẦN 1: TỔNG HỢP NHẬP - XUẤT - TỒN ==========
            st.markdown("#### 📊 Tổng hợp Nhập - Xuất - Tồn kho")
            
            # Query tổng nhập kho theo loại
            df_nhap = pd.read_sql_query('''
                SELECT 
                    ma_so_moi_truong,
                    ten_moi_truong,
                    SUM(so_luong_ban_dau) AS tong_nhap
                FROM kho_moi_truong
                GROUP BY ma_so_moi_truong, ten_moi_truong
            ''', conn)
            
            # Query tổng xuất (từ nhật ký cấy - số túi con sử dụng)
            df_xuat = pd.read_sql_query('''
                SELECT 
                    nkc.ma_so_moi_truong_con AS ma_so_moi_truong,
                    dmt.ten_moi_truong,
                    SUM(nkc.so_tui_con) AS tong_xuat,
                    COUNT(nkc.id) AS so_lan_xuat
                FROM nhat_ky_cay nkc
                JOIN danh_muc_moi_truong dmt ON nkc.ma_so_moi_truong_con = dmt.ma_so
                GROUP BY nkc.ma_so_moi_truong_con, dmt.ten_moi_truong
            ''', conn)
            
            # Query tồn kho từ database (để tham chiếu)
            df_ton_db = pd.read_sql_query('''
                SELECT 
                    ma_so_moi_truong,
                    ten_moi_truong,
                    SUM(so_luong_con_lai) AS tong_ton_db
                FROM kho_moi_truong
                GROUP BY ma_so_moi_truong, ten_moi_truong
            ''', conn)
            
            # Merge 2 dataframes trước
            df_tong_hop = df_nhap.merge(df_xuat, on=['ma_so_moi_truong', 'ten_moi_truong'], how='left')
            
            # Fill NaN cho tổng xuất
            df_tong_hop['tong_xuat'] = df_tong_hop['tong_xuat'].fillna(0).astype(int)
            df_tong_hop['so_lan_xuat'] = df_tong_hop['so_lan_xuat'].fillna(0).astype(int)
            
            # TÍNH TỒN KHO = NHẬP - XUẤT (công thức đúng)
            df_tong_hop['tong_ton'] = df_tong_hop['tong_nhap'] - df_tong_hop['tong_xuat']
            
            # Merge với tồn kho DB để đối chiếu
            df_tong_hop = df_tong_hop.merge(df_ton_db, on=['ma_so_moi_truong', 'ten_moi_truong'], how='left')
            df_tong_hop['tong_ton_db'] = df_tong_hop['tong_ton_db'].fillna(0).astype(int)
            
            # Tính chênh lệch: So sánh tồn kho tính toán vs tồn kho trong DB
            df_tong_hop['chenh_lech'] = df_tong_hop['tong_ton'] - df_tong_hop['tong_ton_db']
            
            # Rename columns
            df_tong_hop = df_tong_hop.rename(columns={
                'ten_moi_truong': 'Loại môi trường',
                'tong_nhap': 'Tổng nhập kho',
                'tong_xuat': 'Tổng xuất (đã dùng)',
                'tong_ton': 'Tồn kho (Tính toán)',
                'tong_ton_db': 'Tồn kho (Database)',
                'so_lan_xuat': 'Số lần xuất',
                'chenh_lech': 'Chênh lệch'
            })
            
            # Hiển thị bảng với highlight
            def highlight_chenh_lech(row):
                if abs(row['Chênh lệch']) > 0:
                    return ['background-color: #fff3cd'] * len(row)
                return [''] * len(row)
            
            if len(df_tong_hop) > 0:
                styled_df = df_tong_hop[['Loại môi trường', 'Tổng nhập kho', 'Tổng xuất (đã dùng)', 'Tồn kho (Tính toán)', 'Tồn kho (Database)', 'Số lần xuất', 'Chênh lệch']].style.apply(highlight_chenh_lech, axis=1)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
                # Thông tin
                st.info("""
                📊 **Công thức:**
                - **Tồn kho (Tính toán)** = Tổng nhập kho - Tổng xuất (đã dùng)
                - **Tồn kho (Database)** = Số lượng còn lại trong từng lô kho
                - **Chênh lệch** = Tồn kho (Tính toán) - Tồn kho (Database)
                
                ✅ **Chênh lệch = 0**: Hệ thống khấu trừ chính xác
                ⚠️ **Chênh lệch ≠ 0**: Có sai lệch giữa lý thuyết và thực tế
                """)
                
                # Cảnh báo nếu có chênh lệch
                df_chenh_lech = df_tong_hop[df_tong_hop['Chênh lệch'] != 0]
                if len(df_chenh_lech) > 0:
                    st.warning(f"⚠️ **Có {len(df_chenh_lech)} loại môi trường có chênh lệch!** Có thể do dữ liệu chưa đồng bộ hoặc có lô bị mất/hỏng chưa ghi nhận.")
                else:
                    st.success("✅ **Đối chiếu chính xác!** Nhập - Xuất - Tồn khớp 100%")
            else:
                st.info("ℹ️ Chưa có dữ liệu môi trường")
            
            st.markdown("---")
            
            # ========== PHẦN 2: LỊCH SỬ XUẤT CHI TIẾT ==========
            st.markdown("#### 📋 Lịch sử Xuất chi tiết (Theo nhật ký cấy)")
            
            # Lọc theo loại môi trường
            danh_sach_loc = ['Tất cả'] + df_tong_hop['Loại môi trường'].tolist()
            loc_moi_truong = st.selectbox("Lọc theo loại môi trường:", options=danh_sach_loc, key="loc_lich_su")
            
            # Query lịch sử xuất
            if loc_moi_truong == 'Tất cả':
                query_lich_su = '''
                    SELECT 
                        nkc.ngay_cay AS "Ngày xuất",
                        nkc.tuan AS "Tuần",
                        dmt.ten_moi_truong AS "Loại môi trường",
                        nkc.nhan_vien AS "Nhân viên sử dụng",
                        nkc.ten_giong AS "Giống cây",
                        nkc.so_tui_con AS "Số túi xuất",
                        nkc.ghi_chu AS "Ghi chú"
                    FROM nhat_ky_cay nkc
                    JOIN danh_muc_moi_truong dmt ON nkc.ma_so_moi_truong_con = dmt.ma_so
                    ORDER BY nkc.ngay_cay DESC, nkc.ngay_tao DESC
                    LIMIT 500
                '''
                df_lich_su = pd.read_sql_query(query_lich_su, conn)
            else:
                # Lấy mã số từ tên
                ma_so_loc = df_tong_hop[df_tong_hop['Loại môi trường'] == loc_moi_truong]['ma_so_moi_truong'].iloc[0]
                query_lich_su = '''
                    SELECT 
                        nkc.ngay_cay AS "Ngày xuất",
                        nkc.tuan AS "Tuần",
                        dmt.ten_moi_truong AS "Loại môi trường",
                        nkc.nhan_vien AS "Nhân viên sử dụng",
                        nkc.ten_giong AS "Giống cây",
                        nkc.so_tui_con AS "Số túi xuất",
                        nkc.ghi_chu AS "Ghi chú"
                    FROM nhat_ky_cay nkc
                    JOIN danh_muc_moi_truong dmt ON nkc.ma_so_moi_truong_con = dmt.ma_so
                    WHERE nkc.ma_so_moi_truong_con = ?
                    ORDER BY nkc.ngay_cay DESC, nkc.ngay_tao DESC
                    LIMIT 500
                '''
                df_lich_su = pd.read_sql_query(query_lich_su, conn, params=(ma_so_loc,))
            
            if len(df_lich_su) > 0:
                st.info(f"📊 Hiển thị **{len(df_lich_su)}** lần xuất gần nhất")
                st.dataframe(df_lich_su, use_container_width=True, hide_index=True)
                
                # Thống kê theo nhân viên
                st.markdown("---")
                st.markdown("#### 👥 Thống kê xuất theo Nhân viên")
                
                df_thong_ke_nv = df_lich_su.groupby('Nhân viên sử dụng').agg({
                    'Số túi xuất': 'sum',
                    'Ngày xuất': 'count'
                }).reset_index()
                df_thong_ke_nv.columns = ['Nhân viên', 'Tổng túi đã dùng', 'Số lần xuất']
                df_thong_ke_nv = df_thong_ke_nv.sort_values('Tổng túi đã dùng', ascending=False)
                
                col_table, col_chart = st.columns([1, 2])
                
                with col_table:
                    st.dataframe(df_thong_ke_nv, use_container_width=True, hide_index=True)
                
                with col_chart:
                    fig = px.bar(
                        df_thong_ke_nv,
                        x='Nhân viên',
                        y='Tổng túi đã dùng',
                        title='Biểu đồ Sử dụng Môi trường theo Nhân viên',
                        color='Tổng túi đã dùng',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("ℹ️ Chưa có lịch sử xuất môi trường. Hãy bắt đầu nhập liệu cấy!")
            
            st.markdown("---")
            
            # ========== PHẦN 3: CHI TIẾT TỒN KHO TỪNG LÔ ==========
            st.markdown("#### 📦 Chi tiết Tồn kho từng Lô")
            
            df_lo = pd.read_sql_query('''
                SELECT 
                    ma_lo AS "Mã lô",
                    ten_moi_truong AS "Loại",
                    ngay_do AS "Ngày đổ",
                    so_luong_ban_dau AS "Số lượng đổ",
                    (so_luong_ban_dau - so_luong_con_lai) AS "Đã xuất",
                    so_luong_con_lai AS "Còn lại",
                    ROUND(CAST(so_luong_con_lai AS FLOAT) / so_luong_ban_dau * 100, 1) AS "% Còn",
                    vi_tri_kho AS "Vị trí"
                FROM kho_moi_truong
                WHERE so_luong_ban_dau > 0
                ORDER BY ten_moi_truong, ngay_do ASC
            ''', conn)
            
            if len(df_lo) > 0:
                # Highlight lô sắp hết
                def highlight_lo(row):
                    if row['Còn lại'] == 0:
                        return ['background-color: #f8d7da'] * len(row)  # Đỏ nhạt - hết
                    elif row['% Còn'] < 20:
                        return ['background-color: #fff3cd'] * len(row)  # Vàng - sắp hết
                    return [''] * len(row)
                
                styled_df_lo = df_lo.style.apply(highlight_lo, axis=1)
                st.dataframe(styled_df_lo, use_container_width=True, hide_index=True)
                
                # Thống kê
                so_lo_het = len(df_lo[df_lo['Còn lại'] == 0])
                so_lo_sap_het = len(df_lo[(df_lo['Còn lại'] > 0) & (df_lo['% Còn'] < 20)])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tổng số lô", len(df_lo))
                with col2:
                    st.metric("Lô đã hết", so_lo_het, delta=None)
                with col3:
                    st.metric("Lô sắp hết (< 20%)", so_lo_sap_het, delta=None)
                
                if so_lo_het > 0:
                    st.info(f"💡 **{so_lo_het} lô đã hết** (nền đỏ). Có thể xóa khỏi kho hoặc lưu lại để đối chiếu.")
                if so_lo_sap_het > 0:
                    st.warning(f"⚠️ **{so_lo_sap_het} lô sắp hết** (nền vàng). Cần đổ thêm môi trường!")
            else:
                st.info("ℹ️ Chưa có lô môi trường nào trong kho")
            
            conn.close()
            
            # Hướng dẫn
            with st.expander("💡 Hướng dẫn đọc báo cáo"):
                st.markdown("""
                **Tổng hợp Nhập - Xuất - Tồn:**
                - **Tổng nhập kho**: Tổng số túi môi trường đã đổ và nhập kho
                - **Tổng xuất (đã dùng)**: Số túi đã sử dụng trong quá trình cấy
                - **Tồn kho hiện tại**: Số túi còn lại trong kho
                - **Chênh lệch**: Nếu = 0 → Đối chiếu chính xác. Nếu ≠ 0 → Cần kiểm tra
                
                **Lịch sử Xuất chi tiết:**
                - Xem chi tiết từng lần xuất: Ngày, Nhân viên, Số lượng
                - Lọc theo loại môi trường để xem chi tiết
                - Thống kê theo nhân viên để biết ai dùng nhiều nhất
                
                **Chi tiết Tồn kho từng Lô:**
                - 🔴 Nền đỏ: Lô đã hết
                - 🟡 Nền vàng: Lô còn < 20% (sắp hết)
                - ⚪ Không màu: Lô còn đủ
                
                **Lợi ích:**
                - ✅ Đối chiếu chính xác nhập - xuất - tồn
                - ✅ Phát hiện sai lệch, thất thoát
                - ✅ Theo dõi hiệu quả sử dụng môi trường
                - ✅ Dự báo nhu cầu đổ môi trường
                """)
    
    # ========== TRANG QUẢN LÝ DANH MỤC (CHỈ ADMIN) ==========
    elif menu == "Quản lý danh mục" and is_admin:
        st.header("⚙️ Quản lý danh mục")
        st.markdown("---")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌿 Tên giống", "🔄 Chu kỳ", "🔢 Mã tình trạng", "🧪 Môi trường", "📦 Giàn/Kệ", "🏪 Vị trí Kho"])
        
        # Tab Tên giống
        with tab1:
            st.subheader("🌿 Quản lý Tên giống")
            
            danh_sach_ten_giong = get_danh_sach_ten_giong()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📋 Danh sách hiện tại")
                if len(danh_sach_ten_giong) > 0:
                    df_tg = pd.DataFrame({'Tên giống': danh_sach_ten_giong})
                    st.dataframe(df_tg, use_container_width=True, hide_index=True)
                else:
                    st.warning("⚠️ Chưa có tên giống nào.")
            
            with col2:
                st.markdown("#### ➕ Thêm mới")
                with st.form("form_them_ten_giong", clear_on_submit=True):
                    ten_giong_moi = st.text_input("Tên giống", key="them_tg")
                    submitted = st.form_submit_button("➕ Thêm", use_container_width=True)
                    
                    if submitted and ten_giong_moi.strip():
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        try:
                            c.execute('''
                                INSERT INTO danh_muc_ten_giong (ten_giong, ngay_tao)
                                VALUES (?, ?)
                            ''', (ten_giong_moi.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            conn.commit()
                            conn.close()
                            st.success(f"✅ Đã thêm: {ten_giong_moi.strip()}")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            conn.close()
                            st.error("❌ Đã tồn tại!")
            
            st.markdown("---")
            st.markdown("#### 🗑️ Xóa")
            if len(danh_sach_ten_giong) > 0:
                with st.form("form_xoa_ten_giong", clear_on_submit=True):
                    ten_giong_xoa = st.selectbox("Chọn tên giống cần xóa", options=danh_sach_ten_giong, key="xoa_tg")
                    submitted = st.form_submit_button("🗑️ Xóa", use_container_width=True)
                    
                    if submitted:
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        c.execute('DELETE FROM danh_muc_ten_giong WHERE ten_giong = ?', (ten_giong_xoa,))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Đã xóa: {ten_giong_xoa}")
                        st.rerun()
        
        # Tab Chu kỳ
        with tab2:
            st.subheader("🔄 Quản lý Chu kỳ")
            
            danh_sach_chu_ky = get_danh_sach_chu_ky()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📋 Danh sách hiện tại")
                if len(danh_sach_chu_ky) > 0:
                    df_ck = pd.DataFrame({'Chu kỳ': danh_sach_chu_ky})
                    st.dataframe(df_ck, use_container_width=True, hide_index=True)
                else:
                    st.warning("⚠️ Chưa có chu kỳ nào.")
            
            with col2:
                st.markdown("#### ➕ Thêm mới")
                with st.form("form_them_chu_ky", clear_on_submit=True):
                    chu_ky_moi = st.text_input("Chu kỳ", key="them_ck")
                    submitted = st.form_submit_button("➕ Thêm", use_container_width=True)
                    
                    if submitted and chu_ky_moi.strip():
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        try:
                            c.execute('''
                                INSERT INTO danh_muc_chu_ky (chu_ky, ngay_tao)
                                VALUES (?, ?)
                            ''', (chu_ky_moi.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            conn.commit()
                            conn.close()
                            st.success(f"✅ Đã thêm: {chu_ky_moi.strip()}")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            conn.close()
                            st.error("❌ Đã tồn tại!")
            
            st.markdown("---")
            st.markdown("#### 🗑️ Xóa")
            if len(danh_sach_chu_ky) > 0:
                with st.form("form_xoa_chu_ky", clear_on_submit=True):
                    chu_ky_xoa = st.selectbox("Chọn chu kỳ cần xóa", options=danh_sach_chu_ky, key="xoa_ck")
                    submitted = st.form_submit_button("🗑️ Xóa", use_container_width=True)
                    
                    if submitted:
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        c.execute('DELETE FROM danh_muc_chu_ky WHERE chu_ky = ?', (chu_ky_xoa,))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Đã xóa: {chu_ky_xoa}")
                        st.rerun()
        
        # Tab Mã tình trạng - ĐƠN GIẢN HÓA TRIỆT ĐỂ
        with tab3:
            st.subheader("🔢 Quản lý Mã tình trạng")
            st.caption("Chỉ quản lý mã số 3 chữ số (VD: 101, 201, 301, 305, 209...)")
            
            # Lấy danh sách hiện tại
            danh_sach_ma = get_danh_sach_ma_tinh_trang()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📋 Danh sách hiện tại")
                if len(danh_sach_ma) > 0:
                    df_ma_simple = pd.DataFrame({'Mã số': danh_sach_ma})
                    st.dataframe(df_ma_simple, use_container_width=True, hide_index=True)
                else:
                    st.warning("⚠️ Chưa có mã tình trạng nào. Hãy thêm mới!")
            
            with col2:
                st.markdown("#### ➕ Thêm mới")
                with st.form("form_them_ma_tinh_trang", clear_on_submit=True):
                    ma_so_moi = st.number_input(
                        "Mã số (3 chữ số) *",
                        min_value=100,
                        max_value=999,
                        value=301,
                        step=1,
                        help="Nhập mã số 3 chữ số (100-999)"
                    )
                    
                    submitted = st.form_submit_button("➕ Thêm", use_container_width=True, type="primary")
                    
                    if submitted:
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        try:
                            c.execute('''
                                INSERT INTO danh_muc_ma_tinh_trang (ma_so, ngay_tao)
                                VALUES (?, ?)
                            ''', (ma_so_moi, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            conn.commit()
                            conn.close()
                            st.success(f"✅ Đã thêm: Mã {ma_so_moi}")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            conn.close()
                            st.error(f"❌ Mã {ma_so_moi} đã tồn tại!")
            
            st.markdown("---")
            st.markdown("#### 🗑️ Xóa")
            if len(danh_sach_ma) > 0:
                with st.form("form_xoa_ma_tinh_trang", clear_on_submit=True):
                    ma_xoa = st.selectbox("Chọn mã cần xóa", options=danh_sach_ma)
                    submitted = st.form_submit_button("🗑️ Xóa", use_container_width=True)
                    
                    if submitted:
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        c.execute('DELETE FROM danh_muc_ma_tinh_trang WHERE ma_so = ?', (ma_xoa,))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Đã xóa: Mã {ma_xoa}")
                        st.rerun()
        
        # Tab Môi trường
        with tab4:
            st.subheader("🧪 Quản lý Môi trường")
            
            # Lấy danh sách môi trường với mã số
            conn = sqlite3.connect('data.db')
            df_mt_full = pd.read_sql_query('SELECT ma_so, ten_moi_truong FROM danh_muc_moi_truong ORDER BY ma_so', conn)
            conn.close()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📋 Danh sách hiện tại")
                if len(df_mt_full) > 0:
                    st.dataframe(df_mt_full, use_container_width=True, hide_index=True)
                else:
                    st.warning("⚠️ Chưa có môi trường nào.")
            
            with col2:
                st.markdown("#### ➕ Thêm mới")
                with st.form("form_them_moi_truong", clear_on_submit=True):
                    ma_so_moi = st.number_input(
                        "Mã số *",
                        min_value=1,
                        value=1,
                        step=1,
                        key="ma_so_mt"
                    )
                    ten_moi_truong_moi = st.text_input("Tên môi trường *", key="ten_mt")
                    submitted = st.form_submit_button("➕ Thêm", use_container_width=True)
                    
                    if submitted:
                        if ten_moi_truong_moi.strip():
                            conn = sqlite3.connect('data.db')
                            c = conn.cursor()
                            try:
                                c.execute('''
                                    INSERT INTO danh_muc_moi_truong (ma_so, ten_moi_truong, ngay_tao)
                                    VALUES (?, ?, ?)
                                ''', (ma_so_moi, ten_moi_truong_moi.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                conn.commit()
                                conn.close()
                                st.success(f"✅ Đã thêm: Mã {ma_so_moi} - {ten_moi_truong_moi.strip()}")
                                st.rerun()
                            except sqlite3.IntegrityError:
                                conn.close()
                                st.error("❌ Mã số hoặc tên môi trường đã tồn tại!")
                        else:
                            st.warning("⚠️ Vui lòng nhập tên môi trường!")
            
            st.markdown("---")
            
            # ========== CẬP NHẬT THEO BẢNG ==========
            st.markdown("#### 📊 Cập nhật theo bảng (Nhiều môi trường cùng lúc)")
            
            with st.expander("📝 Hướng dẫn nhập dữ liệu", expanded=False):
                st.markdown("""
                **Cách 1:** Chỉ nhập mã số (mỗi dòng một mã số)
                ```
                803
                821
                841
                ```
                
                **Cách 2:** Nhập mã số và tên môi trường (mã số, tên)
                ```
                803, MS + BAP 0.5
                821, MS + NAA 0.1
                841, MS + IBA 0.2
                ```
                
                **Lưu ý:** 
                - Mỗi dòng là một môi trường
                - Nếu chỉ nhập mã số, tên môi trường sẽ tự động là "Môi trường [mã số]"
                - Mã số trùng sẽ được bỏ qua hoặc cập nhật tên mới
                """)
            
            # Nút tải file mẫu (đặt ngoài form)
            col_btn_sample, _ = st.columns([1, 3])
            with col_btn_sample:
                sample_data = "803, MS + BAP 0.5\n821, MS + NAA 0.1\n841, MS + IBA 0.2"
                st.download_button(
                    label="📥 Tải file mẫu",
                    data=sample_data,
                    file_name="mau_moi_truong.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with st.form("form_cap_nhat_bang", clear_on_submit=True):
                danh_sach_moi_truong_text = st.text_area(
                    "Nhập danh sách môi trường",
                    placeholder="803\n821\n841\n\nHoặc:\n803, MS + BAP 0.5\n821, MS + NAA 0.1\n841, MS + IBA 0.2",
                    height=200,
                    key="bang_mt"
                )
                
                submitted_bang = st.form_submit_button("💾 Cập nhật từ bảng", use_container_width=True)
                
                if submitted_bang:
                    if danh_sach_moi_truong_text.strip():
                        lines = [line.strip() for line in danh_sach_moi_truong_text.strip().split('\n') if line.strip()]
                        
                        if len(lines) > 0:
                            conn = sqlite3.connect('data.db')
                            c = conn.cursor()
                            
                            thanh_cong = 0
                            loi = 0
                            cap_nhat = 0
                            bo_qua = 0
                            errors = []
                            
                            for line in lines:
                                try:
                                    # Kiểm tra format: mã số, tên hoặc chỉ mã số
                                    if ',' in line:
                                        parts = line.split(',', 1)
                                        ma_so = int(parts[0].strip())
                                        ten_mt = parts[1].strip()
                                    else:
                                        ma_so = int(line.strip())
                                        ten_mt = f"Môi trường {ma_so}"
                                    
                                    # Kiểm tra xem mã số đã tồn tại chưa
                                    c.execute('SELECT COUNT(*) FROM danh_muc_moi_truong WHERE ma_so = ?', (ma_so,))
                                    exists = c.fetchone()[0] > 0
                                    
                                    if exists:
                                        # Cập nhật tên môi trường
                                        c.execute('''
                                            UPDATE danh_muc_moi_truong 
                                            SET ten_moi_truong = ?, ngay_tao = ?
                                            WHERE ma_so = ?
                                        ''', (ten_mt, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ma_so))
                                        cap_nhat += 1
                                    else:
                                        # Thêm mới
                                        c.execute('''
                                            INSERT INTO danh_muc_moi_truong (ma_so, ten_moi_truong, ngay_tao)
                                            VALUES (?, ?, ?)
                                        ''', (ma_so, ten_mt, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                        thanh_cong += 1
                                        
                                except ValueError:
                                    loi += 1
                                    errors.append(f"Dòng không hợp lệ: {line}")
                                except sqlite3.IntegrityError:
                                    bo_qua += 1
                                except Exception as e:
                                    loi += 1
                                    errors.append(f"Lỗi ở dòng '{line}': {str(e)}")
                            
                            conn.commit()
                            conn.close()
                            
                            # Hiển thị kết quả
                            if thanh_cong > 0 or cap_nhat > 0:
                                st.success(f"✅ Đã cập nhật thành công!")
                                st.info(f"📊 Kết quả: {thanh_cong} mới, {cap_nhat} cập nhật, {bo_qua} bỏ qua, {loi} lỗi")
                            
                            if loi > 0:
                                st.warning(f"⚠️ Có {loi} lỗi:")
                                for error in errors:
                                    st.text(error)
                            
                            if thanh_cong > 0 or cap_nhat > 0:
                                st.rerun()
                        else:
                            st.warning("⚠️ Vui lòng nhập ít nhất một môi trường!")
                    else:
                        st.warning("⚠️ Vui lòng nhập danh sách môi trường!")
            
            st.markdown("---")
            
            # ========== XÓA MÔI TRƯỜNG ==========
            tab_xoa1, tab_xoa2 = st.tabs(["🗑️ Xóa đơn lẻ", "🗑️🗑️ Xóa nhiều"])
            
            with tab_xoa1:
                st.markdown("#### 🗑️ Xóa một môi trường")
                if len(df_mt_full) > 0:
                    with st.form("form_xoa_moi_truong", clear_on_submit=True):
                        danh_sach_mt_xoa = [f"Mã {row['ma_so']} - {row['ten_moi_truong']}" for _, row in df_mt_full.iterrows()]
                        moi_truong_xoa = st.selectbox("Chọn môi trường cần xóa", options=danh_sach_mt_xoa, key="xoa_mt")
                        submitted = st.form_submit_button("🗑️ Xóa môi trường này", use_container_width=True)
                        
                        if submitted:
                            # Lấy mã số từ chuỗi đã chọn
                            ma_so_xoa = int(moi_truong_xoa.split(" - ")[0].replace("Mã ", ""))
                            conn = sqlite3.connect('data.db')
                            c = conn.cursor()
                            c.execute('DELETE FROM danh_muc_moi_truong WHERE ma_so = ?', (ma_so_xoa,))
                            conn.commit()
                            conn.close()
                            st.success(f"✅ Đã xóa: {moi_truong_xoa}")
                            st.rerun()
                else:
                    st.info("ℹ️ Không có môi trường nào để xóa.")
            
            with tab_xoa2:
                st.markdown("#### 🗑️🗑️ Xóa nhiều môi trường cùng lúc")
                if len(df_mt_full) > 0:
                    with st.form("form_xoa_nhieu_moi_truong", clear_on_submit=True):
                        st.markdown("**Chọn các môi trường cần xóa:**")
                        
                        # Tạo checkbox cho mỗi môi trường
                        danh_sach_ma_so_xoa = []
                        for _, row in df_mt_full.iterrows():
                            ma_so = row['ma_so']
                            ten_mt = row['ten_moi_truong']
                            if st.checkbox(f"Mã {ma_so} - {ten_mt}", key=f"xoa_check_{ma_so}"):
                                danh_sach_ma_so_xoa.append(ma_so)
                        
                        submitted_nhieu = st.form_submit_button("🗑️ Xóa các môi trường đã chọn", use_container_width=True)
                        
                        if submitted_nhieu:
                            if len(danh_sach_ma_so_xoa) > 0:
                                conn = sqlite3.connect('data.db')
                                c = conn.cursor()
                                
                                ten_da_xoa = []
                                for ma_so in danh_sach_ma_so_xoa:
                                    # Lấy tên môi trường trước khi xóa
                                    c.execute('SELECT ten_moi_truong FROM danh_muc_moi_truong WHERE ma_so = ?', (ma_so,))
                                    result = c.fetchone()
                                    if result:
                                        ten_da_xoa.append(f"Mã {ma_so} - {result[0]}")
                                    
                                    c.execute('DELETE FROM danh_muc_moi_truong WHERE ma_so = ?', (ma_so,))
                                
                                conn.commit()
                                conn.close()
                                
                                st.success(f"✅ Đã xóa {len(danh_sach_ma_so_xoa)} môi trường:")
                                for ten in ten_da_xoa:
                                    st.text(f"  • {ten}")
                                st.rerun()
                            else:
                                st.warning("⚠️ Vui lòng chọn ít nhất một môi trường để xóa!")
                else:
                    st.info("ℹ️ Không có môi trường nào để xóa.")
        
        # TAB 5: QUẢN LÝ GIÀN/KỆ PHÒNG SÁNG
        with tab5:
            st.subheader("📦 Quản lý Giàn/Kệ Phòng Sáng")
            
            danh_sach_gian_ke = get_danh_sach_gian_ke()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📋 Danh sách hiện tại")
                if len(danh_sach_gian_ke) > 0:
                    # Hiển thị dạng bảng với thông tin chi tiết
                    conn = sqlite3.connect('data.db')
                    df_gk = pd.read_sql_query('''
                        SELECT so_gian_ke AS "Số Giàn/Kệ", 
                               ghi_chu AS "Ghi chú",
                               ngay_tao AS "Ngày tạo"
                        FROM danh_muc_gian_ke 
                        ORDER BY so_gian_ke
                    ''', conn)
                    conn.close()
                    st.dataframe(df_gk, use_container_width=True, hide_index=True)
                else:
                    st.warning("⚠️ Chưa có giàn/kệ nào.")
            
            with col2:
                st.markdown("#### ➕ Thêm mới")
                with st.form("form_them_gian_ke", clear_on_submit=True):
                    so_gian_ke_moi = st.text_input(
                        "Số Giàn/Kệ *", 
                        placeholder="VD: Giàn A1, Kệ B2",
                        key="them_gk"
                    )
                    ghi_chu_gk = st.text_input(
                        "Ghi chú",
                        placeholder="VD: Phòng sáng tầng 1",
                        key="ghi_chu_gk"
                    )
                    submitted = st.form_submit_button("➕ Thêm", use_container_width=True)
                    
                    if submitted and so_gian_ke_moi.strip():
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        try:
                            c.execute('''
                                INSERT INTO danh_muc_gian_ke (so_gian_ke, ghi_chu, ngay_tao)
                                VALUES (?, ?, ?)
                            ''', (so_gian_ke_moi.strip(), ghi_chu_gk.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            conn.commit()
                            st.success(f"✅ Đã thêm: {so_gian_ke_moi}")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error(f"❌ Giàn/Kệ '{so_gian_ke_moi}' đã tồn tại!")
                        finally:
                            conn.close()
            
            st.markdown("---")
            st.markdown("#### 🗑️ Xóa")
            if len(danh_sach_gian_ke) > 0:
                with st.form("form_xoa_gian_ke", clear_on_submit=True):
                    gk_xoa = st.selectbox(
                        "Chọn giàn/kệ cần xóa", 
                        options=danh_sach_gian_ke, 
                        key="xoa_gk"
                    )
                    submitted = st.form_submit_button("🗑️ Xóa", use_container_width=True)
                    
                    if submitted:
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        c.execute('DELETE FROM danh_muc_gian_ke WHERE so_gian_ke = ?', (gk_xoa,))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Đã xóa: {gk_xoa}")
                        st.rerun()
            else:
                st.info("Không có giàn/kệ để xóa")
            
            # Hướng dẫn sử dụng
            with st.expander("💡 Hướng dẫn sử dụng"):
                st.markdown("""
                **Giàn/Kệ Phòng Sáng** là vị trí lưu trữ các túi cây trong phòng nuôi.
                
                **Ví dụ đặt tên:**
                - `Giàn A1`, `Giàn A2`, `Giàn A3`...
                - `Kệ B1`, `Kệ B2`, `Kệ B3`...
                - `Phòng 1 - Giàn 01`
                - `Tầng 2 - Kệ Trái`
                
                **Lợi ích:**
                - ✅ Dễ dàng chọn từ danh sách thay vì nhập tay
                - ✅ Tránh lỗi chính tả
                - ✅ Thống kê chính xác số túi trên mỗi giàn
                - ✅ Quản lý kiểm kê hiệu quả
                """)
        
        # TAB 6: QUẢN LÝ VỊ TRÍ KHO MÔI TRƯỜNG
        with tab6:
            st.subheader("🏪 Quản lý Vị trí Kho Môi trường")
            
            danh_sach_vi_tri_kho = get_danh_sach_vi_tri_kho()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📋 Danh sách hiện tại")
                if len(danh_sach_vi_tri_kho) > 0:
                    conn = sqlite3.connect('data.db')
                    df_vtk = pd.read_sql_query('''
                        SELECT vi_tri_kho AS "Vị trí kho", 
                               ghi_chu AS "Ghi chú",
                               ngay_tao AS "Ngày tạo"
                        FROM danh_muc_vi_tri_kho 
                        ORDER BY vi_tri_kho
                    ''', conn)
                    conn.close()
                    st.dataframe(df_vtk, use_container_width=True, hide_index=True)
                else:
                    st.warning("⚠️ Chưa có vị trí kho nào.")
            
            with col2:
                st.markdown("#### ➕ Thêm mới")
                with st.form("form_them_vi_tri_kho", clear_on_submit=True):
                    vi_tri_kho_moi = st.text_input(
                        "Vị trí kho *", 
                        placeholder="VD: Kho A1, Kệ MT tầng 2",
                        key="them_vtk"
                    )
                    ghi_chu_vtk = st.text_input(
                        "Ghi chú",
                        placeholder="VD: Kho lạnh môi trường",
                        key="ghi_chu_vtk"
                    )
                    submitted = st.form_submit_button("➕ Thêm", use_container_width=True)
                    
                    if submitted and vi_tri_kho_moi.strip():
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        try:
                            c.execute('''
                                INSERT INTO danh_muc_vi_tri_kho (vi_tri_kho, ghi_chu, ngay_tao)
                                VALUES (?, ?, ?)
                            ''', (vi_tri_kho_moi.strip(), ghi_chu_vtk.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            conn.commit()
                            st.success(f"✅ Đã thêm: {vi_tri_kho_moi}")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error(f"❌ Vị trí kho '{vi_tri_kho_moi}' đã tồn tại!")
                        finally:
                            conn.close()
            
            st.markdown("---")
            st.markdown("#### 🗑️ Xóa")
            if len(danh_sach_vi_tri_kho) > 0:
                with st.form("form_xoa_vi_tri_kho", clear_on_submit=True):
                    vtk_xoa = st.selectbox(
                        "Chọn vị trí kho cần xóa", 
                        options=danh_sach_vi_tri_kho, 
                        key="xoa_vtk"
                    )
                    submitted = st.form_submit_button("🗑️ Xóa", use_container_width=True)
                    
                    if submitted:
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        c.execute('DELETE FROM danh_muc_vi_tri_kho WHERE vi_tri_kho = ?', (vtk_xoa,))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Đã xóa: {vtk_xoa}")
                        st.rerun()
            else:
                st.info("Không có vị trí kho để xóa")
            
            with st.expander("💡 Hướng dẫn"):
                st.markdown("""
                **Vị trí kho môi trường** là nơi lưu trữ các lô môi trường đã đổ.
                
                **Ví dụ:**
                - `Kho A1`, `Kho A2`
                - `Kệ môi trường tầng 1`
                - `Tủ lạnh môi trường`
                
                **Lợi ích:**
                - ✅ Dễ dàng tra cứu vị trí lô môi trường
                - ✅ Quản lý tồn kho theo từng khu vực
                - ✅ Tối ưu quy trình nhập/xuất kho
                """)
    
    # ========== TRANG QUẢN LÝ TÀI KHOẢN (CHỈ ADMIN) ==========
    elif menu == "Quản lý tài khoản" and is_admin:
        st.header("👥 Quản lý tài khoản")
        st.markdown("---")
        
        # Lấy danh sách tài khoản
        conn = sqlite3.connect('data.db')
        df_tk = pd.read_sql_query('SELECT ten_dang_nhap, ma_nhan_vien, ten_nhan_vien, quyen_han FROM tai_khoan', conn)
        conn.close()
        
        st.subheader("📋 Danh sách tài khoản")
        st.dataframe(df_tk, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("➕ Thêm tài khoản mới")
        
        with st.form("form_them_tai_khoan", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                ten_dang_nhap_moi = st.text_input("Tên đăng nhập *")
                ma_nhan_vien_moi = st.text_input("Mã nhân viên *")
            
            with col2:
                ten_nhan_vien_moi = st.text_input("Tên nhân viên *")
                quyen_han_moi = st.selectbox("Quyền hạn *", ["nhan_vien", "admin"], index=0)
            
            submitted = st.form_submit_button("➕ Thêm tài khoản", use_container_width=True)
            
            if submitted:
                if ten_dang_nhap_moi.strip() and ma_nhan_vien_moi.strip() and ten_nhan_vien_moi.strip():
                    conn = sqlite3.connect('data.db')
                    c = conn.cursor()
                    try:
                        c.execute('''
                            INSERT INTO tai_khoan (ten_dang_nhap, ma_nhan_vien, ten_nhan_vien, quyen_han, ngay_tao)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            ten_dang_nhap_moi.strip(),
                            ma_nhan_vien_moi.strip(),
                            ten_nhan_vien_moi.strip(),
                            quyen_han_moi,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ))
                        conn.commit()
                        conn.close()
                        st.success("✅ Đã thêm tài khoản thành công!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        conn.close()
                        st.error("❌ Tên đăng nhập hoặc mã nhân viên đã tồn tại!")
                else:
                    st.warning("⚠️ Vui lòng nhập đầy đủ thông tin!")
        
        st.markdown("---")
        st.subheader("🗑️ Xóa tài khoản")
        
        if len(df_tk) > 1:  # Không cho xóa nếu chỉ còn 1 tài khoản
            danh_sach_tk = df_tk[df_tk['ten_dang_nhap'] != 'admin']['ten_dang_nhap'].tolist()
            
            if len(danh_sach_tk) > 0:
                with st.form("form_xoa_tai_khoan", clear_on_submit=True):
                    tk_xoa = st.selectbox("Chọn tài khoản cần xóa", options=danh_sach_tk, key="xoa_tk")
                    submitted = st.form_submit_button("🗑️ Xóa tài khoản", use_container_width=True)
                    
                    if submitted:
                        conn = sqlite3.connect('data.db')
                        c = conn.cursor()
                        c.execute('DELETE FROM tai_khoan WHERE ten_dang_nhap = ?', (tk_xoa,))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Đã xóa tài khoản: {tk_xoa}")
                        st.rerun()
        else:
            st.info("ℹ️ Cần ít nhất 1 tài khoản trong hệ thống.")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Thông tin")
    st.sidebar.info(
        """
        **Ứng dụng Quản lý Phòng Nuôi Cấy Mô**
        
        📌 Dữ liệu được lưu tự động trong file `data.db`
        
        💡 Sử dụng menu bên trái để chuyển đổi giữa các chức năng
        """
    )

