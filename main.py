import base64
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

from flask import Flask
import sqlite3

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)

        '''Into The Database'''
        conn = sqlite3.connect('Images.db')
        title = request.form['title']

        cur = conn.cursor()
        cur.execute("INSERT INTO contents (title,img) VALUES(?, ?)",(title, request.files['file'].read()))
        conn.commit()

        flash('Image successfully uploaded and displayed')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)




@app.route('/show/')
def show_image():
    ''' Database'''
    conn = sqlite3.connect('Images.db')

    cur = conn.cursor()
    cur.execute("select * from contents")
    content = cur.fetchone()

    img_base64_bytes = base64.b64encode(content[1])
    title = content[0]

    return render_template('image.html', lastImage = img_base64_bytes.decode("utf-8"), lastTitle=title)


@app.route('/showall/')
def show_images():
    ''' Database'''
    conn = sqlite3.connect('Images.db')

    cur = conn.cursor()
    cur.execute("select * from contents")
    contents = cur.fetchall()
    all_images = []
    for rec in contents:
        images_dict = {
            'title': rec[0],
            'image': base64.b64encode(rec[1]).decode('utf-8')
        }
        all_images.append(images_dict)
    print(all_images)
    return render_template('images.html', recs = all_images)

if __name__ == "__main__":
    app.run()