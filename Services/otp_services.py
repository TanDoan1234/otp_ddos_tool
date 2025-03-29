#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - OTP Services
Các dịch vụ gửi OTP
"""

import random
import time

class OTPServices:
    """Quản lý các dịch vụ gửi OTP"""
    
    def __init__(self, log_callback=None):
        """
        Khởi tạo các dịch vụ OTP
        
        Args:
            log_callback: Callback để ghi log
        """
        self.log_callback = log_callback
        
        # Tên các dịch vụ và phương thức tương ứng
        self.services = {
            "Viettel": self.viettel_otp,
            "Shopee": self.shopee_otp,
            "GHN": self.ghn_otp,
            "Lottemart": self.lottemart_otp,
            "FPT": self.fpt_otp,
            "Điện Máy": self.dienmaay_otp,
            "Tài Chính": self.taichinh_otp,
            "Khác": self.other_otp
        }
    
    def log(self, message):
        """
        Ghi log
        
        Args:
            message: Thông điệp cần ghi
        """
        if self.log_callback:
            self.log_callback(message)
    
    def simulate_request(self, url, method="POST", headers=None, data=None, json=None, timeout=10, proxy=None):
        """
        Mô phỏng việc gửi request tới API
        
        Args:
            url: URL của API
            method: Phương thức HTTP
            headers: Headers
            data: Form data
            json: JSON data
            timeout: Thời gian timeout
            proxy: Proxy (nếu có)
        
        Returns:
            dict: Phản hồi mô phỏng
        """
        # Mô phỏng latency mạng
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
        
        # Mô phỏng các response khác nhau để demo
        responses = [
            {"status": "success", "message": "OTP đã được gửi", "code": 200},
            {"status": "ratelimit", "message": "Vượt quá giới hạn request", "code": 429},
            {"status": "error", "message": "Lỗi máy chủ", "code": 500},
            {"status": "success", "message": "Đã gửi OTP tới thiết bị", "code": 200}
        ]
        
        # Tỉ lệ thành công cao hơn để demo hiệu quả
        weights = [0.7, 0.15, 0.05, 0.1]
        
        # Thêm thông tin proxy nếu có
        proxy_info = f" qua proxy {proxy}" if proxy else ""
        self.log(f"Gửi request {method} tới {url}{proxy_info}")
        
        return random.choices(responses, weights=weights)[0]
    
    def format_response(self, service, response):
        """
        Format response để hiển thị trong log
        
        Args:
            service: Tên dịch vụ
            response: Phản hồi từ API
        
        Returns:
            str: Thông điệp đã format
        """
        if response["code"] == 200:
            return f"✅ Thành công: {response['message']}"
        elif response["code"] == 429:
            return f"⚠️ Rate Limited: {response['message']}"
        else:
            return f"❌ Lỗi: {response['message']}"
    
    def viettel_otp(self, phone, proxy=None):
        """
        Gửi OTP từ Viettel
        
        Args:
            phone: Số điện thoại
            proxy: Proxy (nếu có)
        
        Returns:
            str: Kết quả
        """
        url = "https://api.viettel.vn/api/auth/otp"  # URL giả lập cho demo
        headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500, 600)}.{random.randint(1, 99)}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "phone": phone,
            "type": "register",
            "device_id": f"demo-{random.randint(10000, 99999)}"
        }
        
        response = self.simulate_request(url, headers=headers, json=data, proxy=proxy)
        return self.format_response("Viettel", response)
    
    def shopee_otp(self, phone, proxy=None):
        """
        Gửi OTP từ Shopee
        
        Args:
            phone: Số điện thoại
            proxy: Proxy (nếu có)
        
        Returns:
            str: Kết quả
        """
        url = "https://shopee.vn/api/v2/authentication/send_otp"  # URL giả lập cho demo
        headers = {
            "User-Agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(10, 15)}_{random.randint(0, 9)} like Mac OS X)",
            "X-API-KEY": f"demo-{random.randint(1000, 9999)}",
            "Accept-Language": "vi-VN"
        }
        data = {
            "phone": phone,
            "force_send": True,
            "operation": "register"
        }
        
        response = self.simulate_request(url, headers=headers, json=data, proxy=proxy)
        return self.format_response("Shopee", response)
    
    def ghn_otp(self, phone, proxy=None):
        """
        Gửi OTP từ GHN
        
        Args:
            phone: Số điện thoại
            proxy: Proxy (nếu có)
        
        Returns:
            str: Kết quả
        """
        url = "https://online-gateway.ghn.vn/auth/api/send-otp"  # URL giả lập cho demo
        headers = {
            "User-Agent": "GHN/App/2.0",
            "Content-Type": "application/json"
        }
        data = {
            "phone": phone,
            "type": "login"
        }
        
        response = self.simulate_request(url, headers=headers, json=data, proxy=proxy)
        return self.format_response("GHN", response)
    
    def lottemart_otp(self, phone, proxy=None):
        """
        Gửi OTP từ Lottemart
        
        Args:
            phone: Số điện thoại
            proxy: Proxy (nếu có)
        
        Returns:
            str: Kết quả
        """
        url = "https://www.lottemart.vn/api/v1/auth/otp"  # URL giả lập cho demo
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Content-Type": "application/json"
        }
        data = {
            "phone": phone,
            "action": "login"
        }
        
        response = self.simulate_request(url, headers=headers, json=data, proxy=proxy)
        return self.format_response("Lottemart", response)
    
    def fpt_otp(self, phone, proxy=None):
        """
        Gửi OTP từ FPT
        
        Args:
            phone: Số điện thoại
            proxy: Proxy (nếu có)
        
        Returns:
            str: Kết quả
        """
        url = "https://fptshop.com.vn/api/auth/send-otp"  # URL giả lập cho demo
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0)",
            "Content-Type": "application/json"
        }
        data = {
            "phone": phone,
            "country_code": "84"
        }
        
        response = self.simulate_request(url, headers=headers, json=data, proxy=proxy)
        return self.format_response("FPT", response)
    
    def dienmaay_otp(self, phone, proxy=None):
        """
        Gửi OTP từ Điện Máy
        
        Args:
            phone: Số điện thoại
            proxy: Proxy (nếu có)
        
        Returns:
            str: Kết quả
        """
        url = "https://auth.dienmaycholon.vn/oauth/otp/request"  # URL giả lập cho demo
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh)",
            "Content-Type": "application/json"
        }
        data = {
            "phone_number": phone,
            "verification_type": "register"
        }
        
        response = self.simulate_request(url, headers=headers, json=data, proxy=proxy)
        return self.format_response("Điện Máy", response)
    
    def taichinh_otp(self, phone, proxy=None):
        """
        Gửi OTP từ Tài Chính
        
        Args:
            phone: Số điện thoại
            proxy: Proxy (nếu có)
        
        Returns:
            str: Kết quả
        """
        url = "https://api.tima.vn/api/auth/register/sendCode"  # URL giả lập cho demo
        headers = {
            "User-Agent": "Tima/App/3.2.1",
            "Content-Type": "application/json"
        }
        data = {
            "phone": phone,
            "source": "app"
        }
        
        response = self.simulate_request(url, headers=headers, json=data, proxy=proxy)
        return self.format_response("Tài Chính", response)
    
    def other_otp(self, phone, proxy=None):
        """
        Gửi OTP từ các dịch vụ khác
        
        Args:
            phone: Số điện thoại
            proxy: Proxy (nếu có)
        
        Returns:
            str: Kết quả
        """
        # Chọn ngẫu nhiên một trong các API khác để demo
        services = [
            {"name": "Tiki", "url": "https://tiki.vn/api/v2/customers/otp_codes"},
            {"name": "Momo", "url": "https://api.momo.vn/auth/send-otp"},
            {"name": "ViettelPay", "url": "https://viettelpay.vn/api/auth/get-otp"},
            {"name": "ZaloPay", "url": "https://api.zalopay.vn/v2/account/otp"}
        ]
        
        service = random.choice(services)
        url = service["url"]
        headers = {
            "User-Agent": "Mozilla/5.0 (Mobile)",
            "Content-Type": "application/json"
        }
        data = {
            "phone": phone,
            "platform": "web" if random.random() > 0.5 else "app"
        }
        
        response = self.simulate_request(url, headers=headers, json=data, proxy=proxy)
        return self.format_response(service["name"], response)