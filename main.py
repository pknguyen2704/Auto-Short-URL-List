import requests
import pandas as pd

# Hàm để rút gọn link và custom alias sử dụng TinyURL
def shorten_link_tinyurl(long_url, custom_alias):

    tinyurl_url = 'https://api.tinyurl.com/create'

    # Dữ liệu yêu cầu (bao gồm cả custom alias nếu có)
    data = {
        "url": long_url,
        "domain": "tinyurl.com",
        "alias": custom_alias,
        # "tags": "example,link",
        "description": "string"
    }

    # Gửi yêu cầu POST
    response = requests.post(tinyurl_url, headers={'Authorization': 'Bearer jkRpWJ81OD9i9Mw8W06ANwSCUQo2Z38C8x1H7wsUQS8lA0x1iCOWLE4AwD34'}, json=data)

    # Kiểm tra mã trạng thái HTTP
    if response.status_code == 200:
        try:
            return response.json()['data']['tiny_url']
        except requests.exceptions.JSONDecodeError as e:
            print(f"Lỗi khi giải mã JSON: {e}")
            print(f"Nội dung phản hồi: {response.text}")  # In nội dung phản hồi
    else:
        print(f"API trả về lỗi: {response.status_code}")
        print(f"Nội dung phản hồi: {response.text}")  # In thông báo lỗi từ API

    return None  # Trả về None nếu có lỗi

# Đọc file CSV chứa danh sách các link gốc
df = pd.read_csv('linksList.csv')

# Tạo danh sách chứa các kết quả rút gọn link
shortened_links = []

# Duyệt qua từng hàng trong file CSV và rút gọn link
for index, row in df.iterrows():
    long_url = row['url']
    
    # Tạo custom alias tự động với cấu trúc TVTS + số thứ tự
    custom_alias = f"TVTS2024-{index+1:03d}"
    
    # Rút gọn link với TinyURL và custom alias
    short_link = shorten_link_tinyurl(long_url, custom_alias)
    print(index)
    # Kiểm tra nếu rút gọn thành công
    shortened_links.append({
        "original_url": long_url,
        "shortened_url": short_link,
        "custom_alias": custom_alias
    })
    print(f"Link gốc: {long_url}, Link rút gọn: {short_link}")

# Lưu kết quả vào file CSV mới nếu cần
output_df = pd.DataFrame(shortened_links)
output_df.to_csv('shortened_links.csv', index=False, sep=';')