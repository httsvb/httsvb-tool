import cv2
import numpy as np
import os
import time
import subprocess

# ==========================================
# CẤU HÌNH TOOL
# ==========================================
# Thư mục chứa các ảnh mẫu của các nút (ví dụ: nút "Chơi", "Xác nhận", ...)
IMAGE_DIR = "toolpython 1" 
# Đường dẫn tạm để lưu ảnh chụp màn hình
SCREENSHOT_PATH = "/sdcard/screen.png"
# Độ chính xác tối thiểu để xác nhận là khớp (0.8 = 80%)
THRESHOLD = 0.8 

def take_screenshot():
    """Chụp ảnh màn hình điện thoại bằng quyền root."""
    try:
        # Sử dụng su -c để chụp màn hình từ shell root
        os.system(f"su -c screencap -p {SCREENSHOT_PATH}")
        # Đọc ảnh vào OpenCV
        img = cv2.imread(SCREENSHOT_PATH)
        return img
    except Exception as e:
        print(f"[-] Lỗi khi chụp màn hình: {e}")
        return None

def click(x, y):
    """Thực hiện thao tác chạm (tap) vào tọa độ x, y."""
    print(f"[*] Đang chạm vào tọa độ: ({x}, {y})")
    os.system(f"su -c input tap {x} {y}")

def find_and_click():
    """Quét các ảnh mẫu và thực hiện ấn nếu tìm thấy."""
    # Kiểm tra thư mục ảnh mẫu
    if not os.path.exists(IMAGE_DIR):
        print(f"[-] Thư mục '{IMAGE_DIR}' không tồn tại!")
        return

    # Lấy danh sách các file ảnh trong thư mục
    templates_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not templates_files:
        print(f"[-] Không tìm thấy ảnh mẫu nào trong '{IMAGE_DIR}'")
        return

    print(f"[+] Đã tải {len(templates_files)} ảnh mẫu. Bắt đầu quét...")

    while True:
        screen = take_screenshot()
        
        if screen is None:
            print("[-] Không thể đọc ảnh màn hình. Kiểm tra quyền root và bộ nhớ.")
            time.sleep(2)
            continue

        found_any = False
        for file_name in templates_files:
            template_path = os.path.join(IMAGE_DIR, file_name)
            template = cv2.imread(template_path)
            
            if template is None:
                continue

            # Thực hiện Template Matching
            result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Nếu độ chính xác cao hơn ngưỡng quy định
            if max_val >= THRESHOLD:
                h, w = template.shape[:2]
                # Tính toán tọa độ tâm của ảnh mẫu trên màn hình
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                print(f"[!] Tìm thấy khớp: {file_name} ({int(max_val*100)}%)")
                click(center_x, center_y)
                
                # Nghỉ một lát sau khi ấn để máy kịp xử lý
                time.sleep(1.5)
                found_any = True
                # Sau khi ấn một nút, ta thoát vòng lặp for để chụp màn hình mới (tránh ấn nhầm tọa độ cũ)
                break 
        
        if not found_any:
            # Nếu không tìm thấy nút nào, nghỉ ngắn rồi quét lại
            time.sleep(0.5)

if __name__ == "__main__":
    print("==========================================")
    print("   TOOL AUTO CLICK TERMUX (ROOT ONLY)     ")
    print("      Dành cho FC Online / Game Mobile    ")
    print("==========================================")
    
    try:
        find_and_click()
    except KeyboardInterrupt:
        print("\n[!] Đã dừng tool theo yêu cầu người dùng.")
    except Exception as e:
        print(f"\n[!] Lỗi không mong muốn: {e}")
