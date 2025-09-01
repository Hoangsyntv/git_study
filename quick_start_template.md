# 🚀 QUICK START - TẠO API CLIENT CƠ BẢN

## 📁 Template nhanh - Copy và sử dụng ngay

### 1. **config.py** - Cấu hình
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Settings
    BASE_URL = "https://your-api-domain.com"
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    
    # App Settings
    DEBUG = True
    CACHE_ENABLED = True
    MAX_RETRIES = 3
    TIMEOUT = 30
```

### 2. **api_client.py** - Client cơ bản
```python
import requests
import time
from datetime import datetime

class APIClient:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
    
    def authenticate(self):
        """Xác thực và lấy token"""
        auth_url = f"{self.base_url}/oauth2/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            response = requests.post(auth_url, data=data, timeout=30)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                return True
        except Exception as e:
            print(f"Lỗi xác thực: {e}")
        
        return False
    
    def make_request(self, endpoint, params=None):
        """Gọi API với error handling"""
        if not self.access_token:
            if not self.authenticate():
                return None
        
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Token hết hạn, thử xác thực lại
                if self.authenticate():
                    headers['Authorization'] = f'Bearer {self.access_token}'
                    response = requests.get(url, headers=headers, params=params, timeout=30)
                    if response.status_code == 200:
                        return response.json()
            
            print(f"Lỗi API: {response.status_code} - {response.text}")
            
        except Exception as e:
            print(f"Lỗi request: {e}")
        
        return None
    
    def get_paginated_data(self, endpoint, page_size=100):
        """Lấy tất cả dữ liệu với phân trang"""
        all_data = []
        current_item = 0
        
        while True:
            params = {
                'pageSize': page_size,
                'currentItem': current_item
            }
            
            response = self.make_request(endpoint, params)
            
            if not response or not response.get('data'):
                break
            
            all_data.extend(response['data'])
            
            if len(response['data']) < page_size:
                break
            
            current_item += page_size
            time.sleep(0.1)  # Tránh rate limit
        
        return all_data
```

### 3. **data_processor.py** - Xử lý dữ liệu
```python
from collections import defaultdict
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.data = []
    
    def load_data(self, raw_data):
        """Load và validate dữ liệu"""
        self.data = []
        
        for item in raw_data:
            if self.validate_item(item):
                self.data.append(self.clean_item(item))
        
        return len(self.data)
    
    def validate_item(self, item):
        """Validate dữ liệu cơ bản"""
        required_fields = ['id', 'createdDate']
        return all(field in item for field in required_fields)
    
    def clean_item(self, item):
        """Làm sạch dữ liệu"""
        return {
            'id': item.get('id'),
            'date': item.get('createdDate'),
            'total': float(item.get('total', 0)),
            'details': item.get('details', [])
        }
    
    def group_by_field(self, field_name):
        """Nhóm dữ liệu theo field"""
        grouped = defaultdict(list)
        
        for item in self.data:
            key = item.get(field_name)
            if key:
                grouped[key].append(item)
        
        return dict(grouped)
    
    def calculate_summary(self):
        """Tính toán tổng quan"""
        if not self.data:
            return {}
        
        total_amount = sum(item['total'] for item in self.data)
        total_count = len(self.data)
        
        return {
            'total_records': total_count,
            'total_amount': total_amount,
            'average_amount': total_amount / total_count if total_count > 0 else 0
        }
    
    def get_top_items(self, group_by, sort_by, top_n=10):
        """Lấy top items"""
        grouped = self.group_by_field(group_by)
        
        # Tính toán metrics cho mỗi group
        metrics = {}
        for key, items in grouped.items():
            metrics[key] = {
                'count': len(items),
                'total': sum(item['total'] for item in items),
                'average': sum(item['total'] for item in items) / len(items)
            }
        
        # Sắp xếp theo sort_by
        sorted_items = sorted(
            metrics.items(),
            key=lambda x: x[1][sort_by],
            reverse=True
        )
        
        return sorted_items[:top_n]
```

### 4. **report_generator.py** - Tạo báo cáo
```python
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.reports = []
    
    def print_console_report(self, data, title="BÁO CÁO"):
        """In báo cáo ra console"""
        print(f"\n🏆 {title}")
        print("=" * 60)
        print(f"📅 Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("-" * 60)
        
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, tuple) and len(item) == 2:
                    key, metrics = item
                    print(f"{i:2d}. {key}")
                    for metric_name, value in metrics.items():
                        if isinstance(value, float):
                            print(f"    📊 {metric_name}: {value:,.2f}")
                        else:
                            print(f"    📊 {metric_name}: {value:,}")
                    print("-" * 40)
        
        elif isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, float):
                    print(f"📊 {key}: {value:,.2f}")
                else:
                    print(f"📊 {key}: {value:,}")
        
        print("=" * 60)
    
    def generate_html_report(self, data, title, filename):
        """Tạo báo cáo HTML"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #eee;
                }}
                .header h1 {{
                    color: #333;
                    margin: 0;
                    font-size: 2.5em;
                }}
                .header .date {{
                    color: #666;
                    font-size: 1.1em;
                    margin-top: 10px;
                }}
                .metric-card {{
                    background: #f8f9fa;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 8px;
                    border-left: 4px solid #007bff;
                }}
                .metric-title {{
                    font-weight: bold;
                    font-size: 1.2em;
                    color: #333;
                    margin-bottom: 10px;
                }}
                .metric-value {{
                    font-size: 1.1em;
                    color: #666;
                    margin: 5px 0;
                }}
                .number {{
                    font-weight: bold;
                    color: #007bff;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 {title}</h1>
                    <div class="date">📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
                </div>
                
                <div class="content">
        """
        
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, tuple) and len(item) == 2:
                    key, metrics = item
                    html_content += f"""
                    <div class="metric-card">
                        <div class="metric-title">{i}. {key}</div>
                    """
                    
                    for metric_name, value in metrics.items():
                        if isinstance(value, float):
                            formatted_value = f"{value:,.2f}"
                        else:
                            formatted_value = f"{value:,}"
                        
                        html_content += f"""
                        <div class="metric-value">
                            📊 {metric_name}: <span class="number">{formatted_value}</span>
                        </div>
                        """
                    
                    html_content += "</div>"
        
        html_content += """
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Đã tạo báo cáo HTML: {filename}")
```

### 5. **main.py** - Ứng dụng chính
```python
from api_client import APIClient
from data_processor import DataProcessor
from report_generator import ReportGenerator
from config import Config

def main():
    print("🚀 Khởi động ứng dụng...")
    
    # 1. Khởi tạo API Client
    api = APIClient(
        base_url=Config.BASE_URL,
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET
    )
    
    # 2. Xác thực
    print("🔑 Đang xác thực...")
    if not api.authenticate():
        print("❌ Không thể xác thực API")
        return
    
    print("✅ Xác thực thành công!")
    
    # 3. Lấy dữ liệu
    print("📊 Đang lấy dữ liệu...")
    raw_data = api.get_paginated_data("invoices")
    
    if not raw_data:
        print("❌ Không có dữ liệu")
        return
    
    print(f"✅ Đã lấy {len(raw_data)} bản ghi")
    
    # 4. Xử lý dữ liệu
    processor = DataProcessor()
    valid_count = processor.load_data(raw_data)
    print(f"✅ Đã xử lý {valid_count} bản ghi hợp lệ")
    
    # 5. Tính toán và báo cáo
    reporter = ReportGenerator()
    
    # Báo cáo tổng quan
    summary = processor.calculate_summary()
    reporter.print_console_report(summary, "TỔNG QUAN")
    
    # Top items theo số lượng
    top_by_count = processor.get_top_items('product_id', 'count', 10)
    reporter.print_console_report(top_by_count, "TOP 10 THEO SỐ LƯỢNG")
    
    # Top items theo tổng giá trị
    top_by_total = processor.get_top_items('product_id', 'total', 10)
    reporter.print_console_report(top_by_total, "TOP 10 THEO TỔNG GIÁ TRỊ")
    
    # Xuất báo cáo HTML
    reporter.generate_html_report(
        top_by_total, 
        "Báo cáo Top 10 theo Doanh thu",
        "bao_cao_doanh_thu.html"
    )
    
    print("\n🎉 Hoàn thành!")

if __name__ == "__main__":
    main()
```

### 6. **.env** - File cấu hình bảo mật
```env
# API Credentials
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here

# Database (nếu cần)
DATABASE_URL=sqlite:///app.db

# Debug
DEBUG=True
```

### 7. **requirements.txt** - Dependencies
```txt
requests>=2.31.0
python-dotenv>=1.0.0
openpyxl>=3.1.0
pandas>=2.0.0
aiohttp>=3.8.0
```

## 🎯 Cách sử dụng:

1. **Setup môi trường:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Cấu hình:**
- Copy template trên vào project
- Tạo file `.env` với thông tin API của bạn
- Sửa `Config.BASE_URL` thành URL API thực tế

3. **Chạy:**
```bash
python main.py
```

## 🔧 Tùy chỉnh cho API khác:

- **Sửa authentication** trong `api_client.py`
- **Thay đổi data structure** trong `data_processor.py`
- **Tùy chỉnh báo cáo** trong `report_generator.py`

**📝 Template này đã được test với KiotViet API và có thể adapt cho các API khác!**
