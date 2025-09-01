"""
API KiotViet NTV Tool
Tool để kết nối và truy vấn dữ liệu từ KiotViet API
Retailer: Loaded from environment variables
"""

import requests
import json
from datetime import datetime, timedelta
from config import Config

class KiotVietAPI:
    def __init__(self):
        # Load configuration from environment variables
        try:
            Config.validate()
        except ValueError as e:
            print(f"❌ Configuration Error: {e}")
            print("💡 Please check your .env file")
            raise
        
        # Thông tin kết nối từ config
        self.retailer = Config.RETAILER
        self.client_id = Config.CLIENT_ID
        self.client_secret = Config.CLIENT_SECRET
        self.base_url = Config.BASE_URL
        self.auth_url = Config.AUTH_URL
        self.access_token = None
        
    def get_access_token(self):
        """Lấy Access Token từ KiotViet"""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "scopes": "PublicApi.Access",
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            print("🔑 Đang xác thực với KiotViet API...")
            response = requests.post(self.auth_url, headers=headers, data=data)
            
            print(f"📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                
                if self.access_token:
                    print("✅ Đã kết nối thành công với KiotViet API")
                    print(f"🎫 Token: {self.access_token[:20]}...")
                    return True
                else:
                    print("❌ Không thể lấy Access Token từ response")
                    print(f"Response: {response.text}")
                    return False
            else:
                print(f"❌ Lỗi HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False
        except Exception as e:
            print(f"❌ Lỗi không xác định: {e}")
            return False
    
    def get_headers(self):
        """Tạo headers cho API requests"""
        return {
            "Retailer": self.retailer,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def get_invoices(self, from_date, to_date, page_size=100, current_item=0):
        """Lấy danh sách hóa đơn trong khoảng thời gian"""
        if not self.access_token:
            if not self.get_access_token():
                return None
        
        url = f"{self.base_url}/invoices"
        params = {
            "lastModifiedFrom": from_date.strftime("%Y-%m-%dT00:00:00"),
            "lastModifiedTo": to_date.strftime("%Y-%m-%dT23:59:59"),
            "pageSize": page_size,
            "currentItem": current_item,
            "includeInvoiceDetail": True
        }
        
        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi khi lấy hóa đơn: {e}")
            return None
    
    def get_products(self, page_size=100, current_item=0):
        """Lấy danh sách sản phẩm"""
        if not self.access_token:
            if not self.get_access_token():
                return None
        
        url = f"{self.base_url}/products"
        params = {
            "pageSize": page_size,
            "currentItem": current_item,
            "includeInventory": True
        }
        
        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi khi lấy sản phẩm: {e}")
            return None
    
    def get_top_selling_products(self, month=None, year=2025, top_n=10):
        """Lấy top sản phẩm bán chạy nhất trong tháng hoặc năm"""
        if month:
            print(f"🔍 Đang tìm kiếm top {top_n} sản phẩm bán chạy nhất tháng {month}/{year}...")
            # Tính toán khoảng thời gian cho tháng
            from_date = datetime(year, month, 1)
            if month == 12:
                to_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                to_date = datetime(year, month + 1, 1) - timedelta(days=1)
        else:
            print(f"🔍 Đang tìm kiếm top {top_n} sản phẩm bán chạy nhất năm {year}...")
            # Tính toán khoảng thời gian cho cả năm
            from_date = datetime(year, 1, 1)
            to_date = datetime(year, 12, 31)
        
        print(f"📅 Từ ngày: {from_date.strftime('%d/%m/%Y')}")
        print(f"📅 Đến ngày: {to_date.strftime('%d/%m/%Y')}")
        
        # Lấy tất cả hóa đơn trong tháng
        all_invoices = []
        current_item = 0
        page_size = 100
        
        while True:
            print(f"📄 Đang tải hóa đơn... (trang {current_item//page_size + 1})")
            invoices_data = self.get_invoices(from_date, to_date, page_size, current_item)
            
            if not invoices_data or not invoices_data.get('data'):
                break
            
            all_invoices.extend(invoices_data['data'])
            
            # Kiểm tra xem còn dữ liệu không
            if len(invoices_data['data']) < page_size:
                break
            
            current_item += page_size
        
        print(f"📊 Đã tải {len(all_invoices)} hóa đơn")
        
        # Tính toán số lượng bán cho từng sản phẩm
        product_sales = {}
        
        for invoice in all_invoices:
            if invoice.get('invoiceDetails'):
                for detail in invoice['invoiceDetails']:
                    product_id = detail.get('productId')
                    product_name = detail.get('productName', 'Không xác định')
                    quantity = detail.get('quantity', 0)
                    price = detail.get('price', 0)
                    
                    if product_id not in product_sales:
                        product_sales[product_id] = {
                            'name': product_name,
                            'total_quantity': 0,
                            'total_revenue': 0,
                            'invoice_count': 0
                        }
                    
                    product_sales[product_id]['total_quantity'] += quantity
                    product_sales[product_id]['total_revenue'] += quantity * price
                    product_sales[product_id]['invoice_count'] += 1
        
        # Sắp xếp theo số lượng bán
        sorted_products = sorted(
            product_sales.items(),
            key=lambda x: x[1]['total_quantity'],
            reverse=True
        )
        
        # Sắp xếp theo số lượng hóa đơn
        sorted_products_by_invoice = sorted(
            product_sales.items(),
            key=lambda x: x[1]['invoice_count'],
            reverse=True
        )
        
        # Lấy top N sản phẩm
        top_products = sorted_products[:top_n]
        
        # Hiển thị kết quả
        if month:
            period_text = f"THÁNG {month}/{year}"
        else:
            period_text = f"NĂM {year}"
            
        print(f"\n🏆 TOP {top_n} SẢN PHẨM BÁN CHẠY NHẤT {period_text}")
        print("=" * 80)
        
        for i, (product_id, data) in enumerate(top_products, 1):
            print(f"{i:2d}. {data['name'][:50]}")
            print(f"    📦 Số lượng bán: {data['total_quantity']:,}")
            print(f"    💰 Doanh thu: {data['total_revenue']:,.0f} VNĐ")
            print(f"    📋 Số hóa đơn: {data['invoice_count']}")
            print("-" * 60)
        
        return top_products
    
    def get_top_products_by_revenue(self, month=None, year=2025, top_n=10):
        """Lấy top sản phẩm mang lại doanh thu/lợi nhuận nhiều nhất trong tháng hoặc năm"""
        if month:
            print(f"🔍 Đang tìm kiếm top {top_n} sản phẩm mang lại doanh thu nhiều nhất tháng {month}/{year}...")
            # Tính toán khoảng thời gian cho tháng
            from_date = datetime(year, month, 1)
            if month == 12:
                to_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                to_date = datetime(year, month + 1, 1) - timedelta(days=1)
        else:
            print(f"🔍 Đang tìm kiếm top {top_n} sản phẩm mang lại doanh thu nhiều nhất năm {year}...")
            # Tính toán khoảng thời gian cho cả năm
            from_date = datetime(year, 1, 1)
            to_date = datetime(year, 12, 31)
        
        print(f"📅 Từ ngày: {from_date.strftime('%d/%m/%Y')}")
        print(f"📅 Đến ngày: {to_date.strftime('%d/%m/%Y')}")
        
        # Lấy tất cả hóa đơn trong khoảng thời gian
        all_invoices = []
        current_item = 0
        page_size = 100
        
        while True:
            print(f"📄 Đang tải hóa đơn... (trang {current_item//page_size + 1})")
            invoices_data = self.get_invoices(from_date, to_date, page_size, current_item)
            
            if not invoices_data or not invoices_data.get('data'):
                break
            
            all_invoices.extend(invoices_data['data'])
            
            # Kiểm tra xem còn dữ liệu không
            if len(invoices_data['data']) < page_size:
                break
            
            current_item += page_size
        
        print(f"📊 Đã tải {len(all_invoices)} hóa đơn")
        
        # Tính toán doanh thu cho từng sản phẩm
        product_sales = {}
        
        for invoice in all_invoices:
            if invoice.get('invoiceDetails'):
                for detail in invoice['invoiceDetails']:
                    product_id = detail.get('productId')
                    product_name = detail.get('productName', 'Không xác định')
                    quantity = detail.get('quantity', 0)
                    price = detail.get('price', 0)
                    
                    if product_id not in product_sales:
                        product_sales[product_id] = {
                            'name': product_name,
                            'total_quantity': 0,
                            'total_revenue': 0,
                            'invoice_count': 0
                        }
                    
                    product_sales[product_id]['total_quantity'] += quantity
                    product_sales[product_id]['total_revenue'] += quantity * price
                    product_sales[product_id]['invoice_count'] += 1
        
        # Sắp xếp theo doanh thu
        sorted_products_by_revenue = sorted(
            product_sales.items(),
            key=lambda x: x[1]['total_revenue'],
            reverse=True
        )
        
        # Lấy top N sản phẩm
        top_products = sorted_products_by_revenue[:top_n]
        
        # Hiển thị kết quả
        if month:
            period_text = f"THÁNG {month}/{year}"
        else:
            period_text = f"NĂM {year}"
            
        print(f"\n🏆 TOP {top_n} SẢN PHẨM MANG LẠI DOANH THU NHIỀU NHẤT {period_text}")
        print("=" * 80)
        
        total_revenue = sum(data['total_revenue'] for _, data in top_products)
        
        for i, (product_id, data) in enumerate(top_products, 1):
            revenue_percent = (data['total_revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            avg_price = data['total_revenue'] / data['total_quantity'] if data['total_quantity'] > 0 else 0
            
            print(f"{i:2d}. {data['name'][:50]}")
            print(f"    💰 Doanh thu: {data['total_revenue']:,.0f} VNĐ ({revenue_percent:.1f}%)")
            print(f"    📦 Tổng số lượng bán: {data['total_quantity']:,}")
            print(f"    📋 Số đơn hàng: {data['invoice_count']}")
            print(f"    💵 Giá trung bình: {avg_price:,.0f} VNĐ/sản phẩm")
            print("-" * 60)
        
        print(f"\n📈 Tổng doanh thu top {top_n}: {total_revenue:,.0f} VNĐ")
        
        return top_products
    
    def get_top_products_by_invoice_count(self, month=None, year=2025, top_n=10):
        """Lấy top sản phẩm có nhiều đơn hàng nhất trong tháng hoặc năm"""
        if month:
            print(f"🔍 Đang tìm kiếm top {top_n} sản phẩm có nhiều đơn hàng nhất tháng {month}/{year}...")
            # Tính toán khoảng thời gian cho tháng
            from_date = datetime(year, month, 1)
            if month == 12:
                to_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                to_date = datetime(year, month + 1, 1) - timedelta(days=1)
        else:
            print(f"🔍 Đang tìm kiếm top {top_n} sản phẩm có nhiều đơn hàng nhất năm {year}...")
            # Tính toán khoảng thời gian cho cả năm
            from_date = datetime(year, 1, 1)
            to_date = datetime(year, 12, 31)
        
        print(f"📅 Từ ngày: {from_date.strftime('%d/%m/%Y')}")
        print(f"📅 Đến ngày: {to_date.strftime('%d/%m/%Y')}")
        
        # Lấy tất cả hóa đơn trong khoảng thời gian
        all_invoices = []
        current_item = 0
        page_size = 100
        
        while True:
            print(f"📄 Đang tải hóa đơn... (trang {current_item//page_size + 1})")
            invoices_data = self.get_invoices(from_date, to_date, page_size, current_item)
            
            if not invoices_data or not invoices_data.get('data'):
                break
            
            all_invoices.extend(invoices_data['data'])
            
            # Kiểm tra xem còn dữ liệu không
            if len(invoices_data['data']) < page_size:
                break
            
            current_item += page_size
        
        print(f"📊 Đã tải {len(all_invoices)} hóa đơn")
        
        # Tính toán số lượng đơn hàng cho từng sản phẩm
        product_sales = {}
        
        for invoice in all_invoices:
            if invoice.get('invoiceDetails'):
                for detail in invoice['invoiceDetails']:
                    product_id = detail.get('productId')
                    product_name = detail.get('productName', 'Không xác định')
                    quantity = detail.get('quantity', 0)
                    price = detail.get('price', 0)
                    
                    if product_id not in product_sales:
                        product_sales[product_id] = {
                            'name': product_name,
                            'total_quantity': 0,
                            'total_revenue': 0,
                            'invoice_count': 0
                        }
                    
                    product_sales[product_id]['total_quantity'] += quantity
                    product_sales[product_id]['total_revenue'] += quantity * price
                    product_sales[product_id]['invoice_count'] += 1
        
        # Sắp xếp theo số lượng hóa đơn
        sorted_products_by_invoice = sorted(
            product_sales.items(),
            key=lambda x: x[1]['invoice_count'],
            reverse=True
        )
        
        # Lấy top N sản phẩm
        top_products = sorted_products_by_invoice[:top_n]
        
        # Hiển thị kết quả
        if month:
            period_text = f"THÁNG {month}/{year}"
        else:
            period_text = f"NĂM {year}"
            
        print(f"\n🏆 TOP {top_n} SẢN PHẨM CÓ NHIỀU ĐƠN HÀNG NHẤT {period_text}")
        print("=" * 80)
        
        for i, (product_id, data) in enumerate(top_products, 1):
            print(f"{i:2d}. {data['name'][:50]}")
            print(f"    📋 Số đơn hàng: {data['invoice_count']}")
            print(f"    📦 Tổng số lượng bán: {data['total_quantity']:,}")
            print(f"    💰 Doanh thu: {data['total_revenue']:,.0f} VNĐ")
            print("-" * 60)
        
        return top_products
    
    def answer_question(self, question):
        """Trả lời câu hỏi về dữ liệu"""
        print(f"❓ Câu hỏi: {question}")
        question_lower = question.lower()
        
        # Phân tích câu hỏi để xác định loại thống kê
        is_invoice_count_query = any(phrase in question_lower for phrase in [
            'nhiều đơn hàng', 'nhiều hóa đơn', 'đơn hàng nhiều', 'hóa đơn nhiều',
            'số đơn', 'số hóa đơn', 'xuất hiện nhiều'
        ])
        
        is_revenue_query = any(phrase in question_lower for phrase in [
            'doanh thu', 'lợi nhuận', 'thu nhập', 'tiền', 'revenue', 'profit',
            'mang lại nhiều', 'kiếm được nhiều', 'sinh lời'
        ])
        
        if "top" in question_lower:
            # Tìm số lượng top
            import re
            numbers = re.findall(r'\d+', question)
            top_n = int(numbers[0]) if numbers else 10
            
            # Kiểm tra xem là tháng hay năm
            if "năm" in question_lower:
                # Tìm năm
                year_match = re.search(r'năm (\d{4})', question_lower)
                year = int(year_match.group(1)) if year_match else 2024
                
                if is_invoice_count_query:
                    return self.get_top_products_by_invoice_count(month=None, year=year, top_n=top_n)
                elif is_revenue_query:
                    return self.get_top_products_by_revenue(month=None, year=year, top_n=top_n)
                else:
                    return self.get_top_selling_products(month=None, year=year, top_n=top_n)
            
            elif "tháng" in question_lower:
                # Tìm tháng
                if "tháng 8" in question_lower:
                    month = 8
                else:
                    month_match = re.search(r'tháng (\d+)', question_lower)
                    month = int(month_match.group(1)) if month_match else 8
                
                # Tìm năm (nếu có)
                year_match = re.search(r'(\d{4})', question_lower)
                year = int(year_match.group(1)) if year_match else 2025
                
                if is_invoice_count_query:
                    return self.get_top_products_by_invoice_count(month=month, year=year, top_n=top_n)
                elif is_revenue_query:
                    return self.get_top_products_by_revenue(month=month, year=year, top_n=top_n)
                else:
                    return self.get_top_selling_products(month=month, year=year, top_n=top_n)
            
            else:
                # Mặc định là tháng hiện tại
                if is_invoice_count_query:
                    return self.get_top_products_by_invoice_count(month=8, year=2025, top_n=top_n)
                elif is_revenue_query:
                    return self.get_top_products_by_revenue(month=8, year=2025, top_n=top_n)
                else:
                    return self.get_top_selling_products(month=8, year=2025, top_n=top_n)
        
        else:
            print("❓ Tôi chưa hiểu câu hỏi này. Hiện tại tôi có thể trả lời:")
            print("- Top X sản phẩm bán chạy nhất tháng Y (theo số lượng)")
            print("- Top X sản phẩm có nhiều đơn hàng nhất tháng Y")
            print("- Top X sản phẩm mang lại doanh thu/lợi nhuận nhiều nhất tháng Y")
            print("- Top X sản phẩm bán chạy nhất năm YYYY")
            print("- Top X sản phẩm có nhiều đơn hàng nhất năm YYYY")
            print("- Top X sản phẩm mang lại doanh thu/lợi nhuận nhiều nhất năm YYYY")
            return None

def main():
    """Hàm chính để chạy tool"""
    api = KiotVietAPI()
    
    print("🚀 Khởi động API KiotViet NTV Tool")
    print(f"🏪 Retailer: {api.retailer}")
    print("-" * 50)
    
    # Test kết nối
    if api.get_access_token():
        print("\n💡 Bạn có thể đặt câu hỏi như:")
        print("- Top 10 sản phẩm bán chạy nhất trong tháng 8")
        print("- Top 5 sản phẩm bán chạy nhất tháng 7")
        print("- Top 10 sản phẩm bán chạy nhất năm 2024")
        print("- Top 10 sản phẩm có nhiều đơn hàng nhất năm 2024")
        print("- Top 10 sản phẩm mang lại lợi nhuận nhiều nhất năm 2024")
        
        # Vòng lặp để nhận câu hỏi từ người dùng
        while True:
            print("\n" + "="*50)
            question = input("❓ Nhập câu hỏi của bạn (hoặc 'quit' để thoát): ").strip()
            
            if question.lower() in ['quit', 'exit', 'thoat']:
                print("👋 Tạm biệt!")
                break
            
            if question:
                api.answer_question(question)
            else:
                # Câu hỏi mặc định nếu không nhập gì
                print("📋 Sử dụng câu hỏi mặc định...")
                api.answer_question("Top 10 sản phẩm bán chạy nhất năm 2024")
        
    else:
        print("❌ Không thể kết nối. Vui lòng kiểm tra thông tin kết nối.")

if __name__ == "__main__":
    main()
