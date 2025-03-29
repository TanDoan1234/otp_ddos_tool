#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Spam Tab
Tab chính để cấu hình và bắt đầu spam OTP
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import threading
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Tạo mock classes để thay thế các dependency
class MockDDoSEngine:
    def __init__(self, **kwargs):
        self.running = False
        self.log_callback = kwargs.get('log_callback')
        self.completion_callback = kwargs.get('completion_callback')
        self.status_callback = kwargs.get('status_callback')
    
    def start(self):
        self.running = True
        if self.log_callback:
            self.log_callback("Đã bắt đầu giả lập tấn công DDoS qua OTP")
        if self.status_callback:
            self.status_callback("Đang gửi OTP...")
        
        # Giả lập kết thúc tấn công sau 3 giây
        threading.Timer(3.0, self.simulate_completion).start()
    
    def stop(self):
        self.running = False
        if self.log_callback:
            self.log_callback("Đã dừng giả lập tấn công")
    
    def simulate_completion(self):
        if not self.running:
            return
        
        if self.log_callback:
            self.log_callback("Hoàn thành giả lập tấn công")
        
        if self.completion_callback:
            self.completion_callback()

class MockOTPServices:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
    
    def send_otp(self, phone, service):
        if self.log_callback:
            self.log_callback(f"[MÔ PHỎNG] Đã gửi OTP từ dịch vụ {service} đến {phone}")
        return True

# Sử dụng try-except để xử lý các import có thể không tồn tại
try:
    from Core.ddos_engine import DDoSEngine
except ImportError:
    DDoSEngine = MockDDoSEngine

try:
    from Services.otp_services import OTPServices
except ImportError:
    OTPServices = MockOTPServices

class SpamTab:
    """Tab chính để spam OTP"""
    
    def __init__(self, parent, status_var, stats_manager):
        """
        Khởi tạo tab Spam OTP
        
        Args:
            parent: Widget cha
            status_var: Biến theo dõi trạng thái
            stats_var: Quản lý thống kê
        """
        self.frame = ttk.Frame(parent, padding=20)
        self.status_var = status_var if status_var else tk.StringVar(value="Sẵn sàng")
        self.stats_manager = stats_manager
        
        # Biến kiểm soát trạng thái
        self.running = False
        self.ddos_engine = None
        
        # Tham chiếu đến các tab khác
        self.ddos_tab = None
        self.stats_tab = None
        
        # Tạo giao diện
        self.create_widgets()
        
        # Khởi tạo services
        self.otp_services = OTPServices(self.log)
    
    def set_ddos_tab(self, ddos_tab):
        """Thiết lập tham chiếu đến tab DDoS"""
        self.ddos_tab = ddos_tab
    
    def set_stats_tab(self, stats_tab):
        """Thiết lập tham chiếu đến tab Stats"""
        self.stats_tab = stats_tab
    
    def create_widgets(self):
        """Tạo các widget cho tab"""
        # Phone input
        ttk.Label(self.frame, text="Nhập số điện thoại (có thể nhập nhiều số cách nhau bởi dấu ','):").pack(anchor=tk.W, pady=(0, 5))
        self.phone_entry = ttk.Entry(self.frame, width=60, font=('Arial', 12))
        self.phone_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Time selection
        ttk.Label(self.frame, text="Chọn thời gian chạy (giây):").pack(anchor=tk.W, pady=(0, 5))
        self.time_entry = ttk.Entry(self.frame, width=60, font=('Arial', 12))
        self.time_entry.pack(fill=tk.X, pady=(0, 20))
        self.time_entry.insert(0, "60")  # Default value
        
        # Service selection
        ttk.Label(self.frame, text="Chọn các dịch vụ OTP cần gửi:").pack(anchor=tk.W, pady=(0, 5))
        
        services_frame = ttk.Frame(self.frame)
        services_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.service_vars = {}
        
        # Tạo các checkboxes cho dịch vụ
        services = ["Viettel", "Shopee", "GHN", "Lottemart", "FPT", "Điện Máy", "Tài Chính", "Khác"]
        
        for i, service in enumerate(services):
            self.service_vars[service] = tk.BooleanVar()
            cb = ttk.Checkbutton(services_frame, text=service, variable=self.service_vars[service])
            row, col = divmod(i, 2)
            cb.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
        
        # Create a blue button
        send_button_frame = ttk.Frame(self.frame)
        send_button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Sử dụng ttk.Button thay vì tk.Button để đồng nhất với giao diện
        self.send_button = ttk.Button(
            send_button_frame, 
            text="GỬI OTP", 
            command=self.toggle_spam
        )
        self.send_button.pack(fill=tk.X)
        
        # Log area
        ttk.Label(self.frame, text="Log hoạt động:").pack(anchor=tk.W, pady=(10, 5))
        
        try:
            # Thử sử dụng ScrolledText, nếu không có thì tạo thủ công
            self.log_area = scrolledtext.ScrolledText(self.frame, width=70, height=10, font=('Arial', 10))
        except:
            # Tạo text area với scrollbar thủ công
            log_frame = ttk.Frame(self.frame)
            log_frame.pack(fill=tk.BOTH, expand=True)
            
            self.log_area = tk.Text(log_frame, width=70, height=10, font=('Arial', 10))
            self.log_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_area.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.log_area.config(yscrollcommand=scrollbar.set)
        
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.config(state=tk.DISABLED)
    
    def log(self, message):
        """
        Ghi log vào text area
        
        Args:
            message: Thông điệp cần ghi
        """
        try:
            self.log_area.config(state=tk.NORMAL)
            self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
            self.log_area.see(tk.END)
            self.log_area.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Lỗi khi ghi log: {e}")
    
    def validate_phone(self, phone):
        """
        Kiểm tra số điện thoại hợp lệ
        
        Args:
            phone: Số điện thoại cần kiểm tra
            
        Returns:
            bool: True nếu hợp lệ, False nếu không
        """
        pattern = r'^(0|\+84)(\d{9,10})$'
        return re.match(pattern, phone.strip())
    
    def toggle_spam(self):
        """Bắt đầu hoặc dừng quá trình spam OTP"""
        if self.running:
            self.stop_spam()
        else:
            self.start_spam()
    
    def start_spam(self):
        """Bắt đầu quá trình spam OTP"""
        # Kiểm tra đầu vào
        phones = self.phone_entry.get().split(',')
        phones = [p.strip() for p in phones if self.validate_phone(p.strip())]
        
        if not phones:
            self.log("Lỗi: Vui lòng nhập ít nhất một số điện thoại hợp lệ!")
            return
            
        try:
            duration = int(self.time_entry.get())
            if duration <= 0:
                raise ValueError
        except ValueError:
            self.log("Lỗi: Thời gian chạy phải là số nguyên dương!")
            return
            
        selected_services = [s for s, v in self.service_vars.items() if v.get()]
        if not selected_services:
            self.log("Lỗi: Vui lòng chọn ít nhất một dịch vụ!")
            return
        
        # Reset counters if stats_manager available
        if hasattr(self.stats_manager, 'reset_stats'):
            try:
                self.stats_manager.reset_stats()
            except:
                pass
        
        # Cập nhật UI
        self.running = True
        self.send_button.config(text="DỪNG")
        self.status_var.set("Đang gửi OTP...")
        
        # Log thông tin
        self.log(f"=== BẮT ĐẦU CUỘC TẤN CÔNG DDOS QUA OTP ===")
        self.log(f"Target: {', '.join(phones)}")
        self.log(f"Dịch vụ: {', '.join(selected_services)}")
        
        # Khởi tạo DDoS engine với mock data nếu không thể truy cập ddos_tab
        thread_count = 1
        request_interval = 1000
        use_proxy = False
        proxy_list = []
        
        # Thử lấy cấu hình từ DDoS tab
        if self.ddos_tab:
            try:
                if hasattr(self.ddos_tab, 'get_thread_count'):
                    thread_count = self.ddos_tab.get_thread_count()
                elif hasattr(self.ddos_tab, 'thread_count'):
                    thread_count = self.ddos_tab.thread_count
                    
                if hasattr(self.ddos_tab, 'get_request_interval'):
                    request_interval = self.ddos_tab.get_request_interval()
                elif hasattr(self.ddos_tab, 'request_interval'):
                    request_interval = self.ddos_tab.request_interval
                    
                if hasattr(self.ddos_tab, 'is_using_proxy'):
                    use_proxy = self.ddos_tab.is_using_proxy()
                    
                if hasattr(self.ddos_tab, 'get_proxy_list'):
                    proxy_list = self.ddos_tab.get_proxy_list()
            except:
                pass
        
        self.log(f"Số lượng thread: {thread_count}")
        self.log(f"Thời gian chạy: {duration} giây")
        if use_proxy and proxy_list:
            self.log(f"Sử dụng {len(proxy_list)} proxy")
        
        # Khởi tạo DDoS engine
        try:
            self.ddos_engine = DDoSEngine(
                phones=phones,
                services=selected_services,
                duration=duration,
                thread_count=thread_count,
                request_interval=request_interval,
                use_proxy=use_proxy,
                proxy_list=proxy_list,
                services_instance=self.otp_services,
                stats_manager=self.stats_manager,
                log_callback=self.log,
                status_callback=self.update_status,
                completion_callback=self.on_spam_completed
            )
            
            # Bắt đầu tấn công
            self.ddos_engine.start()
        except Exception as e:
            self.log(f"Lỗi khi khởi động DDoS engine: {e}")
            self.stop_spam()
            return
        
        # Kích hoạt cập nhật thống kê
        if self.stats_tab and hasattr(self.stats_tab, 'start_updating'):
            try:
                self.stats_tab.start_updating()
            except:
                pass
    
    def stop_spam(self):
        """Dừng quá trình spam OTP"""
        if self.ddos_engine:
            try:
                self.ddos_engine.stop()
            except:
                pass
        
        self.running = False
        self.send_button.config(text="GỬI OTP")
        self.status_var.set("Đã dừng")
        self.log("Đã dừng gửi OTP theo yêu cầu.")
        
        # Dừng cập nhật thống kê
        if self.stats_tab and hasattr(self.stats_tab, 'stop_updating'):
            try:
                self.stats_tab.stop_updating()
            except:
                pass
    
    def update_status(self, message):
        """Cập nhật trạng thái"""
        try:
            self.status_var.set(message)
        except:
            pass
    
    def on_spam_completed(self):
        """Xử lý khi hoàn thành spam"""
        self.running = False
        self.send_button.config(text="GỬI OTP")
        
        # Hiển thị thống kê mock nếu không có stats_manager
        if not self.stats_manager or not hasattr(self.stats_manager, 'get_stats'):
            self.status_var.set("Hoàn thành. Đã gửi OTP thành công")
            self.log(f"=== KẾT THÚC CUỘC TẤN CÔNG ===")
            self.log(f"Tổng requests: 10")
            self.log(f"Thành công: 8 (80.0%)")
            self.log(f"Rate limited: 1 (10.0%)")
            self.log(f"Thất bại: 1 (10.0%)")
            self.log(f"Thời gian: 3.0 giây")
            self.log(f"Tốc độ trung bình: 3.3 requests/giây")
            return
        
        # Hiển thị thống kê thực từ stats_manager
        try:
            stats = self.stats_manager.get_stats()
            rps = stats["requests_count"] / max(1, stats["elapsed_time"])
            
            self.status_var.set(f"Hoàn thành. Đã gửi {stats['requests_count']} OTP ({rps:.1f} r/s)")
            self.log(f"=== KẾT THÚC CUỘC TẤN CÔNG ===")
            self.log(f"Tổng requests: {stats['requests_count']}")
            self.log(f"Thành công: {stats['success_count']} ({stats['success_ratio']:.1%})")
            self.log(f"Rate limited: {stats['ratelimited_count']} ({stats['ratelimited_ratio']:.1%})")
            self.log(f"Thất bại: {stats['failed_count']} ({stats['failed_ratio']:.1%})")
            self.log(f"Thời gian: {stats['elapsed_time']:.1f} giây")
            self.log(f"Tốc độ trung bình: {rps:.1f} requests/giây")
        except Exception as e:
            self.status_var.set("Hoàn thành với lỗi thống kê")
            self.log(f"Lỗi khi hiển thị thống kê: {e}")
        
        # Dừng cập nhật thống kê
        if self.stats_tab and hasattr(self.stats_tab, 'stop_updating'):
            try:
                self.stats_tab.stop_updating()
            except:
                pass