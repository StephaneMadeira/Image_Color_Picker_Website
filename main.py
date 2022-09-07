import os
from PIL import Image
from dotenv import load_dotenv
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# ------------- Variables -----------------------------#
UPLOAD_FOLDER = 'static/uploaded_image'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')

# Environment Variables
load_dotenv("D:\Python\EnvironmentVariables\.env.txt")

# ------------- Setup Flask app -----------------------------#
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv("Flask_KEY")


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/generate", methods=["GET", "POST"])
# Using POST to add the photo and see which colors are on it
def generate():
    if request.method == 'POST':
        f = request.files['image']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        img = Image.open(f'static/uploaded_image/{f.filename}').convert("P", palette=Image.Palette.ADAPTIVE,
                                                                        colors=10).convert("RGB")
        # Set the maxcolors number to the image's pixels number
        colors = img.getcolors(img.size[0] * img.size[1])
        colors.sort(reverse=True)
        ten_colors = colors[:10]
        return render_template("index.html", colors=ten_colors, image=f.filename)


if __name__ == '__main__':
    app.run()
