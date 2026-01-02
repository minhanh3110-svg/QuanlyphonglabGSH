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
    
    # Bảng danh mục Giàn/Kệ (Phòng sáng)
    c.execute('''
        CREATE TABLE IF NOT EXISTS danh_muc_gian_ke (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            so_gian_ke TEXT NOT NULL UNIQUE,
            ghi_chu TEXT,
            ngay_tao TEXT
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

def get_danh_sach_gian_ke():
    """Lấy danh sách giàn/kệ từ database"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT so_gian_ke FROM danh_muc_gian_ke ORDER BY so_gian_ke')
    result = [row[0] for row in c.fetchall()]
    conn.close()
    return result

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
    
    # Menu
    if is_admin:
        menu = st.sidebar.selectbox(
            "📋 Chọn chức năng",
            ["Nhập liệu", "In tem nhãn", "Báo cáo Năng suất", "Quản lý Phòng Sáng", "Tổng hợp Phòng Sáng", "Quản lý danh mục", "Quản lý tài khoản"]
        )
    else:
        menu = st.sidebar.selectbox(
            "📋 Chọn chức năng",
            ["Nhập liệu", "In tem nhãn", "Báo cáo Năng suất", "Quản lý Phòng Sáng"]
        )
    
    # ========== TRANG NHẬP LIỆU ==========
    if menu == "Nhập liệu":
        st.header("📝 Nhập liệu mới")
        st.markdown("---")
        
        # Lấy danh sách từ database
        danh_sach_ten_giong = get_danh_sach_ten_giong()
        danh_sach_chu_ky = get_danh_sach_chu_ky()
        danh_sach_moi_truong = get_danh_sach_moi_truong()  # Dict: mã số -> tên
        danh_sach_tinh_trang = ["Sạch", "Khuẩn nhẹ", "Khuẩn nặng", "Nấm", "Khuẩn môi trường", "Khác"]
        
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
                
                # Tự động tính tháng và tuần
                thang = ngay_cay.month
                tuan = tinh_tuan(ngay_cay)
                
                st.info(f"📆 Tháng: {thang} | Tuần: {tuan}")
                
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
                
                tinh_trang = st.selectbox(
                    "Tình trạng *",
                    options=danh_sach_tinh_trang,
                    index=0,
                    help="Chọn tình trạng cây"
                )
                
                box_cay = st.number_input(
                    "Box cấy *",
                    min_value=1,
                    value=1,
                    step=1,
                    help="Số lượng box cấy"
                )
                
                st.markdown("---")
                st.markdown("#### 👨‍🌾 Thông tin túi mẹ")
                
                so_tui_me = st.number_input(
                    "Số túi mẹ *",
                    min_value=0,
                    value=0,
                    step=1,
                    help="Số lượng túi mẹ"
                )
                
                so_cum_tui_me = st.number_input(
                    "Số cụm/túi mẹ *",
                    min_value=0,
                    value=0,
                    step=1,
                    help="Số cụm trên mỗi túi mẹ"
                )
                
                st.markdown("---")
                st.markdown("#### 🌱 Thông tin túi con")
                
                so_tui_con = st.number_input(
                    "Số túi con *",
                    min_value=0,
                    value=0,
                    step=1,
                    help="Số lượng túi con"
                )
                
                so_cum_tui_con = st.number_input(
                    "Số cụm/túi con *",
                    min_value=0,
                    value=0,
                    step=1,
                    help="Số cụm trên mỗi túi con"
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
                st.markdown("#### 👨‍🌾 Thông tin túi mẹ")
                
                so_tui_me = st.number_input(
                    "Số túi mẹ *",
                    min_value=1,
                    value=1,
                    step=1
                )
                
                so_cum_tui_me = st.number_input(
                    "Số cụm/túi mẹ *",
                    min_value=1,
                    value=1,
                    step=1
                )
                
                st.markdown("---")
                st.markdown("#### 🌱 Thông tin túi con")
                
                so_tui_con = st.number_input(
                    "Số túi con *",
                    min_value=1,
                    value=1,
                    step=1
                )
                
                so_cum_tui_con = st.number_input(
                    "Số cụm/túi con *",
                    min_value=1,
                    value=1,
                    step=1
                )
                
                st.markdown("---")
                
                st.markdown("#### 📝 Ghi chú")
                ghi_chu = st.text_area(
                    "Ghi chú",
                    placeholder="Nhập ghi chú nếu có...",
                    height=100
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
                                ngay_cay, thang, tuan, nhan_vien, ma_nhan_vien, ten_giong, chu_ky, tinh_trang,
                                box_cay, ma_so_moi_truong_me, ma_so_moi_truong_con,
                                so_tui_me, so_cum_tui_me, so_tui_con, so_cum_tui_con,
                                tong_so_cay_con, gio_bat_dau, gio_ket_thuc, tong_gio_lam, nang_suat, ghi_chu, ma_qr, ngay_tao
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            ngay_cay.strftime("%Y-%m-%d"), thang, tuan,
                            user_info['ten_nhan_vien'], user_info['ma_nhan_vien'],
                            ten_giong, chu_ky, tinh_trang, box_cay,
                            ma_so_moi_truong_me, ma_so_moi_truong_con,
                            so_tui_me, so_cum_tui_me, so_tui_con, so_cum_tui_con,
                            tong_so_cay_con,
                            gio_bat_dau.strftime("%H:%M"), gio_ket_thuc.strftime("%H:%M"),
                            tong_gio_lam, nang_suat, ghi_chu, ma_qr_unique, ngay_tao
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
                        # Khởi tạo số túi dựa trên tình trạng ban đầu
                        so_tui_sach = so_tui_con if tinh_trang == "Sạch" else 0
                        so_tui_khuan_nhe = so_tui_con if tinh_trang == "Khuẩn nhẹ" else 0
                        so_tui_khuan_nang = so_tui_con if tinh_trang == "Khuẩn nặng" else 0
                        so_tui_nam = so_tui_con if tinh_trang == "Nấm" else 0
                        so_tui_khuan_moi_truong = so_tui_con if tinh_trang == "Khuẩn môi trường" else 0
                        so_tui_khac = so_tui_con if tinh_trang == "Khác" else 0
                        
                        tong_so_tui = so_tui_con
                        tong_so_cay = so_tui_sach * so_cum_tui_con  # Chỉ tính cây sạch
                        
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
                            ten_giong, chu_ky, so_gian_ke_value, "Đang nuôi",
                            so_tui_sach, so_tui_khuan_nhe, so_tui_khuan_nang, so_tui_nam,
                            so_tui_khuan_moi_truong, so_tui_khac,
                            tong_so_tui, tong_so_cay, tuan_xuat, ngay_xuat,
                            ghi_chu, ngay_tao, ngay_tao
                        ))
                        
                        conn.commit()
                        conn.close()
                        
                        st.success("✅ Lưu dữ liệu thành công! Đã tự động tạo bản ghi trong phòng sáng.")
                        
                        # Hiển thị nút in tem
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
    
    # ========== TRANG IN TEM NHÃN ==========
    elif menu == "In tem nhãn":
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
    
    # ========== TRANG BÁO CÁO NĂNG SUẤT ==========
    elif menu == "Báo cáo Năng suất":
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
    
    # ========== TRANG QUẢN LÝ PHÒNG SÁNG ==========
    elif menu == "Quản lý Phòng Sáng":
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
    
    # ========== TRANG QUẢN LÝ DANH MỤC (CHỈ ADMIN) ==========
    elif menu == "Quản lý danh mục" and is_admin:
        st.header("⚙️ Quản lý danh mục")
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["🌿 Tên giống", "🔄 Chu kỳ", "🧪 Môi trường"])
        
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
        
        # Tab Môi trường
        with tab3:
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
        
        # TAB 4: QUẢN LÝ GIÀN/KỆ PHÒNG SÁNG
        with tab4:
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
