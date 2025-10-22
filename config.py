# /thu_ky_tien_bot/config.py

import os
import pytz
from dotenv import load_dotenv

load_dotenv()

# --- CẤU HÌNH BOT THƯ KÝ ---
SECRETARY_TELEGRAM_TOKEN = os.getenv('SECRETARY_TELEGRAM_TOKEN')
SECRETARY_CHAT_ID = os.getenv('SECRETARY_CHAT_ID')

# --- CẤU HÌNH LIÊN KẾT & MEDIA ---
MAIN_GROUP_LINK = 'https://t.me/+KUseOkZUXL0wY2M1'
REMINDER_VIDEO_PATH = os.path.join('media', 'reminder.mp4') 
INTRODUCTION_VIDEO_PATH = os.path.join('media', 'introduction.mp4')
# <<< THÊM MỚI: Đường dẫn đến ảnh chia vốn >>>
CAPITAL_DIVISION_IMAGE_PATH = os.path.join('media', 'chia_von.jpg')

# --- CẤU HÌNH THỜI GIAN ---
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
SESSION_INTERVAL_MINUTES = 10