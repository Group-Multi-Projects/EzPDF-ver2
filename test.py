import requests
import time

# Địa chỉ của server Nginx (hoặc IP của bạn)
url = "http://localhost/client"  # Đổi thành địa chỉ server của bạn
response = requests.get(url)
print(f"Mã trạng thái: {response.status_code}")

# # Số lượng yêu cầu bạn muốn gửi
# num_requests = 20

# for i in range(num_requests):

#     try:
#         # Gửi yêu cầu đến server
#         response = requests.get(url)
#         print(f"Yêu cầu {i+1} gửi thành công, mã trạng thái: {response.status_code}")
#     except requests.exceptions.RequestException as e:
#         print(f"Yêu cầu {i+1} gặp lỗi: {e}")
    
#     # Giới hạn tốc độ yêu cầu để vượt quá rate/burst của Nginx
#     # Gửi yêu cầu liên tục mà không nghỉ để vượt quá giới hạn tốc độ của Nginx
#     time.sleep(0.1)  # Điều chỉnh thời gian nghỉ giữa các yêu cầu nếu cần
