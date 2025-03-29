#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Config
Cấu hình chung cho ứng dụng
"""

import os
import json
from .utils import load_config, save_config

class Config:
    """Quản lý cấu hình ứng dụng"""
    
    # Đường dẫn mặc định
    CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".otp_ddos_tool")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
    HISTORY_DIR = os.path.join(CONFIG_DIR, "history")
    PROXY_DIR = os.path.join(CONFIG_DIR, "proxies")
    
    # Cấu hình mặc định
    DEFAULT_CONFIG = {
        "thread_count": 1,
        "request_interval": 1000,
        "use_proxy": False,
        "auto_rotate_ip": False,
        "random_headers": True,
        "services": [
            "Viettel",
            "Shopee",
            "GHN",
            "Lottemart",
            "FPT",
            "Điện Máy",
            "Tài Chính",
            "Khác"
        ],
        "last_used_phones": [],
        "last_used_duration": 60
    }
    
    def __init__(self):
        """Khởi tạo cấu hình"""
        # Tạo thư mục cấu hình nếu chưa tồn tại
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        os.makedirs(self.HISTORY_DIR, exist_ok=True)
        os.makedirs(self.PROXY_DIR, exist_ok=True)
        
        # Tải cấu hình
        self.config = self.load_config()
    
    def load_config(self):
        """
        Tải cấu hình từ file
        
        Returns:
            dict: Cấu hình
        """
        config = load_config(self.CONFIG_FILE)
        
        # Sử dụng cấu hình mặc định nếu không tìm thấy
        if not config:
            config = self.DEFAULT_CONFIG.copy()
            self.save_config(config)
        
        return config
    
    def save_config(self, config=None):
        """
        Lưu cấu hình ra file
        
        Args:
            config: Cấu hình (nếu None thì sử dụng cấu hình hiện tại)
        
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        if config is None:
            config = self.config
        
        return save_config(self.CONFIG_FILE, config)
    
    def get(self, key, default=None):
        """
        Lấy giá trị cấu hình
        
        Args:
            key: Khóa
            default: Giá trị mặc định nếu không tìm thấy
        
        Returns:
            Giá trị cấu hình
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        Cập nhật giá trị cấu hình
        
        Args:
            key: Khóa
            value: Giá trị
        """
        self.config[key] = value
        self.save_config()
    
    def get_config(self):
        """
        Lấy toàn bộ cấu hình
        
        Returns:
            dict: Cấu hình
        """
        return self.config.copy()
    
    def update_config(self, new_config):
        """
        Cập nhật toàn bộ cấu hình
        
        Args:
            new_config: Cấu hình mới
        """
        self.config.update(new_config)
        self.save_config()
    
    def reset_config(self):
        """
        Reset cấu hình về mặc định
        
        Returns:
            dict: Cấu hình mặc định
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
        return self.config
    
    def save_history(self, stats, settings):
        """
        Lưu lịch sử tấn công
        
        Args:
            stats: Thông tin thống kê
            settings: Thông tin cài đặt
        
        Returns:
            str: Đường dẫn file lịch sử
        """
        import time
        
        # Tạo tên file theo thời gian
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.HISTORY_DIR, f"report_{timestamp}.json")
        
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
        
        # Lưu file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        
        return file_path
    
    def get_history_list(self):
        """
        Lấy danh sách lịch sử tấn công
        
        Returns:
            list: Danh sách lịch sử
        """
        history_files = os.listdir(self.HISTORY_DIR)
        history_files = [f for f in history_files if f.startswith("report_") and f.endswith(".json")]
        history_files.sort(reverse=True)  # Sắp xếp mới nhất trước
        
        history_list = []
        for file in history_files:
            file_path = os.path.join(self.HISTORY_DIR, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history_list.append({
                        "file": file,
                        "datetime": data.get("datetime", ""),
                        "total_requests": data.get("metrics", {}).get("total_requests", 0),
                        "success_rate": data.get("success_rate", 0),
                        "duration": data.get("metrics", {}).get("duration", 0),
                        "path": file_path
                    })
            except Exception as e:
                print(f"Lỗi khi đọc file lịch sử {file}: {str(e)}")
        
        return history_list
    
    def get_history(self, file_name):
        """
        Lấy thông tin chi tiết của một lịch sử tấn công
        
        Args:
            file_name: Tên file lịch sử
        
        Returns:
            dict: Thông tin lịch sử
        """
        file_path = os.path.join(self.HISTORY_DIR, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi khi đọc file lịch sử {file_name}: {str(e)}")
            return {}
    
    def save_proxy_list(self, name, proxy_list):
        """
        Lưu danh sách proxy
        
        Args:
            name: Tên danh sách
            proxy_list: Danh sách proxy
        
        Returns:
            str: Đường dẫn file
        """
        file_path = os.path.join(self.PROXY_DIR, f"{name}.txt")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(proxy_list))
        
        return file_path
    
    def get_proxy_lists(self):
        """
        Lấy danh sách các file proxy
        
        Returns:
            list: Danh sách tên file
        """
        proxy_files = os.listdir(self.PROXY_DIR)
        proxy_files = [f for f in proxy_files if f.endswith(".txt")]
        return proxy_files
    
    def load_proxy_list(self, name):
        """
        Tải danh sách proxy từ file
        
        Args:
            name: Tên danh sách (tên file không bao gồm .txt)
        
        Returns:
            list: Danh sách proxy
        """
        if not name.endswith(".txt"):
            name += ".txt"
        
        file_path = os.path.join(self.PROXY_DIR, name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Lỗi khi đọc file proxy {name}: {str(e)}")
            return []