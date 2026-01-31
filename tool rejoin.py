#!/usr/bin/env python3

import os
import sys
import time
import shutil
import subprocess
import ssl
import json
import zipfile
import glob
import urllib.request
import urllib.error
import re
import random
from urllib.parse import urlparse, parse_qs
from http.cookiejar import CookieJar

CONFIG_FILE = "roblox_tool_config.json"

KNOWN_CLONES = [
    "com.roblox.client",
    "vnx.iwr.jmv", "wue.yg.gh", "zbx.zf.uk", "tfzv.anol.bx",
    "gjw.za.pv", "ful.ym.wg", "hpxm.rhi.kozl", "mqc.dtzd.xzo",
    "zes.wli.lt", "urmz.nsl.ip", "ib.ioi.tly", "jvgn.an.bosk",
    "zf.po.nbo", "yv.vbgp.dt", "uus.ilt.wigg", "erj.khpm.cgj",        
]

DRIVE_LINK = "https://drive.usercontent.google.com/download?id=1Jf-wDNORG33u5BHV_W2QCsNbBvK5ot9k&export=download&authuser=0"

MOD_LIST = [
    {
        "name": "Arc APK (Pack 8 Versions)", 
        "url": DRIVE_LINK
    },
]

class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD}║        AUTO REJOIN | BY HTTSVB            ║{Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD}║      {Colors.GREEN}Fix lỗi Login Cookie & Kết nối{Colors.ENDC}{Colors.CYAN}       ║{Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚═══════════════════════════════════════════╝{Colors.ENDC}")
    print(f"{Colors.HEADER} ► System: Android/Termux{Colors.ENDC}")
    print("---------------------------------------------")

def log(msg, type="info"):
    if type == "error": print(f"[{Colors.FAIL}✗{Colors.ENDC}] {msg}")
    elif type == "success": print(f"[{Colors.GREEN}✓{Colors.ENDC}] {msg}")
    elif type == "warn": print(f"[{Colors.WARNING}!{Colors.ENDC}] {msg}")
    else: print(f"[*] {msg}")

def safe_input(prompt):
    sys.stdout.flush()
    try:
        return input(prompt)
    except EOFError:
        return ""

def run_cmd_safe(cmd_list):
    try:
        subprocess.run(cmd_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    except: pass

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except: pass
    return {}

def save_config(key, value):
    config = load_config()
    config[key] = value
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def delete_config_key(key):
    config = load_config()
    if key in config:
        del config[key]
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return True
    return False

def delete_all_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        return True
    return False

def change_android_id():
    print(f"\n{Colors.WARNING}>>> THAY ĐỔI ANDROID ID (HWID) <<<{Colors.ENDC}")
    if shutil.which("su") is None:
        log("Lỗi: Cần Root!", "error")
        safe_input("Enter...")
        return
    try:
        current_id = subprocess.getoutput("su -c 'settings get secure android_id'").strip()
        print(f" ► ID Hiện tại: {Colors.CYAN}{current_id}{Colors.ENDC}")
    except: current_id = "Unknown"

    print(f"\n{Colors.CYAN}Nhập ID Mới (16 ký tự Hex):{Colors.ENDC}")
    new_id = safe_input(f"[{Colors.WARNING}?{Colors.ENDC}] ID Mới: ").strip().lower()

    if len(new_id) != 16:
        log("Lỗi: ID phải đúng 16 ký tự.", "error")
        safe_input("Enter...")
        return

    try:
        cmd = f"su -c 'settings put secure android_id {new_id}'"
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        check_id = subprocess.getoutput("su -c 'settings get secure android_id'").strip()
        if check_id == new_id:
            log(f"THÀNH CÔNG! ID mới: {Colors.BOLD}{new_id}{Colors.ENDC}", "success")
        else:
            log("Thất bại.", "error")
    except Exception as e:
        log(f"Lỗi: {e}", "error")
    safe_input("\nEnter để quay lại...")

def get_user_installed_packages():
    try:
        cmd = subprocess.run(["pm", "list", "packages", "-3"], capture_output=True, text=True)
        lines = cmd.stdout.splitlines()
        pkgs = []
        ignore_prefixes = [
            "com.android", "android", "com.google", "com.samsung", "com.sec", 
            "com.facebook", "com.zing", "com.vng", "vn.zalopay", "com.miui", 
            "com.xiaomi", "com.huawei", "com.oppo", "com.vivo", "com.realme", 
            "com.oneplus", "com.termux", "com.amazon", "com.microsoft", 
            "com.spotify", "com.netflix", "com.opera", "org.mozilla", 
            "com.shopee", "com.lazada", "com.grab", "com.be", "com.gojek",
            "com.instagram", "com.twitter", "com.linkedin", "com.pinterest",
            "com.snapchat", "com.tiktok", "com.zhiliaoapp", "com.ss.android",
            "com.skype", "com.discord", "org.telegram", "com.whatsapp",
            "com.adobe", "com.office", "com.wps", "com.mt", "adguard",
            "com.og", "bin.mt", "com.android.chrome"
        ]
        for line in lines:
            pkg = line.replace("package:", "").strip()
            is_ignored = False
            for ig in ignore_prefixes:
                if pkg.startswith(ig) or ig in pkg:
                    is_ignored = True
                    break
            if "roblox" in pkg.lower() or pkg in KNOWN_CLONES:
                is_ignored = False
            if not is_ignored:
                pkgs.append(pkg)
        return pkgs
    except: return []

def force_stop_package(pkg_name):
    use_adb = os.environ.get("USE_ADB") == "1"
    try:
        if use_adb:
            run_cmd_safe(["adb", "shell", "am", "force-stop", pkg_name])
        else:
            os.system(f"su -c 'am force-stop {pkg_name}' > /dev/null 2>&1")
    except: pass

def inject_cookie(pkg_name, cookie):
    print(f"\n{Colors.WARNING}Đang nạp Cookie (Fix Permission)...{Colors.ENDC}")
    # 1. Kill App trước khi làm bất cứ gì
    force_stop_package(pkg_name)
    
    cmd_find = f"su -c 'find /data/data/{pkg_name}/shared_prefs -name \"*.xml\"'"
    try:
        res = subprocess.run(cmd_find, shell=True, capture_output=True, text=True)
        xml_files = res.stdout.splitlines()
        target_xml = None
        if not xml_files:
            log("Không tìm thấy data game. Hãy vào game 1 lần trước!", "error")
            return
        
        # Ưu tiên tìm file có tên package
        for f in xml_files:
            if pkg_name in f:
                target_xml = f
                break
        if not target_xml: target_xml = xml_files[0]
        
        # 2. Đọc nội dung file gốc
        content_bytes = subprocess.check_output(f"su -c 'cat {target_xml}'", shell=True)
        content = content_bytes.decode('utf-8', errors='ignore')

        # 3. Chỉnh sửa nội dung
        key_pattern = r'<string name="ROBLOSECURITY">.*?</string>'
        new_entry = f'<string name="ROBLOSECURITY">{cookie}</string>'
        
        if re.search(key_pattern, content):
            new_content = re.sub(key_pattern, new_entry, content)
        else:
            new_content = content.replace('</map>', f'    {new_entry}\n</map>')

        # 4. Ghi file AN TOÀN (Giữ nguyên quyền sở hữu)
        temp_file = "temp_cookie.xml"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        # Dùng lệnh cat để ghi đè nội dung thay vì cp (cp sẽ làm thay đổi chủ sở hữu file thành root)
        os.system(f"su -c 'cat {os.path.abspath(temp_file)} > {target_xml}'")
        
        os.remove(temp_file)
        
        # Kill app lần cuối để đảm bảo nó reload lại file mới
        force_stop_package(pkg_name)
        log("Thành công! Hãy mở game kiểm tra.", "success")
    except Exception as e:
        log(f"Lỗi: {e}", "error")

def handle_zip_file(zip_path, extract_to):
    try:
        if not zipfile.is_zipfile(zip_path): return []
        print(f"\n{Colors.CYAN}Đang xử lý dữ liệu...{Colors.ENDC}")
        folder_name = os.path.splitext(os.path.basename(zip_path))[0] + f"_{int(time.time())}"
        extract_path = os.path.join(extract_to, folder_name)
        if not os.path.exists(extract_path): os.makedirs(extract_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        apk_files = []
        for root, dirs, files in os.walk(extract_path):
            for file in files:
                if file.lower().endswith(".apk"):
                    apk_files.append(os.path.join(root, file))
        return apk_files
    except: return []

class Downloader:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        self.context = ssl._create_unverified_context()
        self.cookie_jar = CookieJar()

    def download_auto(self, url, save_dir):
        try:
            req = urllib.request.Request(url, headers=self.headers)
            https_handler = urllib.request.HTTPSHandler(context=self.context)
            cookie_processor = urllib.request.HTTPCookieProcessor(self.cookie_jar)
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler, https_handler, cookie_processor)
            
            response = opener.open(req, timeout=60)
            
            content_type = response.info().get_content_type()
            if "text/html" in content_type:
                html_content = response.read().decode('utf-8', errors='ignore')
                confirm_code = None
                match = re.search(r'confirm=([a-zA-Z0-9_\-]+)', html_content)
                if match: confirm_code = match.group(1)
                else:
                    match_input = re.search(r'name="confirm" value="([a-zA-Z0-9_\-]+)"', html_content)
                    if match_input: confirm_code = match_input.group(1)
                if confirm_code:
                    separator = "&" if "?" in url else "?"
                    url_confirm = f"{url}{separator}confirm={confirm_code}"
                    req = urllib.request.Request(url_confirm, headers=self.headers)
                    response = opener.open(req, timeout=60)
                else:
                    match_href = re.search(r'href="(\/download[^"]+)"', html_content)
                    if match_href:
                        new_path = match_href.group(1).replace('&amp;', '&')
                        confirm_url = f"https://drive.usercontent.google.com{new_path}"
                        req = urllib.request.Request(confirm_url, headers=self.headers)
                        response = opener.open(req, timeout=60)
                    else: return None 

            headers = response.info()
            filename = headers.get_filename()
            if not filename: filename = "Pack_Roblox.zip"
            if "text/html" in headers.get_content_type(): return None
            
            dest_path = os.path.join(save_dir, filename)
            try: file_size = int(headers.get("Content-Length", 0))
            except: file_size = 0
            
            print(f"\n{Colors.GREEN}Đang tải hack...{Colors.ENDC}")
            
            with open(dest_path, 'wb') as f:
                downloaded = 0
                block_sz = 32 * 1024 * 1024 
                while True:
                    buffer = response.read(block_sz)
                    if not buffer: break
                    downloaded += len(buffer)
                    f.write(buffer)
                    
                    if file_size > 0:
                        percent = downloaded * 100 / file_size
                        sys.stdout.write(f"\r{Colors.CYAN}Đang tải hack... {int(percent)}%{Colors.ENDC}")
                        sys.stdout.flush()
            
            sys.stdout.write(f"\r{Colors.CYAN}Đang tải hack... 100%{Colors.ENDC}\n")
            
            if os.path.getsize(dest_path) < 10000: return None
            return dest_path
        except Exception: return None

class App:
    def __init__(self):
        self.place_id = ""
        self.downloader = Downloader()
        self.target_packages = []
        cfg = load_config()
        self.place_id = cfg.get("place_id", "")
        self.target_packages = cfg.get("target_packages", [])
    
    def set_id(self):
        try:
            print(f"ID: {self.place_id}")
            pid = safe_input(f"[{Colors.WARNING}?{Colors.ENDC}] ID Mới: ").strip()
            if pid.isdigit(): 
                self.place_id = pid
                save_config("place_id", pid)
        except: pass

    def auto_setup_packages(self):
        print(f"\n{Colors.GREEN}>>> AUTO SETUP <<<{Colors.ENDC}")
        pkgs = get_user_installed_packages()
        if not pkgs:
            log("Không tìm thấy app!", "error")
            return
        
        found = []
        for p in pkgs:
            if p in KNOWN_CLONES or "roblox" in p.lower():
                found.append(p)
        
        if found:
            self.target_packages = found
            save_config("target_packages", self.target_packages)
            log(f"Đã lưu {len(found)} Pak.", "success")
            for p in found: print(f" - {p}")
        else:
            log("Không tìm thấy Pak phù hợp.", "warn")
        safe_input("Enter...")

    def manual_select_packages(self):
        print(f"\n{Colors.WARNING}>>> CHỌN THỦ CÔNG <<<{Colors.ENDC}")
        pkgs = get_user_installed_packages()
        if not pkgs:
            log("Trống.", "error")
            return
        for i, p in enumerate(pkgs, 1): print(f"{Colors.BOLD}{i}. {p}{Colors.ENDC}")
        raw = safe_input(f"[{Colors.CYAN}?{Colors.ENDC}] Chọn số (VD: 1 3): ").strip()
        try:
            indices = [int(x) - 1 for x in raw.split() if x.isdigit()]
            selected = [pkgs[idx] for idx in indices if 0 <= idx < len(pkgs)]
            if selected:
                self.target_packages = selected
                save_config("target_packages", self.target_packages)
                log(f"Đã lưu {len(selected)} App.", "success")
        except: pass
        safe_input("Enter...")

    def clear_pak_config(self):
        self.target_packages = []
        delete_config_key("target_packages")
        log("Đã xóa Pak.", "success")
        safe_input("Enter...")

    def clear_place_id(self):
        self.place_id = ""
        delete_config_key("place_id")
        log("Đã xóa ID.", "success")
        safe_input("Enter...")

    def clear_all_data(self):
        self.place_id = ""
        self.target_packages = []
        delete_all_config()
        log("Đã Reset toàn bộ.", "success")
        safe_input("Enter...")

    def run_auto(self):
        if not self.place_id:
            print("Chưa nhập ID Game!")
            time.sleep(1)
            return
        if not self.target_packages:
            print("Chưa chọn Pak!")
            time.sleep(1)
            return
        try: 
            delay_min = float(safe_input(f"[{Colors.WARNING}?{Colors.ENDC}] Thời gian treo (phút): ").strip() or 20)
            delay_sec = int(delay_min * 60)
        except: delay_sec = 1200 

        clear_screen()
        print(f"{Colors.GREEN}>>> AUTO FARM ĐANG CHẠY...{Colors.ENDC}")
        print(f"Game ID: {self.place_id} | Apps: {len(self.target_packages)}")
        use_adb = os.environ.get("USE_ADB") == "1"
        uri = f"roblox://placeID?placeId={self.place_id}"
        
        try:
            while True:
                for pkg in self.target_packages:
                    print(f"\n{Colors.CYAN}>>> APP: {pkg} <<<{Colors.ENDC}")
                    base_cmd = ["am", "start", "-a", "android.intent.action.VIEW", "-d", uri, "-p", pkg]
                    final_cmd = ["adb", "shell"] + base_cmd if use_adb else base_cmd
                    run_cmd_safe(final_cmd)
                    
                    remaining = delay_sec
                    while remaining > 0:
                        mins, secs = divmod(remaining, 60)
                        sys.stdout.write(f"\r[{time.strftime('%H:%M')}] Treo còn {mins:02d}:{secs:02d}   ")
                        sys.stdout.flush()
                        time.sleep(1)
                        remaining -= 1
                    
                    print(f"\n[{time.strftime('%H:%M')}] Kill App...")
                    force_stop_package(pkg)
                    time.sleep(2) 
        except KeyboardInterrupt: pass

    def run_cookie_login(self):
        if not self.target_packages: return
        print(f"\n{Colors.WARNING}>>> NẠP COOKIE (ROOT) <<<{Colors.ENDC}")
        for i, p in enumerate(self.target_packages, 1): print(f"{i}. {p}")
        try:
            idx = int(safe_input("Số: ")) - 1
            if 0 <= idx < len(self.target_packages):
                pkg = self.target_packages[idx]
                cookie = safe_input(f"[{Colors.CYAN}?{Colors.ENDC}] Cookie: ").strip()
                if cookie: inject_cookie(pkg, cookie)
        except: pass
        safe_input("Enter...")

    def install_apk(self, path):
        cmds = ["settings put global package_verifier_enable 0", "settings put global upload_apk_enable 0"]
        for c in cmds: subprocess.run(f"su -c '{c}'", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        print(f"-> Cài đặt: {Colors.BOLD}{os.path.basename(path)}{Colors.ENDC}")
        if os.environ.get("USE_ADB") == "1":
            run_cmd_safe(["adb", "install", "-r", "-g", "-d", "--bypass-low-target-sdk-block", path])
        else:
            subprocess.run(f"su -c 'pm install -r -g -d \"{path}\"'", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def process_file(self, file_path, save_path):
        if file_path.lower().endswith(".zip"):
            apk_list = handle_zip_file(file_path, save_path)
            if not apk_list:
                print("Lỗi ZIP!")
                return
            print(f"\n{Colors.WARNING}DANH SÁCH:{Colors.ENDC}")
            for i, apk in enumerate(apk_list, 1): print(f"{Colors.BOLD}{i}. {os.path.basename(apk)}{Colors.ENDC}")
            
            try:
                count_input = safe_input(f"\n[{Colors.WARNING}?{Colors.ENDC}] Nhập số lượng bản muốn cài (VD: 3): ").strip()
                count = int(count_input)
                if count <= 0: return
                if count > len(apk_list): count = len(apk_list)
                selected = apk_list[:count]
                if selected:
                    print(f"\n{Colors.GREEN}>>> CÀI ĐẶT {len(selected)} PHIÊN BẢN...{Colors.ENDC}")
                    for apk in selected:
                        self.install_apk(apk)
                        time.sleep(1)
                    print(f"\n{Colors.GREEN}Xong!{Colors.ENDC}")
            except: pass

        elif file_path.lower().endswith(".apk"):
            q = safe_input(f"[{Colors.WARNING}?{Colors.ENDC}] Cài đặt? (y/n): ").lower()
            if q == 'y': self.install_apk(file_path)

    def run_mod_menu(self):
        while True:
            print_banner()
            for i, mod in enumerate(MOD_LIST, 1): print(f"{Colors.BOLD}{i}. {mod['name']}{Colors.ENDC}")
            print(f"{Colors.BOLD}0. Quay lại{Colors.ENDC}")
            choice = safe_input(f"\n{Colors.CYAN}Chọn >> {Colors.ENDC}").strip()
            if choice == '0': return
            selected_mod = None
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(MOD_LIST): selected_mod = MOD_LIST[idx]
            except: pass
            if not selected_mod: continue
            save_path = "/sdcard/Download"
            if not os.path.exists(save_path): save_path = os.path.expanduser("~")
            file_path = self.downloader.download_auto(selected_mod["url"], save_path)
            if not file_path:
                print("Lỗi tải.")
                safe_input("Enter...")
            else: self.process_file(file_path, save_path)
            safe_input("Enter...")

    def menu(self):
        while True:
            print_banner()
            if self.place_id: print(f" ► ID: {Colors.GREEN}{self.place_id}{Colors.ENDC}")
            else: print(f" ► ID: {Colors.FAIL}(Trống){Colors.ENDC}")
            
            if self.target_packages:
                app_count = len(self.target_packages)
                app_str = f"{app_count} Apps" if app_count > 1 else self.target_packages[0]
                print(f" ► Apps: {Colors.CYAN}{app_str}{Colors.ENDC}")
            else:
                print(f" ► Apps: {Colors.FAIL}(Chưa chọn){Colors.ENDC}")
            
            print(f"{Colors.BOLD}--- CẤU HÌNH ---{Colors.ENDC}")
            print("1. Auto Setup (Tự động chọn Pak)")
            print("2. Chọn Pak Thủ Công")
            print("3. Cài đặt ID Game")
            print(f"{Colors.BOLD}--- CHỨC NĂNG ---{Colors.ENDC}")
            print("4. Chạy Auto Rejoin (Auto Kill)")
            print(f"5. Cài đặt Hack (Store)")
            print(f"6. Nạp Cookie Login (Root)")
            print(f"7. Fake HWID / Android ID (Root)")
            print(f"{Colors.BOLD}--- XÓA DỮ LIỆU ---{Colors.ENDC}")
            print("8. Xóa Pak đang lưu")
            print("9. Xóa Place ID đang lưu")
            print("10. Xóa Toàn bộ Config")
            print("0. Thoát")
            
            c = safe_input(f"\n{Colors.CYAN}Chọn >> {Colors.ENDC}").strip()
            if c == '1': self.auto_setup_packages()
            elif c == '2': self.manual_select_packages()
            elif c == '3': self.set_id()
            elif c == '4': self.run_auto()
            elif c == '5': self.run_mod_menu()
            elif c == '6': self.run_cookie_login()
            elif c == '7': change_android_id()
            elif c == '8': self.clear_pak_config()
            elif c == '9': self.clear_place_id()
            elif c == '10': self.clear_all_data()
            elif c == '0': sys.exit()

if __name__ == "__main__":
    try: app = App(); app.menu()
    except KeyboardInterrupt: pass
