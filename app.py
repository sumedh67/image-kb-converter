# ...existing code...
from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    try:
        # Get uploaded image
        image_file = request.files['image']
        target_kb = int(request.form['target_kb'])

        # Open image
        img = Image.open(image_file)
        quality = 95

        # Compress in memory
        output = BytesIO()
        while True:
            output.seek(0)
            img.save(output, format='JPEG', optimize=True, quality=quality)
            size_kb = output.tell() / 1024
            if size_kb <= target_kb or quality <= 10:
                break
            quality -= 5

        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name="compressed.jpg",
            mimetype="image/jpeg"
        )
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
