import os
import sys
from flask import Flask, request, render_template_string, send_file
import yt_dlp

app = Flask(__name__)

# تحديد مسار تخزين مؤقت متوافق مع خوادم Vercel السحابية
os.environ['HOME'] = '/tmp'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Smart Video Downloader 🚀</title>
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: white; padding-top: 50px; }
        input[type="text"] { width: 70%; padding: 12px; border-radius: 8px; border: none; margin-bottom: 20px; font-size: 16px; color: #000; }
        button { padding: 12px 25px; border-radius: 8px; border: none; background: #ff0055; color: white; font-size: 16px; cursor: pointer; }
        .ads-banner { margin: 30px auto; width: 300px; height: 250px; background: #222; border: 1px dashed #555; line-height: 250px; color: #aaa; }
    </style>
</head>
<body>
    <h1>High Quality Video Downloader 🔥</h1>
    <p>Enter YouTube, Facebook, or TikTok video link below:</p>
    <form action="/download" method="post">
        <input type="text" name="url" placeholder="Paste your link here..." required><br>
        <button type="submit">Download Best Quality ✨</button>
    </form>
    <div class="ads-banner">
        Ads Space (إعلان يدعم استمرار الموقع مجاناً)
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    
    # إعدادات مخصصة لتفادي جدران الحماية وتحميل الفيديو في الذاكرة المؤقتة للسيرفر السحابي
    ydl_opts = {
        'format': 'best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
        'cachedir': False,
        'no_warnings': True,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Download Error: {str(e)}"

# تعيين التطبيق للخادم السحابي
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
