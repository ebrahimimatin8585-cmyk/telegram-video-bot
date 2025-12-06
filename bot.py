#!/usr/bin/env python3
# بات تلگرام دائمی - نسخه Render.com
# تیم وب صفر و یک

import os
import sys
import time
import requests
import re
import subprocess
import tempfile
import json
from threading import Thread
from flask import Flask

# ==================== Flask برای نگه‌داری آنلاین ====================
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>بات تلگرام - تیم وب صفر و یک</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .status {
                background: rgba(0, 255, 0, 0.2);
                padding: 10px 20px;
                border-radius: 50px;
                display: inline-block;
                margin: 20px 0;
                font-weight: bold;
            }
            .features {
                text-align: right;
                margin: 30px 0;
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
            }
            .btn {
                display: inline-block;
                background: #4CAF50;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 50px;
                margin: 10px;
                font-size: 1.2em;
                transition: all 0.3s;
            }
            .btn:hover {
                background: #45a049;
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 بات تلگرام دانلود ویدیو</h1>
            <div class="status">✅ وضعیت: آنلاین و فعال</div>
            
            <div class="features">
                <h2>✨ ویژگی‌ها:</h2>
                <p>• ۲۴ ساعته آنلاین</p>
                <p>• دانلود از یوتیوب، اینستاگرام، تیک‌تاک</p>
                <p>• کاملاً رایگان</p>
                <p>• سرعت بالا</p>
                <p>• پشتیبانی از فرمت‌های مختلف</p>
            </div>
            
            <h2>🛠️ توسعه‌دهنده: تیم وب صفر و یک</h2>
            
            <a href="https://t.me/zero_one_downloder_bot" class="btn" target="_blank">
                🔗 استفاده از بات
            </a>
            <a href="https://t.me/web01zero" class="btn" target="_blank">
                📞 پشتیبانی
            </a>
            
            <p style="margin-top: 30px; opacity: 0.8;">
                آخرین به‌روزرسانی: """ + time.strftime("%Y/%m/%d %H:%M:%S") + """
            </p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return json.dumps({
        'status': 'online',
        'service': 'telegram-video-bot',
        'developer': 'تیم وب صفر و یک',
        'timestamp': time.time()
    })

@app.route('/ping')
def ping():
    return 'pong'

# شروع سرور Flask در Thread جداگانه
def start_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

Thread(target=start_flask, daemon=True).start()

# ==================== بخش اصلی بات تلگرام ====================
TOKEN = os.environ.get("TELEGRAM_TOKEN", "00")

print("=" * 60)
print("🚀 بات تلگرام دائمی - راه‌اندازی شد")
print("👨‍💻 توسعه‌دهنده: تیم وب صفر و یک")
print("🌐 پنل مدیریت: http://0.0.0.0:5000")
print("📱 بات: @zero_one_downloder_bot")
print("=" * 60)

def send_telegram(chat_id, text, reply_id=None):
    """ارسال پیام به تلگرام"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        if reply_id:
            data['reply_to_message_id'] = reply_id
        
        response = requests.post(url, data=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"⚠️ خطای ارسال تلگرام: {e}")
        return None

def download_video_async(url, chat_id, msg_id):
    """دانلود ویدیو در پس‌زمینه"""
    try:
        send_telegram(chat_id, "🔍 در حال بررسی لینک...", msg_id)
        
        # اطلاعات ویدیو
        cmd_info = ['yt-dlp', '--dump-json', '--no-warnings', url]
        result = subprocess.run(cmd_info, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            send_telegram(chat_id, "❌ لینک نامعتبر یا دسترسی نداریم!", msg_id)
            return
        
        info = json.loads(result.stdout)
        title = info.get('title', 'ویدیو')
        duration = info.get('duration', 0)
        
        send_telegram(chat_id, f"📹 <b>{title[:50]}</b>\n⏱️ مدت: {duration} ثانیه", msg_id)
        
        if duration > 600:
            send_telegram(chat_id, "⚠️ ویدیوهای بیشتر از ۱۰ دقیقه پشتیبانی نمی‌شوند!", msg_id)
            return
        
        # دانلود
        send_telegram(chat_id, "⏳ در حال دانلود... لطفاً صبر کنید", msg_id)
        
        temp_dir = tempfile.mkdtemp()
        output_file = os.path.join(temp_dir, "video.mp4")
        
        cmd_download = [
            'yt-dlp',
            '-f', 'best[height<=720]/best[ext=mp4]',
            '-o', output_file,
            '--quiet',
            '--no-warnings',
            url
        ]
        
        result = subprocess.run(cmd_download, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            send_telegram(chat_id, "❌ خطا در دانلود ویدیو!", msg_id)
            return
        
        # پیدا کردن فایل
        video_file = None
        for file in os.listdir(temp_dir):
            if file.endswith(('.mp4', '.mkv', '.webm')):
                video_file = os.path.join(temp_dir, file)
                break
        
        if not video_file:
            send_telegram(chat_id, "❌ فایل دانلود شده یافت نشد!", msg_id)
            return
        
        # ارسال به تلگرام
        file_size = os.path.getsize(video_file) / (1024 * 1024)
        send_telegram(chat_id, f"📤 در حال آپلود... ({file_size:.1f} MB)", msg_id)
        
        with open(video_file, 'rb') as f:
            files = {'video': f}
            data = {
                'chat_id': chat_id,
                'caption': f"✅ <b>{title}</b>\n\n📊 حجم: {file_size:.1f} MB\n⚡ توسط تیم <b>وب صفر و یک</b>",
                'parse_mode': 'HTML'
            }
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendVideo",
                files=files,
                data=data,
                timeout=120
            )
        
        if response.status_code == 200:
            send_telegram(chat_id, "✅ ویدیو با موفقیت ارسال شد!", msg_id)
        else:
            send_telegram(chat_id, f"❌ خطا در ارسال: کد {response.status_code}", msg_id)
        
        # پاکسازی
        try:
            os.remove(video_file)
            os.rmdir(temp_dir)
        except:
            pass
            
    except Exception as e:
        send_telegram(chat_id, f"❌ خطا: {str(e)[:100]}", msg_id)

# متن‌های بات
WELCOME_TEXT = """✨ <b>بات دانلود ویدیو دائمی</b> ✨

🛠️ <b>توسعه‌دهنده:</b> تیم <b>وب صفر و یک</b>

✅ <b>ویژگی‌ها:</b>
• ۲۴ ساعته آنلاین (حتی اگر کامپیوتر خاموش باشد)
• دانلود از همه پلتفرم‌ها
• سرعت بالا
• کاملاً رایگان

📝 <b>نحوه استفاده:</b>
فقط لینک ویدیو را بفرستید

🔥 <b>پشتیبانی از:</b>
• YouTube • Instagram • TikTok
• Twitter/X • Facebook • Reddit

⚡ <b>بات دائمی و همیشه آنلاین</b> ⚡

📞 پشتیبانی: @web01zero"""

# حلقه اصلی بات
print("✅ بات تلگرام شروع به کار کرد...")

last_update_id = 0

while True:
    try:
        # دریافت پیام‌های جدید
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {
            'offset': last_update_id + 1,
            'timeout': 30,
            'allowed_updates': '["message"]'
        }
        
        response = requests.get(url, params=params, timeout=40)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ok') and data.get('result'):
                for update in data['result']:
                    last_update_id = update['update_id']
                    
                    if 'message' in update:
                        msg = update['message']
                        chat_id = msg['chat']['id']
                        text = msg.get('text', '')
                        msg_id = msg.get('message_id')
                        
                        print(f"📩 [{chat_id}]: {text[:40]}...")
                        
                        if text == '/start':
                            send_telegram(chat_id, WELCOME_TEXT)
                        
                        elif 'http' in text:
                            match = re.search(r'(https?://[^\s]+)', text)
                            if match:
                                video_url = match.group(0)
                                
                                # شروع دانلود در Thread جداگانه
                                Thread(
                                    target=download_video_async,
                                    args=(video_url, chat_id, msg_id),
                                    daemon=True
                                ).start()
                        
                        elif text:
                            send_telegram(chat_id, "📎 لینک ویدیو را ارسال کنید\n/start برای اطلاعات بیشتر", msg_id)
        
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n👋 بات متوقف شد")
        break
    except Exception as e:
        print(f"⚠️ خطا: {e}")
        time.sleep(5)
