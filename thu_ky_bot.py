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
    # Trang web đơn giản để dịch vụ UptimeRobot hoặc chính Render kiểm tra
    return "Thư Ký Tiên Bot is alive!"

def run_web_server():
    # Render sẽ tự động cung cấp PORT qua biến môi trường
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- PHẦN MÃ NGUỒN BOT ---

# Cấu hình logging để dễ dàng theo dõi hoạt động và lỗi của bot
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler() # In log ra console của Render
    ]
)

# Lịch trình chi tiết 100 ca trong ngày
SESSION_SCHEDULE = [
    (1, time(7, 0)), (2, time(7, 10)), (3, time(7, 20)), (4, time(7, 30)), (5, time(7, 40)),
    (6, time(7, 50)), (7, time(8, 0)), (8, time(8, 10)), (9, time(8, 20)), (10, time(8, 30)),
    (11, time(8, 40)), (12, time(8, 50)), (13, time(9, 0)), (14, time(9, 10)), (15, time(9, 20)),
    (16, time(9, 30)), (17, time(9, 40)), (18, time(9, 50)), (19, time(10, 0)), (20, time(10, 10)),
    (21, time(10, 20)), (22, time(10, 30)), (23, time(10, 40)), (24, time(10, 50)), (25, time(11, 0)),
    (26, time(11, 10)), (27, time(11, 20)), (28, time(11, 30)), (29, time(11, 40)), (30, time(11, 50)),
    (31, time(12, 0)), (32, time(12, 10)), (33, time(12, 20)), (34, time(12, 30)), (35, time(12, 40)),
    (36, time(12, 50)), (37, time(13, 0)), (38, time(13, 10)), (39, time(13, 20)), (40, time(13, 30)),
    (41, time(13, 40)), (42, time(13, 50)), (43, time(14, 0)), (44, time(14, 10)), (45, time(14, 20)),
    (46, time(14, 30)), (47, time(14, 40)), (48, time(14, 50)), (49, time(15, 0)), (50, time(15, 10)),
    (51, time(15, 20)), (52, time(15, 30)), (53, time(15, 40)), (54, time(15, 50)), (55, time(16, 0)),
    (56, time(16, 10)), (57, time(16, 20)), (58, time(16, 30)), (59, time(16, 40)), (60, time(16, 50)),
    (61, time(17, 0)), (62, time(17, 10)), (63, time(17, 20)), (64, time(17, 30)), (65, time(17, 40)),
    (66, time(17, 50)), (67, time(18, 0)), (68, time(18, 10)), (69, time(18, 20)), (70, time(18, 30)),
    (71, time(18, 40)), (72, time(18, 50)), (73, time(19, 0)), (74, time(19, 10)), (75, time(19, 20)),
    (76, time(19, 30)), (77, time(19, 40)), (78, time(19, 50)), (79, time(20, 0)), (80, time(20, 10)),
    (81, time(20, 20)), (82, time(20, 30)), (83, time(20, 40)), (84, time(20, 50)), (85, time(21, 0)),
    (86, time(21, 10)), (87, time(21, 20)), (88, time(21, 30)), (89, time(21, 40)), (90, time(21, 50)),
    (91, time(22, 0)), (92, time(22, 10)), (93, time(22, 20)), (94, time(22, 30)), (95, time(22, 40)),
    (96, time(22, 50)), (97, time(23, 0)), (98, time(23, 10)), (99, time(23, 20)), (100, time(23, 30))
]

INTRODUCTION_MESSAGES = [
    f"""<b>💎   𝗞𝗬̉ 𝗟𝗨𝗔̣̂𝗧 𝗟𝗔̀ 𝗦𝗨̛́𝗖 𝗠𝗔̣𝗡𝗛   💎</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>Thị trường luôn biến động, nhưng kỷ luật là thứ giúp chúng ta đứng vững. Luôn nhớ nguyên tắc vàng:</i>

🎯  <b>Chốt lãi đúng mục tiêu.</b>
🎯  <b>Cắt lỗ không do dự.</b>

Cùng nhau, chúng ta sẽ đi trên con đường dài và an toàn!""",
    f"""<b>🤝   Đ𝗢̂̀𝗡𝗚 𝗛𝗔̀𝗡𝗛 𝗖𝗨̀𝗡𝗚 𝗖𝗛𝗨𝗬𝗘̂𝗡 𝗚𝗜𝗔   🤝</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>Bạn không hề đơn độc! Luôn có Boss và đội ngũ hỗ trợ theo sát từng phiên. Hãy tin tưởng vào kinh nghiệm và tín hiệu được đưa ra.</i>

Việc của bạn chỉ là:
   ✅  <b>Chuẩn bị vốn.</b>
   ✅  <b>Sẵn sàng vào lệnh đúng thời điểm.</b>""",
]

# Hàm tạo nội dung tin nhắn nhắc nhở ca kéo
def create_reminder_message(session_time: datetime, ca_number: int) -> str:
    time_str = session_time.strftime('%H:%M')
    today_str = session_time.strftime('%d/%m')
    reminders = [
        "Một cái đầu lạnh sẽ tạo nên một chiến thắng lớn!",
        "Kỷ luật là chìa khóa vàng dẫn đến thành công!",
        "Cùng nhau tạo nên một ca kéo thật bùng nổ nào!",
        "Tập trung, quyết đoán và chiến thắng!",
        "Thị trường đang chờ đợi những nhà vô địch!"
    ]
    link_text = "【 💎   𝗡𝗛𝗔̂́𝗣 𝗩𝗔̀𝗢 Đ𝗔̂𝗬 Đ𝗘̂̉ 𝗧𝗛𝗔𝗠 𝗚𝗜𝗔   💎 】"
    header = f"🚨   <b>BÁO HIỆU CA {ca_number} - NGÀY {today_str}</b>   🚨"
    separator = "━━━━━━━━━━━━━━━━━━━━━━━━"
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

━━━━━━━━━━━━━━━━━━━━━━
💬  <i>Cần hỗ trợ hãy liên hệ <b>BOSS: @BossMinhHieuu</b></i>
━━━━━━━━━━━━━━━━━━━━━━

🪄  <i>Lời nhắn nhủ: {random.choice(reminders)}</i>
"""

# Hàm tạo các tin nhắn khác
def create_good_morning_message() -> str:
    return """☀️✨   𝗖𝗛𝗔̀𝗢 𝗕𝗨𝗢̂̉𝗜 𝗦𝗔́𝗡𝗚, Đ𝗔̣𝗜 𝗚𝗜𝗔 Đ𝗜̀𝗡𝗛!   
━━━━━━━━━━━━━━━━━━━━━━━
<i>Thư Ký Tiên chúc cả nhà một ngày mới tràn đầy năng lượng, giao dịch thuận lợi và gặt hái thật nhiều thắng lợi!</i>

Hãy cùng nhau bắt đầu một ngày thật rực rỡ nhé! 🚀"""

def create_good_night_message() -> str:
    return """🌙✨   𝗖𝗛𝗨́𝗖 𝗖𝗔̉ 𝗡𝗛𝗔̀ 𝗡𝗚𝗨̉ 𝗡𝗚𝗢𝗡   
━━━━━━━━━━━━━━━━━━━━━━━
<i>Một ngày làm việc đã qua. Anh em hãy nghỉ ngơi thật tốt để lấy lại năng lượng cho những trận chiến ngày mai nhé.</i>

Hẹn gặp lại cả nhà vào sáng mai! ❤️"""

def create_introduction_message() -> str:
    return random.choice(INTRODUCTION_MESSAGES)

def create_capital_division_message() -> str:
    return """💰💰   𝗕𝗔̉𝗡𝗚 𝗖𝗛𝗜𝗔 𝗩𝗢̂́𝗡 𝗧𝗜𝗘̂𝗨 𝗖𝗛𝗨𝗔̂̉𝗡 (𝗟𝗘̣̂𝗡𝗛 𝟭𝟬%)  
━━━━━━━━━━━━━━━━━━━━━━━━
<i>Để đảm bảo an toàn và tối ưu lợi nhuận, anh em vui lòng tuân thủ nghiêm ngặt cách đi vốn theo bảng hướng dẫn.</i>

‼️  <b>LƯU Ý:</b> Vào lệnh đúng <b>10%</b> trên tổng số vốn của bạn.

━━━━━━━━━━━━━━━━━━━━━━━━
💬  <i>Cần hỗ trợ hãy liên hệ <b>BOSS: @BossMinhHieuu</b></i>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Kỷ luật là chìa khóa để chiến thắng!</b>"""

def create_schedule_message() -> str:
    messages = [
        "Anh em nhớ bám sát khung giờ để không bỏ lỡ ca nào nhé!",
        "Lưu lại lịch làm việc để cùng nhau chiến thắng mỗi ngày!",
        "Thành công đến từ kỷ luật. Hãy tuân thủ đúng khung giờ!",
    ]
    return f"""⏰   <b>KHUNG GIỜ LÀM VIỆC MINH HIẾU BCR</b>   
━━━━━━━━━━━━━━━━━━━━━━━━
{random.choice(messages)}

Cùng nhau chinh phục 100 ca mỗi ngày! 💪"""

# Các hàm gửi tin nhắn (dạng text, video, photo)
async def send_simple_message(bot: Bot, message: str, return_message: bool = False):
    try:
        sent_msg = await bot.send_message(
            chat_id=config.SECRETARY_CHAT_ID,
            text=message,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        if return_message:
            return sent_msg
    except Exception as e:
        logging.error(f"❌ Lỗi khi gửi tin nhắn đơn giản: {e}")
    return None

async def send_reminder_video(bot: Bot, session_time: datetime, ca_number: int):
    caption = create_reminder_message(session_time, ca_number)
    sent_message = None
    try:
        with open(config.REMINDER_VIDEO_PATH, 'rb') as video_file:
            sent_message = await bot.send_video(
                chat_id=config.SECRETARY_CHAT_ID,
                video=video_file,
                caption=caption,
                parse_mode='HTML'
            )
        logging.info(f"🧚‍♀️  Đã gửi video nhắc nhở CA {ca_number} lúc {session_time.strftime('%H:%M')}.")
    except FileNotFoundError:
        logging.warning(f"Không tìm thấy file VIDEO nhắc nhở tại '{config.REMINDER_VIDEO_PATH}'. Gửi tạm tin nhắn văn bản.")
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

            await asyncio.sleep(300) # Chờ 5 phút
            await bot.unpin_chat_message(
                chat_id=config.SECRETARY_CHAT_ID,
                message_id=sent_message.message_id
            )
            logging.info(f"ℹ️  Đã gỡ ghim tin nhắn nhắc nhở (ID: {sent_message.message_id}).")
        except Exception as e:
            logging.error(f"❌ Không thể ghim/gỡ ghim tin nhắn: {e}. Vui lòng kiểm tra quyền của bot.")

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
        logging.warning(f"Không tìm thấy file ẢNH chia vốn tại '{config.CAPITAL_DIVISION_IMAGE_PATH}'. Bỏ qua.")
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
        logging.warning(f"Không tìm thấy file VIDEO giới thiệu tại '{config.INTRODUCTION_VIDEO_PATH}'. Gửi tạm tin nhắn văn bản.")
        await send_simple_message(bot, caption)
    except Exception as e:
        logging.error(f"❌ Lỗi khi gửi video giới thiệu: {e}")

async def send_schedule_photo(bot: Bot):
    caption = create_schedule_message()
    try:
        with open(config.SCHEDULE_IMAGE_PATH, 'rb') as photo_file:
            await bot.send_photo(
                chat_id=config.SECRETARY_CHAT_ID,
                photo=photo_file,
                caption=caption,
                parse_mode='HTML'
            )
        logging.info("⏰  Đã gửi ảnh khung giờ làm việc.")
    except FileNotFoundError:
        logging.warning(f"Không tìm thấy file ẢNH khung giờ tại '{config.SCHEDULE_IMAGE_PATH}'. Bỏ qua.")
    except Exception as e:
        logging.error(f"❌ Lỗi khi gửi ảnh khung giờ: {e}")

# Hàm xử lý một chuỗi thông báo: Video nhắc nhở -> Ảnh chia vốn
async def handle_session_reminder(bot: Bot, session_time: datetime, ca_number: int):
    # Tạo một tác vụ chạy nền cho việc gửi video, ghim và gỡ ghim để không làm block các tác vụ khác
    asyncio.create_task(send_reminder_video(bot, session_time, ca_number))
    await asyncio.sleep(1) # Chờ 1 giây để đảm bảo tin nhắn chia vốn đi sau
    await send_capital_division_photo(bot)

# Vòng lặp chính của bot
async def main_loop():
    try:
        if not all([config.SECRETARY_TELEGRAM_TOKEN, config.SECRETARY_CHAT_ID]):
            logging.critical("❌ Thiếu TOKEN hoặc CHAT_ID. Vui lòng kiểm tra file .env hoặc biến môi trường.")
            return

        bot = Bot(token=config.SECRETARY_TELEGRAM_TOKEN)
        bot_info = await bot.get_me()
        logging.info(f"✅ Token hợp lệ. Bot '{bot_info.full_name}' đã sẵn sàng.")

        logging.info("🚀 Bot Thư Ký Tiên (v5.0 - 100 Ca) đã khởi động! Hoạt động từ 06:50 đến 23:35.")

        sent_flags = {
            'last_reminder_minute': -1,
            'last_info_minute': -1,
            'last_info_type': 'schedule', # Loại tin thông tin (intro/schedule) đã gửi lần cuối
            'today': date.today(),
            'is_sleeping_logged': False
        }
        start_time = time(6, 50)
        end_time = time(23, 35) # Giờ gửi tin chúc ngủ ngon

        while True:
            now = datetime.now(config.VN_TZ)
            # Kiểm tra xem có đang trong giờ nghỉ không
            is_sleeping_time = not (start_time <= now.time() < end_time)

            if is_sleeping_time:
                if not sent_flags['is_sleeping_logged']:
                    logging.info(f"🌙 Bot đang trong giờ nghỉ ngơi. Sẽ hoạt động lại lúc {start_time.strftime('%H:%M')}.")
                    sent_flags['is_sleeping_logged'] = True
                if now.date() != sent_flags['today']: # Reset cờ khi qua ngày mới trong lúc đang ngủ
                    sent_flags = {
                        'last_reminder_minute': -1, 'last_info_minute': -1, 'last_info_type': 'schedule',
                        'today': now.date(), 'is_sleeping_logged': True
                    }
                    logging.info(f"☀️  Đã qua ngày mới {now.strftime('%d/%m/%Y')}! Đã reset trạng thái.")
                await asyncio.sleep(60) # Kiểm tra lại sau 1 phút
                continue

            if sent_flags['is_sleeping_logged']:
                sent_flags['is_sleeping_logged'] = False
                logging.info("☀️  Bot bắt đầu ca làm việc!")

            # Logic reset trạng thái khi bắt đầu một ngày làm việc mới
            if now.date() != sent_flags['today']:
                sent_flags = {
                    'last_reminder_minute': -1, 'last_info_minute': -1, 'last_info_type': 'schedule',
                    'today': now.date(), 'is_sleeping_logged': False
                }
                logging.info(f"☀️  Chào ngày mới {now.strftime('%d/%m/%Y')}! Đã reset trạng thái.")
                sent_flags.pop('morning_sent', None)
                sent_flags.pop('night_sent', None)

            # --- LỊCH TRÌNH GỬI TIN NHẮN ---

            # 1. Gửi tin chào buổi sáng (chỉ một lần lúc 7:00)
            if now.hour == 7 and now.minute == 0 and 'morning_sent' not in sent_flags:
                await send_simple_message(bot, create_good_morning_message())
                sent_flags['morning_sent'] = True

            # 2. Gửi tin chúc ngủ ngon (chỉ một lần lúc 23:35)
            if now.time() >= end_time and 'night_sent' not in sent_flags:
                await send_simple_message(bot, create_good_night_message())
                sent_flags['night_sent'] = True

            # 3. Gửi xen kẽ Video giới thiệu và Ảnh lịch làm việc mỗi 30 phút
            if now.minute in [0, 30] and now.minute != sent_flags['last_info_minute']:
                if sent_flags['last_info_type'] == 'schedule':
                    await send_introduction_video(bot)
                    sent_flags['last_info_type'] = 'intro'
                else:
                    await send_schedule_photo(bot)
                    sent_flags['last_info_type'] = 'schedule'
                sent_flags['last_info_minute'] = now.minute

            # 4. Gửi thông báo ca kéo dựa trên lịch trình 100 ca
            for ca_number, session_t in SESSION_SCHEDULE:
                # Thời gian bắt đầu ca
                session_start_dt = datetime.combine(now.date(), session_t, tzinfo=config.VN_TZ)
                # Thời gian gửi thông báo (trước 3 phút)
                reminder_dt = session_start_dt - timedelta(minutes=3)

                # Kiểm tra xem có phải lúc gửi thông báo không
                if now.hour == reminder_dt.hour and now.minute == reminder_dt.minute and now.minute != sent_flags['last_reminder_minute']:
                    sent_flags['last_reminder_minute'] = now.minute
                    await handle_session_reminder(bot, session_start_dt, ca_number)
                    break # Thoát vòng lặp sau khi tìm thấy và xử lý ca phù hợp

            await asyncio.sleep(5) # Nghỉ 5 giây trước khi kiểm tra lại

    except Exception as e:
        logging.critical(f"❌ LỖI NGHIÊM TRỌNG TRONG VÒNG LẶP CHÍNH CỦA BOT: {e}", exc_info=True)


# --- KHỞI ĐỘNG CẢ BOT VÀ WEB SERVER ---
if __name__ == "__main__":
    logging.info("▶️  Bắt đầu chạy script...")

    # Chạy bot trong một luồng (thread) riêng để không chặn web server
    bot_thread = Thread(target=lambda: asyncio.run(main_loop()))
    bot_thread.start()

    # Chạy web server trong luồng chính để Render nhận diện
    logging.info("🌐 Web server đang khởi động...")
    run_web_server()