# 📖 HƯỚNG DẪN KẾT NỐI API VÀ TẠO BÁO CÁO

## 🎯 Mục tiêu
Hướng dẫn từng bước để kết nối API và tạo ra các báo cáo phân tích dữ liệu như tool KiotViet API đã xây dựng.

## 📋 Mục lục
1. [Tìm hiểu về API](#1-tìm-hiểu-về-api)
2. [Chuẩn bị môi trường](#2-chuẩn-bị-môi-trường)
3. [Xác thực API](#3-xác-thực-api)
4. [Truy xuất dữ liệu](#4-truy-xuất-dữ-liệu)
5. [Xử lý và phân tích](#5-xử-lý-và-phân-tích)
6. [Tạo báo cáo](#6-tạo-báo-cáo)
7. [Tối ưu hóa](#7-tối-ưu-hóa)

---

## 1. Tìm hiểu về API

### 🔍 API là gì?
**API (Application Programming Interface)** là cách để các ứng dụng "nói chuyện" với nhau.

### 📖 Các loại API phổ biến:
- **REST API**: Sử dụng HTTP requests (GET, POST, PUT, DELETE)
- **GraphQL**: Truy vấn dữ liệu linh hoạt
- **SOAP**: Giao thức cũ, ít dùng

### 🛠️ Thông tin cần thu thập:
```
✅ Base URL: https://public.kiotapi.com
✅ Authentication method: OAuth 2.0
✅ API endpoints: /invoices, /products, /customers
✅ Rate limits: Giới hạn requests/phút
✅ Documentation: Link tài liệu chính thức
```

---

## 2. Chuẩn bị môi trường

### 🐍 Python setup:
```bash
# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Cài đặt thư viện cần thiết
pip install requests
pip install datetime
pip install json
```

### 📁 Cấu trúc project:
```
project/
│
├── config.py          # Cấu hình API
├── api_client.py       # Class kết nối API
├── data_processor.py   # Xử lý dữ liệu
├── report_generator.py # Tạo báo cáo
└── main.py            # File chính
```

---

## 3. Xác thực API

### 🔐 Các phương thức xác thực phổ biến:

#### **A. API Key (Đơn giản nhất)**
```python
headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}
```

#### **B. OAuth 2.0 (Như KiotViet)**
```python
def get_access_token(self):
    """Lấy access token từ OAuth 2.0"""
    auth_url = f"{self.base_url}/oauth2/token"
    
    data = {
        'grant_type': 'client_credentials',
        'client_id': self.client_id,
        'client_secret': self.client_secret,
        'scope': 'PublicApi.Access'
    }
    
    response = requests.post(auth_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        self.access_token = token_data['access_token']
        return True
    return False
```

#### **C. Basic Authentication**
```python
import base64

credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {'Authorization': f'Basic {credentials}'}
```

---

## 4. Truy xuất dữ liệu

### 📊 Các bước truy xuất:

#### **Bước 1: Tạo function cơ bản**
```python
def make_api_request(self, endpoint, params=None):
    """Function cơ bản để gọi API"""
    url = f"{self.base_url}/{endpoint}"
    headers = {
        'Authorization': f'Bearer {self.access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Lỗi: {response.status_code} - {response.text}")
        return None
```

#### **Bước 2: Xử lý phân trang (Pagination)**
```python
def get_all_data(self, endpoint, page_size=100):
    """Lấy tất cả dữ liệu với phân trang"""
    all_data = []
    current_page = 0
    
    while True:
        params = {
            'pageSize': page_size,
            'currentItem': current_page * page_size
        }
        
        response = self.make_api_request(endpoint, params)
        
        if not response or not response.get('data'):
            break
        
        all_data.extend(response['data'])
        
        # Nếu số dữ liệu < page_size thì đã hết
        if len(response['data']) < page_size:
            break
        
        current_page += 1
    
    return all_data
```

#### **Bước 3: Xử lý lỗi và retry**
```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    """Decorator để retry khi gặp lỗi"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Lỗi lần {attempt + 1}: {e}. Thử lại sau {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def get_invoices_with_retry(self, from_date, to_date):
    """Lấy hóa đơn với retry"""
    return self.get_invoices(from_date, to_date)
```

---

## 5. Xử lý và phân tích

### 📈 Các bước xử lý dữ liệu:

#### **Bước 1: Làm sạch dữ liệu**
```python
def clean_invoice_data(self, raw_data):
    """Làm sạch dữ liệu hóa đơn"""
    cleaned_data = []
    
    for invoice in raw_data:
        # Kiểm tra dữ liệu bắt buộc
        if not invoice.get('invoiceDetails'):
            continue
        
        # Chuẩn hóa dữ liệu
        clean_invoice = {
            'id': invoice.get('id'),
            'date': invoice.get('createdDate'),
            'total': invoice.get('total', 0),
            'details': []
        }
        
        for detail in invoice['invoiceDetails']:
            clean_detail = {
                'product_id': detail.get('productId'),
                'product_name': detail.get('productName', '').strip(),
                'quantity': detail.get('quantity', 0),
                'price': detail.get('price', 0)
            }
            clean_invoice['details'].append(clean_detail)
        
        cleaned_data.append(clean_invoice)
    
    return cleaned_data
```

#### **Bước 2: Tính toán metrics**
```python
def calculate_product_metrics(self, invoices):
    """Tính toán các chỉ số cho sản phẩm"""
    product_metrics = {}
    
    for invoice in invoices:
        for detail in invoice['details']:
            product_id = detail['product_id']
            
            if product_id not in product_metrics:
                product_metrics[product_id] = {
                    'name': detail['product_name'],
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'invoice_count': 0,
                    'avg_price': 0
                }
            
            # Cập nhật metrics
            metrics = product_metrics[product_id]
            metrics['total_quantity'] += detail['quantity']
            metrics['total_revenue'] += detail['quantity'] * detail['price']
            metrics['invoice_count'] += 1
    
    # Tính giá trung bình
    for product_id, metrics in product_metrics.items():
        if metrics['total_quantity'] > 0:
            metrics['avg_price'] = metrics['total_revenue'] / metrics['total_quantity']
    
    return product_metrics
```

#### **Bước 3: Sắp xếp và ranking**
```python
def get_top_products(self, product_metrics, sort_by='revenue', top_n=10):
    """Lấy top sản phẩm theo tiêu chí"""
    
    sort_keys = {
        'revenue': lambda x: x[1]['total_revenue'],
        'quantity': lambda x: x[1]['total_quantity'],
        'orders': lambda x: x[1]['invoice_count']
    }
    
    if sort_by not in sort_keys:
        raise ValueError(f"sort_by phải là: {list(sort_keys.keys())}")
    
    sorted_products = sorted(
        product_metrics.items(),
        key=sort_keys[sort_by],
        reverse=True
    )
    
    return sorted_products[:top_n]
```

---

## 6. Tạo báo cáo

### 📊 Các loại báo cáo:

#### **A. Báo cáo đơn giản (Console)**
```python
def print_simple_report(self, top_products, title="BÁO CÁO BÁN HÀNG"):
    """In báo cáo đơn giản ra console"""
    print(f"\n🏆 {title}")
    print("=" * 60)
    
    for i, (product_id, data) in enumerate(top_products, 1):
        print(f"{i:2d}. {data['name'][:40]}")
        print(f"    💰 Doanh thu: {data['total_revenue']:,.0f} VNĐ")
        print(f"    📦 Số lượng: {data['total_quantity']:,}")
        print(f"    📋 Số đơn: {data['invoice_count']}")
        print("-" * 50)
```

#### **B. Báo cáo HTML**
```python
def generate_html_report(self, data, filename="report.html"):
    """Tạo báo cáo HTML"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Báo cáo bán hàng</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .number {{ text-align: right; }}
        </style>
    </head>
    <body>
        <h1>📊 Báo cáo bán hàng</h1>
        <table>
            <tr>
                <th>STT</th>
                <th>Tên sản phẩm</th>
                <th>Doanh thu</th>
                <th>Số lượng</th>
                <th>Số đơn</th>
            </tr>
    """
    
    for i, (product_id, data) in enumerate(data, 1):
        html_content += f"""
            <tr>
                <td>{i}</td>
                <td>{data['name']}</td>
                <td class="number">{data['total_revenue']:,.0f} VNĐ</td>
                <td class="number">{data['total_quantity']:,}</td>
                <td class="number">{data['invoice_count']}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Đã tạo báo cáo: {filename}")
```

#### **C. Báo cáo Excel**
```python
# Cần cài: pip install openpyxl
import openpyxl
from openpyxl.styles import Font, PatternFill

def generate_excel_report(self, data, filename="report.xlsx"):
    """Tạo báo cáo Excel"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Báo cáo bán hàng"
    
    # Header
    headers = ["STT", "Tên sản phẩm", "Doanh thu", "Số lượng", "Số đơn"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
    
    # Dữ liệu
    for row, (product_id, data) in enumerate(data, 2):
        ws.cell(row=row, column=1, value=row-1)
        ws.cell(row=row, column=2, value=data['name'])
        ws.cell(row=row, column=3, value=data['total_revenue'])
        ws.cell(row=row, column=4, value=data['total_quantity'])
        ws.cell(row=row, column=5, value=data['invoice_count'])
    
    wb.save(filename)
    print(f"✅ Đã tạo báo cáo Excel: {filename}")
```

---

## 7. Tối ưu hóa

### ⚡ Các kỹ thuật tối ưu:

#### **A. Caching dữ liệu**
```python
import pickle
import os
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_filename(self, key):
        return os.path.join(self.cache_dir, f"{key}.pkl")
    
    def is_cache_valid(self, filename, max_age_hours=1):
        """Kiểm tra cache còn hợp lệ không"""
        if not os.path.exists(filename):
            return False
        
        file_time = datetime.fromtimestamp(os.path.getmtime(filename))
        return datetime.now() - file_time < timedelta(hours=max_age_hours)
    
    def get_cached_data(self, key, max_age_hours=1):
        """Lấy dữ liệu từ cache"""
        filename = self.get_cache_filename(key)
        
        if self.is_cache_valid(filename, max_age_hours):
            with open(filename, 'rb') as f:
                return pickle.load(f)
        return None
    
    def save_to_cache(self, key, data):
        """Lưu dữ liệu vào cache"""
        filename = self.get_cache_filename(key)
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
```

#### **B. Async requests (Nâng cao)**
```python
import asyncio
import aiohttp

async def fetch_data_async(self, session, url, params=None):
    """Fetch dữ liệu bất đồng bộ"""
    headers = {'Authorization': f'Bearer {self.access_token}'}
    
    async with session.get(url, headers=headers, params=params) as response:
        if response.status == 200:
            return await response.json()
        return None

async def get_multiple_endpoints_async(self, endpoints):
    """Lấy dữ liệu từ nhiều endpoint cùng lúc"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for endpoint in endpoints:
            url = f"{self.base_url}/{endpoint}"
            task = self.fetch_data_async(session, url)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
```

---

## 🎯 Ví dụ hoàn chỉnh - Main Application

```python
# main.py
from datetime import datetime, timedelta
from api_client import APIClient
from data_processor import DataProcessor
from report_generator import ReportGenerator

def main():
    # 1. Khởi tạo API client
    api = APIClient(
        base_url="https://public.kiotapi.com",
        client_id="your_client_id",
        client_secret="your_client_secret"
    )
    
    # 2. Xác thực
    if not api.authenticate():
        print("❌ Không thể xác thực API")
        return
    
    print("✅ Kết nối API thành công")
    
    # 3. Lấy dữ liệu
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # 30 ngày gần nhất
    
    print("📊 Đang lấy dữ liệu...")
    invoices = api.get_invoices(start_date, end_date)
    
    if not invoices:
        print("❌ Không có dữ liệu")
        return
    
    # 4. Xử lý dữ liệu
    processor = DataProcessor()
    cleaned_data = processor.clean_data(invoices)
    product_metrics = processor.calculate_metrics(cleaned_data)
    
    # 5. Tạo báo cáo
    reporter = ReportGenerator()
    
    # Top sản phẩm theo doanh thu
    top_revenue = processor.get_top_products(product_metrics, 'revenue', 10)
    reporter.print_report(top_revenue, "TOP 10 SẢN PHẨM THEO DOANH THU")
    
    # Top sản phẩm theo số đơn
    top_orders = processor.get_top_products(product_metrics, 'orders', 10)
    reporter.print_report(top_orders, "TOP 10 SẢN PHẨM THEO SỐ ĐƠN")
    
    # Xuất báo cáo
    reporter.generate_html_report(top_revenue, "bao_cao_doanh_thu.html")
    reporter.generate_excel_report(top_revenue, "bao_cao_doanh_thu.xlsx")
    
    print("\n🎉 Hoàn thành!")

if __name__ == "__main__":
    main()
```

---

## 🛡️ Best Practices

### 1. **Bảo mật**
- Không hardcode API keys trong code
- Sử dụng environment variables
- Implement rate limiting
- Log requests nhưng không log sensitive data

### 2. **Error Handling**
```python
try:
    data = api.get_data()
except requests.exceptions.Timeout:
    print("❌ Timeout - API phản hồi quá chậm")
except requests.exceptions.ConnectionError:
    print("❌ Không thể kết nối đến API")
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP Error: {e.response.status_code}")
except Exception as e:
    print(f"❌ Lỗi không xác định: {e}")
```

### 3. **Performance**
- Sử dụng pagination hiệu quả
- Cache dữ liệu không thay đổi thường xuyên
- Sử dụng connection pooling
- Implement concurrent requests khi có thể

### 4. **Monitoring**
```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_client.log'),
        logging.StreamHandler()
    ]
)

def log_api_request(self, endpoint, params, response_time):
    logging.info(f"API Call: {endpoint} | Params: {params} | Time: {response_time}ms")
```

---

## 🎓 Tổng kết

### ✅ Checklist hoàn chỉnh:
- [ ] Tìm hiểu API documentation
- [ ] Setup môi trường Python
- [ ] Implement authentication
- [ ] Xây dựng data fetching logic
- [ ] Xử lý errors và edge cases
- [ ] Implement data processing
- [ ] Tạo reporting system
- [ ] Add caching và optimization
- [ ] Testing và debugging
- [ ] Documentation

### 🚀 Bước tiếp theo:
1. **Mở rộng**: Thêm nhiều loại báo cáo
2. **Tự động hóa**: Schedule reports định kỳ
3. **UI/UX**: Tạo web interface
4. **Visualization**: Thêm charts và graphs
5. **AI/ML**: Implement predictive analytics

---

*📝 Tài liệu này được tạo dựa trên kinh nghiệm thực tế xây dựng KiotViet API Tool*
