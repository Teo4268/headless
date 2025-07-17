from flask import Flask, request, send_file, render_template_string
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 📤 Route nhận ảnh từ client
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('screenshot')
    client_ip = request.remote_addr.replace(":", "_")

    if file:
        ip_folder = os.path.join(UPLOAD_FOLDER, client_ip)
        os.makedirs(ip_folder, exist_ok=True)
        filepath = os.path.join(ip_folder, 'latest.png')
        file.save(filepath)
        print(f"📥 Đã nhận ảnh từ IP {client_ip}")
        return f'Screenshot received from {client_ip}!'
    return 'No file received.', 400

# 🌐 Trang hiển thị ảnh
@app.route('/')
def index():
    ip_folders = sorted(os.listdir(UPLOAD_FOLDER))
    ip_images = [f"/image/{ip}" for ip in ip_folders if os.path.exists(os.path.join(UPLOAD_FOLDER, ip, "latest.png"))]

    html = '''
    <html>
    <head>
        <title>Giám sát ảnh tự động</title>
        <meta http-equiv="refresh" content="5"> <!-- auto reload -->
        <style>
            body { font-family: Arial; background: #f2f2f2; padding: 20px; }
            h2 { color: #333; }
            .group { background: white; padding: 10px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 0 10px #ccc; }
            img { max-width: 100%; border: 1px solid #999; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>📡 Ảnh mới nhất theo IP</h1>
        {% for ip in ip_images %}
        <div class="group">
            <h2>IP: {{ ip.split('/')[-1] }}</h2>
            <img src="{{ ip }}?t={{ timestamp }}">
        </div>
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(html, ip_images=ip_images, timestamp=datetime.now().timestamp())

# 📸 Trả ảnh của từng IP
@app.route('/image/<ip>')
def image(ip):
    path = os.path.join(UPLOAD_FOLDER, ip, 'latest.png')
    if os.path.exists(path):
        return send_file(path, mimetype='image/png')
    return 'Image not found', 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860, debug=True)
