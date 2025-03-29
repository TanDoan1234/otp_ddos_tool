#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Utils
Các hàm tiện ích sử dụng trong ứng dụng
"""

import random
import re
import time
import json
import os
import logging
import datetime

def validate_phone(phone):
    """
    Kiểm tra số điện thoại hợp lệ
    
    Args:
        phone: Số điện thoại cần kiểm tra
        
    Returns:
        bool: True nếu hợp lệ, False nếu không
    """
    pattern = r'^(0|\+84)(\d{9,10})$'
    return re.match(pattern, phone.strip())

def format_time(seconds):
    """
    Format thời gian từ giây sang chuỗi hh:mm:ss
    
    Args:
        seconds: Số giây
        
    Returns:
        str: Chuỗi thời gian đã format
    """
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def generate_random_user_agent():
    """
    Tạo ngẫu nhiên User-Agent
    
    Returns:
        str: User-Agent
    """
    os_list = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 6.1; Win64; x64",
        "Macintosh; Intel Mac OS X 10_15_7",
        "X11; Linux x86_64",
        "iPhone; CPU iPhone OS 14_7_1 like Mac OS X",
        "Linux; Android 11; SM-G991B"
    ]
    
    browser_list = [
        f"AppleWebKit/{random.randint(500, 600)}.{random.randint(1, 99)}",
        f"Chrome/{random.randint(70, 110)}.0.{random.randint(1000, 9999)}.{random.randint(10, 999)}",
        f"Firefox/{random.randint(70, 110)}.0",
        f"Safari/{random.randint(500, 600)}.{random.randint(1, 99)}",
        f"Edge/{random.randint(70, 110)}.0.{random.randint(1000, 9999)}.{random.randint(10, 999)}"
    ]
    
    os_choice = random.choice(os_list)
    browser_choice = random.choice(browser_list)
    
    return f"Mozilla/5.0 ({os_choice}) {browser_choice}"

def generate_random_referer():
    """
    Tạo ngẫu nhiên Referer
    
    Returns:
        str: Referer
    """
    domains = [
        "google.com",
        "facebook.com",
        "youtube.com",
        "twitter.com",
        "instagram.com",
        "tiktok.com",
        "shopee.vn",
        "lazada.vn",
        "tiki.vn",
        "vnexpress.net"
    ]
    
    protocols = ["http", "https"]
    
    domain = random.choice(domains)
    protocol = random.choice(protocols)
    
    return f"{protocol}://{domain}/"

def generate_random_cookie():
    """
    Tạo ngẫu nhiên Cookie
    
    Returns:
        str: Cookie
    """
    cookie_names = [
        "session", "token", "id", "auth", "user", "visitor",
        "consent", "locale", "lang", "theme", "device"
    ]
    
    # Tạo 2-5 cookie
    num_cookies = random.randint(2, 5)
    cookies = []
    
    for _ in range(num_cookies):
        name = random.choice(cookie_names)
        value = ''.join(random.choices('0123456789abcdef', k=16))
        cookies.append(f"{name}={value}")
    
    return "; ".join(cookies)

def export_report(file_path, stats, settings):
    """
    Xuất báo cáo kiểm thử DDoS
    
    Args:
        file_path: Đường dẫn file
        stats: Thông tin thống kê
        settings: Thông tin cài đặt
        
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Tạo dữ liệu báo cáo
        report = {
            "timestamp": time.time(),
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "title": "Báo cáo kiểm thử DDoS qua OTP",
            "metrics": {
                "total_requests": stats.get("requests_count", 0),
                "successful_requests": stats.get("success_count", 0),
                "failed_requests": stats.get("failed_count", 0),
                "ratelimited_requests": stats.get("ratelimited_count", 0),
                "requests_per_second": stats.get("requests_per_second", 0),
                "duration": stats.get("elapsed_time", 0)
            },
            "settings": settings,
            "success_rate": stats.get("success_ratio", 0) * 100
        }
        
        # Ghi ra file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Lỗi khi xuất báo cáo: {str(e)}")
        return False

def load_config(file_path):
    """
    Tải cấu hình từ file
    
    Args:
        file_path: Đường dẫn file
        
    Returns:
        dict: Cấu hình
    """
    try:
        if not os.path.exists(file_path):
            return {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi khi tải cấu hình: {str(e)}")
        return {}

def save_config(file_path, config):
    """
    Lưu cấu hình ra file
    
    Args:
        file_path: Đường dẫn file
        config: Cấu hình
        
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Lỗi khi lưu cấu hình: {str(e)}")
        return False

# Thêm class Logger mới
class Logger:
    def __init__(self):
        self.logger = logging.getLogger('OTPTool')
        self.logger.setLevel(logging.DEBUG)
        
        # Tạo thư mục logs nếu chưa tồn tại
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Log file với timestamp
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f'logs/otp_tool_{current_time}.log'
        
        # File Handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def log(self, message, level="INFO"):
        """
        Ghi log với mức độ được chỉ định
        
        Args:
            message: Nội dung log
            level: Mức độ log (INFO, WARNING, ERROR, DEBUG)
        """
        level = level.upper()
        
        if level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "DEBUG":
            self.logger.debug(message)
        elif level == "SUCCESS":  # Tùy chỉnh level
            self.logger.info(f"SUCCESS - {message}")