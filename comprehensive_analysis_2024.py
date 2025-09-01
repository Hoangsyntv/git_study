#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from API_kiotviet_NTV import KiotVietAPI

def comprehensive_analysis_2024():
    """Phân tích tổng hợp: So sánh sản phẩm theo số đơn hàng và doanh thu năm 2024"""
    api = KiotVietAPI()
    
    if not api.get_access_token():
        print("❌ Không thể kết nối API")
        return
    
    print("✅ Kết nối API thành công\n")
    print("🔍 BÁO CÁO PHÂN TÍCH TỔNG HỢP NĂM 2024")
    print("=" * 80)
    
    # 1. Top 10 sản phẩm có nhiều đơn hàng nhất
    print("\n📋 1. TOP 10 SẢN PHẨM CÓ NHIỀU ĐƠN HÀNG NHẤT:")
    print("-" * 60)
    invoice_result = api.answer_question("top 10 sản phẩm có nhiều đơn hàng nhất năm 2024")
    
    # 2. Top 10 sản phẩm mang lại doanh thu cao nhất
    print("\n\n💰 2. TOP 10 SẢN PHẨM MANG LẠI DOANH THU CAO NHẤT:")
    print("-" * 60)
    revenue_result = api.answer_question("top 10 sản phẩm mang lại lợi nhuận cao nhất năm 2024")
    
    # 3. Phân tích tổng hợp
    print("\n\n📊 3. PHÂN TÍCH TỔNG HỢP VÀ SO SÁNH:")
    print("-" * 60)
    
    if invoice_result and revenue_result:
        # Tạo danh sách tên sản phẩm từ cả hai kết quả
        invoice_products = [item[1]['name'] for item in invoice_result]
        revenue_products = [item[1]['name'] for item in revenue_result]
        
        # Tìm sản phẩm xuất hiện trong cả hai top 10
        common_products = set(invoice_products) & set(revenue_products)
        
        print(f"🎯 SẢN PHẨM XUẤT HIỆN TRONG CẢ HAI TOP 10:")
        if common_products:
            for i, product in enumerate(common_products, 1):
                # Tìm vị trí trong mỗi bảng xếp hạng
                invoice_rank = invoice_products.index(product) + 1
                revenue_rank = revenue_products.index(product) + 1
                print(f"  {i}. {product}")
                print(f"     📋 Xếp hạng đơn hàng: #{invoice_rank}")
                print(f"     💰 Xếp hạng doanh thu: #{revenue_rank}")
        else:
            print("  ❌ Không có sản phẩm nào xuất hiện trong cả hai top 10")
        
        print(f"\n🔍 PHÂN TÍCH CHIẾN LƯỢC:")
        print(f"  📈 Tổng số sản phẩm khác nhau trong 2 top 10: {len(set(invoice_products + revenue_products))}")
        print(f"  🎯 Sản phẩm cân bằng (cả đơn hàng & doanh thu): {len(common_products)}")
        print(f"  📋 Sản phẩm chỉ nhiều đơn hàng: {len(set(invoice_products) - common_products)}")
        print(f"  💰 Sản phẩm chỉ doanh thu cao: {len(set(revenue_products) - common_products)}")
        
        print(f"\n💡 KHUYẾN NGHỊ KINH DOANH:")
        if len(common_products) >= 3:
            print("  ✅ Doanh nghiệp có nhiều sản phẩm cân bằng tốt")
            print("  🎯 Tập trung phát triển các sản phẩm xuất hiện trong cả hai top")
        else:
            print("  ⚠️  Cần cân bằng portfolio sản phẩm")
            print("  🎯 Tìm cách tăng đơn hàng cho sản phẩm doanh thu cao")
            print("  💰 Tìm cách tăng giá trị cho sản phẩm có nhiều đơn hàng")

if __name__ == "__main__":
    comprehensive_analysis_2024()
