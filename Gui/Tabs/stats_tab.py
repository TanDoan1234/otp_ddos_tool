#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Stats Tab
Tab hiển thị thống kê và biểu đồ
"""

import tkinter as tk
from tkinter import ttk, filedialog
import json
import time
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Tạo mock class cho PieChart
class SimplePieChart:
    def __init__(self, canvas):
        self.canvas = canvas
        # Màu sắc cho biểu đồ
        self.colors = ["#2ecc71", "#f39c12", "#e74c3c"]  # Success, Warning, Error
        
        # Vẽ biểu đồ mẫu
        self.update_chart(0, 0, 0)
    
    def update_chart(self, success, ratelimited, failed):
        # Xóa canvas
        self.canvas.delete("all")
        
        # Kích thước canvas
        width = self.canvas.winfo_width() or 400
        height = self.canvas.winfo_height() or 300
        
        # Tính tổng
        total = success + ratelimited + failed
        if total == 0:
            # Vẽ vòng tròn trống
            self.canvas.create_oval(
                width/2 - 100, height/2 - 100,
                width/2 + 100, height/2 + 100,
                outline="#ccc", width=2
            )
            self.canvas.create_text(
                width/2, height/2,
                text="Không có dữ liệu",
                font=("Arial", 14)
            )
            return
        
        # Vẽ biểu đồ tròn
        start_angle = 0
        
        # Success slice
        if success > 0:
            end_angle = start_angle + (success / total) * 360
            self.draw_slice(width/2, height/2, 100, start_angle, end_angle, self.colors[0])
            start_angle = end_angle
        
        # Ratelimited slice
        if ratelimited > 0:
            end_angle = start_angle + (ratelimited / total) * 360
            self.draw_slice(width/2, height/2, 100, start_angle, end_angle, self.colors[1])
            start_angle = end_angle
        
        # Failed slice
        if failed > 0:
            end_angle = start_angle + (failed / total) * 360
            self.draw_slice(width/2, height/2, 100, start_angle, end_angle, self.colors[2])
        
        # Vẽ chú thích
        legend_y = height - 80
        
        # Success legend
        self.canvas.create_rectangle(width - 180, legend_y, width - 160, legend_y + 20, fill=self.colors[0])
        self.canvas.create_text(width - 100, legend_y + 10, text=f"Thành công: {success}", anchor="w")
        
        # Ratelimited legend
        self.canvas.create_rectangle(width - 180, legend_y + 30, width - 160, legend_y + 50, fill=self.colors[1])
        self.canvas.create_text(width - 100, legend_y + 40, text=f"Rate limited: {ratelimited}", anchor="w")
        
        # Failed legend
        self.canvas.create_rectangle(width - 180, legend_y + 60, width - 160, legend_y + 80, fill=self.colors[2])
        self.canvas.create_text(width - 100, legend_y + 70, text=f"Thất bại: {failed}", anchor="w")
    
    def draw_slice(self, x, y, radius, start_angle, end_angle, fill):
        # Chuyển đổi từ độ sang radian
        import math
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Tính toán các điểm
        x1 = x + radius * math.cos(start_rad)
        y1 = y + radius * math.sin(start_rad)
        x2 = x + radius * math.cos(end_rad)
        y2 = y + radius * math.sin(end_rad)
        
        # Vẽ phần slice
        # Nếu slice nhỏ hơn 180 độ
        if end_angle - start_angle <= 180:
            self.canvas.create_arc(
                x - radius, y - radius,
                x + radius, y + radius,
                start=start_angle, extent=end_angle-start_angle,
                fill=fill, outline="white", width=1
            )
        else:
            # Nếu slice lớn hơn 180 độ, chia thành hai phần
            self.canvas.create_arc(
                x - radius, y - radius,
                x + radius, y + radius,
                start=start_angle, extent=180,
                fill=fill, outline="white", width=1
            )
            self.canvas.create_arc(
                x - radius, y - radius,
                x + radius, y + radius,
                start=start_angle+180, extent=end_angle-start_angle-180,
                fill=fill, outline="white", width=1
            )

# Sử dụng try-except để xử lý các import có thể không tồn tại
try:
    from Gui.Widgets.charts import PieChart
except ImportError:
    PieChart = SimplePieChart

# Tạo mock object cho stats_manager nếu cần
class MockStatsManager:
    def __init__(self):
        self.stats = {
            "requests_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "ratelimited_count": 0,
            "elapsed_time": 0,
            "success_ratio": 0,
            "failed_ratio": 0,
            "ratelimited_ratio": 0
        }
    
    def get_stats(self):
        return self.stats
    
    def get_settings(self):
        return {}
    
    def reset_stats(self):
        self.stats = {
            "requests_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "ratelimited_count": 0,
            "elapsed_time": 0,
            "success_ratio": 0,
            "failed_ratio": 0,
            "ratelimited_ratio": 0
        }
    
    def update_stats(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.stats:
                self.stats[key] = value

class StatsTab:
    """Tab hiển thị thống kê"""
    
    def __init__(self, parent, stats_manager=None):
        """
        Khởi tạo tab thống kê
        
        Args:
            parent: Widget cha
            stats_manager: Quản lý thống kê
        """
        self.frame = ttk.Frame(parent, padding=20)
        self.stats_manager = stats_manager or MockStatsManager()
        
        # Biến kiểm soát cập nhật
        self.updating = False
        self.update_thread = None
        
        # Tạo giao diện
        self.create_widgets()
        
        # Cập nhật ban đầu
        self.update_stats_display()
    
    def create_widgets(self):
        """Tạo các widget cho tab"""
        # Tạo frame cho các biểu đồ
        self.stats_canvas = tk.Canvas(self.frame, bg="white", height=300)
        self.stats_canvas.pack(fill=tk.X, expand=False, pady=(0, 10))
        
        # Đảm bảo canvas đã được render trước khi tạo biểu đồ
        self.frame.update()
        
        # Tạo biểu đồ
        self.pie_chart = PieChart(self.stats_canvas)
        
        # Thêm frame thông tin số liệu
        info_frame = ttk.LabelFrame(self.frame, text="Thông tin chi tiết", padding=10)
        info_frame.pack(fill=tk.X)
        
        # Tạo grid cho các metric
        metrics_frame = ttk.Frame(info_frame)
        metrics_frame.pack(fill=tk.X)
        
        # Cột 1
        ttk.Label(metrics_frame, text="Tổng requests:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(metrics_frame, text="Thành công:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Cột 2
        self.total_requests_var = tk.StringVar(value="0")
        self.success_requests_var = tk.StringVar(value="0")
        ttk.Label(metrics_frame, textvariable=self.total_requests_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(metrics_frame, textvariable=self.success_requests_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Cột 3
        ttk.Label(metrics_frame, text="Rate limited:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Label(metrics_frame, text="Lỗi:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        
        # Cột 4
        self.ratelimited_var = tk.StringVar(value="0")
        self.error_var = tk.StringVar(value="0")
        ttk.Label(metrics_frame, textvariable=self.ratelimited_var).grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        ttk.Label(metrics_frame, textvariable=self.error_var).grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Thêm nút xuất báo cáo
        self.export_button = ttk.Button(
            info_frame, 
            text="Xuất báo cáo kiểm thử DDoS", 
            command=self.export_report
        )
        self.export_button.pack(fill=tk.X, pady=(10, 0))
        
        # Thêm nút làm mới thống kê
        self.refresh_button = ttk.Button(
            info_frame,
            text="Làm mới thống kê",
            command=self.update_stats_display
        )
        self.refresh_button.pack(fill=tk.X, pady=(10, 0))
    
    def start_updating(self):
        """Bắt đầu cập nhật thống kê"""
        self.updating = True
        self.update_thread = threading.Thread(target=self.update_stats_thread, daemon=True)
        self.update_thread.start()
    
    def stop_updating(self):
        """Dừng cập nhật thống kê"""
        self.updating = False
        if self.update_thread and self.update_thread.is_alive():
            try:
                self.update_thread.join(1.0)  # Wait for thread to finish
            except:
                pass
    
    def update_stats_thread(self):
        """Thread cập nhật thống kê"""
        while self.updating:
            try:
                self.update_stats_display()
                time.sleep(1)  # Cập nhật mỗi giây
            except Exception as e:
                print(f"Lỗi khi cập nhật thống kê: {e}")
                # Nếu có lỗi, delay dài hơn để tránh spam
                time.sleep(5)
    
    def update_stats_display(self):
        """Cập nhật hiển thị thống kê"""
        try:
            # Lấy thống kê hiện tại
            stats = self.stats_manager.get_stats()
            
            # Cập nhật các label
            self.total_requests_var.set(str(stats["requests_count"]))
            self.success_requests_var.set(str(stats["success_count"]))
            self.ratelimited_var.set(str(stats["ratelimited_count"]))
            self.error_var.set(str(stats["failed_count"]))
            
            # Vẽ biểu đồ
            self.pie_chart.update_chart(
                stats["success_count"],
                stats["ratelimited_count"],
                stats["failed_count"]
            )
        except Exception as e:
            print(f"Lỗi khi cập nhật hiển thị thống kê: {e}")
    
    def export_report(self):
        """Xuất báo cáo kiểm thử DDoS"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Lưu báo cáo",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                # Lấy thống kê hiện tại
                stats = self.stats_manager.get_stats()
                
                # Tạo dữ liệu báo cáo
                report = {
                    "timestamp": time.time(),
                    "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "title": "Báo cáo kiểm thử DDoS qua OTP",
                    "metrics": {
                        "total_requests": stats["requests_count"],
                        "successful_requests": stats["success_count"],
                        "failed_requests": stats["failed_count"],
                        "ratelimited_requests": stats["ratelimited_count"]
                    },
                    "settings": self.stats_manager.get_settings(),
                    "elapsed_time": stats["elapsed_time"],
                    "success_rate": stats["success_ratio"] * 100
                }
                
                # Ghi ra file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi xuất báo cáo: {str(e)}")