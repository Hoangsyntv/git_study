#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from API_kiotviet_NTV import KiotVietAPI

def analyze_marketing_potential():
    """Phân tích sản phẩm tiềm năng cần đẩy mạnh marketing"""
    api = KiotVietAPI()
    
    if not api.get_access_token():
        print("❌ Không thể kết nối API")
        return
    
    print("✅ Kết nối API thành công\n")
    print("🎯 PHÂN TÍCH SẢN PHẨM TIỀM NĂNG CHO MARKETING NĂM 2024")
    print("=" * 80)
    
    # Lấy dữ liệu từ API
    from datetime import datetime
    
    # Lấy tất cả hóa đơn năm 2024
    all_invoices = []
    current_item = 0
    page_size = 100
    
    from_date = datetime(2024, 1, 1)
    to_date = datetime(2024, 12, 31)
    
    print("📊 Đang thu thập dữ liệu...")
    while True:
        print(f"📄 Đang tải hóa đơn... (trang {current_item//page_size + 1})")
        invoices_data = api.get_invoices(from_date, to_date, page_size, current_item)
        
        if not invoices_data or not invoices_data.get('data'):
            break
        
        all_invoices.extend(invoices_data['data'])
        
        if len(invoices_data['data']) < page_size:
            break
        
        current_item += page_size
    
    print(f"✅ Đã thu thập {len(all_invoices)} hóa đơn")
    
    # Phân tích dữ liệu
    product_metrics = {}
    
    for invoice in all_invoices:
        if invoice.get('invoiceDetails'):
            for detail in invoice['invoiceDetails']:
                product_id = detail.get('productId')
                product_name = detail.get('productName', 'Không xác định')
                quantity = detail.get('quantity', 0)
                price = detail.get('price', 0)
                
                if product_id not in product_metrics:
                    product_metrics[product_id] = {
                        'name': product_name,
                        'total_quantity': 0,
                        'total_revenue': 0,
                        'invoice_count': 0,
                        'avg_price': 0,
                        'avg_quantity_per_order': 0
                    }
                
                product_metrics[product_id]['total_quantity'] += quantity
                product_metrics[product_id]['total_revenue'] += quantity * price
                product_metrics[product_id]['invoice_count'] += 1
    
    # Tính toán các chỉ số bổ sung
    for product_id, metrics in product_metrics.items():
        if metrics['total_quantity'] > 0:
            metrics['avg_price'] = metrics['total_revenue'] / metrics['total_quantity']
        if metrics['invoice_count'] > 0:
            metrics['avg_quantity_per_order'] = metrics['total_quantity'] / metrics['invoice_count']
    
    # Lọc sản phẩm có tiềm năng marketing
    # Tiêu chí: Doanh thu cao (>100M) nhưng ít đơn hàng (<20)
    marketing_candidates = []
    
    for product_id, metrics in product_metrics.items():
        # Tiêu chí sản phẩm tiềm năng:
        # 1. Doanh thu >= 50 triệu VNĐ (sản phẩm có giá trị)
        # 2. Số đơn hàng <= 30 (chưa phổ biến)
        # 3. Giá trung bình >= 200k (không phải sản phẩm rẻ tiền)
        
        if (metrics['total_revenue'] >= 50_000_000 and 
            metrics['invoice_count'] <= 30 and 
            metrics['avg_price'] >= 200_000):
            
            # Tính điểm tiềm năng
            revenue_score = min(metrics['total_revenue'] / 1_000_000_000, 1.0) * 40  # Max 40 điểm
            price_score = min(metrics['avg_price'] / 10_000_000, 1.0) * 30  # Max 30 điểm
            scarcity_score = max(30 - metrics['invoice_count'], 0)  # Max 30 điểm
            
            potential_score = revenue_score + price_score + scarcity_score
            
            metrics['potential_score'] = potential_score
            metrics['revenue_per_order'] = metrics['total_revenue'] / metrics['invoice_count'] if metrics['invoice_count'] > 0 else 0
            
            marketing_candidates.append((product_id, metrics))
    
    # Sắp xếp theo điểm tiềm năng
    marketing_candidates.sort(key=lambda x: x[1]['potential_score'], reverse=True)
    
    # Hiển thị TOP 10
    top_10_candidates = marketing_candidates[:10]
    
    print(f"\n🎯 TOP 10 SẢN PHẨM TIỀM NĂNG CẦN ĐẨY MẠNH QUẢNG CÁO")
    print("💡 Tiêu chí: Doanh thu cao (≥50M) + Ít đơn hàng (≤30) + Giá cao (≥200k)")
    print("=" * 100)
    
    if not top_10_candidates:
        print("❌ Không tìm thấy sản phẩm phù hợp với tiêu chí")
        return
    
    for i, (product_id, metrics) in enumerate(top_10_candidates, 1):
        print(f"\n{i:2d}. {metrics['name'][:60]}")
        print(f"    🎯 Điểm tiềm năng: {metrics['potential_score']:.1f}/100")
        print(f"    💰 Doanh thu: {metrics['total_revenue']:,.0f} VNĐ")
        print(f"    📋 Số đơn hàng: {metrics['invoice_count']} đơn (CẦN TĂNG)")
        print(f"    💵 Giá trung bình: {metrics['avg_price']:,.0f} VNĐ/sản phẩm")
        print(f"    📊 Doanh thu/đơn: {metrics['revenue_per_order']:,.0f} VNĐ")
        print(f"    📦 Số lượng/đơn: {metrics['avg_quantity_per_order']:.1f} sản phẩm")
        print("-" * 80)
    
    # Phân tích chiến lược marketing
    print(f"\n📈 PHÂN TÍCH CHIẾN LƯỢC MARKETING:")
    print("-" * 60)
    
    # Nhóm theo mức giá
    high_value_products = [item for item in top_10_candidates if item[1]['avg_price'] >= 1_000_000]
    medium_value_products = [item for item in top_10_candidates if 500_000 <= item[1]['avg_price'] < 1_000_000]
    
    print(f"🔥 Sản phẩm cao cấp (≥1M VNĐ): {len(high_value_products)} sản phẩm")
    if high_value_products:
        for _, metrics in high_value_products[:3]:
            print(f"   • {metrics['name'][:40]} - {metrics['avg_price']:,.0f} VNĐ")
    
    print(f"⭐ Sản phẩm trung cấp (500k-1M VNĐ): {len(medium_value_products)} sản phẩm")
    if medium_value_products:
        for _, metrics in medium_value_products[:3]:
            print(f"   • {metrics['name'][:40]} - {metrics['avg_price']:,.0f} VNĐ")
    
    # Khuyến nghị chiến lược
    print(f"\n💡 KHUYẾN NGHỊ CHIẾN LƯỢC:")
    print("-" * 60)
    
    if high_value_products:
        print("🎯 SẢN PHẨM CAO CẤP:")
        print("   • Tập trung vào khách hàng doanh nghiệp, dự án lớn")
        print("   • Marketing B2B qua LinkedIn, triển lãm ngành")
        print("   • Tạo case study, portfolio dự án thành công")
        print("   • Chương trình ưu đãi cho đơn hàng lớn")
    
    if medium_value_products:
        print("\n⭐ SẢN PHẨM TRUNG CẤP:")
        print("   • Marketing mix B2B và B2C")
        print("   • Social media advertising (Facebook, Instagram)")
        print("   • Content marketing về lợi ích sản phẩm")
        print("   • Chương trình khuyến mại, combo deal")
    
    print(f"\n📊 TỔNG KẾT CƠ HỘI:")
    total_potential_revenue = sum(item[1]['total_revenue'] for item in top_10_candidates)
    total_orders = sum(item[1]['invoice_count'] for item in top_10_candidates)
    avg_revenue_per_order = total_potential_revenue / total_orders if total_orders > 0 else 0
    
    print(f"   💰 Tổng doanh thu hiện tại: {total_potential_revenue:,.0f} VNĐ")
    print(f"   📋 Tổng số đơn hiện tại: {total_orders} đơn")
    print(f"   📈 Trung bình doanh thu/đơn: {avg_revenue_per_order:,.0f} VNĐ")
    print(f"   🚀 Tiềm năng tăng trưởng: Nếu mỗi sản phẩm tăng gấp đôi số đơn")
    print(f"      → Doanh thu có thể đạt: {total_potential_revenue * 2:,.0f} VNĐ")
    
    return top_10_candidates

if __name__ == "__main__":
    analyze_marketing_potential()
