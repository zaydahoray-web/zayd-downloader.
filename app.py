from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

style_content = """
<style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        padding-top: 80px;
    }
    h1 { font-size: 2.5rem; color: #00fff0; text-shadow: 0 0 10px rgba(0,255,240,0.5); }
    .card {
        background: rgba(255, 255, 255, 0.06);
        padding: 40px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        width: 360px;
    }
    input[type="text"] {
        padding: 15px 25px;
        font-size: 1rem;
        border: 2px solid #00fff0;
        border-radius: 30px;
        margin-bottom: 25px;
        width: 100%;
        box-sizing: border-box;
        background: rgba(0,0,0,0.4);
        color: white;
        outline: none;
    }
    .btn {
        background: linear-gradient(90deg, #00fff0, #0088cc);
        color: white;
        border: none;
        padding: 15px 35px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        border-radius: 30px;
        transition: 0.3s;
        width: 100%;
    }
    .btn:hover { transform: scale(1.02); }
    .status { margin-top: 25px; font-size: 1.2rem; font-weight: bold; color: #ff9800; }
</style>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    status_message = ""
    if request.method == 'POST':
        video_url = request.form.get('url')
        if video_url:
            try:
                ydl_opts = {
                    'outtmpl': '/tmp/%(title)s.%(ext)s',
                    'format': 'best',
                    'nocheckcertificate': True,
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                status_message = "Success! Video downloaded to cloud server. 🎉"
            except Exception as e:
                status_message = "Error: Connection issue or blocked link."

    html_content = f"""
    <html>
    <head><title>Zayd Downloader</title>{style_content}</head>
    <body>
        <h1>Zayd's Premium Downloader ⚡</h1>
        <p>Advanced anti-block video download engine</p>
        <div class="card">
            <form id="downloadForm" method="POST">
                <input type="text" name="url" placeholder="Paste video link here..." required><br>
                <button type="submit" class="btn">Download Now</button>
            </form>
            <div class="status" id="statusBox">{status_message}</div>
        </div>
        <script>
            document.getElementById('downloadForm').onsubmit = function() {{
                document.getElementById('statusBox').innerHTML = "Downloading video file... Please wait ⏳";
            }};
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
  
