from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password= "",
    database="image_upload"
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        user_class = request.form['class']
        age = request.form['age']
        file = request.files['image']

        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)

            # Store user data in the database
            cursor.execute("INSERT INTO user_info (name, class,age, image_path) VALUES (%s,%s, %s, %s)", 
                           (name, user_class,age, image_path))
            db.commit()

            return redirect(url_for('result', name=name, user_class=user_class, age=age,image=file.filename))

    return render_template('index.html')

@app.route('/result')
def result():
    name = request.args.get('name')
    user_class = request.args.get('user_class')
    age = request.args.get('age')
    image = request.args.get('image')
    return render_template('result.html', name=name, user_class=user_class, age=age,image=image)

if __name__ == '__main__':
    app.run(debug=True)

