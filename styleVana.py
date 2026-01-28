import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def fetch_ulta_product_data():
    url = "https://www.stylevana.com/en_US/category/brand"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers, verify=False)

    brand_names = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # .BrandListSection__Listing 안의 모든 .pal-c-Link__label 찾기
        container = soup.find(class_='all-brand-container')
        brands = container.find_all(class_='brand-wrapper')

        for brand in brands:
            a = brand.find('a')
            brand_name = a.get_text(strip=True)
            brand_names.append(brand_name)

    return brand_names

# 데이터 추출
data = fetch_ulta_product_data()
print(f"총 {len(data)}개의 브랜드 추출 완료")
print("처음 10개 브랜드:", data[:10])


# DataFrame 생성
df = pd.DataFrame({
    '브랜드명': data,
    'Extracted Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
})

# 저장 폴더 확인 및 생성
output_dir = 'brandParsingData'
os.makedirs(output_dir, exist_ok=True)

# CSV 파일로 저장
csv_filename = os.path.join(output_dir, f'stylevana_brands_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
print(f"\nCSV 파일 저장 완료: {csv_filename}")

# Excel 파일로 저장
excel_filename = os.path.join(output_dir, f'stylevana_brands_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
df.to_excel(excel_filename, index=False, engine='openpyxl')
print(f"Excel 파일 저장 완료: {excel_filename}")