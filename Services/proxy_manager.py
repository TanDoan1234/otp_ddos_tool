#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Proxy Manager
Quản lý danh sách proxy
"""

import random
import time
import threading

class ProxyManager:
    """Quản lý danh sách proxy"""
    
    def __init__(self, log_callback=None):
        """
        Khởi tạo Proxy Manager
        
        Args:
            log_callback: Callback để ghi log
        """
        self.log_callback = log_callback
        self.proxies = []
        self.active_proxies = []
        self.blacklisted_proxies = []
        
        # Khóa thread
        self.lock = threading.Lock()
    
    def log(self, message):
        """
        Ghi log
        
        Args:
            message: Thông điệp cần ghi
        """
        if self.log_callback:
            self.log_callback(message)
    
    def add_proxies(self, proxy_list):
        """
        Thêm danh sách proxy
        
        Args:
            proxy_list: Danh sách proxy cần thêm
        """
        with self.lock:
            self.proxies = list(set(self.proxies + proxy_list))
            self.active_proxies = list(set(self.active_proxies + proxy_list))
            self.log(f"Đã thêm {len(proxy_list)} proxy. Tổng số: {len(self.proxies)}")
    
    def load_from_file(self, file_path):
        """
        Tải danh sách proxy từ file
        
        Args:
            file_path: Đường dẫn file chứa danh sách proxy
            
        Returns:
            int: Số lượng proxy đã tải
        """
        try:
            with open(file_path, 'r') as f:
                proxy_list = [line.strip() for line in f if line.strip()]
            
            self.add_proxies(proxy_list)
            return len(proxy_list)
        except Exception as e:
            self.log(f"Lỗi khi tải proxy từ file: {str(e)}")
            return 0
    
    def get_random_proxy(self):
        """
        Lấy một proxy ngẫu nhiên từ danh sách
        
        Returns:
            str: Proxy hoặc None nếu không có
        """
        with self.lock:
            if not self.active_proxies:
                return None
            
            return random.choice(self.active_proxies)
    
    def mark_proxy_failed(self, proxy):
        """
        Đánh dấu một proxy là hỏng
        
        Args:
            proxy: Proxy cần đánh dấu
        """
        with self.lock:
            if proxy in self.active_proxies:
                self.active_proxies.remove(proxy)
                self.blacklisted_proxies.append(proxy)
                self.log(f"Proxy {proxy} đã bị đánh dấu hỏng. Còn lại {len(self.active_proxies)} proxy hoạt động")
    
    def rotate_proxies(self):
        """
        Xoay vòng danh sách proxy
        
        Returns:
            str: Proxy được chọn
        """
        with self.lock:
            # Reset danh sách nếu cần
            if len(self.active_proxies) < len(self.proxies) / 2:
                self.active_proxies = self.proxies.copy()
                self.blacklisted_proxies = []
                self.log(f"Đã làm mới danh sách proxy. Có {len(self.active_proxies)} proxy hoạt động")
            
            return self.get_random_proxy()
    
    def find_proxies(self):
        """
        Tự động tìm proxy từ các nguồn miễn phí (demo)
        
        Returns:
            list: Danh sách proxy tìm được
        """
        # Đây là danh sách giả để demo
        self.log("Đang tìm proxy miễn phí...")
        time.sleep(1.5)  # Mô phỏng thời gian tìm kiếm
        
        demo_proxies = [
            "103.28.121.58:80",
            "103.83.232.122:80",
            "118.70.12.171:53281",
            "113.161.59.136:8080",
            "27.72.244.228:8080",
            "103.90.229.80:3128",
            "113.161.130.101:8080",
            "103.94.18.13:8088",
            "103.75.184.179:38564",
            "125.212.200.60:3128"
        ]
        
        self.add_proxies(demo_proxies)
        return demo_proxies
    
    def get_proxy_count(self):
        """
        Lấy số lượng proxy
        
        Returns:
            dict: Thông tin số lượng
        """
        with self.lock:
            return {
                "total": len(self.proxies),
                "active": len(self.active_proxies),
                "blacklisted": len(self.blacklisted_proxies)
            }