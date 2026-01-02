"""
Script tao logo mac dinh cho ung dung Quan ly Lab Nuoi Cay
Chay script nay de tao file logo.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_default_logo():
    """Tao logo mac dinh voi hinh cay va chu"""
    # Kich thuoc logo (vuong)
    size = 500
    
    # Tao anh voi nen trong suot
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Mau sac
    green_dark = (45, 80, 22)      # Xanh dam
    green_light = (86, 171, 47)    # Xanh nhat
    green_leaf = (168, 224, 99)    # Xanh la
    brown = (101, 67, 33)          # Nau (than cay)
    
    # Ve vong tron nen (gradient effect)
    center = size // 2
    for i in range(10, 0, -1):
        radius = center - 20 + (i * 5)
        alpha = int(50 - (i * 4))
        color = (*green_leaf, alpha)
        draw.ellipse([center - radius, center - radius, 
                      center + radius, center + radius], 
                     fill=color)
    
    # Ve than cay (giua)
    trunk_width = 40
    trunk_height = 180
    trunk_x = center - trunk_width // 2
    trunk_y = center + 50
    draw.rectangle([trunk_x, trunk_y, 
                    trunk_x + trunk_width, trunk_y + trunk_height],
                   fill=brown)
    
    # Ve la cay (3 tang)
    def draw_leaf_layer(y_pos, radius, color):
        """Ve mot tang la"""
        # La giua (lon nhat)
        draw.ellipse([center - radius, y_pos - radius,
                      center + radius, y_pos + radius],
                     fill=color)
        # La trai
        draw.ellipse([center - radius - 60, y_pos - radius + 30,
                      center - 60, y_pos + radius + 30],
                     fill=color)
        # La phai
        draw.ellipse([center + 60, y_pos - radius + 30,
                      center + radius + 60, y_pos + radius + 30],
                     fill=color)
    
    # Tang duoi (xanh dam)
    draw_leaf_layer(center + 80, 80, green_dark)
    
    # Tang giua (xanh trung binh)
    draw_leaf_layer(center + 20, 90, green_light)
    
    # Tang tren (xanh nhat)
    draw_leaf_layer(center - 40, 100, green_leaf)
    
    # Ve chu viet tat "LAB" o giua
    try:
        # Thu load font
        font_large = ImageFont.truetype("arialbd.ttf", 120)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fallback to default
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Ve chu "LAB" o trung tam voi outline
    text_main = "LAB"
    # Lay kich thuoc text de center
    bbox = draw.textbbox((0, 0), text_main, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = center - text_width // 2
    text_y = center - text_height // 2 - 20
    
    # Ve outline (vien)
    outline_width = 3
    for adj_x in range(-outline_width, outline_width + 1):
        for adj_y in range(-outline_width, outline_width + 1):
            draw.text((text_x + adj_x, text_y + adj_y), 
                     text_main, font=font_large, fill=(255, 255, 255, 255))
    
    # Ve chu chinh
    draw.text((text_x, text_y), text_main, 
              font=font_large, fill=green_dark)
    
    # Ve chu phu "Tissue Culture" phia duoi
    text_sub = "Tissue Culture"
    bbox_sub = draw.textbbox((0, 0), text_sub, font=font_small)
    text_sub_width = bbox_sub[2] - bbox_sub[0]
    text_sub_x = center - text_sub_width // 2
    text_sub_y = text_y + text_height + 10
    
    # Outline cho chu phu
    for adj_x in range(-2, 3):
        for adj_y in range(-2, 3):
            draw.text((text_sub_x + adj_x, text_sub_y + adj_y), 
                     text_sub, font=font_small, fill=(255, 255, 255, 200))
    
    draw.text((text_sub_x, text_sub_y), text_sub, 
              font=font_small, fill=green_light)
    
    # Ve icon la nho o 4 goc
    def draw_small_leaf(x, y, size_leaf):
        """Ve la nho trang tri"""
        draw.ellipse([x, y, x + size_leaf, y + size_leaf],
                     fill=(*green_leaf, 150))
    
    leaf_size = 30
    margin = 40
    # Goc tren trai
    draw_small_leaf(margin, margin, leaf_size)
    draw_small_leaf(margin + 15, margin + 20, leaf_size - 10)
    
    # Goc tren phai
    draw_small_leaf(size - margin - leaf_size, margin, leaf_size)
    draw_small_leaf(size - margin - leaf_size - 15, margin + 20, leaf_size - 10)
    
    # Goc duoi trai
    draw_small_leaf(margin, size - margin - leaf_size, leaf_size)
    draw_small_leaf(margin + 15, size - margin - leaf_size - 20, leaf_size - 10)
    
    # Goc duoi phai
    draw_small_leaf(size - margin - leaf_size, size - margin - leaf_size, leaf_size)
    draw_small_leaf(size - margin - leaf_size - 15, size - margin - leaf_size - 20, leaf_size - 10)
    
    # Luu file
    output_path = "logo.png"
    img.save(output_path, 'PNG')
    print(f"[OK] Da tao logo mac dinh: {output_path}")
    print(f"Kich thuoc: {size}x{size}px")
    print(f"Duong dan: {os.path.abspath(output_path)}")
    
    return output_path

if __name__ == "__main__":
    print("Dang tao logo mac dinh...")
    print("=" * 50)
    
    logo_path = create_default_logo()
    
    print("=" * 50)
    print("\nHUONG DAN:")
    print("1. File logo.png da duoc tao trong thu muc hien tai")
    print("2. Ban co the thay the bang logo cong ty cua minh")
    print("3. Dam bao file logo co:")
    print("   - Dinh dang: PNG (nen trong suot)")
    print("   - Kich thuoc: Toi thieu 500x500px")
    print("   - Ty le: Hinh vuong (1:1)")
    print("4. Doi ten logo cua ban thanh 'logo.png'")
    print("5. Khoi dong lai ung dung de thay logo moi")
    print("\nHoan tat!")


