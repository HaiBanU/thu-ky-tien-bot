import os
import pytz
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

# --- CẤU HÌNH BOT THƯ KÝ ---
# Lấy token và ID của kênh chat từ biến môi trường
SECRETARY_TELEGRAM_TOKEN = os.getenv('SECRETARY_TELEGRAM_TOKEN')
SECRETARY_CHAT_ID = os.getenv('SECRETARY_CHAT_ID')

# --- CẤU HÌNH LIÊN KẾT & MEDIA ---
# Đường dẫn tới các file media. Bot sẽ tìm các file này trong thư mục 'media'
MAIN_GROUP_LINK = 'https://t.me/+KUseOkZUXL0wY2M1'
REMINDER_VIDEO_PATH = os.path.join('media', 'reminder.mp4')
INTRODUCTION_VIDEO_PATH = os.path.join('media', 'introduction.mp4')
CAPITAL_DIVISION_IMAGE_PATH = os.path.join('media', 'chia_von.jpg')
SCHEDULE_IMAGE_PATH = os.path.join('media', 'khung_gio_len_ca.jpg') # Ảnh lịch 100 ca

# --- CẤU HÌNH THỜI GIAN ---
# Đặt múi giờ Việt Nam
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')