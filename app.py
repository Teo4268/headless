from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('screenshot')
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, 'latest.png')
        file.save(filepath)
        return 'Screenshot received!'
    return 'No file received.', 400

@app.route('/')
def view_image():
    return render_template_string('''
        <h1>Ảnh mới nhất:</h1>
        <img src="/image" style="max-width:90%">
    ''')

@app.route('/image')
def image():
    path = os.path.join(UPLOAD_FOLDER, 'latest.png')
    return send_file(path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
