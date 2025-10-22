# /thu_ky_tien_bot/thu_ky_bot.py

import asyncio
import logging
import random
import os
from datetime import datetime, timedelta, date, time
from telegram import Bot
from flask import Flask
from threading import Thread

import config

# --- CẤU HÌNH WEB SERVER ĐỂ CHẠY TRÊN RENDER ---
app = Flask(__name__)

@app.route('/')
def hello():
    # Đây là trang web đơn giản mà UptimeRobot sẽ truy cập
    return "Thư Ký Tiên Bot is alive!"

def run_web_server():
    # Render sẽ tự động cung cấp PORT qua biến môi trường
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- PHẦN MÃ NGUỒN BOT (KHÔNG THAY ĐỔI) ---

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

INTRODUCTION_MESSAGES = [
    f"""<b>💎   𝗞𝗬̉ 𝗟𝗨𝗔̣̂𝗧 𝗟𝗔̀ 𝗦𝗨̛́𝗖 𝗠𝗔̣𝗡𝗛   💎</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>Thị trường luôn biến động, nhưng kỷ luật là thứ giúp chúng ta đứng vững. Luôn nhớ nguyên tắc vàng:</i>

🎯  <b>Chốt lãi đúng mục tiêu.</b>
🎯  <b>Cắt lỗ không do dự.</b>

Cùng nhau, chúng ta sẽ đi trên con đường dài và an toàn!""",
    f"""<b>🤝   Đ𝗢̂̀𝗡𝗚 𝗛𝗔̀𝗡𝗛 𝗖𝗨̀𝗡𝗚 𝗖𝗛𝗨𝗬𝗘̂𝗡 𝗚𝗜𝗔   🤝</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>Bạn không hề đơn độc! Luôn có Boss và đội ngũ hỗ trợ theo sát từng phiên. Hãy tin tưởng vào kinh nghiệm và tín hiệu được đưa ra.</i>

Việc của bạn chỉ là:
   ✅  <b>Chuẩn bị vốn.</b>
   ✅  <b>Sẵn sàng vào lệnh đúng thời điểm.</b>""",
]

def create_reminder_message(session_time: datetime) -> str:
    time_str = session_time.strftime('%H:%M')
    reminders = [
        "Một cái đầu lạnh sẽ tạo nên một chiến thắng lớn!",
        "Kỷ luật là chì khóa vàng dẫn đến thành công!",
        "Cùng nhau tạo nên một ca kéo thật bùng nổ nào!",
        "Tập trung, quyết đoán và chiến thắng!",
        "Thị trường đang chờ đợi những nhà vô địch!"
    ]
    link_text = "【 💎   𝗡𝗛𝗔̂́𝗣 𝗩𝗔̀𝗢 Đ𝗔̂𝗬 Đ𝗘̂̉ 𝗧𝗛𝗔𝗠 𝗚𝗜𝗔   💎 】"
    header = "🚨   <b>BÁO HIỆU CA KÉO 1 LỆNH</b>   🚨"
    separator = "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    return f"""
<b><a href="{config.MAIN_GROUP_LINK}">️‍🔥 THÔNG BÁO KHẨN TỪ THƯ KÝ TIÊN ️‍🔥</a></b>
{separator}
{header}
{separator}

🔔   Đếm ngược: Chỉ còn <b>𝟯 𝗽𝗵𝘂́𝘁</b> nữa là đến
<b>CA KÉO TIẾP THEO</b> lúc <b>{time_str}</b>.

<b>Anh em vui lòng:</b>
    ✨ Ổn định chỗ ngồi, giữ tinh thần thoải mái.
    💰 Chuẩn bị sẵn vốn theo đúng kỷ luật.

👇   <b>VÀO NHÓM NHẬN LỆNH TẠI ĐÂY</b>   👇

<a href="{config.MAIN_GROUP_LINK}"><b>{link_text}</b></a>
<a href="{config.MAIN_GROUP_LINK}"><b>{config.MAIN_GROUP_LINK}</b></a>

🪄  <i>Lời nhắn nhủ: {random.choice(reminders)}</i>
"""

def create_good_morning_message() -> str:
    return """☀️✨   𝗖𝗛𝗔̀𝗢 𝗕𝗨𝗢̂̉𝗜 𝗦𝗔́𝗡𝗚, Đ𝗔̣𝗜 𝗚𝗜𝗔 Đ𝗜̀𝗡𝗛!   ✨☀️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>Thư Ký Tiên chúc cả nhà một ngày mới tràn đầy năng lượng, giao dịch thuận lợi và gặt hái thật nhiều thắng lợi!</i>

Hãy cùng nhau bắt đầu một ngày thật rực rỡ nhé! 🚀"""

def create_good_night_message() -> str:
    return """🌙✨   𝗖𝗛𝗨́𝗖 𝗖𝗔̉ 𝗡𝗛𝗔̀ 𝗡𝗚𝗨̉ 𝗡𝗚𝗢𝗡   ✨🌙
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>Một ngày làm việc đã qua. Anh em hãy nghỉ ngơi thật tốt để lấy lại năng lượng cho những trận chiến ngày mai nhé.</i>

Hẹn gặp lại cả nhà vào sáng mai! ❤️"""

def create_introduction_message() -> str:
    return random.choice(INTRODUCTION_MESSAGES)

def create_capital_division_message() -> str:
    return """💰💰   𝗕𝗔̉𝗡𝗚 𝗖𝗛𝗜𝗔 𝗩𝗢̂́𝗡 𝗧𝗜𝗘̂𝗨 𝗖𝗛𝗨𝗔̂̉𝗡 (𝗟𝗘̣̂𝗡𝗛 𝟭𝟬%)  💰 💰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>Để đảm bảo an toàn và tối ưu lợi nhuận, anh em vui lòng tuân thủ nghiêm ngặt cách đi vốn theo bảng hướng dẫn.</i>

‼️  <b>LƯU Ý:</b> Vào lệnh đúng <b>10%</b> trên tổng số vốn của bạn.

<b>Kỷ luật là chìa khóa để chiến thắng!</b>"""

async def send_simple_message(bot: Bot, message: str, return_message: bool = False):
    try:
        sent_msg = await bot.send_message(
            chat_id=config.SECRETARY_CHAT_ID,
            text=message,
            parse_mode='HTML',
            disable_web_page_preview=False
        )
        if return_message:
            return sent_msg
    except Exception as e:
        logging.error(f"❌ Lỗi khi gửi tin nhắn đơn giản: {e}")
    return None

async def send_reminder_video(bot: Bot, session_time: datetime):
    caption = create_reminder_message(session_time)
    sent_message = None
    try:
        with open(config.REMINDER_VIDEO_PATH, 'rb') as video_file:
            sent_message = await bot.send_video(
                chat_id=config.SECRETARY_CHAT_ID,
                video=video_file,
                caption=caption,
                parse_mode='HTML'
            )
        logging.info(f"🧚‍♀️  Đã gửi video nhắc nhở ca {session_time.strftime('%H:%M')}.")
    except FileNotFoundError:
        logging.warning(f"Không tìm thấy file VIDEO nhắc nhở. Gửi tạm tin nhắn văn bản.")
        sent_message = await send_simple_message(bot, caption, return_message=True)
    except Exception as e:
        logging.error(f"❌ Lỗi khi gửi video nhắc nhở: {e}")

    if sent_message:
        try:
            await bot.pin_chat_message(
                chat_id=config.SECRETARY_CHAT_ID,
                message_id=sent_message.message_id
            )
            logging.info(f"📌  Đã ghim tin nhắn nhắc nhở (ID: {sent_message.message_id}).")
        except Exception as e:
            logging.error(f"❌ Không thể ghim tin nhắn: {e}. Vui lòng kiểm tra quyền của bot.")

async def send_capital_division_photo(bot: Bot):
    caption = create_capital_division_message()
    try:
        with open(config.CAPITAL_DIVISION_IMAGE_PATH, 'rb') as photo_file:
            await bot.send_photo(
                chat_id=config.SECRETARY_CHAT_ID,
                photo=photo_file,
                caption=caption,
                parse_mode='HTML'
            )
        logging.info("💰  Đã gửi ảnh hướng dẫn chia vốn.")
    except FileNotFoundError:
        logging.warning(f"Không tìm thấy file ẢNH chia vốn. Bỏ qua.")
    except Exception as e:
        logging.error(f"❌ Lỗi khi gửi ảnh chia vốn: {e}")

async def send_introduction_video(bot: Bot):
    caption = create_introduction_message()
    try:
        with open(config.INTRODUCTION_VIDEO_PATH, 'rb') as video_file:
            await bot.send_video(
                chat_id=config.SECRETARY_CHAT_ID,
                video=video_file,
                caption=caption,
                parse_mode='HTML'
            )
        logging.info("🎬  Đã gửi video giới thiệu nhóm.")
    except FileNotFoundError:
        logging.warning(f"Không tìm thấy file VIDEO giới thiệu. Gửi tạm tin nhắn văn bản.")
        await send_simple_message(bot, caption)
    except Exception as e:
        logging.error(f"❌ Lỗi khi gửi video giới thiệu: {e}")

async def handle_session_reminder(bot: Bot, session_time: datetime):
    await send_reminder_video(bot, session_time)
    await asyncio.sleep(1)
    await send_capital_division_photo(bot)

async def main_loop():
    if not all([config.SECRETARY_TELEGRAM_TOKEN, config.SECRETARY_CHAT_ID]):
        logging.critical("❌ Thiếu TOKEN hoặc CHAT_ID. Vui lòng kiểm tra biến môi trường.")
        return

    bot = Bot(token=config.SECRETARY_TELEGRAM_TOKEN)
    logging.info("🚀 Bot Thư Ký Tiên (v4.1 - Deploy) đã khởi động! Hoạt động từ 06:50 đến 22:00.")
    
    sent_flags = { 'last_reminder_minute': -1, 'last_intro_hour': -1, 'today': date.today(), 'is_sleeping_logged': False }
    start_time = time(6, 50)
    end_time_hour = 22

    while True:
        now = datetime.now(config.VN_TZ)
        is_sleeping_time = now.time() < start_time or now.hour > end_time_hour
        
        if is_sleeping_time:
            if not sent_flags['is_sleeping_logged']:
                logging.info(f"🌙 Bot đang trong giờ nghỉ ngơi. Sẽ hoạt động lại lúc {start_time.strftime('%H:%M')}.")
                sent_flags['is_sleeping_logged'] = True
            if now.date() != sent_flags['today']:
                sent_flags = { 'last_reminder_minute': -1, 'last_intro_hour': -1, 'today': now.date(), 'is_sleeping_logged': True }
                logging.info(f"☀️  Đã qua ngày mới {now.strftime('%d/%m/%Y')}! Đã reset trạng thái.")
            await asyncio.sleep(60)
            continue
        
        if sent_flags['is_sleeping_logged']:
            sent_flags['is_sleeping_logged'] = False
            logging.info("☀️  Bot bắt đầu ca làm việc!")

        if now.date() != sent_flags['today']:
            sent_flags = { 'last_reminder_minute': -1, 'last_intro_hour': -1, 'today': now.date(), 'is_sleeping_logged': False }
            logging.info(f"☀️  Chào ngày mới {now.strftime('%d/%m/%Y')}! Đã reset trạng thái.")

        if now.hour == 7 and 'morning_sent' not in sent_flags:
            await send_simple_message(bot, create_good_morning_message())
            sent_flags['morning_sent'] = True
        if now.hour in [8, 12, 16, 20] and now.hour != sent_flags['last_intro_hour']:
            await send_introduction_video(bot)
            sent_flags['last_intro_hour'] = now.hour
        if now.hour == 22 and 'night_sent' not in sent_flags:
            await send_simple_message(bot, create_good_night_message())
            sent_flags['night_sent'] = True
        is_reminder_time = (now.minute + 3) % config.SESSION_INTERVAL_MINUTES == 0
        if is_reminder_time and now.minute != sent_flags['last_reminder_minute']:
            sent_flags['last_reminder_minute'] = now.minute
            session_start_time = now.replace(second=0, microsecond=0) + timedelta(minutes=3)
            asyncio.create_task(handle_session_reminder(bot, session_start_time))
        await asyncio.sleep(5)

# --- KHỞI ĐỘNG CẢ BOT VÀ WEB SERVER ---
if __name__ == "__main__":
    # Chạy bot trong một luồng (thread) riêng để không chặn web server
    bot_thread = Thread(target=lambda: asyncio.run(main_loop()))
    bot_thread.start()
    
    # Chạy web server trong luồng chính để Render nhận diện
    run_web_server()