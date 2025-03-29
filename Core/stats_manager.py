#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Stats Manager
Quản lý thống kê trong quá trình tấn công
"""

import time
import threading

class StatsManager:
    """Quản lý thống kê"""
    
    def __init__(self):
        """Khởi tạo quản lý thống kê"""
        # Thống kê cơ bản
        self.requests_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.ratelimited_count = 0
        
        # Thời gian
        self.start_time = None
        self.end_time = None
        
        # Cài đặt
        self.settings = {}
        
        # Khóa thread
        self.lock = threading.Lock()
    
    def reset_stats(self):
        """Reset thống kê"""
        with self.lock:
            self.requests_count = 0
            self.success_count = 0
            self.failed_count = 0
            self.ratelimited_count = 0
            self.start_time = time.time()
            self.end_time = None
    
    def record_request(self, success=True, ratelimited=False):
        """
        Ghi nhận một request
        
        Args:
            success: Thành công hay không
            ratelimited: Bị rate limit hay không
        """
        with self.lock:
            self.requests_count += 1
            
            if ratelimited:
                self.ratelimited_count += 1
            elif success:
                self.success_count += 1
            else:
                self.failed_count += 1
    
    def set_settings(self, settings):
        """
        Cập nhật cài đặt
        
        Args:
            settings: Cài đặt mới
        """
        with self.lock:
            self.settings = settings
    
    def end_session(self):
        """Kết thúc phiên tấn công"""
        with self.lock:
            if self.start_time and not self.end_time:
                self.end_time = time.time()
    
    def get_elapsed_time(self):
        """
        Lấy thời gian đã trôi qua
        
        Returns:
            float: Thời gian tính bằng giây
        """
        now = self.end_time if self.end_time else time.time()
        return now - (self.start_time or now)
    
    def get_stats(self):
        """
        Lấy thống kê hiện tại
        
        Returns:
            dict: Thống kê
        """
        with self.lock:
            total = max(1, self.requests_count)
            elapsed_time = self.get_elapsed_time()
            
            return {
                "requests_count": self.requests_count,
                "success_count": self.success_count,
                "failed_count": self.failed_count,
                "ratelimited_count": self.ratelimited_count,
                "success_ratio": self.success_count / total,
                "failed_ratio": self.failed_count / total,
                "ratelimited_ratio": self.ratelimited_count / total,
                "elapsed_time": elapsed_time,
                "requests_per_second": self.requests_count / max(1, elapsed_time)
            }
    
    def get_settings(self):
        """
        Lấy cài đặt
        
        Returns:
            dict: Cài đặt
        """
        with self.lock:
            return self.settings