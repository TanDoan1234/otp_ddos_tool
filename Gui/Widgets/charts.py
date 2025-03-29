#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Chart Widgets
Các widget biểu đồ sử dụng trong ứng dụng
"""

import tkinter as tk
import math

class PieChart:
    """Widget biểu đồ tròn"""
    
    def __init__(self, canvas):
        """
        Khởi tạo biểu đồ tròn
        
        Args:
            canvas: Canvas để vẽ biểu đồ
        """
        self.canvas = canvas
        self.success_count = 0
        self.ratelimited_count = 0
        self.failed_count = 0
        
        # Màu sắc
        self.success_color = "#2ecc71"  # Xanh lá
        self.ratelimited_color = "#f1c40f"  # Vàng
        self.failed_color = "#e74c3c"  # Đỏ
        
        # Đăng ký sự kiện resize
        self.canvas.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """Xử lý khi canvas thay đổi kích thước"""
        self.update_chart(self.success_count, self.ratelimited_count, self.failed_count)
    
    def update_chart(self, success_count, ratelimited_count, failed_count):
        """
        Cập nhật biểu đồ với dữ liệu mới
        
        Args:
            success_count: Số lượng request thành công
            ratelimited_count: Số lượng request bị rate limit
            failed_count: Số lượng request thất bại
        """
        self.success_count = success_count
        self.ratelimited_count = ratelimited_count
        self.failed_count = failed_count
        
        # Xóa các phần tử cũ
        self.canvas.delete("all")
        
        # Lấy kích thước canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 50 or height < 50:  # Canvas chưa sẵn sàng
            return
        
        # Vẽ tiêu đề
        self.canvas.create_text(
            width // 2, 
            20, 
            text="Thống kê tấn công DDoS OTP", 
            font=("Arial", 14, "bold")
        )
        
        # Vẽ biểu đồ tròn
        total = max(1, success_count + ratelimited_count + failed_count)
        success_ratio = success_count / total
        ratelimited_ratio = ratelimited_count / total
        failed_ratio = failed_count / total
        
        # Tính toán vị trí
        center_x = width // 4
        center_y = height // 2
        radius = min(center_x, center_y) - 20
        
        # Vẽ các phần
        self._draw_pie_segment(center_x, center_y, radius, 0, success_ratio * 360, self.success_color)
        self._draw_pie_segment(center_x, center_y, radius, success_ratio * 360, 
                               ratelimited_ratio * 360, self.ratelimited_color)
        self._draw_pie_segment(center_x, center_y, radius, 
                               (success_ratio + ratelimited_ratio) * 360, 
                               failed_ratio * 360, self.failed_color)
        
        # Vẽ chú thích
        legend_x = center_x * 2
        legend_y = center_y - radius // 2
        
        # Thành công
        self._draw_legend_item(
            legend_x, legend_y, 
            self.success_color, 
            f"Thành công: {success_count} ({success_ratio:.1%})"
        )
        
        # Rate limited
        self._draw_legend_item(
            legend_x, legend_y + 30, 
            self.ratelimited_color, 
            f"Rate Limited: {ratelimited_count} ({ratelimited_ratio:.1%})"
        )
        
        # Thất bại
        self._draw_legend_item(
            legend_x, legend_y + 60, 
            self.failed_color, 
            f"Thất bại: {failed_count} ({failed_ratio:.1%})"
        )
    
    def _draw_pie_segment(self, center_x, center_y, radius, start_angle, extent, color):
        """
        Vẽ một phân đoạn của biểu đồ tròn
        
        Args:
            center_x: Tọa độ X của tâm
            center_y: Tọa độ Y của tâm
            radius: Bán kính
            start_angle: Góc bắt đầu (độ)
            extent: Độ rộng góc (độ)
            color: Màu sắc
        """
        if extent <= 0:
            return
            
        self.canvas.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=extent,
            fill=color, outline="#FFFFFF", width=1,
            style=tk.PIESLICE
        )
    
    def _draw_legend_item(self, x, y, color, text):
        """
        Vẽ một mục trong chú thích
        
        Args:
            x: Tọa độ X
            y: Tọa độ Y
            color: Màu sắc
            text: Nội dung
        """
        self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=color, outline="")
        self.canvas.create_text(x + 25, y + 10, text=text, anchor=tk.W)


class LineGraph:
    """Widget biểu đồ đường"""
    
    def __init__(self, canvas):
        """
        Khởi tạo biểu đồ đường
        
        Args:
            canvas: Canvas để vẽ biểu đồ
        """
        self.canvas = canvas
        self.data_points = []
        
        # Cài đặt
        self.max_points = 60  # Hiển thị tối đa 60 điểm
        self.padding = 40  # Padding từ viền canvas
        
        # Màu sắc
        self.line_color = "#3498db"  # Xanh dương
        self.axis_color = "#2c3e50"  # Xám đậm
        
        # Đăng ký sự kiện resize
        self.canvas.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """Xử lý khi canvas thay đổi kích thước"""
        self.draw_graph()
    
    def add_data_point(self, value):
        """
        Thêm một điểm dữ liệu mới
        
        Args:
            value: Giá trị điểm dữ liệu
        """
        self.data_points.append(value)
        
        # Giới hạn số điểm
        if len(self.data_points) > self.max_points:
            self.data_points = self.data_points[-self.max_points:]
        
        self.draw_graph()
    
    def draw_graph(self):
        """Vẽ biểu đồ đường"""
        # Xóa các phần tử cũ
        self.canvas.delete("all")
        
        # Lấy kích thước canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 50 or height < 50 or not self.data_points:  # Canvas chưa sẵn sàng hoặc không có dữ liệu
            return
        
        # Tính toán giá trị lớn nhất và nhỏ nhất
        min_value = min(self.data_points)
        max_value = max(self.data_points)
        
        # Đảm bảo có khoảng cách giữa giá trị nhỏ nhất và lớn nhất
        if max_value == min_value:
            max_value += 1
            min_value = max(0, min_value - 1)
        
        # Vùng vẽ
        plot_width = width - 2 * self.padding
        plot_height = height - 2 * self.padding
        
        # Vẽ trục
        # Trục X
        self.canvas.create_line(
            self.padding, height - self.padding,
            width - self.padding, height - self.padding,
            fill=self.axis_color, width=2
        )
        
        # Trục Y
        self.canvas.create_line(
            self.padding, self.padding,
            self.padding, height - self.padding,
            fill=self.axis_color, width=2
        )
        
        # Vẽ đường
        if len(self.data_points) > 1:
            points = []
            for i, value in enumerate(self.data_points):
                x = self.padding + i * plot_width / (len(self.data_points) - 1)
                y = height - self.padding - (value - min_value) * plot_height / (max_value - min_value)
                points.append(x)
                points.append(y)
            
            self.canvas.create_line(points, fill=self.line_color, width=2, smooth=True)
            
            # Vẽ điểm
            for i in range(0, len(points), 2):
                x, y = points[i], points[i+1]
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=self.line_color, outline="")
        
        # Vẽ nhãn trục Y
        for i in range(5):
            value = min_value + i * (max_value - min_value) / 4
            y = height - self.padding - i * plot_height / 4
            
            # Vẽ đường kẻ ngang
            self.canvas.create_line(
                self.padding, y,
                width - self.padding, y,
                fill="#e0e0e0", dash=(2, 4)
            )
            
            # Vẽ nhãn
            self.canvas.create_text(
                self.padding - 5, y,
                text=f"{value:.1f}", anchor=tk.E,
                font=("Arial", 8)
            )